# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-01-28
# Description:
# pip3.9 install seaborn
# 官网 https://www.joinquant.com/research?target=research&url=/user/60048557286/notebooks/%E6%96%B0%E6%89%8B%E6%8C%87%E5%BC%95.ipynb
# *****************************************************************

import pandas as pd
import seaborn as sns


df = get_price('510300.XSHG', start_date='2014-01-01', end_date='2015-01-31', frequency='daily', fields=['open','close'])

get_