#!/usr/bin/python3
# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
import json
import ast
import define
from tool.fen_ci import cut_words, filter_tags
class AppCtx(object):
    def __init__(self):
        self.url = "https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={1}&platform=desktop&sort_by=default"
        self.question_id = -1
        self.initial_offset = 0
        self.model = None
        self.stop_word_table = None
        self.comments = None
        self.comments_rich_text_split = None
        self.word_count = None
        self.doc_vec_list = None
        self.crawler_website = ''#zhi_hu dou_ban...
        self.is_crawler_finish = False #是否已经跑过爬虫
        self.cur_comment = 0 #当前在阅读器中正在看的comment编号
        self.cur_recommend = 0
        self.recommend_list = []
        self.like_list = []
        self.keyword_include = []
        self.keyword_not_include = []
    def init(self):
        self._load_model('./data/' + str(define.word_vector_dimension) + '/wiki_model')
        self.stop_word_table = self._build_stop_word_table(define.stop_word_table_path)
        self._load_comments(define.comments_path)
    def reload(self):
        if self.model is None:
            self._load_model('./data/' + str(define.word_vector_dimension) + '/wiki_model')
        if self.stop_word_table is None:
            self.stop_word_table = self._build_stop_word_table(define.stop_word_table_path)
        if self.comments is None:
            self._load_comments(define.comments_path)
    def _build_stop_word_table(self, path):
        stop_word_table = []
        with open(path) as f:
            line = f.readline()
            while(line):
                stop_word_table.append(line.strip('\n'))
                line = f.readline()
        stop_word_table.append('\n')
        self.stop_word_table = stop_word_table
        return True
    def _load_comments(self, file_path):
        with open(file_path) as f:
            comments = f.readlines()
            comments_list = []
            for c in comments:
                c.strip()
                comments_list.append(ast.literal_eval(c))
            self.comments = comments_list
            #print(comments_list)
            #comments = json.loads(comments['content']) 
            #使得评论按照点赞从高到低排序
            #self.comments = sorted(comments, key=lambda x : int(x['vote_up_count']), reverse=True)
    def _load_model(self, file_path):
        self.model = Word2Vec.load(file_path)
    def _get_comments_rich_text(self):
        '''
        将所有的评论内容拼成str
        '''
        rich_text = ''
        if self.stop_word_table is None:
            self._build_stop_word_table(define.stop_word_table_path)
        for c in self.comments:
            rich_text += filter_tags(c['content'])
        #print(self.stop_word_table)
        rich_text = cut_words(rich_text, self.stop_word_table)
        self.comments_rich_text_split = rich_text
        self._get_word_count()
        return True
    def _get_word_count(self):
        '''
        获取rich text split中的词语计数
        '''
        if self.comments_rich_text_split is None:
            return False
        word_list = self.comments_rich_text_split.split(' ')
        word_set = set(word_list)
        word_count = {}
        for w in word_set:
            word_count[w] = word_list.count(w)
        word_count = sorted(word_count.items(), key = lambda x : x[1], reverse=True)
        #print(word_count)
        self.word_count = word_count
        return True
    def get_word_count_result(self, n):
        result = ""
        if self.word_count is not None:
            for i in range(min(n, len(self.word_count))):
                print(self.word_count[i])
                result += self.word_count[i][0]
                result += ' '
                result += str(self.word_count[i][1])
                result += '\n'
            return result
        return False


        

if __name__ == '__main__':
    app_ctx = AppCtx()
    app_ctx._load_comments('./data/comments.txt')
    text = app_ctx._get_comments_rich_text()
    