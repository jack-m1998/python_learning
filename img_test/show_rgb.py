# -*- coding: utf-8 -*-
"""
Author: majia
time: 2024/6/12
filename: show_rgb
"""

import numpy as np

# opencv
import cv2

# matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def opencv_display_rgb(img_path, type):
    # 假设您知道图像的宽度和高度
    width = 1920  # 图像的宽度
    height = 1080  # 图像的高度

    # 打开.bgr图像文件
    with open(img_path, 'rb') as f:
        data = f.read()

        # uint8 rgb image
        if type == 'uint8':
            # img_hwc = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))
            img_chw = np.frombuffer(data, dtype=np.uint8).reshape((3, height, width))
            img_hwc = img_chw.transpose((1, 2, 0))
            img_hwc_float = img_hwc.astype(np.float32) / 255
        elif type == 'float32':
            # float rgb image
            img_chw = np.frombuffer(data, dtype=np.float32).reshape((3, height, width))
            img_hwc = img_chw.transpose((1, 2, 0))
        else:
            print('type illegal')

    # 图像的数据格式
    print(f'图像数据格式为：{img_hwc.dtype}')

    # OpenCV默认以BGR格式存储，所以可以直接显示
    cv2.imshow(f'图像类型:RGB   图片大小{round(img_hwc.size * img_hwc.itemsize / 1024 / 1024, 1)}M   数据格式:{img_hwc.dtype}', img_hwc)
    # cv2.imshow('Concatenated Image', concatenated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def opencv_display_rgb_more(img_path, type):
    # 假设您知道图像的宽度和高度
    width = 1920  # 图像的宽度
    height = 1080  # 图像的高度

    # 打开.bgr图像文件
    with open(img_path, 'rb') as f:
        data = f.read()

        # uint8 rgb image
        if type == 'uint8':
            # img_hwc = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))
            img_chw = np.frombuffer(data, dtype=np.uint8).reshape((3, height, width))
            img_hwc = img_chw.transpose((1, 2, 0))
            img_hwc_float = img_hwc.astype(np.float32) / 255
        elif type == 'float32':
            # float rgb image
            img_chw = np.frombuffer(data, dtype=np.float32).reshape((3, height, width))
            img_hwc = img_chw.transpose((1, 2, 0))
        else:
            print('type illegal')

    images = [img_hwc, img_hwc, img_hwc]  # img1, img2, img3是RGB格式的图片数组

    # 计算合并后的图片的宽度和高度
    width = max(img.shape[1] for img in images)
    height = sum(img.shape[0] for img in images)

    # 创建一个足够大的空白画布
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    # 将每张图片放置到画布上
    y_offset = 0
    for img in images:
        canvas[y_offset:y_offset + img.shape[0], :img.shape[1]] = img
        y_offset += img.shape[0]

    # 使用OpenCV显示合并后的图片
    cv2.imshow('Merged Images', canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # # OpenCV默认以BGR格式存储，所以可以直接显示
    # cv2.imshow(f'图像类型:RGB   图片大小{round(img_hwc.size * img_hwc.itemsize / 1024 / 1024, 1)}M   数据格式:{img_hwc.dtype}', img_hwc)
    # # cv2.imshow('Concatenated Image', concatenated_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def opencv_rgb_uint8_to_float32(img_path):
    # 假设您知道图像的宽度和高度
    width = 1920  # 图像的宽度
    height = 1080  # 图像的高度

    # 打开.bgr图像文件
    with open(img_path, 'rb') as f:
        data = f.read()
        img_chw = np.frombuffer(data, dtype=np.uint8).reshape((3, height, width))

        # 将图像数据转换为float32类型
        img_chw_float = img_chw.astype(np.float32)

        # 保存图像
        save_path = 'rgb_float32.bgr'  # 您希望保存图像的路径
        cv2.imwrite(save_path, img_chw_float)


def opencv_display_yuv420(img_path):
    # 假设您知道图像的宽度和高度
    width = 1920  # 图像的宽度
    height = 1080  # 图像的高度
    # 读取YUV图像文件
    with open(img_path, 'rb') as f:
        yuv_data = f.read()

    # 将原始YUV420数据转换为YUV I420格式的图像
    yuv_i420 = np.frombuffer(yuv_data, dtype=np.uint8).reshape((height * 3 // 2, width))

    # 将YUV I420图像转换为BGR格式
    bgr_image = cv2.cvtColor(yuv_i420, cv2.COLOR_YUV420sp2BGR)

    # 显示图像
    cv2.imshow('YUV420 Image', bgr_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def opencv_print_rgb_data_type(img_path):
    # 假设您知道图像的宽度和高度
    width = 1920  # 图像的宽度
    height = 1080  # 图像的高度

    # 打开.bgr图像文件
    with open(img_path, 'rb') as f:
        data = f.read()
        img = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))

    print(img.dtype)


def matplotlib_display_rgb(img_path):
    img = mpimg.imread(img_path)  # 替换为您的图像文件路径

    # 使用imshow()函数显示图像
    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    rgb_files = [
        ('chn0_w1920_h1080_rgb_uint8.bgr', 'uint8'),
        ('chn0_w1920_h1080_rgb_float.bgr', 'float32'),
        ('chn0_w1920_h1080_rgb_float_out.bgr', 'float32'),
    ]

    rgb_file = rgb_files[0]
    opencv_display_rgb(rgb_file[0], rgb_file[1])

    # opencv_display_rgb_more(rgb_file[0], rgb_file[1])

    # rgb_img_path = 'chn0_w1920_h1080_RGB.bgr'
    # opencv_display_rgb(rgb_img_path, 'uint8')
    # rgb_img_path = 'ch0_rgb_float.bgr'
    # opencv_display_rgb(rgb_img_path, 'float32')

    # opencv_rgb_uint8_to_float32(rgb_img_path)

    # yuv_img_path = 'chn0_w1920_h1080_YUV.yuv'
    # opencv_display_yuv420(yuv_img_path)

    # opencv_print_rgb_data_type(rgb_img_path)
    # matplotlib_display_rgb(rgb_img_path)