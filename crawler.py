#--*--coding:utf-8--*--
import requests
import json
import time
import re
import datetime
import pandas as pd
 
def get_data(url):
    '''
    功能：访问 url 的网页，获取网页内容并返回
    参数：
        url ：目标网页的 url
    返回：目标网页的 html 内容
    '''
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
 
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text
    
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")
        
def parse_data(html):
    '''
    功能：提取 html 页面信息中的关键信息，并整合一个数组并返回
    参数：html 根据 url 获取到的网页内容
    返回：存储有 html 中提取出的关键信息的数组
    '''
    json_data = json.loads(html)['data']
    comments = []
    
    try:
        for item in json_data:
 
            comment = []
            comment.append(item['author']['name'])    # 姓名
            comment.append(item['author']['gender'])  # 性别
            comment.append(item['author']['url'])     # 个人主页
            comment.append(item['voteup_count'])      # 点赞数
            comment.append(item['comment_count'])     # 评论数
            comment.append(item['url'])               # 回答链接
            comment.append(item['content'])           # 回答内容
            comments.append(comment)
            
        return comments
    
    except Exception as e:
        print(comment)
        print(e)
        
def save_data(comments):
    '''
    功能：将comments中的信息输出到文件中/或数据库中。
    参数：comments 将要保存的数据  
    '''
    filename = 'data/comments.csv'
    
    dataframe = pd.DataFrame(comments)
    dataframe.to_csv(filename, mode='a', index=False, sep=',', header=False)
    #dataframe.to_csv(filename, mode='a', index=False, sep=',', header=['name','gender','user_url','voteup','cmt_count','url'])
    
 
def main():
    
    url = 'https://www.zhihu.com/api/v4/questions/264508629/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=5&platform=desktop&sort_by=default'
    
    # get total cmts number
    html = get_data(url)
    totals = json.loads(html)['paging']['totals']
    
    print(totals)
    print('---'*10)
    
    page = 0
    
    while(page < totals):
        url = 'https://www.zhihu.com/api/v4/questions/264508629/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset='+ str(page) +'&platform=desktop&sort_by=default'
 
        html = get_data(url)
        comments = parse_data(html)
        save_data(comments)
        
        print(page)
        page += 5
    
    
if __name__ == '__main__':
    main()
    print("完成！！")
