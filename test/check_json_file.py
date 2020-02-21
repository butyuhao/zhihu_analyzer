import json
from test_html_filter import filter_tags
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from app_context import AppCtx
app_ctx = AppCtx()
app_ctx._load_comments(('./data/comments.txt'))
for c in app_ctx.comments:
  
  if (c['gender'] == -1):
    print(c['personal_url'])
