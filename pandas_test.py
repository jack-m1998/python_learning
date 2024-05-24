# -*- coding: utf-8 -*-
"""
Author: majia
time: 2024/5/25
filename: pandas_test
"""

import numpy as np
import pandas as pd


def readExcel():
    df = pd.DataFrame(pd.read_excel(r'C:\Users\26544\Desktop\测试1\4月订单明细表.xlsx'))
    print(df)
    # 维度查看
    print(df.shape)


if __name__ == '__main__':
    readExcel()
