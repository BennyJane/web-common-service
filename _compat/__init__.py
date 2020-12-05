# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning    ：The Hard Way Is Easier
import os
import sys


def isWindows():
    window_platform = False
    if sys.platform.startswith('win'):
        window_platform = True
    return window_platform


win = isWindows()


def modifyPath(relativePath: str) -> str:
    """
    :param relativePath:  目标文件的相对路径,默认输入linux下路径: logs/api; 开头不能有斜杠
    :return:
    """
    if win:
        path = '\\'.join(relativePath.split('\/'))
    else:
        path = '/'.join(relativePath.split('\\'))
    return path


root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
