import os
import nltk
from nltk.stem import WordNetLemmatizer #词性还原 词形归并工具
from nltk.tokenize import word_tokenize #分词
from nltk.corpus import stopwords       #去停用词
from nltk.stem.porter import PorterStemmer #词干提取
import chardet                          #检测编码格式
import re                               #匹配去标点符号，特殊字符

nltk.download('stopwords')
cachedStopWords = stopwords.words("english")    #选用英文停用词词典

def word_tokenize_stopwords_removal(all_text, i):

    # 去除英文文本中的其他字符，进行分词
    other = re.sub("[+:\.\!\/_,$%^*(+\"\'<>=]+|[+——！，。？、~@#￥%……&*（）]+", " ", all_text)
    clear_other = word_tokenize(other)
    words = [word for word in clear_other if (str.isalpha(word) is not False)]
    path_cutwords = 'E:\\21.3大三下\互联网搜索引擎\Deal_Txt\YinWen_Res\CutWords_'
    with open(path_cutwords + str(i) + '_E.txt', 'w', encoding='utf-8') as f:
        f.write(str(words))
    print('Words written.')

    # 英文文本小写，并除去长度小于等于2的单词，去除停用词
    word_stopped = [w.lower() for w in words if (w.lower() not in cachedStopWords and len(w) > 2
                                                 and str.isalpha(w) is not False)]
    path_cutstop = 'E:\\21.3大三下\互联网搜索引擎\Deal_Txt\YinWen_Res\CutStopWords_'
    with open(path_cutstop + str(i) + '_E.txt', 'w', encoding='utf-8') as f:
        f.write(str(word_stopped))

    # 词干提取，即PorterStemming
    porter_stemming = []
    mylemm = WordNetLemmatizer()  # 初始化词形还原对象
    porter_stemmer = PorterStemmer()  # 词干提取
    for word in word_stopped:
        porter_stemming.append(porter_stemmer.stem(mylemm.lemmatize(word)))
    path_word_stems = 'E:\\21.3大三下\互联网搜索引擎\Deal_Txt\YinWen_Res\Porter_Stemming_'
    with open(path_word_stems + str(i) + '_E.txt', 'w', encoding='utf-8') as f:
        f.write(str(porter_stemming))

    # 词干提取后，进行字符化
    path_word_stems_space = 'E:\\21.3大三下\互联网搜索引擎\Deal_Txt\YinWen_Res\Porter_StemmingZifu_'
    with open(path_word_stems_space + str(i) + '_E.txt', 'w', encoding='utf-8') as f:
        f.write(' '.join(porter_stemming))
    print('WordsStopped written.')

    return word_stopped

if __name__ == '__main__':
    path = "E:\\21.3大三下\互联网搜索引擎\Deal_Txt\Article_E" # 英文
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    i = 1
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            with open(path + "/" + file, "rb") as f:  # 二进制格式文件参数为rb
                text = f.read()  # 是bytes
            encode_type = chardet.detect(text)  # 检测编码格式
            if encode_type['encoding'] != None:  # 排除不能解码的情况
                text = text.decode(encode_type['encoding'])  # 进行相应解码，赋给原标识符（变量）
                word_tokenize_stopwords_removal(text, i) # 返回列表
                i += 1