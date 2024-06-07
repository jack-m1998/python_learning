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


def save_groups(grouped, sheet_name, output_dir):
    for group_name, group in tqdm(grouped, desc='分类文件正在保存', unit='file'):
        output_path = os.path.join(output_dir, clean_filename(f"{group_name}.xlsx"))
        if not os.path.exists(output_path):
            with ExcelWriter(output_path, engine='openpyxl') as writer:
                group.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            with ExcelWriter(output_path, engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
                group.to_excel(writer, sheet_name=sheet_name, index=False)


def data_classification(input_excel_name, output_dir, first_column_name, second_column_name):
    """
    将文件根据一级列和二级列分类，并保存到指定路径
    :param input_excel_name: 输入文件路径
    :param output_dir: 输出文件路劲
    :param first_column_name: 一级分类列
    :param second_column_name: 二级分类列（当一列分类列中包含'*'符号时，根据二级分类列分类）
    :return: 无
    """
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
    # try:
    #     buyer_account_column = df.columns[df.columns.str.contains(first_column_name)][0]
    # except IndexError:
    #     print(f"错误：找不到包含'{first_column_name}'的列。")
    #     return

    # 检查买家账号列是否存在
    if first_column_name not in df.columns:
        print(f"错误：找不到'{first_column_name}'列。")
        return

    # 检查输出目录是否存在，如果不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 数据分类（“买家账号”带有“*”号的根据“店铺”列进行分类，不带有“*”号的则正常根据“买家账号”列进行分类）
    star_mask = df[first_column_name].str.contains(r'\*', regex=True)
    normal_accounts = df[~star_mask]
    star_accounts = df[star_mask]

    # 输出工作簿名称
    output_sheet_name = os.path.splitext(os.path.basename(input_excel_name))[0]

    # 处理不带"*"的买家账号,根据‘买家账号分类’
    normal_grouped = normal_accounts.groupby(first_column_name)
    save_groups(normal_grouped, output_sheet_name, output_dir)

    # 处理带"*"的买家账号,根据‘店铺’列分类
    if not star_accounts.empty:
        if second_column_name not in df.columns:
            print(f"错误：找不到'{second_column_name}'列。")
            return
        else:
            star_grouped = star_accounts.groupby(second_column_name)
            save_groups(star_grouped, output_sheet_name, output_dir)

    # 按买家账号分组
    # grouped = df.groupby(buyer_account_column)
    # input_filename = os.path.splitext(os.path.basename(input_excel_name))[0]

    # 遍历每个分组，并将其保存为单独的Excel文件，分类的文件工作簿名为输入excel文件名
    # for buyer_account, group in tqdm(grouped, desc='分类文件正在保存', unit='file'):
    #     # 创建输出文件的路径
    #     output_path = os.path.join(output_dir, clean_filename(f"{buyer_account}.xlsx"))
    #     # try:
    #     #     # 保存分组到Excel文件
    #     #     group.to_excel(output_path, sheet_name=input_filename, index=False)
    #     # except Exception as e:
    #     #     print(f"保存文件时发生错误：{e}")
    #     #     continue
    #
    #     # 检查文件是否存在，不存在则创建，存在则追加
    #     if not os.path.exists(output_path):
    #         with ExcelWriter(output_path, engine='openpyxl') as writer:
    #             group.to_excel(writer, sheet_name=input_filename, index=False)
    #     else:
    #         # 使用ExcelWriter的mode='a'参数来追加数据
    #         with ExcelWriter(output_path, engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
    #             group.to_excel(writer, sheet_name=input_filename, index=False)

    print(f"=================分类完成：{base_name}=================\n")


def data_classification_new(input_excel_name, output_dir, first_column_name, second_column_name):
    """
    将文件根据一级列和二级列分类，并保存到指定路径
    :param input_excel_name: 输入文件路径
    :param output_dir: 输出文件路劲
    :param first_column_name: 一级分类列
    :param second_column_name: 二级分类列（为空时按照一级分类列分类）
    :return: 无
    """
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

    # 检查买家账号列是否存在
    if first_column_name not in df.columns:
        print(f"错误：找不到'{first_column_name}'列。")
        return

    # 检查输出目录是否存在，如果不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 二级分类列为空时按照一级分类列分类
    output_sheet_name = os.path.splitext(os.path.basename(input_excel_name))[0]

    if len(second_column_name) == 0:
        normal_grouped = df.groupby(first_column_name)
        save_groups(normal_grouped, output_sheet_name, output_dir)
    else:
        # 数据分类（先根据一级分类列分将通济天和其他分类，然后根据二级分类列分类）
        tjt_mask = df[first_column_name].str.contains('通济天')
        normal_accounts = df[~tjt_mask]
        tjt_accounts = df[tjt_mask]

        # 输出工作簿名称

        # 处理非通济天的买家账号,根据‘买家账号分类’
        normal_grouped = normal_accounts.groupby(second_column_name)
        save_groups(normal_grouped, output_sheet_name, output_dir)

        # 处理通济天的买家账号,根据‘店铺’列分类
        if not tjt_accounts.empty:
            if first_column_name not in df.columns:
                print(f"错误：找不到'{first_column_name}'列。")
                return
            else:
                star_grouped = tjt_accounts.groupby(first_column_name)
                save_groups(star_grouped, output_sheet_name, output_dir)



    print(f"=================分类完成：{base_name}=================\n")


def data_handle(input_excel_name, discount_excel_name):
    # input_filename = os.path.splitext(os.path.basename(input_excel_name))[0]
    sheet_name = 'Sheet1'
    try:
        # 尝试加载数据
        df = pd.read_excel(input_excel_name, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"错误：文件 '{input_excel_name}' 不存在。")
        return

    try:
        # 尝试加载折扣表
        discount_df = pd.read_excel(discount_excel_name, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"错误：文件 '{discount_excel_name}' 不存在。")
        return

    # 将折扣信息转化为字典,并匹配折扣信息
    discount_dict = discount_df.set_index('买家帐号')['零售价折扣'].to_dict()
    df['零售价折扣'] = df['买家帐号'].map(discount_dict)

    # 合并数据,将折扣匹配到对应的买家
    # df = pd.merge(df, discount_df, on='买家帐号', how='left')

    # df['零售价单价'] = 70
    # df['零售价折扣'] = 0.7777
    # df['促销价单价'] = df['零售价单价'] * df['零售价折扣']
    #
    # # 保存小数点后一位
    # df['促销价单价'] = df['促销价单价'].round(1)
    #
    # df['对账单价'] = 60

    # 计算差异，并根据条件设置“差异”列的值
    df['差异'] = df.apply(lambda row: '无' if row['零售价单价'] - row['对账单价'] == 0 else '有', axis=1)

    # output_dir = r'测试1'
    # output_path = os.path.join(output_dir, (f"{input_filename}_handle.xlsx"))

    df.to_excel(input_excel_name, sheet_name=sheet_name, index=False)
    print(f'{input_excel_name} 处理完成')


def data_handle_ddmx(input_excel_name, discount_excel_name):
    # input_filename = os.path.splitext(os.path.basename(input_excel_name))[0]
    sheet_name = 'Sheet1'
    try:
        # 尝试加载数据
        df = pd.read_excel(input_excel_name, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"错误：文件 '{input_excel_name}' 不存在。")
        return

    try:
        # 尝试加载折扣表
        discount_df = pd.read_excel(discount_excel_name, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"错误：文件 '{discount_excel_name}' 不存在。")
        return

    # 将折扣信息转化为字典,并匹配折扣信息
    discount_dict = discount_df.set_index('买家账号')['折扣'].to_dict()
    df['折扣'] = df['买家账号'].map(discount_dict)
    df['折扣'] = df['折扣'].fillna(df['平台站点'].map(discount_dict))
    df['单价'] = df['商品单价'] / df['折扣']
    df['对账单价'] = (df['单价'] * df['折扣']).round(3)
    df['对账金额'] = (df['对账单价'] * df['数量']).round(3)
    df['差异'] = df['商品金额'] - df['对账金额']

    df.to_excel(input_excel_name, sheet_name=sheet_name, index=False)
    print(f'{input_excel_name} 处理完成')


def data_handle_xschd(input_excel_name, discount_excel_name):
    # input_filename = os.path.splitext(os.path.basename(input_excel_name))[0]
    sheet_name = 'Sheet1'
    try:
        # 尝试加载数据
        df = pd.read_excel(input_excel_name, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"错误：文件 '{input_excel_name}' 不存在。")
        return

    try:
        # 尝试加载折扣表
        discount_df = pd.read_excel(discount_excel_name, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"错误：文件 '{discount_excel_name}' 不存在。")
        return

    # 将折扣信息转化为字典,并匹配折扣信息
    discount_dict = discount_df.set_index('买家账号')['折扣'].to_dict()
    df['折扣'] = df['买家账号'].map(discount_dict)
    df['折扣'] = df['折扣'].fillna(df['店铺'].map(discount_dict))
    df['单价'] = df['售价'] / df['折扣']
    df['对账单价'] = (df['单价'] * df['折扣']).round(3)
    df['对账金额'] = (df['对账单价'] * df['实发数量']).round(3)
    df['差异'] = df['基本金额'] - df['对账金额']

    df.to_excel(input_excel_name, sheet_name=sheet_name, index=False)
    print(f'{input_excel_name} 处理完成')


def data_handle_xsthd(input_excel_name, discount_excel_name):
    # input_filename = os.path.splitext(os.path.basename(input_excel_name))[0]
    sheet_name = 'Sheet1'
    try:
        # 尝试加载数据
        df = pd.read_excel(input_excel_name, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"错误：文件 '{input_excel_name}' 不存在。")
        return

    try:
        # 尝试加载折扣表
        discount_df = pd.read_excel(discount_excel_name, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"错误：文件 '{discount_excel_name}' 不存在。")
        return

    # 将折扣信息转化为字典,并匹配折扣信息
    discount_dict = discount_df.set_index('买家账号')['折扣'].to_dict()
    df['折扣'] = df['买家账号'].map(discount_dict)
    df['折扣'] = df['折扣'].fillna(df['店铺名称'].map(discount_dict))
    df['单价'] = df['单价'] / df['折扣']
    df['对账单价'] = (df['单价'] * df['折扣']).round(3)
    df['对账金额'] = (df['对账单价'] * df['申请数量']).round(3)
    df['差异'] = df['申请金额'] - df['对账金额']

    df.to_excel(input_excel_name, sheet_name=sheet_name, index=False)
    print(f'{input_excel_name} 处理完成')


if __name__ == '__main__':
    # excelName = r'测试1\4月订单明细表.xlsx'
    # outputDir = r'测试1\output'
    # columnName = '买家帐号'

    # 参数描述：
    #   参数1：输入文件路径
    #   参数2：输出文件路劲
    #   参数3：一级分类列
    #   参数4：二级分类列（当一列分类列中包含'*'符号时，根据二级分类列分类）
    # excel_files = [
    #     (r'测试1\4月订单明细表.xlsx', r'测试1\分类结果', '买家帐号', '店铺'),
    #     (r'测试1\余额变动明细.xlsx', r'测试1\分类结果', '客户', '店铺'),
    #     (r'测试1\销售退货单.xlsx', r'测试1\分类结果', '买家帐号', '店铺'),
    #     (r'测试1\销售出货单.xlsx', r'测试1\分类结果', '买家账号', '店铺'),
    # ]

    # 订单明细表数据处理
    data_handle_ddmx(r'5月对账单\5月订单明细表.xlsx', r'5月对账单\erp客户对应折扣.xlsx')

    # 销售出库单数据处理
    data_handle_xschd(r'5月对账单\5月销售出库单（分销商）.xlsx', r'5月对账单\erp客户对应折扣.xlsx')
    data_handle_xschd(r'5月对账单\5月销售出库单（聚货通）.xlsx', r'5月对账单\erp客户对应折扣.xlsx')

    # 销售退货单数据处理
    data_handle_xsthd(r'5月对账单\5月销售退货单（分销商）.xlsx', r'5月对账单\erp客户对应折扣.xlsx')
    data_handle_xsthd(r'5月对账单\5月销售退货单（聚货通）.xlsx', r'5月对账单\erp客户对应折扣.xlsx')

    # excel_files = [
    #     (r'5月对账单\5月订单明细表.xlsx', r'5月对账单\分类结果', '买家账号', '平台站点'),
    #     (r'5月对账单\5月销售出库单（分销商）.xlsx', r'5月对账单\分类结果', '买家账号', '店铺'),
    #     (r'5月对账单\5月销售出库单（聚货通）.xlsx', r'5月对账单\分类结果', '买家账号', '店铺'),
    #     (r'5月对账单\5月销售退货单（分销商）.xlsx', r'5月对账单\分类结果', '买家账号', '店铺名称'),
    #     (r'5月对账单\5月销售退货单（聚货通）.xlsx', r'5月对账单\分类结果', '买家账号', '店铺名称'),
    # ]
    #
    # # data_handle(r'测试1\4月订单明细表_handle.xlsx', r'测试1\店铺折扣.xlsx')
    #
    # for excelName, outputDir, firstColumnName, SecondColumnName in excel_files:
    #     data_classification(excelName, outputDir, firstColumnName, SecondColumnName)

    excel_files = [
        (r'5月对账单\5月订单明细表.xlsx', r'5月对账单\分类结果', '平台站点', '买家账号'),
        (r'5月对账单\5月销售出库单（分销商）.xlsx', r'5月对账单\分类结果', '店铺', ''),
        (r'5月对账单\5月销售出库单（聚货通）.xlsx', r'5月对账单\分类结果', '店铺', '买家账号'),
        (r'5月对账单\5月销售退货单（分销商）.xlsx', r'5月对账单\分类结果', '店铺名称', ''),
        (r'5月对账单\5月销售退货单（聚货通）.xlsx', r'5月对账单\分类结果', '店铺名称', '买家账号'),
    ]

    for excelName, outputDir, firstColumnName, SecondColumnName in excel_files:
        data_classification_new(excelName, outputDir, firstColumnName, SecondColumnName)
