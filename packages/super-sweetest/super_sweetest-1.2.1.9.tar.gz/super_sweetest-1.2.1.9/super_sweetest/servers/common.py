# coding=utf-8

# @Time: 2020/3/5 10:57
# @Auther: liyubin

import json

"""
公共读写方法
"""

def write_data(file_name, data_, flag='', mode='w+'):
    if flag.lower() == 'json' and mode.lower() == 'w+':
        with open(file_name, 'w+', encoding='utf-8') as fp:
            json.dump(data_, fp)
    elif flag.lower() == 'eval' and mode.lower() == 'w+':
        with open(file_name, 'w+', encoding='utf-8')as fp:
            fp.write(eval(data_))
    elif mode.lower() == 'w+':
        with open(file_name, 'w+', encoding='utf-8')as fp:
            fp.write(data_)
    else:
        with open(file_name, 'a+', encoding='utf-8')as fp:
            fp.write(data_)


def read_data(file_name, flag='json', mode='r'):
    if mode == 'r':
        with open(file_name, 'r', encoding='utf-8')as fp:
            data_ = fp.read()
    elif mode == 'rb':
        with open(file_name, 'rb')as fp: # 不加encoding
            data_ = fp.read()
    else:
        with open(file_name, 'r+', encoding='utf-8')as fp:
            data_ = fp.read()
    if flag == 'json':
        try:
            return json.loads(data_)
        except Exception as e:
            raise 'Json文件内容格式错误' + str(e)
    elif flag == 'eval':
        return eval(data_)
    else:
        return data_


def read_json_to_copywrite(error_json_file, copywrite_file, language):
    """
    读取识别后错误的json内容去重写入对应语言的文案中
    :param error_json_file:
    :param copywrite_file:
    :param language:
    :return:
    """
    # 读取错误list或者文案原本dict
    with open(error_json_file, 'rb')as fp:
        data = json.load(fp)
    print("准备写入的，识别后UI文本内容：", data)
    # 读取自动化中使用的按语言分类的文案内容
    with open(copywrite_file, 'rb')as fp1:
     copywriting = json.load(fp1)


    # 提取错误list和原始dict，如果 不 在语言分类文案中
    v_str = ''
    if isinstance(data, dict):
        for k, v in data.items():
            if v not in copywriting[language]:
             v_str = v + v_str
    else:
        for v in data:
            if v not in copywriting[language]:
                v_str = v + v_str

    # 追加对应语言的不重复的文本
    copywriting_en_v = copywriting[language] + v_str
    copywriting[language] = copywriting_en_v

    print("最新文案内容：", copywriting)

    # 写入最终文案到 语言分类的文案内容
    with open(copywrite_file, 'w')as fp2:
        json.dump(copywriting, fp2)