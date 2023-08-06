'''
Tests that primitive parser, that accept a character or a fixed string work.
'''

from aptwe import char_, str_, ParseError


def test_that_string_parser_works():
    '''
    Tests that a string parser constructed by `str_` accepts the argument
    string.
    '''
    parser = str_("test")
    assert parser.loads("test") == "test"
    try:
        parser.loads("town")
    except ParseError:
        assert True


def test_that_char_parser_works():
    '''
    Test that the family of `char_` parsers work, specifically, the function
    returns a parser, that
    1. accepts any character, if called without arguments
    2. accepts any character that is in the string, if called with ones string
    3. accepts a character for which a predicate returns true, if called with
       a function predicate.
    '''
    parser = char_()
    assert parser.loads('a') == 'a'

    parser = char_('a')
    assert parser.loads('a') == 'a'
    try:
        parser.loads('b')
    except ParseError:
        assert True

    parser = char_('ab')
    assert parser.loads('a') == 'a'
    assert parser.loads('b') == 'b'
    try:
        parser.loads('c')
    except ParseError:
        assert True

    parser = char_(str.isdigit)
    assert parser.loads('1') == '1'
    try:
        parser.loads('a')
    except ParseError:
        assert True
