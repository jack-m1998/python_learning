# -*- coding: utf-8 -*-
"""
Author: majia
time: 2024/5/26
filename: bill_data_collation
"""

from openpyxl import load_workbook
from pandas import ExcelWriter
from tqdm import tqdm
import pandas as pd
import os
import re


def clean_filename(filename):
    # 定义Windows系统中不允许的非法字符
    invalid_chars = r'[\<>:\"/|?*]'
    # 使用正则表达式替换非法字符为空字符串
    clean_name = re.sub(invalid_chars, '', filename)
    return clean_name


def data_classification(input_excel_name, output_dir, column_name):
    base_name = os.path.basename(input_excel_name)
    print(f"================= 开始分类：{base_name} ==============")

    sheet_name = 'Sheet1'
    try:
        # 尝试加载数据
        df = pd.read_excel(input_excel_name, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"错误：文件 '{input_excel_name}' 不存在。")
        return
    except ValueError as e:
        if 'No sheet named' in str(e):
            print(f"错误：'{sheet_name}' 工作簿不存在于文件中。")
        else:
            print(f"未知的ValueError: {e}")
        return
    except Exception as e:
        print(f"读取Excel文件时发生未知错误：{e}")
        return

        # 尝试自动查找包含"买家账号"的列名
    try:
        buyer_account_column = df.columns[df.columns.str.contains(column_name)][0]
    except IndexError:
        print(f"错误：找不到包含'{column_name}'的列。")
        return

    # 检查输出目录是否存在，如果不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 按买家账号分组
    grouped = df.groupby(buyer_account_column)
    input_filename = os.path.splitext(os.path.basename(input_excel_name))[0]

    # 遍历每个分组，并将其保存为单独的Excel文件，分类的文件工作簿名为输入excel文件名
    for buyer_account, group in tqdm(grouped, desc='分类文件正在保存', unit='file'):
        # 创建输出文件的路径
        output_path = os.path.join(output_dir, clean_filename(f"{buyer_account}.xlsx"))
        # try:
        #     # 保存分组到Excel文件
        #     group.to_excel(output_path, sheet_name=input_filename, index=False)
        # except Exception as e:
        #     print(f"保存文件时发生错误：{e}")
        #     continue

        # 检查文件是否存在，不存在则创建，存在则追加
        if not os.path.exists(output_path):
            with ExcelWriter(output_path, engine='openpyxl') as writer:
                group.to_excel(writer, sheet_name=input_filename, index=False)
        else:
            # 使用ExcelWriter的mode='a'参数来追加数据
            with ExcelWriter(output_path, engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
                group.to_excel(writer, sheet_name=input_filename, index=False)

    print(f"=================分类完成：{base_name}=================\n")


if __name__ == '__main__':
    # excelName = r'测试1\4月订单明细表.xlsx'
    # outputDir = r'测试1\output'
    # columnName = '买家帐号'

    excel_files = [
        (r'测试1\4月订单明细表.xlsx', r'测试1\分类结果', '买家帐号'),
        (r'测试1\余额变动明细.xlsx', r'测试1\分类结果', '客户'),
        (r'测试1\销售退货单.xlsx', r'测试1\分类结果', '买家帐号'),
        (r'测试1\销售出货单.xlsx', r'测试1\分类结果', '买家账号'),
    ]

    for excelName, outputDir, columnName in excel_files:
        data_classification(excelName, outputDir, columnName)