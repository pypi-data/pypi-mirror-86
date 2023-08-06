#coding=utf-8

# import logging
# logging.basicConfig(filename='logging.log',
#                     format='%(asctime)s %(message)s',
#                     filemode="w", level=logging.DEBUG)

# 更新：



loginParam={

    "retweet": {
        "ajwvr": "6",
        "id": "4554794956226910",
        "page": 1,
    },

    "comment": {
        "ajwvr": "6",
        "id": "4554794956226910",
        # "root_comment_max_id": "139259012294856",
        # "root_comment_max_id_type": "0",
        # "root_comment_ext_param": "",
        "page": 1,
        "filter": "hot",
        "sum_comment_number": "85",
        "filter_tips_before": "0",
        "from": "singleWeiBo",
    },

}

loginUrls =  {
    'proxyWeb': 'https://www.xicidaili.com/nn/',
    'proxies': {
        # "http": 'http://127.0.0.1:80',
        "https": 'https://127.0.0.1:80'
    },
    "retweet":"https://weibo.com/aj/v6/mblog/info/big?",
    "comment":"https://weibo.com/aj/v6/comment/big?",


}
loginHeaders = {

    "home": {
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "TC-V5-G0=4de7df00d4dc12eb0897c97413797808; _s_tentry=www.google.com; Apache=902545514870.0345.1600846345176; SINAGLOBAL=902545514870.0345.1600846345176; ULV=1600846345180:1:1:1:902545514870.0345.1600846345176:; SSOLoginState=1601197609; login_sid_t=9d8fc5fed4cb9e5cd73c5d1a96fc4ee2; cross_origin_proto=SSL; UOR=www.google.com,weibo.com,www.baidu.com; WBtopGlobal_register_version=2020110622; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWgxyR8DlA5uOfXLUFsnVlP5JpX5KMhUgL.FoeXS0.NeoqN1KM2dJLoI7_DMcHfSoqcP0zEe5tt; SCF=AhkV6ZZAx6qPys4LoUJKrEDD1WfzsAaXRvFPrvuN10KgHZ7_UOtPPc5IwLtehF6cD3BwObP6TKFMJuz17vyAX7A.; SUB=_2A25yvxxNDeRhGeVK7FsW8ijLwjuIHXVRzQqFrDV8PUNbmtANLWfwkW9NTCmeblVf8rPc--6uzHJT2aQEEX668g9X; ALF=1637654427; wb_view_log_3479726797=1536*8641.25; ASP.NET_SessionId=yy3mnikt0zqeolotjahrrkte; fvlid=1605284317709aRf8bjOAb0; webim_unReadCount=%7B%22time%22%3A1606184261283%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A40%2C%22msgbox%22%3A0%7D",
        "referer": "https://weibo.com/1742666164/Jn4c3wZmj?filter=hot&type=comment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41",
        "x-requested-with": "XMLHttpRequest"
    },

    "comment": {
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "TC-V5-G0=4de7df00d4dc12eb0897c97413797808; _s_tentry=www.google.com; Apache=902545514870.0345.1600846345176; SINAGLOBAL=902545514870.0345.1600846345176; ULV=1600846345180:1:1:1:902545514870.0345.1600846345176:; SSOLoginState=1601197609; login_sid_t=9d8fc5fed4cb9e5cd73c5d1a96fc4ee2; cross_origin_proto=SSL; UOR=www.google.com,weibo.com,www.baidu.com; WBtopGlobal_register_version=2020110622; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWgxyR8DlA5uOfXLUFsnVlP5JpX5KMhUgL.FoeXS0.NeoqN1KM2dJLoI7_DMcHfSoqcP0zEe5tt; SCF=AhkV6ZZAx6qPys4LoUJKrEDD1WfzsAaXRvFPrvuN10KgHZ7_UOtPPc5IwLtehF6cD3BwObP6TKFMJuz17vyAX7A.; SUB=_2A25yvxxNDeRhGeVK7FsW8ijLwjuIHXVRzQqFrDV8PUNbmtANLWfwkW9NTCmeblVf8rPc--6uzHJT2aQEEX668g9X; ALF=1637654427; wb_view_log_3479726797=1536*8641.25; ASP.NET_SessionId=yy3mnikt0zqeolotjahrrkte; fvlid=1605284317709aRf8bjOAb0; webim_unReadCount=%7B%22time%22%3A1606184261283%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A40%2C%22msgbox%22%3A0%7D",
        "referer": "https://weibo.com/1742666164/Jn4c3wZmj?filter=hot&type=comment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41",
        "x-requested-with": "XMLHttpRequest"
    },

}

loginMsg='''

https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E4%B8%AD%E5%9B%BD%E9%93%B6%E8%A1%8C+%E7%94%B5%E5%AD%90%E9%93%B6%E8%A1%8C&x_bfe_rqs=03E80&x_bfe_tjscore=0.000000&tngroupname=organic_news&newVideo=12&pn=10


'''

loginCookie='wxuin=1610134497; devicetype=android-24; version=2607023a; lang=zh_CN; rewardsn=; wxtokenkey=777; pass_ticket=n7zaWPtBa5p3vItJykj3ZkhXHZ3HchLLwnoEsl+lH2ICQgOCN0EXBSUl85YaESOe; wap_sid2=COHn4v8FEooBeV9ITm1XYmY2bE9rWkpTZDZxbEljVTRpWWdQUkVNbFNxNk1SNURWQWlSVWpzbF9PbnVWb3piN1hERk9rVVBtQ0VHTEdxVVdObjNWZEptSkxVRk5SbDNubTBFdXRYRmIyYVcxazViTUgxOFFJNEkwTkNXVzl5SXhRblRiV3RGb3FzeXR4d1NBQUF+MPvxpf0FOA1AAQ=='

