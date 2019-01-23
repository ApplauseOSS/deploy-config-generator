import re
import shlex

from deploy_config_generator.errors import VarsParseError, VarsReplacementError

BASE_VAR_END_TOKENS = ('\r', '\n', ' ')


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
            lexer = shlex.shlex(fh, posix=True)
            VAR_END_TOKENS = BASE_VAR_END_TOKENS + (lexer.eof, )
            # Don't consider newlines or spaces as whitespace, as we need to
            # know when we reach the end of a var definition
            lexer.whitespace = ['\t']
            var_name = var_value = None
            found_equals = False
            while True:
                try:
                    token = lexer.get_token()
                except ValueError as e:
                    raise VarsParseError(str(e), path=path, line=lexer.lineno)
                # Save var if we hit a newline, space, or EOF
                if token in VAR_END_TOKENS:
                    if var_name:
                        if not found_equals:
                            lineno = lexer.lineno
                            # Show the line number where the var definition started
                            # rather than the one after the newline
                            if token in ('\r', '\n'):
                                lineno = lexer.lineno - 1
                            raise VarsParseError("Did not find expected token '=' after var name", path=path, line=lineno)
                        try:
                            self[var_name] = self.replace_vars(var_value, allow_var_references=allow_var_references)
                        except Exception as e:
                            raise VarsParseError(str(e), path=path, line=(lexer.lineno - 1))
                        var_name = var_value = None
                        found_equals = False
                    if token == lexer.eof:
                        break
                    continue
                if not found_equals:
                    if token == '=':
                        if var_name is None:
                            raise VarsParseError("Encountered '=' before var name", path=path, line=lexer.lineno)
                        found_equals = True
                        var_value = ''
                        continue
                    else:
                        # Consider any token before the = to be the var name
                        if var_name is not None:
                            raise VarsParseError("Found unexpected token '%s' before '='" % token, path=path, line=lexer.lineno)
                        var_name = token
                else:
                    var_value += token

    def replace_vars(self, value, allow_var_references=True):
        def replace_var(match):
            if not allow_var_references:
                raise VarsReplacementError("Found variable reference where not allowed")
            try:
                return self[match.group(1)]
            except KeyError:
                raise VarsReplacementError("Unknown variable '%s'" % match.group(1))

        ret = value
        # Common regex for var name
        # Must start with letter/underscore and contain only letter/number/underscore
        re_var_name = r'([A-Za-z_][A-Za-z0-9_]+)'
        # Replace bracketed vars
        ret = re.sub(r'\$\{%s\}' % (re_var_name), replace_var, ret)
        # Replace non-bracketed vars
        ret = re.sub(r'\$%s' % (re_var_name), replace_var, ret)

        return ret
