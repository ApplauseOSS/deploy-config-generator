import re
import six

from deploy_config_generator.errors import VarsParseError, VarsReplacementError

EOF_TOKEN = None
NEWLINE_TOKEN = '\n'
SKIP_TOKENS = ('\r', )
WHITESPACE_TOKENS = (' ', '\t')
VAR_END_TOKENS = (NEWLINE_TOKEN, EOF_TOKEN) + WHITESPACE_TOKENS
SINGLE_QUOTE_TOKEN = "'"
DOUBLE_QUOTE_TOKEN = '"'
QUOTE_TOKENS = (SINGLE_QUOTE_TOKEN, DOUBLE_QUOTE_TOKEN)

# Common regex for var name
# Must start with letter/underscore and contain only letter/number/underscore
RE_VAR_NAME = r'([A-Za-z_][A-Za-z0-9_]*)'

ESCAPE_SEQUENCES = {
    r'\"': '"',
    r'\n': '\n',
}


class Vars(dict):

    '''
    This class manages a set of variables and provides facilities for performing
    replacements of those variables and reading in vars files
    '''

    def clear(self):
        self.clear()

    def read_vars_file(self, path, allow_var_references=True):
        with open(path, 'r') as f:
            VarsParser(fh=f, path=path, varset=self, allow_var_references=allow_var_references).parse()

    def replace_vars(self, value, allow_var_references=True):
        def replace_var(match):
            if not allow_var_references:
                raise VarsReplacementError("Found variable reference where not allowed")
            var_name = match.group(2)
            try:
                return self[var_name]
            except KeyError:
                raise VarsReplacementError("Unknown variable '%s'" % var_name)

        if isinstance(value, list):
            ret = []
            for item in value:
                ret.append(self.replace_vars(item))
        elif isinstance(value, dict):
            ret = {}
            for item in value:
                ret[item] = self.replace_vars(value[item])
        elif isinstance(value, six.string_types):
            ret = value
            # Find and Replace var references
            # The first capture group (named 'curly') looks for an opening curly brace, and
            # the last capture group looks for a closing curly brace *if* the first capture
            # group matched anything
            ret = re.sub(r'\$(?P<curly>\{)?%s(?(curly)\})' % RE_VAR_NAME, replace_var, ret)
        else:
            ret = value

        return ret


class VarsParser(object):

    '''
    This class is used for parsing shell-style vars files
    '''

    def __init__(self, varset, path=None, fh=None, allow_var_references=True):
        self.path = path
        self.varset = varset
        self.fh = fh
        self.allow_var_references = allow_var_references
        self.lineno = 1
        self.reset_state()

    def reset_state(self):
        '''
        Reset the parser state for each new line or variable definition
        '''
        self.var_name = None
        self.var_value = None
        self.found_equals = False
        self.found_dollar_sign = False
        self.found_escape = False
        self.found_comment = False
        self.in_quotes = None

    def add_token_to_var_name(self, token):
        self.var_name += token

    def add_token_to_var_value(self, token):
        self.var_value += token

    def process_var_name(self, token):
        '''
        Processes what should be the variable name and an equals sign
        '''
        if token == '#':
            self.found_comment = True
            return
        if token == '=':
            if self.var_name is None:
                raise VarsParseError("Encountered '=' before var name", path=self.path, line=self.lineno)
            self.found_equals = True
            self.var_value = ''
            return
        else:
            # Consider any tokens before the = to be the var name
            if self.var_name is None:
                self.var_name = ''
            self.add_token_to_var_name(token)
            if re.match(RE_VAR_NAME, self.var_name) is None:
                raise VarsParseError("Found unexpected token '%s' before '='" % token, path=self.path, line=self.lineno)

    def process_var_value(self, token):
        '''
        Process what should be the variable value
        '''
        if token in QUOTE_TOKENS and not self.var_value.endswith('\\'):
            if self.in_quotes:
                if token == self.in_quotes:
                    self.in_quotes = None
                else:
                    self.add_token_to_var_value(token)
            else:
                self.in_quotes = token
            return
        # Set the flag to do var processing if a $ is found while not in single quotes
        if token == '$':
            if self.in_quotes != SINGLE_QUOTE_TOKEN:
                self.found_dollar_sign = True
        # Set the flag to do escape processing if a \ is found while not in single quotes
        if token == '\\':
            if self.in_quotes != SINGLE_QUOTE_TOKEN:
                self.found_escape = True
        self.add_token_to_var_value(token)

    def process_var_end_token(self, token):
        '''
        Process tokens that should be the end of a variable definition
        '''
        if self.var_name:
            tmp_lineno = self.lineno
            # Show the line number where the var definition started
            # rather than the one after the newline
            if token == NEWLINE_TOKEN:
                tmp_lineno = self.lineno - 1
            if not self.found_equals:
                raise VarsParseError("Did not find expected token '=' after var name", path=self.path, line=tmp_lineno)
            if self.in_quotes:
                # If we're in quotes and it's not EOL/EOF, add the token
                # to the value and continue
                if token in WHITESPACE_TOKENS:
                    self.add_token_to_var_value(token)
                    return
                raise VarsParseError("Did not find expected closing quote `%s`" % self.in_quotes, path=self.path, line=tmp_lineno)
            self.finalize_var()
            self.reset_state()

    def finalize_var(self):
        '''
        Process escape sequences, replace variable references, and save var
        '''
        try:
            # Process escape sequences
            if self.found_escape:
                self.var_value = self.replace_escape_sequences(self.var_value)
            # Assign value to var, optionally doing var replacement
            if self.found_dollar_sign:
                self.varset[self.var_name] = self.varset.replace_vars(self.var_value, allow_var_references=self.allow_var_references)
            else:
                self.varset[self.var_name] = self.var_value
        except Exception as e:
            raise VarsParseError(str(e), path=self.path, line=(self.lineno - 1))

    def parse(self):
        '''
        Main parsing function
        '''
        data = self.fh.read()
        # Iterate over each char in input, plus EOF
        for token in (list(data) + [EOF_TOKEN]):
            if token in SKIP_TOKENS:
                continue
            # Increment line number when encountering a newline
            if token == NEWLINE_TOKEN:
                self.lineno += 1
            # Reset the found_comment flag if reaching EOL/EOF
            if self.found_comment:
                if token in (NEWLINE_TOKEN, EOF_TOKEN):
                    self.reset_state()
                continue
            # Save var if we hit a newline, space, or EOF
            if token in VAR_END_TOKENS:
                self.process_var_end_token(token)
                if token == EOF_TOKEN:
                    break
                continue
            # Ignore any tokens while in a comment
            if self.found_comment:
                continue
            if not self.found_equals:
                self.process_var_name(token)
            else:
                self.process_var_value(token)

    def replace_escape_sequences(self, value):
        def replace_escape(match):
            if match.group(0) in ESCAPE_SEQUENCES:
                return ESCAPE_SEQUENCES[match.group(0)]
            return match.group(0)

        ret = value
        ret = re.sub(r'\\.', replace_escape, ret)

        return ret
