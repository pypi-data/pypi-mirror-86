'''
Defines character parsers that accepts characters for which the method
`str.is`* returns true.
'''

from ..primitives import char_

alnum_ = char_(str.isalnum)
alpha_ = char_(str.isalpha)
digit_ = char_(str.isdigit)
lower_ = char_(str.islower)
upper_ = char_(str.isupper)
space_ = char_(str.isspace)
