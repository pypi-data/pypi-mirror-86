#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : zb
# @Time    : 2020/11/17 23:21
# @Blog    : https://blog.zbmain.com

import sys, os

__common_data_path = len(sys.argv) > 1 and sys.argv[1] == '0' and '/home/common/' or '/Users/common/'
'''
    Mac Win|Linux运行环境下数据文件绝对路径地址切换方法
    使用方法:
    - python xx.py -> /Users/common/  >> [Mac|Win]
    - python xx.py 0 -> /home/common/  >> [Linux]
    - os.path.join(__common_data_path,file_path)
'''


def __join(filepath):
    '''
    绝对数据路径拼接

    :param filepath:
    :return: /common/ [filepath]
    '''
    return os.path.join(__common_data_path, filepath)


if __name__ == '':
    print(__join('main.py'))
