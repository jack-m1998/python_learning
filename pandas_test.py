# -*- coding: utf-8 -*-
"""
Author: majia
time: 2024/5/25
filename: pandas_test
"""

import numpy as np
import pandas as pd


def excel_test():
    source_data = pd.read_excel(r'C:\Users\26544\Desktop\测试1\4月订单明细表.xlsx')
    df = pd.DataFrame(source_data)
    print(df)

    # 维度查看
    # print("维度：\n{}".format(df.shape))

    # 数据表信息
    # print("数据表信息：\n{}".format(df.info))

    # 查看所有行的列索引名
    # print("得到一个对象：\n{}".format(df.index))
    # print("得到一个列表：\n{}".format(df.index.values))

    # 查看所有列的列索引名
    # print("得到一个对象：\n{}".format(df.columns))
    # print("得到一个列表：\n{}".format(df.columns.values))

    # 查看某一列的所有值
    # print("查看某一列的所有值：\n{}".format(df["买家帐号"].values))

    # 查看第3行的数据
    # print("查看某一列的所有值：\n{}".format(df.iloc[3].values))

    # 查看数据表的值
    # print("查看数据表的值：\n{}".format(df.values))

    # 数据输出
    source_data.to_excel(r'C:\Users\26544\Desktop\测试1\test.xlsx', sheet_name='4月订单明细表', index=False)


if __name__ == '__main__':
    excel_test()
