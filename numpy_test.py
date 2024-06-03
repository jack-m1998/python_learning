# -*- coding: utf-8 -*-
"""
Author: majia
time: 2024/6/3
filename: numpy_test
"""

import numpy as np


def numpy_test():
    # 创建一个2x3的数组
    array = np.array([[1, 2, 3], [4, 5, 6]])

    # 打印原始数组
    print("原始数组:")
    print(array)

    # 计算所有元素的总和
    summ = np.sum(array)
    print("元素总和:", summ)

    # 计算数组的平均值
    mean = np.mean(array)
    print("平均值:", mean)

    # 计算数组的标准差
    std_dev = np.std(array)
    print("标准差:", std_dev)

    # 找到数组中的最大值
    max_value = np.max(array)
    print("最大值:", max_value)

    # 找到数组中的最小值
    min_value = np.min(array)
    print("最小值:", min_value)

    return


if __name__ == '__main__':
    numpy_test()
