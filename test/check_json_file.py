import json
f = open('./data/comments.json')
comments = f.readlines()
comments = json.loads(comments[0])
comments = sorted(comments, key=lambda x : int(x['vote_up_count']), reverse=True)
print(comments[0:3])
