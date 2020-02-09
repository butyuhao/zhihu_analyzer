import jieba
import jieba.analyse
import jieba.posseg as pseg
import re
import codecs, sys
stop_word_table = []
def build_stop_word_table(path):

    with open(path) as f:
        line = f.readline()
        while(line):
            stop_word_table.append(line.strip('\n'))
            line = f.readline()
    return stop_word_table

def _in_table(x, table = stop_word_table):
    if x in table:
        return False
    else:
        return True

def cut_words(sentence, stop_word_table = None):
    #print sentence
    r = re.compile('[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+')
    sentence = re.sub(r, '', sentence)

    line = jieba.cut(sentence.strip(), HMM = True, use_paddle = True, cut_all=False)
    if stop_word_table is not None:
        line = filter(_in_table, line)
    return " ".join(list(line))

def get_file_len(f):
    for i, l in enumerate(f):
        pass
    return i + 1
if __name__ == '__main__':
    f = codecs.open('../data/wiki.txt', 'r', encoding="utf8")
    target = codecs.open("../data/wiki_processed.txt", 'w', encoding="utf8")
    stop_word_table = build_stop_word_table('../data/stop_word.txt')
    line = f.readline()
    i = 0
    while line:
        i += 1
        line_seg = cut_words(line, stop_word_table = stop_word_table)
        if i % 10000 == 0:
            print('Start processing article {0}'.format(i))

        target.writelines(line_seg)
        line = f.readline()
    print('Finish!')

    f.close()
    target.close()

