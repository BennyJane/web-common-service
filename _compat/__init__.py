import sys


def isWindows():
    window_platform = False
    if sys.platform.startswith('win'):
        window_platform = True
    return window_platform


win = isWindows()


def modifyPath(relativePath: str) -> str:
    """
    :param relativePath:  目标文件的相对路径,默认输入linux下路径
    :return:
    """
    if win:
        relativePath = '\\'.join(relativePath.split('\\'))
    return relativePath
