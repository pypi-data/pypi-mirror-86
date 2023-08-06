'''
Defines all exceptions.
'''


class ParseError(Exception):
    '''
    Exception indicating a parse error.
    '''

    def __init__(self, pos, reason='Not Matched'):
        '''
        Parameters:
        ===========
            pos: int
                stream position where the error occured
            reason: str
                human-readable reason for the error
        '''
        super().__init__('Parse error at %d. %s' % (pos, reason))
        self.pos = pos
        self.reason = reason
