#--*--coding:utf-8--*--
import requests
import json
import time
import re
import datetime
import pandas as pd

user_info_key = ['id', 'name', 'url_token',  'gender', 'use_default_avatar', 'avatar_url', 'follower_count',  'articles_count', 'answer_count', 'headline', 'is_realname', 'is_org', 'self_recommend']

def get_data(url):
    '''
    功能：访问 url 的网页，获取网页内容并返回
    参数：
        url ：目标网页的 url
    返回：目标网页的 html 内容
    '''
    headers = {
        'accept': '*/*',#'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Linux; Android 5.1; OPPO A59s Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36',
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
    user_info_value_list = []
    try:
        for item in json_data[1:]:
            user_info_value = []
            if user_info_key[0] in item.keys(): # user_info_key[0] 是 'id'
                user_info_value.append(item['id'])
                for key in user_info_key[1:]:
                    if key in item.keys():
                        user_info_value.append(item[key])
                    else:
                        user_info_value.append('None')
            else:
                continue
            user_info_value_list.append(user_info_value)
        return user_info_value_list
    
    except Exception as e:
        print('Exception:')
        print(item)
        print(e)
        
def save_data(user_info_value_list):
    '''
    功能：将comments中的信息输出到文件中/或数据库中。
    参数：comments 将要保存的数据  
    '''
    filename = './data/user_db.csv'
    
    dataframe = pd.DataFrame(user_info_value_list)
    dataframe.to_csv(filename, mode='a', index=False, sep=',', header=False)
    #dataframe.to_csv(filename, mode='a', index=False, sep=',', header=['name','gender','user_url','voteup','cmt_count','url'])
    
 
def main():
    
    url = 'https://www.zhihu.com/api/v4/members/wang-zi-qing-59/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
    html = get_data(url)
    # get total cmts number
    totals = json.loads(html)['paging']['totals']
    
    user_info_value_list = parse_data(html)
    save_data(user_info_value_list)
    page = 20
    
    while(page < totals):

        url = 'https://www.zhihu.com/api/v4/members/wang-zi-qing-59/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=' + str(page) + '&limit=20'
 
        html = get_data(url)
        user_info_value_list = parse_data(html)
        save_data(user_info_value_list)
        print(user_info_value_list)
        print(page)
        page += 20
    
if __name__ == '__main__':
    main()
    print("完成！！")
