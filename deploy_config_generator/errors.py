class VarsParseError(Exception):

    '''
    Exception wrapper class used by vars file parser
    '''

    def __init__(self, msg, line=None, path=None):
        if line:
            msg = 'line %d: %s' % (line, msg)
        if path:
            msg = '%s: %s' % (path, msg)
        super(VarsParseError, self).__init__(msg)
        self.path = path
        self.line = line


class VarsReplacementError(Exception):

    '''
    Exception wrapper class used by vars file parser
    '''


class DeployConfigError(Exception):

    '''
    Exception wrapper class used for the deploy config
    '''

    def __init__(self, msg, line=None):
        if line:
            msg = 'line %d: %s' % (line, msg)
        super(DeployConfigError, self).__init__(msg)
        self.line = line


class ConfigGenerationError(Exception):

    '''
    Exception wrapper class used when generating config
    '''
