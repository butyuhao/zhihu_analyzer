import jieba
import jieba.analyse
import jieba.posseg as pseg
import re
import codecs, sys

def cut_words(sentence, stop_word_table = None):
    #print sentence
    r = re.compile('[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+')
    sentence = re.sub(r, '', sentence)

    line = jieba.cut(sentence.strip(), HMM = True, use_paddle = True, cut_all=False)
    if stop_word_table is not None:
        line = [x for x in line if x not in stop_word_table]
    return " ".join(list(line))

def filter_tags(html_str):
    re_p=re.compile('<p>',re.I)
    re_slash_p=re.compile('</p>',re.I)
    re_span=re.compile('<span.*</span>')
    re_a=re.compile('<a.*>')
    re_figure=re.compile('<figure.*</figure>')
    re_br=re.compile('<br/>')
    re_img=re.compile('<img.*/>')
    re_tag=re.compile('</?[a-z]*[0-9]*>')
    re_p_empty=re.compile('<p class="ztext-empty-paragraph">')
    s=re_p.sub('',html_str)
    s=re_slash_p.sub('',s)
    s=re_span.sub('',s)
    s=re_a.sub('n',s)
    s=re_figure.sub('',s)
    s=re_br.sub('',s)
    s=re_img.sub('',s)
    s=re_tag.sub('',s)
    s=re_p_empty.sub('',s)
    blank_line=re.compile('n+')
    s=blank_line.sub('n',s)
    return s

