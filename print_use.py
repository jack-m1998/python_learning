# -*- coding: utf-8 -*-
"""
Author: majia
time: 2024/5/25
filename: print_use
"""
from datetime import datetime


def print_sample():
    # 单引号输出，一对单引号，单引号里可以用双引号，并可以将单引号打印出来
    print('hello')
    print('"hello"')

    # 双引号输出，一对双引号，双引号里可以用单引号，并可以将单引号打印出来
    print("hello")
    print("'hell'")

    # 三引号输出，一对三引号，引用多行文本
    multilinetext = """
    They who cannot do as they would,
    must do as they can.
    不能如愿而行，
    也须尽力而为。
    """
    print(multilinetext)

    # 换行方法，使用'\n'
    print("hello\nit's me")

    # 换行方法，使用end，用end参数来设置你想要的结束符号
    print("hello", end=" ")
    print("it's me", end="\n")
    print("i'm ok", end="|")
    print("\n")

    # 区隔符 sep
    print("谋事在人", "成事在天", "有生命便有希望", sep="&")
    print("www", "csdn", "net", sep=".")

    # 制表符
    print("不能如愿而行\t也须尽力而为")

    # '+'连接输出
    print("学习"+" "+"python")

    # 输出数学表达式
    print(1+2+3)

    # 打印输出反斜杠 \
    print("不能如愿而行\\也须尽力而为")

    # 变量输出
    test_str = "你好"
    print(test_str)

    # 数据的格式化输出
    name = "jack-m"
    print("我的名字是 %s " % name)

    age = 100
    print("我的年龄是 %d" % age + "岁了")

    s = '逆境清醒'
    x = len(s)
    print('%s名字的长度是 %d' % (s, x))

    print('%c' % 90)

    # format格式化输出
    name = "jack"
    age = 25
    print("My name is {} and I am {} years old.".format(name, age))
    print("My name is {1} and I am {0} years old.".format(age, name))
    print("My name is {name} and I am {age} years old.".format(name=name, age=age))

    num = 3.14159
    print("The value of pi is approximately {:.2f}.".format(num))

    now = datetime.now()
    print("Current date and time: {:%Y-%m-%d %H:%M:%S}".format(now))


if __name__ == '__main__':
    print_sample()
