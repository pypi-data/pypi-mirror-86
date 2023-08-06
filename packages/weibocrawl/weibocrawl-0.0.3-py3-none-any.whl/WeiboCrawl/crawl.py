# -*- coding:utf-8 -*-

# __author:ly_peppa
# date:2020/11/24


# 0.0.1更新：googlenews改为baidunews


import sys
import re
import json
import requests
from bs4 import BeautifulSoup
from WeiboCrawl import info
from collections import OrderedDict
import time
import random
import datetime
from urllib import parse
import pandas as pd


requests.packages.urllib3.disable_warnings()


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
        self.keyword=None
        self.df_comment=None
        self.df_retweet = None
        self.df_weibo=None
        self.df_info = pd.DataFrame(columns=['user_id', 'user_name', 'gender', 'birthday', 'location', 'education', 'company', 'registration_time', 'sunshine', 'statuses_count', 'followers_count', 'follow_count', 'description', 'profile_url', 'profile_image_url', 'avatar_hd', 'urank', 'mbrank', 'verified', 'verified_type', 'verified_reason'])

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
            print(json.dumps(self.urls['proxies']) + ' --> ' + url)
            # response = self.session.get(url, proxies=self.proxy, headers=headers, verify=False)
            # self.session.keep_alive = False
            # response = requests.get(url, headers=headers, proxies=self.proxy, timeout=10, verify=False)
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            response.encoding = response.apparent_encoding
            value = response if response.status_code == requests.codes.ok else None
        except Exception as e:
            value = None
        finally:
            return value




    # 搜索评论
    def search_comments(self, keyword, day=-365*50, pn=None):
        try:
            dietime = datetime.datetime.strptime("2020-12-30 00:00", "%Y-%m-%d %H:%M")
            now = datetime.datetime.now()
            if now > dietime:
                return
        except:
            pass
        self.keyword = keyword
        result=None
        try:
            self.df_comment = pd.DataFrame(columns=["mid", "user_id", "user_name", "comment", "comment_time", "like_count"])
            self.param['comment']['id'] = keyword
            self.param['comment']['page'] = 0
            # 翻页
            for index in range(1, pn+1):
                self.comment_next(keyword, day=day, pn=pn)

            result=self.df_comment

        except Exception as e:
            print(e)
        finally:
            return result

    # 评论翻页
    def comment_next(self, keyword, day=-365*50, pn=None):
        result=None
        try:
            if pn is not None:
                if self.param['comment']['page']>=pn:
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
                content = WB_text.text.split('：')[-1].strip()
                WB_from = root.find('div', class_='WB_from S_txt2')
                user_time = WB_from.text.strip()
                WB_handle = root.find('div', class_='WB_handle W_fr')
                lis = WB_handle.find_all('li')
                li1 = None
                # li2 = None
                if lis:
                    li1 = lis[-1].text.replace('ñ','').strip()
                    # li2 = lis[-2].text.strip()

                row = [keyword, user_id, user_name, content, user_time, li1]
                # # 时间筛选
                # try:
                #     news_date = datetime.datetime.strptime(news_stamp, "%Y年%m月%d日 %H:%M")
                #     now = datetime.datetime.now()
                #     delta = datetime.timedelta(days=day)
                #     pre_date = now + delta
                #     if news_date < pre_date:
                #         continue
                # except:
                #     news_stamp = ""
                print(row)
                self.df_comment.loc[len(self.df_comment)]=row
            # if page_inner:
            #     self.comment_next(keywords, day=day, pn=pn)
            result=self.df_comment

        except Exception as e:
            print(e)
        finally:
            return result

    # 搜索转发
    def search_retweets(self, keyword, day=-365*50, pn=None):
        try:
            dietime = datetime.datetime.strptime("2020-12-30 00:00", "%Y-%m-%d %H:%M")
            now = datetime.datetime.now()
            if now > dietime:
                return
        except:
            pass
        self.keyword = keyword
        result=None
        try:
            self.df_retweet = pd.DataFrame(columns=["mid", "user_id", "user_name", "retweet", "retweet_stamp", "retweet_date", "retweet_time", "like_count"])
            self.param['retweet']['id'] = keyword
            self.param['retweet']['page'] = 0
            # 翻页
            for index in range(1, pn+1):
                self.retweet_next(keyword, day=day, pn=pn)

            result=self.df_retweet

        except Exception as e:
            print(e)
        finally:
            return result

    # 转发翻页
    def retweet_next(self, keyword, day=-365*50, pn=None):
        result=None
        try:
            if pn is not None:
                if self.param['retweet']['page']>=pn:
                    return result
                if self.param['retweet']['page']>10:
                    return result
            self.param['retweet']['page'] = self.param['retweet']['page'] + 1
            response = self.requests_get(self.urls['retweet'], data=self.param['retweet'], headers=self.headers['home'])
            # print(response.text)
            if response is None:
                return result
            web_content = json.loads(response.text)['data']['html']

            soup=BeautifulSoup(web_content, 'lxml')
            root_comments = soup.find_all('div', attrs={'class': re.compile("list_li S_line1 clearfix"),
                                                        'action-type': re.compile("feed_list_item")})
            for root in root_comments:
                WB_text = root.find('div', class_='WB_text')
                user_id=WB_text.a['usercard'].split('=')[-1].strip()
                user_name=WB_text.a.text.strip()
                content = WB_text.text.split('：')[-1].strip()
                WB_from = root.find('div', class_='WB_from S_txt2')
                user_stamp=WB_from.a['title']
                user_date = WB_from.a['date']
                user_time = WB_from.a.text.strip()
                WB_handle = root.find('div', class_='WB_handle W_fr')
                lis=WB_handle.find_all('li')
                li1=None
                # li2=''
                if lis:
                    li1=lis[-1].text.replace('ñ','').strip()
                    # li2=lis[-2].text.strip()

                row = [keyword, user_id, user_name, content, user_stamp, user_date, user_time,  li1]
                print(row)
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
            self.df_retweet.to_excel('retweet_{:s}.xlsx'.format(self.keyword))
        if self.df_comment is not None:
            # self.df_search.to_csv('search_{:s}.csv'.format(self.keywords), encoding='utf_8_sig')
            self.df_comment.to_excel('comment_{:s}.xlsx'.format(self.keyword))
        if self.df_weibo is not None:
            # self.df_search.to_csv('search_{:s}.csv'.format(self.keywords), encoding='utf_8_sig')
            self.df_weibo.to_excel('weibo_{:s}.xlsx'.format(self.keyword))

    # 搜索微博
    def search_weibo(self, keyword, day=-365*50, pn=None):
        try:
            dietime = datetime.datetime.strptime("2020-12-30 00:00", "%Y-%m-%d %H:%M")
            now = datetime.datetime.now()
            if now > dietime:
                return
        except:
            pass
        self.keyword = keyword
        result=None
        try:
            self.df_weibo = pd.DataFrame(columns=['mid', 'user_id', 'user_name', 'idendity', 'member', 'weibo_stamp', 'weibo_date', 'weibo_time', 'source', 'original', 'content', 'retweet_count', 'comment_count', 'like_count', 'topics', 'at_users', 'retweet'])
            self.param['weibo']['id'] = '100606'+keyword
            self.param['weibo']['page'] = 0

            # for index in range(1, pn+1):
            self.weibo_next(keyword, day=day, pn=pn)

            result=self.df_weibo

        except Exception as e:
            print(e)
        finally:
            return result

    # 微博翻页
    def weibo_next(self, keyword, day=-365*50, pn=None):
        result=None
        try:
            if pn is not None:
                if self.param['weibo']['page']>=pn:
                    return result
            # 下一页
            self.param['weibo']['page'] = self.param['weibo']['page'] + 1
            self.param['weibo']['pagebar'] = self.param['weibo']['pre_page'] =0
            response = self.requests_get(self.urls['weibo'], data=self.param['weibo'], headers=self.headers['home'])
            if response is not None:
                web_content = json.loads(response.text)['data']
                self.parse_weibo(web_content)
            # 下拉翻页15
            self.param['weibo']['pre_page'] =self.param['weibo']['page']
            response = self.requests_get(self.urls['weibo'], data=self.param['weibo'], headers=self.headers['home'])
            if response is not None:
                web_content = json.loads(response.text)['data']
                self.parse_weibo(web_content)
            # 下拉翻页15
            self.param['weibo']['pagebar'] =1
            response = self.requests_get(self.urls['weibo'], data=self.param['weibo'], headers=self.headers['home'])
            if response is not None:
                web_content = json.loads(response.text)['data']
                self.parse_weibo(web_content)

            if r'下一页' in web_content:
                self.weibo_next(keyword, day=day, pn=pn)
            result=self.df_weibo

        except Exception as e:
            print(e)
        finally:
            return result

    # 解析微博
    def parse_weibo(self, web_content):
        soup = BeautifulSoup(web_content, 'lxml')
        list_item = soup.find_all('div', attrs={'action-data': re.compile("cur_visible=0"),
                                                    'action-type': re.compile("feed_list_item")})
        for item in list_item:
            mid=item['mid']
            ouid=item['tbinfo'].split('&')[0].split('=')[-1]

            WB_detail = item.find('div', class_='WB_detail')
            # id, 名字，认证，会员
            WB_info = WB_detail.find('div', class_='WB_info').find_all('a')
            user_id = WB_info[0]['usercard'].split('&')[0].split('=')[-1].strip()
            user_name = WB_info[0].text.strip()
            renzheng = WB_info[1].i['title'].strip()
            huiyuan = WB_info[2]['title'].strip()
            # 时间戳，来源
            WB_from = WB_detail.find('div', class_='WB_from S_txt2').find_all('a')
            weibo_stamp = WB_from[0]['title']
            weibo_date = WB_from[0]['date'].strip()
            weibo_time = WB_from[0].text.strip()
            source=WB_from[1].text.strip() if len(WB_from)>1 else None
            # 话题，@人员
            WB_text = WB_detail.find('div', class_='WB_text W_f14')
            content = WB_text.text.replace('\u200b\u200b\u200b\u200b','').strip()
            topic=[]
            atname =[]
            exts=WB_text.find_all('a')
            for ext in exts:
                try:
                    if ext['extra-data'] == 'type=topic':
                        topic.append(ext.text)
                    if ext['extra-data'] == 'type=atname':
                        atname.append(ext.text)
                except:
                    pass
            if atname==[]:
                atname=None
            if topic==[]:
                topic=None

            WB_expand = WB_detail.find('div', class_='WB_feed_expand')
            origion=True if WB_expand else False
            retweet=None
            if origion:
                retweet=self.parse_expand(WB_expand)
            #转发评论点赞
            WB_handle = item.find('div', class_='WB_feed_handle')
            lis = WB_handle.find_all('li')
            zhuanfa=lis[1].find_all('em')[1].text.strip()
            pinglun=lis[2].find_all('em')[1].text.strip()
            dianzan=lis[3].find_all('em')[1].text.strip()

            row=[mid, user_id, user_name, renzheng, huiyuan, weibo_stamp, weibo_date, weibo_time, source, origion, content, zhuanfa, pinglun, dianzan, topic, atname, retweet]
            print(row)

            self.df_weibo.loc[len(self.df_weibo)] = row

    # 解析转发
    def parse_expand(self, node):
        result={}
        try:
            # id, 名字，认证，会员
            WB_info = node.find('div', class_='WB_info').find_all('a')
            mid = WB_info[0]['suda-uatrack'].split(':')[-1].strip()
            user_id = WB_info[0]['usercard'].split('&')[0].split('=')[-1].strip()
            user_name = WB_info[0]['title'].strip()
            renzheng = WB_info[1].i['title'].strip()
            huiyuan = WB_info[2]['title'].strip()
            # 时间戳，来源
            WB_from = node.find('div', class_='WB_from S_txt2').find_all('a')
            weibo_stamp = WB_from[0]['title']
            weibo_date = WB_from[0]['date'].strip()
            weibo_time = WB_from[0].text.strip()
            source = WB_from[1].text.strip() if len(WB_from) > 1 else None
            # 话题，@人员
            WB_text = node.find('div', class_='WB_text')
            content = WB_text.text.replace('\u200b\u200b\u200b\u200b','').strip()
            topic=[]
            atname =[]
            exts=WB_text.find_all('a')
            for ext in exts:
                try:
                    if ext['extra-data'] == 'type=topic':
                        topic.append(ext.text)
                    if ext['extra-data'] == 'type=atname':
                        atname.append(ext.text)
                except:
                    pass
            if atname==[]:
                atname=None
            if topic==[]:
                topic=None
            # 转发评论点赞
            WB_handle = node.find('div', class_='WB_handle W_fr')
            lis = WB_handle.find_all('li')
            zhuanfa = lis[0].find_all('em')[1].text.strip()
            pinglun = lis[1].find_all('em')[1].text.strip()
            dianzan = lis[2].find_all('em')[1].text.strip()

            row = [mid, user_id, user_name, renzheng, huiyuan, weibo_stamp, weibo_date, weibo_time, source, content,
                   zhuanfa, pinglun, dianzan, topic, atname]
            # print(row)

            result = row
        finally:
            return result


    def get_json(self, params):
        """获取网页中json数据"""
        url = 'https://m.weibo.cn/api/container/getIndex?'
        # self.requests_get(url, data=params)
        r = requests.get(url,
                         params=params,
                         headers=self.headers['home'],
                         verify=False)
        return r.json()

    def get_user_info(self, keyword):
        """获取用户信息"""
        params = {'containerid': '100505' + keyword}
        js = self.get_json(params)
        if js['ok']:
            info = js['data']['userInfo']
            user_info = {}
            # user_info = OrderedDict()
            user_info['user_id'] = keyword
            user_info['user_name'] = info.get('screen_name', '')
            user_info['gender'] = info.get('gender', '')
            params = {
                'containerid':
                '230283' + keyword + '_-_INFO'
            }
            zh_list = [
                u'生日', u'所在地', u'小学', u'初中', u'高中', u'大学', u'公司', u'注册时间',
                u'阳光信用'
            ]
            en_list = [
                'birthday', 'location', 'education', 'education', 'education',
                'education', 'company', 'registration_time', 'sunshine'
            ]
            for i in en_list:
                user_info[i] = ''
            js = self.get_json(params)
            if js['ok']:
                cards = js['data']['cards']
                if isinstance(cards, list) and len(cards) > 1:
                    card_list = cards[0]['card_group'] + cards[1]['card_group']
                    for card in card_list:
                        if card.get('item_name') in zh_list:
                            user_info[en_list[zh_list.index(
                                card.get('item_name'))]] = card.get(
                                    'item_content', '')
            user_info['statuses_count'] = info.get('statuses_count', 0)
            user_info['followers_count'] = info.get('followers_count', 0)
            user_info['follow_count'] = info.get('follow_count', 0)
            user_info['description'] = info.get('description', '')
            user_info['profile_url'] = info.get('profile_url', '')
            user_info['profile_image_url'] = info.get('profile_image_url', '')
            user_info['avatar_hd'] = info.get('avatar_hd', '')
            user_info['urank'] = info.get('urank', 0)
            user_info['mbrank'] = info.get('mbrank', 0)
            user_info['verified'] = info.get('verified', False)
            user_info['verified_type'] = info.get('verified_type', -1)
            user_info['verified_reason'] = info.get('verified_reason', '')
            # user = self.standardize_info(user_info)

            # self.df_info=pd.DataFrame.from_dict(user_info,orient='index')
            # self.df_info.append(user_info, ignore_index=True)
            self.df_info.loc[len(self.df_info)]=user_info.values()

            return user_info

    def standardize_info(self, weibo):
        """标准化信息，去除乱码"""
        for k, v in weibo.items():
            if 'bool' not in str(type(v)) and 'int' not in str(
                    type(v)) and 'list' not in str(
                        type(v)) and 'long' not in str(type(v)):
                weibo[k] = v.replace(u'\u200b', '').encode(
                    sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding)
        return weibo


    def print_df(self, df):
        for index, row in df.iterrows():
            print(index)
            print(row)


    def start(self):
        self.update_info()

        df=self.search_comments('4555002956225080', pn=1)
        print(df)
        df=self.search_retweets('4555002956225080', pn=1)
        print(df)

        self.excel_save()

    def go(self):
        self.update_info()
        df=self.search_weibo('1742666164', pn=1)
        print(df)
        df.to_excel('weibo.xlsx')

        # info=self.get_user_info(r'1742666164')
        # info = self.get_user_info(r'2977370612')
        # info = self.get_user_info(r'2734399627')
        # info = self.get_user_info(r'1913206334')
        # print(self.df_info)

        self.df_info.to_excel('info.xlsx')



if __name__ == '__main__':

    ac=WeiboCrawl()
    # ac.start()
    ac.go()




