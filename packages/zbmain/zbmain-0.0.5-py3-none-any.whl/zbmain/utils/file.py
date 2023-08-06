#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : zb
# @Time    : 2020/11/18 22:27
# @Blog    : https://blog.zbmain.com


def write(char,filepath = 'tmp.txt'):
    with open(filepath,"a") as file:
            file.write(str(char)+"\n")

