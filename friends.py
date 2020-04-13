# Project   : friends_subtitles 
# File      : friends.py
# Author    : Byron Zhao
# Email     : 330726651@qq.com
# DateTime  : 2020/4/13 9:13
# MadeBy    : PyCharm
# pyinstaller -F 文件名.py

# import logging
# import sys
# 
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# 
# handler1 = logging.StreamHandler(sys.stdout)
# handler1.setLevel(logging.DEBUG)
# 
# handler2 = logging.FileHandler(__name__ + "log.txt", encoding="utf8")
# handler2.setLevel(logging.WARNING)
# 
# formatter = logging.Formatter(
#     "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s")
# handler1.setFormatter(formatter)
# handler2.setFormatter(formatter)
# 
# logger.addHandler(handler1)
# logger.addHandler(handler2)


# 10个文件夹的视频，10个文件夹的字幕
# 把字幕移动到视频文件夹

# 把1个文件夹的字幕移动到1个视频文件夹

# D:\python_temp\friends_experiment\subtitle_files
# D:\python_temp\friends_experiment\videofiles

import os
import re
import shutil

def get_files(file_type, folder):
    """
    获取文件夹 folder 下所有 file_type 类型的文件，并返回列表
    :param file_type:
    :param folder:
    :return:
    """
    result = []
    files = os.listdir(folder)
    for i in files:
        if os.path.isfile(os.path.join(folder, i)) and i[-len(file_type):] == file_type:
            result.append(i)
    return result


def match(filename, lst, s1="s", e1="e", s2="S", e2="e"):
    """
    提取filename中 s1+数字+e1+数字 形式的信息，并在lst中匹配与之一致的信息
    :param filename:
    :param lst:
    :param s1:
    :param e1:
    :param s2:
    :param e2:
    :return: lst中与filename编号一致的内容
    """
    result = None
    rule = s1+"\d*"+ e1+"\d*"

    if re.search(rule, filename) is not None:
        se = re.search(rule, filename).group(0)
        season = re.search(s1+"\d*", se).group(0)[1:]
        episodes = re.search(e1+"\d*", se).group(0)[1:]
        match_contant = s2+season+e2+episodes
        for i in lst:
            if match_contant in i:
                result = i
                break
    return result
#
#
def rename(filename, type="ass"):
    name = os.path.splitext(filename)[0]
    return name+"."+type

#
#
def folder_map(folder_key, folder_value, season1="S", season2="S"):
    result = {}
    keys = os.listdir(folder_key)
    values = os.listdir(folder_value)
    for eachfolder in keys:
        matched_folder = match(eachfolder, values, s1=season1, e1="", s2=season2, e2="")
        if matched_folder is not None:
            complit_key = os.path.join(folder_key, eachfolder)
            complit_value = os.path.join(folder_value, matched_folder)
            result[complit_key] = complit_value

    return result
# #
#
def folder_move(video_folder, ass_folder):
    mkv = get_files("mkv", video_folder)
    ass = get_files("ass", ass_folder)
    for i in mkv:
        match_result = match(i, ass)
        if match_result != None:
            new_name = rename(i, "ass")
            path_n_file_src = os.path.join(ass_folder, match_result)
            path_n_file_dst = os.path.join(video_folder, new_name)
            shutil.move(path_n_file_src, path_n_file_dst)
# #
#
def main(basefolder1, basefolder2):
    folders = folder_map(basefolder1, basefolder2)
    for i in folders:
        folder_move(i, folders[i])
    print("finished")



if __name__ == '__main__':
    subtitle_position = r"D:\python_temp\friends_experiment\subtitle_files111"
    video_position = r"D:\python_temp\friends_experiment\videofiles222"
    main(video_position, subtitle_position)

    # debug code
    # checking_folder = r"D:\python_temp\friends_experiment\subtitle_files\akhdasdh_S09_afljadskf"
    # checking = get_files("ass", checking_folder)
    # print(checking)
    # m = match('[HDmeiju.COM]friends.s09e11.720p.bluray.x264-cinefile.mkv',  checking)
    # print(m)


    # print(folder_map(video_position, subtitle_position))
    # n = rename("[HDmeiju.COM]friends.s09e11.720p.bluray.x264-cinefile.mkv")
    # print(n)
    # folder_move(r"D:\python_temp\friends_experiment\videofiles\Friends.S09.720p.BluRay.x264-PSYCHD", r"D:\python_temp\friends_experiment\subtitle_files\akhdasdh_S09_afljadskf")





