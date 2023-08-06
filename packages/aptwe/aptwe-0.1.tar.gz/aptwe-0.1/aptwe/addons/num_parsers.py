'''
Defines `int` and `float` parsers.
'''

from .char_parsers import digit_
from ..primitives import char_, str_
from ..functions import concat, value_or, getitem

__num_ = (+digit_)[concat]
__sign_ = (-char_('+-'))[value_or(str)]
__exp_ = (-(char_('eE') >> __sign_ >> __num_)[concat])[value_or(str)]
__esc_char_ = (str_('\\') >> char_())[getitem(1)] | char_('"').inv()

int_ = (__sign_ >> __num_)[concat][int] @ 'int'
float_ = (__sign_ >> __num_ >> str_('.') >> (-__num_)[value_or(str)]
          >> __exp_)[concat][float] @ 'float'
