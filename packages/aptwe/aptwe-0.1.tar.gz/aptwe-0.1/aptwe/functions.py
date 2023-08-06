'''
Defines useful functions to be used with the `parser[func]` notation to create
a parser that applies `func` onto the parse result.
'''


def getitem(arg):
    '''
    Creates a function that returns the item indexed by `arg`.
    '''
    if isinstance(arg, int):
        return lambda values: values[arg]
    if isinstance(arg, tuple):
        return lambda values: tuple(values[index] for index in arg)
    raise ValueError('index should be an int or a tuple of ints.')


def value_or(factory):
    '''
    Creates a function that return the input argument if it is not None else
    returns `factory()`
    '''
    return lambda value: value or factory()


def concat(list_of_strings: list):
    '''
    Joins a list of strings.
    '''
    return ''.join(list_of_strings)
