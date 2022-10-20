# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2022-10-12
# Description: # python -L
# http://www.51testing.com/html/86/n-7793486.html
# *****************************************************************

import importlib
# importlib.set_lazy_imports(True)


importlib.set_lazy_imports(True,excluding=["one.mod", "spam"])


from lazy_loader import *


print("imports done")








