'''
All parsers inherit from `BaseParser` which defines operators to compose
parsers into more complex ones.

`Parser` can be used to warp around another parser, furthermore, this instance
can contain the current parser for defining recursions.
'''

import io
from .exceptions import ParseError


class BaseParser:
    '''
    Parsers have two basic use cases:

    1. Parsing: parsers are functions that read from a stream as argument.

    2. Parser generation: Combine parsers by operators:

        Usage            | Notation              | Result type of `__call__`
        ================================================================
                           p_i                     P_i
        ----------------------------------------------------------------
        concatenation      p_1 >> ... >> p_n       Tuple[P_1, ..., P_n]
        alteratnation      p_1 | ... | p_n         Union[P_1, ..., P_n]
        optional           -p_i                    Optional[P_i]
        repetition                                 List[P_i]
            zero or more   ~p_i
            one or more    +p_i
            list           p_i % p_j
        recursion          q[...] = p_i            P_i
        mapping            p_i[Callable[P_i, R]]   R
        alias              p_i @ '<some-name>'     P_i
    '''

    def __rshift__(self, other):
        '''
        Creates a parser that parses first using `self` and then using
        `other`.

        Example:
        ~~~
        p = char_(str.isdigit) >> str_(',') >> char_(str.isalpha)
        p.loads('4,hello') # Returns ('4', ',', 'hello')
        ~~~
        '''
        # pylint: disable=E1101
        first = ((self, ) if not isinstance(self, _ConcatenationParser)
                 else self._sequence)
        second = ((other, ) if not isinstance(other, _ConcatenationParser)
                  else other._sequence)
        return _ConcatenationParser(first + second)

    def __or__(self, other):
        '''
        Creates a parser that tries to parse using either `self` or `other`.

        Example:
        ~~~
        p = char_(str.isdigit) | str_('world')
        p.loads('4') # Returns '4'
        p.loads('world') # Returns 'world'
        p.loads('wonder') # raises ParseError
        ~~~
        '''
        # pylint: disable=E1101
        first = ((self, ) if not isinstance(self, _AlternationParser)
                 else self._choices)
        second = ((other, ) if not isinstance(other, _AlternationParser)
                  else other._choices)
        return _AlternationParser(first + second)

    def __neg__(self):
        '''
        Creates a parser that tries to parse using `self` or returns `None`

        Example:
        ~~~
        p = -char_(str.isdigit)
        p.loads('6') # Returns '6'
        p.loads('pan') # Returns None
        ~~~
        '''
        return _OptionalParser(self)

    def __pos__(self):
        '''
        Creates a parser that tries to parse one or many times using `self`.

        Example:
        ~~~
        p = +char_(str.isdigit) >> str_('x')
        p.loads('42x') # Returns (['4', '2'], 'x')
        p.loads('4x') # Returns (['4'], 'x')
        p.loads('x') # raises ParseError
        '''
        return _RepetitionParser(self, min_repeats=1)

    def __invert__(self):
        '''
        Creates a parser that tries to parse zero or many times using `self`.

        Example:
        ~~~
        p = ~char_(str.isdigit) >> str_('x')
        p.loads('42x') # Returns (['4', '2'], 'x')
        p.loads('4x') # Returns (['4'], 'x')
        p.loads('x') # Returns ([], 'x')
        ~~~
        '''
        return _RepetitionParser(self)

    def __mod__(self, other):
        '''
        Creates a parser that tries to parse zero or many times using `self`.
        Between each parse call to `self` the parser `other` is used.

        Example:
        ~~~
        p = char_(str.isdigit) % str_('x')
        p.loads('4x2') # Returns ['4', '2']
        p.loads('4') # Returns ['4']
        p.loads('') # Returns []
        ~~~
        '''
        return _ListParser(self, other)

    def __getitem__(self, func):
        '''
        Creates a parser that parses using `self` and applies the parse result
        to the function `func`.

        Example:
        ~~~
        p = +char_(str.isdigit)
        p.loads('42') # Returns ['4', '2']
        p[concat].loads('42') # Returns '42'
        p[concat][int].loads('42') # Returns 42
        ~~~
        '''
        return _CallableWrapperParser(self, func)

    def __matmul__(self, name: str):
        '''
        Creates a parser that aliases `self` using the given `name`.

        Example:
        ~~~
        ~~~
        p = ~char_(str.isdigit) >> str_('x')
        repr(p) # Returns "({c|isdigit(c)}* 'x')"
        q = p @ 'digits_x'
        repr(q) # Returns "digits_x"
        '''
        parser = Parser(name)
        parser[...] = self
        return parser

    def __call__(self, stream: io.IOBase):
        '''
        Parses a stream.

        Parameters:
        ===========
            stream: (io.IOBase)
                Stream that implements `read`, `tell` and `seek`.
        '''
        raise NotImplementedError

    def load(self, stream: io.IOBase):
        '''
        Parses a stream.

        Parameters:
        ===========
            stream: (io.IOBase)
                Stream that implements `read`, `tell` and `seek`.
        '''
        return self(stream)

    def loads(self, string: str):
        '''
        Parses a string.

        Parameters:
        ===========
            string: (str)
                String to be decoded.
        '''
        return self(io.StringIO(string))


class Parser(BaseParser):
    '''
    Alias to another parser stored in `instance`.
    '''

    def __init__(self, name: str = 'Parser', instance: BaseParser = None):
        '''
        Creates a named alias to another parser.

        Parameters:
        ===========
            name: (str)
                string name of the parser returned by `repr`
            instance: (BaseParser)
                another parser
        '''
        self.name = name
        self.instance = instance

    def __setitem__(self, key: type(Ellipsis), other: BaseParser):
        '''
        Warps around an exiting parser.

        Example:
        ~~~
        p = Parser('p')
        p[...] = str_('x') | (char_(str.isdigit) >> p)
        p.loads('42x') # Returns ('4', ('2', 'x'))
        p.loads('4x') # Returns ('2', 'x')
        p.loads('x') # Returns ('x')
        ~~~
        '''
        self.instance = other

    def __repr__(self):
        return self.name

    def __call__(self, stream: io.IOBase):
        if self.instance is None:
            raise ValueError('Parser is not instantiated. Assign a value '
                             'using parser[...] = ...')
        return self.instance(stream)


class _CharacterParser(BaseParser):

    def __init__(self, pred, name: str = None):
        super().__init__()
        self.__pred = pred
        self.__name = name

    def __repr__(self):
        if self.__name is not None:
            return self.__name
        return '{c|%s(c)}' % self.__pred.__name__

    def __call__(self, stream: io.IOBase):
        pos = stream.tell()
        char = stream.read(1)
        if char != '' and self.__pred(char):
            return char
        raise ParseError(pos, 'Expected any of %s.' % repr(self))

    def inv(self):
        '''
        Inverts this character parser. The returned parser will match anything
        that `self` will not match, and will not match something for which
        `self` will match.
        '''
        def pred(char):
            return not self.__pred(char)
        name = '%sᶜ' % repr(self)
        return _CharacterParser(pred, name)


class _StringParser(BaseParser):

    def __init__(self, string: str):
        super().__init__()
        self.__string = string

    def __repr__(self):
        return repr(self.__string)

    def __call__(self, stream: io.IOBase):
        pos = stream.tell()
        if stream.read(len(self.__string)) == self.__string:
            return self.__string
        raise ParseError(pos, 'Expected string %s.' % repr(self.__string))


class _OptionalParser(BaseParser):

    def __init__(self, parser: BaseParser):
        super().__init__()
        self.__parser = parser

    def __repr__(self):
        return repr(self.__parser) + '?'

    def __call__(self, stream: io.IOBase):
        pos = stream.tell()
        try:
            return self.__parser(stream)
        except ParseError:
            pass
        stream.seek(pos)
        return None


class _ConcatenationParser(BaseParser):

    def __init__(self, sequence):
        super().__init__()
        self._sequence = sequence

    def __repr__(self):
        return '(' + ' '.join(repr(parser) for parser in self._sequence) + ')'

    def __call__(self, stream: io.IOBase):
        return tuple(parser(stream) for parser in self._sequence)


class _AlternationParser(BaseParser):

    def __init__(self, choices):
        super().__init__()
        self._choices = choices

    def __repr__(self):
        return ('(' + ' | '.join(repr(parser) for parser in self._choices)
                + ')')

    def __call__(self, stream: io.IOBase):
        pos = stream.tell()

        exceptions = []
        for choice in self._choices:
            try:
                return choice(stream)
            except ParseError as exception:
                exceptions.append(exception)
            stream.seek(pos)

        furthest_pos = max(e.pos for e in exceptions)
        exceptions = [exception for exception in exceptions
                      if exception.pos == furthest_pos]

        if len(exceptions) == 1:
            raise exceptions[0]

        reasons = (exception.reason for exception in exceptions)
        joined_reasons = '\n'.join('Option %d: %s' % (index, reason)
                                   for index, reason in enumerate(reasons))
        raise ParseError(furthest_pos,
                         'Tried these options:\n%s' % joined_reasons)


class _CallableWrapperParser(BaseParser):

    def __init__(self, parser: BaseParser, func):
        super().__init__()
        self.__parser = parser
        self.__func = func

    def __repr__(self):
        return repr(self.__parser)

    def __call__(self, stream: io.IOBase):
        return self.__func(self.__parser(stream))


class _RepetitionParser(BaseParser):

    def __init__(self, parser: BaseParser, min_repeats=0, max_repeats=None):
        super().__init__()
        self.__parser = parser
        self.__min_repeats = min_repeats
        self.__max_repeats = max_repeats

    def __repr__(self):
        if self.__min_repeats == 0 and self.__max_repeats is None:
            return '%s*' % repr(self.__parser)
        if self.__min_repeats == 1 and self.__max_repeats is None:
            return '%s+' % repr(self.__parser)
        if self.__max_repeats is None:
            return '%s{%d,}' % (repr(self.__parser), self.__min_repeats)
        return '%s{%d,%d}' % (repr(self.__parser),
                              self.__min_repeats, self.__max_repeats)

    def __call__(self, stream: io.IOBase):
        values = []
        for _ in range(self.__min_repeats):
            values.append(self.__parser(stream))

        repeats = self.__min_repeats
        while self.__max_repeats is None or repeats < self.__max_repeats:
            pos = stream.tell()
            try:
                values.append(self.__parser(stream))
            except ParseError:
                stream.seek(pos)
                break

        return values


class _ListParser(BaseParser):

    def __init__(self, parser: BaseParser, sep_parser: BaseParser):
        super().__init__()
        self.__parser = parser
        self.__sep_parser = sep_parser

    def __repr__(self):
        return '%s %% %s' % (repr(self.__parser),  repr(self.__sep_parser))

    def __call__(self, stream: io.IOBase):
        values = []

        pos = stream.tell()
        try:
            value = self.__parser(stream)
        except ParseError:
            stream.seek(pos)
            return values
        values.append(value)

        while True:
            pos = stream.tell()
            try:
                self.__sep_parser(stream)
            except ParseError:
                stream.seek(pos)
                break
            value = self.__parser(stream)
            values.append(value)

        return values
