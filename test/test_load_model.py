from gensim.models import Word2Vec

en_wiki_word2vec_model = Word2Vec.load('../data/500/wiki_model')

test_words = ['金融','上','股票','跌','经济']
for i in range(len(test_words)):
    res = en_wiki_word2vec_model.most_similar(test_words[i])
    print (test_words[i])
    print (res)
# Get the word vector for given word
#model['topic']
# Get most similar word vector
# model.most_similar()