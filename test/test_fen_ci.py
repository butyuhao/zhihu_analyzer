import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from tool.fen_ci import *

f = codecs.open('./wiki.txt', 'r', encoding="utf8")
target = codecs.open("./wiki_processed.txt", 'w', encoding="utf8")
stop_word_table = build_stop_word_table('./baidu_stop_word.txt')
line = f.readline()
i = 0
while line:
    i += 1
    print('Start processing article {0}'.format(i))
    line = cut_words(line, stop_word_table = stop_word_table)
    print(line)
    target.writelines(line)
    line = f.readline()

f.close()
target.close()