import re
import jieba
import os
from langconv import *
import chardet

# 去除中文字符以外的其他字符
def clear_other(sen):
    # 正则表达式，a-z，A-Z，0-9
    pattern1 = '[a-zA-Z0-9]'
    # 去除表情
    pattern2 = re.compile(u'[\U00010000-\U0010ffff]')
    # 去除其他字符
    pattern3 = re.compile(u'[^\s1234567890:：' + '\u4e00-\u9fa5]+')
    # 去除标点符号
    pattern4 = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
    step1 = re.sub(pattern1, '', sen)
    step2 = re.sub(pattern2, '', step1)
    step3 = re.sub(pattern3, '', step2)
    step4 = re.sub(pattern4, '', step3)
    # 去除空格
    last = ''.join(step4.split())
    return last

def clear_stopwords(sens, i):
    sens_list = []
    # 读取停用词表
    stopwords = {}.fromkeys([line.rstrip() for line in open('cn_stopwords.txt', encoding="utf-8")])
    # 将停用词转换为列表
    stopwords_list = set(stopwords)
    for sen in sens:
        # 用jieba进行中文分词
        words_list = jieba.lcut(sen)
        # 这一句好神奇啊，用一句话得到了句子列表，该列表是去除了中文停用词的
        sen_words = [w for w in words_list if w not in stopwords_list]
        # 这一句是将列表转换为字符串，即重新转换为句子
        after_sen = ''.join(sen_words)
        # 将每一个转换完成的句子，都存在一个新的列表中
        sens_list.append(after_sen)
    # 将之前定义好的新的列表，转换为句子，这一次去除停用词就完成了
    sens = ''.join(sens_list)
    # 再次分词，只不过用cut的话，返回的就是不是列表了
    sens = jieba.cut(sens, cut_all=False)
    sens_list = list(sens)
    txt = str(sens_list)
    path_cut_list = 'E:\\21.3大三下\互联网搜索引擎\Deal_Txt\ZhongWen_Res\CutWordList_C'
    with open(path_cut_list + str(i) + '_C.txt', 'w', encoding='utf-8') as f:
        f.write(txt)
    path_cut = 'E:\\21.3大三下\互联网搜索引擎\Deal_Txt\ZhongWen_Res\CutWordZiFu_C'
    with open(path_cut + str(i) + '_C.txt', 'w', encoding='utf-8') as f:
        f.write(" ".join(i for i in sens_list))


if __name__ == '__main__':
    # 中文爬取文本文件目录
    # path = "E:\\21.3大三下\互联网搜索引擎\Deal_Txt\Article_C"
    path = "E:\\21.3大三下\互联网搜索引擎\工程文件-参考\contents_C"
    # 得到文件夹下的所有文件名称
    files = os.listdir(path)
    i = 1
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            with open(path + "/" + file, "rb") as f:  # 二进制格式文件参数为rb
                text = f.read()  # 是bytes
            encode_type = chardet.detect(text)  # 检测编码格式
            if encode_type['encoding'] != None:  # 排除不能解码的情况
                text = text.decode(encoding='gb18030')  # 进行相应解码，赋给原标识符（变量）
                txt = clear_other(text)

                clear_stopwords(txt, i)
                i += 1
