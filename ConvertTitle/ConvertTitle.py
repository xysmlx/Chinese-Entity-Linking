from langconv import *
import codecs
from hanziconv import HanziConv


def simple2tradition(line):
    # 将简体转换成繁体
    line = Converter('zh-hant').convert(line.decode('utf-8'))
    line = line.encode('utf-8')
    return line


def tradition2simple(line):
    # 将繁体转换成简体
    line = Converter('zh-hans').convert(line.decode('utf-8'))
    line = line.encode('utf-8')
    return line


# 最大正向匹配
def conv(string, dic):
    i = 0
    while i < len(string):
        for j in range(len(string) - i, 0, -1):
            if string[i:][:j] in dic:
                t = dic[string[i:][:j]]
                string = string[:i] + t + string[i:][j:]
                i += len(t) - 1
                break
        i += 1
    return string

# 生成转换字典


def mdic():
    table = codecs.open('ZhConversion.php', 'r', 'utf-8').readlines()
    dic = dict()
    name = []
    for line in table:
        if line[0] == '$':
            # print line.split()[0][1:]
            name.append(dic)
            dic = dict()
        if line[0] == "'":
            word = line.split("'")
            dic[word[1]] = word[3]
    name[3].update(name[1])  # 简繁通用转换规则(zh2Hant)加上台湾区域用法(zh2TW)
    name[4].update(name[1])  # 简繁通用转换规则(zh2Hant)加上香港区域用法(zh2HK)
    name[5].update(name[2])  # 繁简通用转换规则(zh2Hans)加上大陆区域用法(zh2CN)
    return name[3], name[4], name[5]

# if __name__ == "__main__":
#     a = "头发发展萝卜卜卦秒表表达 "
#     b = "大衛碧咸在寮國見到了布希"
#     c = "大卫·贝克汉姆在老挝见到了布什"

#     [dic_TW, dic_HK, dic_CN] = mdic()
#     str_TW = conv(a, dic_TW)
#     str_HK = conv(c, dic_HK)
#     str_CN = conv(b, dic_CN)
# print a, ' <-> ', str_TW, '\n', c, ' < -> ', str_HK, '\n', b, ' < -> ',
# str_CN


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

if __name__ == '__main__':
    fin = codecs.open("zhwiki-20151226-all-titles-in-ns0", "r", "utf-8")
    fout = codecs.open("zhwiki-titles-converted", "w", "utf-8")
    #[dic_TW, dic_HK, dic_CN] = mdic()
    # print(HanziConv.toSimplified("!_"))
    cnt = 0
    while(True):
        cnt += 1
        if(cnt % 10000 == 0):
            print(cnt)
        line = fin.readline()
        if(line == ""):
            break
        if(check_contain_chinese(line)):
            fout.write(HanziConv.toSimplified(line))
