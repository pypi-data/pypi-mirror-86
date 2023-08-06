'''
Defines functions for creating Parser primitives.
'''

from .parser import _StringParser, _CharacterParser


def char_(*args):
    '''
    Creates a character parser. Following options for input arguments are
    possible:

    Input Arguments | Character parser that matches
    ==============================================================
    ()                Anything
    (String, )        Any char in the string
    (Callable, )      Any char for which the function returns True
    '''
    if len(args) == 0:
        return _CharacterParser(lambda _: True, '𝐔')
    if len(args) == 1:
        arg, = args
        if isinstance(arg, str) and len(arg) == 1:
            pred = arg.__eq__
            name = '{%s}' % repr(arg)
            return _CharacterParser(pred, name)
        if isinstance(arg, str) and len(arg) >= 1:
            arg = set(arg)
            pred = arg.__contains__
            name = '{%s}' % ','.join(map(repr, arg))
            return _CharacterParser(pred, name)
        if callable(arg):
            return _CharacterParser(arg)
    raise ValueError('Cannot create character parser with arguments %s'
                     % args)


def str_(string: str):
    '''
    Creates a parser that matches `string`.
    '''
    return _StringParser(string)
