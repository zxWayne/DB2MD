# -*- coding:utf-8 -*-
import os
import re


def create_folder(folder_name, perfix=None, R=True):
    if perfix is not None:
        if R is True and os.path.isdir(perfix):
            folder_name = perfix + "\\" + folder_name
        else:
            print("路径不存在")
            return False
    if os.path.isdir(folder_name):
        return True
    os.makedirs(folder_name)
    if os.path.isdir(folder_name):
        return True
    else:
        return False


def get_current_folder_file(folder_path, suffix=None):
    """
    获取文件夹下的文件名称
    :param folder_path: 要获取的文件夹路径
    :param str suffix: 过滤文件名后缀,正则表达式
    :return: 文件名列表
    """
    if not os.path.isdir(folder_path):
        return []
    files = os.listdir(folder_path)

    if suffix is not None:
        return_file_name_list = []
        for file_name in files:
            if re.match(suffix, file_name):
                return_file_name_list.append(file_name)
        return return_file_name_list
    else:
        return files


def get_folder_files_recurrence(path, file_list):
    """
    递归获取文件夹下所有的文件
    :param path: 文件夹路径
    :param list file_list:匹配到的内容存放列表
    """
    lsdir = os.listdir(path)
    dirs = [i for i in lsdir if os.path.isdir(os.path.join(path, i))]
    if dirs:
        for i in dirs:
            get_folder_files_recurrence(os.path.join(path, i), file_list)
    files = [i for i in lsdir if os.path.isfile(os.path.join(path, i))]
    for f in files:
        file_list.append(os.path.join(path, f))


def get_files_recurrence(path, suffix=None):
    """
    递归获取文件夹下所有的指定匹配文件
    :param path: 文件夹路径
    :param suffix: 匹配的正则表达式
    :return: 匹配到的文件
    """
    all_files = []
    get_folder_files_recurrence(path, all_files)
    filtered_file_list = []
    for file_name in all_files:
        if re.match(suffix, file_name):
            filtered_file_list.append(file_name)

    return filtered_file_list


def create_path(file_path):
    """
    生成文件路径
    :param str file_path:
    :return:
    """
    # 判断是文件路径还是文件夹路径
    path = os.path.dirname(file_path)
    if not os.path.isdir(path):
        os.makedirs(path)


if __name__ == '__main__':
    create_path(r"E:\项目文档\生态采集系统\调查原始数据\\")
