'''
APTWE is a framework to create recursive descent parsers. It intends to define
parsers inside the Python syntax similarily to writing EBNF. For example:

~~~
nested_lists_ = Parser('NestedLists')
list_contents_ = int_ >> str_(',') >> int_
list_ = (str_('[') >> list_contents_ >> str_(']'))[getitem(1)]
nested_lists_[...] = int_ | list_

nested_lists_.loads('[1,[2,3]]') # Returns [1,[2,3]]
~~~
'''

from .parser import BaseParser, Parser
from .primitives import char_, str_
from .functions import getitem, value_or, concat
from .exceptions import ParseError
