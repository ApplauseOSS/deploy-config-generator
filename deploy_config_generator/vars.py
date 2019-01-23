import re

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

# For historical reasons, we only want to process escaped double quotes.
# If we add more escape sequences here, it will likely break things in the wild.
ESCAPE_SEQUENCES = {
    r'\"': '"',
}


class Vars(dict):

    '''
    This class manages reading of bash-style vars files and replacement of
    those vars in input strings (used for vars files and service deploy config
    files
    '''

    def clear(self):
        self.clear()

    def read_vars_file(self, path, allow_var_references=True):
        with open(path, 'r') as f:
            self.read_vars(f, path=path, allow_var_references=allow_var_references)

    def read_vars(self, fh, path=None, allow_var_references=True):
        var_name = var_value = None
        found_equals = False
        found_dollar_sign = False
        found_escape = False
        found_comment = False
        in_quotes = None
        lineno = 1
        data = fh.read()
        # Iterate over each char in input, plus EOF
        for token in (list(data) + [EOF_TOKEN]):
            if token in SKIP_TOKENS:
                continue
            # Increment line number when encountering a newline
            if token == NEWLINE_TOKEN:
                lineno += 1
            # Reset the found_comment flag if reaching EOL/EOF
            if found_comment:
                if token in (NEWLINE_TOKEN, EOF_TOKEN):
                    found_comment = False
                continue
            # Save var if we hit a newline, space, or EOF
            if token in VAR_END_TOKENS:
                if var_name:
                    tmp_lineno = lineno
                    # Show the line number where the var definition started
                    # rather than the one after the newline
                    if token == NEWLINE_TOKEN:
                        tmp_lineno = lineno - 1
                    if not found_equals:
                        raise VarsParseError("Did not find expected token '=' after var name", path=path, line=tmp_lineno)
                    if in_quotes:
                        # If we're in quotes and it's not EOL/EOF, add the token
                        # to the value and continue
                        if token in WHITESPACE_TOKENS:
                            var_value += token
                            continue
                        raise VarsParseError("Did not find expected closing quote `%s`" % in_quotes, path=path, line=tmp_lineno)
                    try:
                        # Process escape sequences
                        if found_escape:
                            var_value = self.replace_escape_sequences(var_value)
                        # Assign value to var, optionally doing var replacement
                        if found_dollar_sign:
                            self[var_name] = self.replace_vars(var_value, allow_var_references=allow_var_references)
                        else:
                            self[var_name] = var_value
                    except Exception as e:
                        raise VarsParseError(str(e), path=path, line=(lineno - 1))
                    var_name = var_value = None
                    found_equals = False
                    found_dollar_sign = False
                    found_escape = False
                if token == EOF_TOKEN:
                    break
                continue
            # Ignore any tokens while in a comment
            if found_comment:
                continue
            if not found_equals:
                # Looking for the var name and =
                if token == '#':
                    found_comment = True
                    continue
                if token == '=':
                    if var_name is None:
                        raise VarsParseError("Encountered '=' before var name", path=path, line=lineno)
                    found_equals = True
                    var_value = ''
                    continue
                else:
                    # Consider any tokens before the = to be the var name
                    if var_name is None:
                        var_name = ''
                    var_name += token
                    if re.match(RE_VAR_NAME, var_name) is None:
                        raise VarsParseError("Found unexpected token '%s' before '='" % token, path=path, line=lineno)
            else:
                # Looking for var value
                if token in QUOTE_TOKENS and not var_value.endswith('\\'):
                    if in_quotes:
                        if token == in_quotes:
                            in_quotes = None
                        else:
                            var_value += token
                    else:
                        in_quotes = token
                    continue
                # Set the flag to do var processing if a $ is found while not in single quotes
                if token == '$':
                    if in_quotes != SINGLE_QUOTE_TOKEN:
                        found_dollar_sign = True
                # Set the flag to do escape processing if a \ is found while not in single quotes
                if token == '\\':
                    if in_quotes != SINGLE_QUOTE_TOKEN:
                        found_escape = True
                var_value += token

    def replace_escape_sequences(self, value):
        def replace_escape(match):
            if match.group(0) in ESCAPE_SEQUENCES:
                return ESCAPE_SEQUENCES[match.group(0)]
            return match.group(0)

        ret = value
        ret = re.sub(r'\\.', replace_escape, ret)

        return ret

    def replace_vars(self, value, allow_var_references=True):
        def replace_var(match):
            if not allow_var_references:
                raise VarsReplacementError("Found variable reference where not allowed")
            try:
                return self[match.group(1)]
            except KeyError:
                raise VarsReplacementError("Unknown variable '%s'" % match.group(1))

        ret = value
        # Replace bracketed vars
        ret = re.sub(r'\$\{%s\}' % RE_VAR_NAME, replace_var, ret)
        # Replace non-bracketed vars
        ret = re.sub(r'\$%s' % RE_VAR_NAME, replace_var, ret)

        return ret
