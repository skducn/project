#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2024-8-5
# Description: 获取对象的属性和方法
#****************************************************************

def inspect_object(obj):
    print(f"Attributes of {obj}:")
    for attr in dir(obj):
        if not attr.startswith("__"):
            print(f"  - {attr}")


inspect_object(str)
# Attributes of <class 'str'>:
#   - capitalize
#   - casefold
#   - center
#   - count
#   - encode
#   - endswith
#   - expandtabs
#   - find
#   - format
#   - format_map
#   - index
#   - isalnum
#   - isalpha
#   - isascii
#   - isdecimal
#   - isdigit
#   - isidentifier
#   - islower
#   - isnumeric
#   - isprintable
#   - isspace
#   - istitle
#   - isupper
#   - join
#   - ljust
#   - lower
#   - lstrip
#   - maketrans
#   - partition
#   - replace
#   - rfind
#   - rindex
#   - rjust
#   - rpartition
#   - rsplit
#   - rstrip
#   - split
#   - splitlines
#   - startswith
#   - strip
#   - swapcase
#   - title
#   - translate
#   - upper
#   - zfill

inspect_object(list)
# Attributes of <class 'list'>:
#   - append
#   - clear
#   - copy
#   - count
#   - extend
#   - index
#   - insert
#   - pop
#   - remove
#   - reverse
#   - sort

inspect_object(dict)
# Attributes of <class 'dict'>:
#   - clear
#   - copy
#   - fromkeys
#   - get
#   - items
#   - keys
#   - pop
#   - popitem
#   - setdefault
#   - update
#   - values

inspect_object(set)
# Attributes of <class 'set'>:
#   - add
#   - clear
#   - copy
#   - difference
#   - difference_update
#   - discard
#   - intersection
#   - intersection_update
#   - isdisjoint
#   - issubset
#   - issuperset
#   - pop
#   - remove
#   - symmetric_difference
#   - symmetric_difference_update
#   - union
#   - update

inspect_object(tuple)
# Attributes of <class 'tuple'>:
#   - count
#   - index