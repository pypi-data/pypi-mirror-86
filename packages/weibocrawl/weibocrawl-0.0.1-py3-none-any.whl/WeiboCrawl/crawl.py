# -*- coding:utf-8 -*-

# __author:ly_peppa
# date:2020/11/24


# 0.0.1更新：googlenews改为baidunews



import re
import json
import requests
from bs4 import BeautifulSoup
from WeiboCrawl import info
import time
import random
import datetime
from urllib import parse
import pandas as pd


class WeiboCrawl():

    def __init__(self):
        self.author_wx = 'ly_peppa'
        self.author_qq = '3079886558'
        self.author_email = 'iseu1130@sina.cn'
        self.urls = {}                      # 目标网页
        self.headers = {}                   # Get/Post请求头
        self.param = {}
        self.cookie=requests.cookies.RequestsCookieJar()
        self.session = requests.session()
        self.keywords=None
        self.df_comment=None
        self.df_retweet = None

    # 从配置文件中更新登录链接信息
    def update_info(self):
        self.urls = info.loginUrls                                                  #http地址
        self.headers = info.loginHeaders
        self.param = info.loginParam
        self.cookie.set("cookie", info.loginCookie)
        self.session.cookies.update(self.cookie)

    # 发送Get请求
    def requests_get(self, url, data=None, headers=None):
        try:
            url = url if data is None else url+parse.urlencode(data)
            time.sleep(random.random() * 0.5 + 0.1)  # 0-1区间随机数
            #没有缓存就开始抓取
            print(self.urls['proxies']['https'] + ' --> ' + url)
            # response = self.session.get(url, proxies=self.proxy, headers=headers, verify=False)
            # self.session.keep_alive = False
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = response.apparent_encoding
            value = response if response.status_code == requests.codes.ok else None
        except Exception as e:
            value = None
        finally:
            return value

    # 搜索评论
    def search_comments(self, keywords, day=-365*50, pn=None):
        self.keywords = keywords
        result=None
        try:
            self.df_comment = pd.DataFrame(columns=["Keywords", "user_id", "user_name", "comment", "stamp", "zan"])
            self.param['comment']['id'] = keywords
            self.param['comment']['page'] = 0

            for index in range(1, pn+1):
                self.comment_next(keywords, day=day, pn=pn)

            result=self.df_comment

        except Exception as e:
            print(e)
        finally:
            return result

    # 评论翻页
    def comment_next(self, keywords, day=-365*50, pn=None):
        result=None
        try:
            if pn is not None:
                if self.param['comment']['page']>pn:
                    return result
                if self.param['comment']['page']>10:
                    return result
            # self.param['comment']['id'] = keywords
            self.param['comment']['page'] = self.param['comment']['page'] + 1
            response = self.requests_get(self.urls['comment'], data=self.param['comment'], headers=self.headers['home'])
            # print(response.text)
            if response is None:
                return result
            web_content = json.loads(response.text)['data']['html']
            soup = BeautifulSoup(web_content, 'lxml')
            page_inner = soup.find('span', class_='more_txt')
            list_box = soup.find('div', class_='list_box')
            root_comments = list_box.find_all('div', attrs={'class': re.compile("list_li S_line1 clearfix"),
                                                            'node-type': re.compile("root_comment")})
            for root in root_comments:
                WB_text = root.find('div', class_='WB_text')
                user_id = WB_text.a['usercard'].split('=')[-1].strip()
                user_name = WB_text.a.text.strip()
                comment = WB_text.text.split('：')[-1].strip()
                WB_from = root.find('div', class_='WB_from S_txt2')
                user_date = WB_from.text.strip()
                WB_handle = root.find('div', class_='WB_handle W_fr')
                lis = WB_handle.find_all('li')
                li1 = ''
                li2 = ''
                if lis:
                    li1 = lis[-1].text.replace('ñ','').strip()
                    li2 = lis[-2].text.strip()

                row = [keywords, user_id, user_name, comment, user_date, li1]
                # print(row)
                # try:
                #     news_date = datetime.datetime.strptime(news_stamp, "%Y年%m月%d日 %H:%M")
                #     now = datetime.datetime.now()
                #     delta = datetime.timedelta(days=day)
                #     pre_date = now + delta
                #     if news_date < pre_date:
                #         continue
                # except:
                #     news_stamp = ""
                # print(row)
                self.df_comment.loc[len(self.df_comment)]=row

            if page_inner:
                self.comment_next(keywords, day=day, pn=pn)
            result=self.df_comment

        except Exception as e:
            print(e)
        finally:
            return result

    # 搜索转发
    def search_retweets(self, keywords, day=-365*50, pn=None):
        self.keywords = keywords
        result=None
        try:
            self.df_retweet = pd.DataFrame(columns=["Keywords", "user_id", "user_name", "retweet", "stamp", "zan"])
            self.param['retweet']['id'] = keywords
            self.param['retweet']['page'] = 0

            for index in range(1, pn+1):
                self.retweet_next(keywords, day=day, pn=pn)

            result=self.df_retweet

        except Exception as e:
            print(e)
        finally:
            return result

    # 转发翻页
    def retweet_next(self, keywords, day=-365*50, pn=None):
        result=None
        try:
            if pn is not None:
                if self.param['retweet']['page']>pn:
                    return result
                if self.param['retweet']['page']>10:
                    return result
            # self.param['comment']['id'] = keywords
            self.param['retweet']['page'] = self.param['retweet']['page'] + 1
            response = self.requests_get(self.urls['retweet'], data=self.param['retweet'], headers=self.headers['home'])
            # print(response.text)
            if response is None:
                return result
            web_content = json.loads(response.text)['data']['html']

            soup=BeautifulSoup(web_content, 'lxml')
            root_comments = soup.find_all('div', attrs={'class': re.compile("list_li S_line1 clearfix"),
                                                        'action-type': re.compile("feed_list_item")})
            # print(root_comments)
            for root in root_comments:
                WB_text = root.find('div', class_='WB_text')
                user_id=WB_text.a['usercard'].split('=')[-1].strip()
                user_name=WB_text.a.text.strip()
                comment = WB_text.text.split('：')[-1].strip()
                WB_from = root.find('div', class_='WB_from S_txt2')
                user_stamp=WB_from.a['title']
                user_date = WB_from.a.text.strip()
                WB_handle = root.find('div', class_='WB_handle W_fr')
                lis=WB_handle.find_all('li')
                li1=''
                # li2=''
                if lis:
                    li1=lis[-1].text.replace('ñ','').strip()
                    # li2=lis[-2].text.strip()

                row = [keywords, user_id, user_name, comment, user_date, li1]
                # print(row)
                # try:
                #     news_date = datetime.datetime.strptime(news_stamp, "%Y年%m月%d日 %H:%M")
                #     now = datetime.datetime.now()
                #     delta = datetime.timedelta(days=day)
                #     pre_date = now + delta
                #     if news_date < pre_date:
                #         continue
                # except:
                #     news_stamp = ""
                # print(row)
                self.df_retweet.loc[len(self.df_retweet)]=row

            # if page_inner:
            #     self.retweet_next(keywords, day=day, pn=pn)
            result=self.df_retweet

        except Exception as e:
            print(e)
        finally:
            return result

    # 保存
    def excel_save(self):
        if self.df_retweet is not None:
            # self.df_detail.to_csv('detail_{:s}.csv'.format(self.keywords), encoding='utf_8_sig')
            self.df_retweet.to_excel('retweet_{:s}.xlsx'.format(self.keywords))
        if self.df_comment is not None:
            # self.df_search.to_csv('search_{:s}.csv'.format(self.keywords), encoding='utf_8_sig')
            self.df_comment.to_excel('comment_{:s}.xlsx'.format(self.keywords))





    def print_df(self, df):
        for index, row in df.iterrows():
            print(index)
            print(row)


    def start(self):
        self.update_info()

        self.param['comment']['id']="4554976677862363"
        df=self.search_comments('4554794956226910', pn=1)
        print(df)

        self.param['retweet']['id']="4554976677862363"
        df=self.search_retweets('4554794956226910', pn=2)
        print(df)

        self.excel_save()



if __name__ == '__main__':

    ac=WeiboCrawl()
    ac.start()


