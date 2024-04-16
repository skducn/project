# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
# *****************************************************************

import chardet

a = b"test"
print(chardet.detect(a))  # {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}


def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        result = chardet.detect(data)
        return result


result = detect_file_encoding("/Users/linghuchong/Downloads/51/Python/project/a.txt")
print(result)  # {'encoding': 'GB2312', 'confidence': 0.99, 'language': 'Chinese'}



