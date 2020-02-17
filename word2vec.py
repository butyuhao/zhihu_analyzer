import json
from gensim.models import Word2Vec
from copy import deepcopy
from tool.fen_ci import cut_words
from tqdm import tqdm
import define
import numpy as np
import math
from app_context import AppCtx
def get_w2v_mean(line, app_ctx):
    model = app_ctx.model
    word_list = line.split(' ')
    word_count = 0
    doc_vec = np.zeros((define.word_vector_dimension, ))
    for w in word_list:
        if w in model:
            #print(model[w])
            word_count += 1
            doc_vec += model[w]
    if not (word_count == 0):
        doc_vec = doc_vec / word_count
    return doc_vec
def cosine_similarity(x, y, norm=False):
    """ 计算两个向量x和y的余弦相似度 """
    assert len(x) == len(y), "len(x) != len(y)"
    zero_list = np.array([0] * len(x))
    if (x == zero_list).all() or (y == zero_list).all():
        return float(1) if (x == y).all() else float(0)

    res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))

    return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内
def get_similar_doc(doc_list, n, app_ctx):
    ''' 在comments中找到与doc最相似的前n个文章
    '''
    get_doc_vec_list(app_ctx)
    doc_vec_mean = np.zeros((define.word_vector_dimension, ))
    if len(doc_list) == 0:
        return False

    for d in doc_list:
        doc_vec_mean += app_ctx.doc_vec_list[d]
    doc_vec_mean /= len(doc_list)
    similarity = {}
    for i, vec in enumerate(app_ctx.doc_vec_list):
        similarity[i] = cosine_similarity(doc_vec_mean, vec)
    similarity = sorted(similarity.items(), key=lambda x : x[1], reverse=True)
    app_ctx.recommend_list = []
    for i in range(min(n, len(similarity))):
        app_ctx.recommend_list.append(similarity[i][0])
    return True
    
def get_doc_vec_list(app_ctx):
    ''' 
    获得当前app_ctx中comments所对应的vector的list
    因为在word2vec部分有判断词语是否在model中，这边cut_word
    的时候不需要传入停用词表
    '''
    doc_vec_list = []
    for comment in tqdm(app_ctx.comments):
        c = cut_words(comment['content'])
        doc_vec = get_w2v_mean(c, app_ctx)
        doc_vec_list.append(doc_vec)
    app_ctx.doc_vec_list = doc_vec_list
    return True

if __name__ == '__main__':
    app_ctx = AppCtx()
    app_ctx.init()
    #print(app_ctx.comments[1])
    get_similar_doc([1], 10, app_ctx)

    #print(type(comments))

