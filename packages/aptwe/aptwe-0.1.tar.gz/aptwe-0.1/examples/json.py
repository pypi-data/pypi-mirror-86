'''
A Json parser.
'''

from aptwe import Parser, str_, char_, getitem, concat
from aptwe.addons import float_, int_, space_

_parser = Parser('Json')
__esc_char_ = (str_('\\') >> char_())[getitem(1)] | char_('"').inv()
_string = (str_('"')
           >> (~__esc_char_)[concat]
           >> str_('"'))[getitem(1)] @ 'string'
_whitespace = ~space_
_dict_key = (_whitespace >> _string >> _whitespace)[getitem(1)] @ 'dict_key'
_dict_entry = (_dict_key >> str_(':') >> _parser)[getitem((0, 2))]
_dict = (str_('{')
         >> (_dict_entry % str_(','))[dict]
         >> str_('}'))[getitem(1)] @ 'dict'
_list = (str_('[')
         >> _parser % str_(',')
         >> str_(']'))[getitem(1)] @ 'list'
_parser[...] = (_whitespace
                >> (float_ | int_ | _string | _dict | _list)
                >> _whitespace)[getitem(1)]

load = _parser.load
loads = _parser.loads
