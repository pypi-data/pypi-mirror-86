'''
Tests that parser composition rules work.
'''

from aptwe import Parser, str_, ParseError


def test_that_concatenation_works():
    '''
    Tests that a concatenation parser should return a tuple of parse results
    '''
    parser = str_('hello') >> str_(' ') >> str_('world')
    assert parser.loads('hello world') == ('hello', ' ', 'world')


def test_that_alternation_works():
    '''
    Tests that an alternation parser returns the parse results of either one
    of the composed parsers.
    '''
    parser = str_('hello world') | str_('hello')
    assert parser.loads('hello') == 'hello'
    assert parser.loads('hello world') == 'hello world'


def test_that_optional_works():
    '''
    Tests that an optional parser returns either the parse result or None.
    '''
    parser = -str_('hello world')
    assert parser.loads('hello world') == 'hello world'
    assert parser.loads('hello') is None


def test_that_repetition_works():
    '''
    Tests that a repetition parser returns a list of parse results.
    '''
    parser = +str_('abc')
    try:
        parser.loads('')
    except ParseError:
        assert True
    assert parser.loads('abc') == ['abc']
    assert parser.loads('abcabc') == ['abc', 'abc']

    parser = ~str_('abc')
    assert parser.loads('') == []
    assert parser.loads('abc') == ['abc']
    assert parser.loads('abcabc') == ['abc', 'abc']


def test_that_recursion_works():
    '''
    Tests that a recursion parser can be constructed by usage of `Parser` and
    the `parser[...] = ...` notation. Checks if the rule `p = \'b\'|\'a\'p`
    works.
    '''
    parser = Parser()
    parser[...] = str_('b') | str_('a') >> parser
    assert parser.loads('b') == 'b'
    assert parser.loads('ab') == ('a', 'b')
    assert parser.loads('aab') == ('a', ('a', 'b'))
    assert parser.loads('aaab') == ('a', ('a', ('a', 'b')))


def test_that_chaining_functions_work():
    '''
    Tests that the function chaining parser returns the result of the
    function call with the parse result as argument.
    '''
    parser = str_('42')[int]
    assert parser.loads('42') == 42
