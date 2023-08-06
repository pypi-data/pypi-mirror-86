#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-05-30 22:51:45
# @Description : 包含基本的文件读写，指定扩展名文件查找等基本工具


__version__ = "0.1.9"


import math


def dict_sorted(data: dict, flag: int = 0, ascending: bool = True):
    """
    对dict排序

    Args:
        data(dict): 目标数据dict类型
        flat(int):  默认为0，表示按照字典的key进行排序；1表示按照value进行排序
        ascending(bool): 默认为True，表示按照升序排序；False表示降序排序

    Returns:
        dict: 排序后的数据
    """
    return dict(sorted(data.items(), key=lambda x: x[flag], reverse=not ascending))


def list_deduplicate(data: list):
    """列表项为dict类型的去重

    Args:
        data(list): 目标数据，list类型

    Returns:
        list: 去重后的数据
    """
    return [dict(t) for t in set([tuple(d.items()) for d in data])]


def sort_list(
    data: list,
    ascending: bool = True,
    flag: int = 0,
    position: int = 0,
    key: str = "",
):
    """
    对 list 进行排序

    Args:
        data(list): list 类型数据，item 为 dict 或者 basic type
        ascending(bool): 默认为 True，表示升序；False 表示降序
        flag(int): 0 表示元素为基本类型，1 表示元素为 dict，2 表示元素为 tuple
        position(int): 如果元素为 basic type，position 保持默认即可；
            如果元素为 tuple，position 的数值表示以哪个 index 位置的值排序
        key(str): 如果元素为 dict，key 表示按照哪个 key 的 value 进行排序

    Returns:
        list: 排序后的数据
    """
    if flag == 0:
        # basic type
        data.sort(reverse=not ascending)
    elif flag == 1:
        # dict type
        if key == "":
            key, _ = data[0].items()[0]
        data.sort(key=lambda x: x.get(key, 0), reverse=not ascending)
    elif flag == 2:
        # tuple type
        if position < 0 or position >= len(data[0]):
            position = 0
        data.sort(key=lambda x: x[position], reverse=not ascending)

    return data


def strips(string: str):
    """
    去除字符串两端的空格符和换行符，并且去除中间的换行符
    """
    return string.strip().replace("\n", "").replace("\r", "").replace("\r\n", "")


def remove_0_str(data: list):
    """
    去除list列表中为长度为0的字符串，用于字符串split后，列表中出现长度为0字符串的去除
    """
    return [item for item in data if len(str(item)) != 0]


def chunks(arr, m):
    """分割列表，但是子list元素个数尽可能平均

    Args:
        arr (list): 待分割的list
        m (int): 分成几份

    Returns:
        list: 分割后的每个子list都是返回结果list的一个元素
    """
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i : i + n] for i in range(0, len(arr), n)]


#  if __name__ == "__main__":
#      # get_paths_from_dir测试
#      #  result = get_paths_from_dir("../", "py", recusive=True)
#      #  print(result)
#
#      # #### sort_list测试
#      # alist = [
#      #     {"level": 19, "star": 36, "time": 1},
#      #     {"level": 20, "star": 40, "time": 2},
#      #     {"level": 20, "star": 40, "time": 3},
#      #     {"level": 20, "star": 40, "time": 4},
#      #     {"level": 20, "star": 40, "time": 5},
#      #     {"level": 20, "star": 40},
#      #     {"level": 18, "star": 40, "time": 1},
#      # ]
#      # result = sort_list(alist, ascending=False, flag=1, key="time")
#      #
#      # alist = [
#      #     (1, 2, 3),
#      #     (0, 1, 2),
#      #     (3, 4),
#      #     (2, 3, 4),
#      # ]
#      # result = sort_list(data=alist, ascending=False, flag=2, position=1)
#      #
#      # alist = [6, 4, 9, 10, 0]
#      # alist = ["acc", "cdef", "xyz", "0234", "123"]
#      # result = sort_list(data=alist, ascending=False)
#      #
#      # print(result)
#
#      # data = {"b": 1, "a": 2}
#      # res = dict_sorted(data, flag=1, ascending=True)
#      # print(res)
#
#      pass
