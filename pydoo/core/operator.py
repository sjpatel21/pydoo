# -*- coding: utf-8 -*-


EQUAL = '='
NOT_EQUAL = '!='

GREATER = '>'

GREATER_OR_EQUAL = '>='

LESS = '<'

LESS_OR_EQUAL = '<='

""" returns true if value is either None or False, otherwise behaves
    like =
    """
UNSET_OR_EQUAL = '=?'

LIKE_EQUAL = '=like'
""" matches field_name against the value pattern. An underscore _ in
the pattern stands for (matches) any single character; a percent
sign % matches any string of zero or more characters.
"""

""" matches field_name against the %value% pattern. Similar to =like
but wraps value with '%' before matching
"""
LIKE = 'like'

""" doesn't match against the %value% pattern
"""
NOT_LIKE = 'not like'

""" case insensitive like
"""
ILIKE = 'ilike'

""" case insensitive not like
"""
NOT_ILIKE = 'not ilike'

""" case insensitive =like
"""
ILIKE_EQUAL = '=ilike'

""" is equal to any of the items from value, value should be a list
of items
"""
IN = 'in'

""" is unequal to all of the items from value
"""
NOT_IN = 'not in'

""" is a child (descendant) of a value record.
Takes the semantics of the model into account (i.e following the
relationship field named by _parent_name).
"""
CHILD_OF = 'child_of'
