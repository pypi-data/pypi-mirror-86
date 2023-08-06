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

    "weibo": {
        "ajwvr": "6",
        "domain": "100606",
        "is_ori": "1",
        "is_forward": "1",
        "is_text": "1",
        "is_pic": "1",
        "is_video": "1",
        "is_music": "1",
        "is_article": "1",
        "key_word": "",
        "start_time": "2020-03-01",
        "end_time": "2020-09-30",
        "is_search": "1",
        "is_searchadv": "1",
        "pagebar": 0,
        "pl_name": "Pl_Official_MyProfileFeed__23",
        "id": "1006061742666164",
        "script_uri": "/lancome",
        "feed_type": "0",
        "page": 1,
        "pre_page": 1,
        "domain_op": "100606",
        # "__rnd": "1606325093740"
    }

}

loginUrls =  {
    'proxyWeb': 'https://www.xicidaili.com/nn/',
    'proxies': {
        # "http": 'http://127.0.0.1:80',
        "https": 'https://127.0.0.1:1080'
    },
    "retweet":"https://weibo.com/aj/v6/mblog/info/big?",
    "comment":"https://weibo.com/aj/v6/comment/big?",
    "weibo":"https://weibo.com/p/aj/v6/mblog/mbloglist?",


}
loginHeaders = {

    "home": {
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "UOR=login.sina.com.cn,weibo.com,login.sina.com.cn; SINAGLOBAL=5579701838206.736.1605880029171; SSOLoginState=1606628214; wb_view_log_3479726797=1536*8641.25; _s_tentry=login.sina.com.cn; Apache=2393852256911.655.1606628221135; ULV=1606628221145:9:9:1:2393852256911.655.1606628221135:1606543374334; ALF=1638169203; SCF=Alx6A-qiJFwbh6ziknk_s1AyMls2FBOF9t8ivMLmXxCS18SdvP36puupPhqwE23ER5YMfTvPS9GJzRryFO62G1U.; SUB=_2A25yxzakDeRhGeVK7FsW8ijLwjuIHXVRtS9srDV8PUNbmtAKLW3YkW9NTCmebhi7PyeeViD0AEEB2B4zcGOzKtMb; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWgxyR8DlA5uOfXLUFsnVlP5JpX5KzhUgL.FoeXS0.NeoqN1KM2dJLoI7_DMcHfSoqcP0zEe5tt; webim_unReadCount=%7B%22time%22%3A1606633563784%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A43%2C%22msgbox%22%3A0%7D",
        # "referer": "https://weibo.com/lancome?is_hot=1&sudaref=passport.weibo.com",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41",
        "x-requested-with": "XMLHttpRequest"
    },

    "weibo": {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "cookie": "wvr=6; UOR=login.sina.com.cn,weibo.com,login.sina.com.cn; SINAGLOBAL=5579701838206.736.1605880029171; wb_view_log_3479726797=1536*8641.25; ALF=1637978842; SSOLoginState=1606442844; SCF=Alx6A-qiJFwbh6ziknk_s1AyMls2FBOF9t8ivMLmXxCSSKdtZqd4AEfEBkVEgiANosmViLJVDu-TRXwAVbUHcI0.; SUB=_2A25yxC8MDeRhGeVK7FsW8ijLwjuIHXVRsAfErDV8PUNbmtANLXPEkW9NTCmebm3nUKL0PVWttwaBVVcpVgItk9fn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWgxyR8DlA5uOfXLUFsnVlP5JpX5KzhUgL.FoeXS0.NeoqN1KM2dJLoI7_DMcHfSoqcP0zEe5tt; webim_unReadCount=%7B%22time%22%3A1606442918691%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A39%2C%22msgbox%22%3A0%7D; _s_tentry=login.sina.com.cn; Apache=418625672905.9967.1606442918717; ULV=1606442918728:7:7:6:418625672905.9967.1606442918717:1606381477124",
        "referer": "https://weibo.com/lancome?is_hot=1&sudaref=passport.weibo.com",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"
    },



}

loginMsg='''

https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E4%B8%AD%E5%9B%BD%E9%93%B6%E8%A1%8C+%E7%94%B5%E5%AD%90%E9%93%B6%E8%A1%8C&x_bfe_rqs=03E80&x_bfe_tjscore=0.000000&tngroupname=organic_news&newVideo=12&pn=10


'''

loginCookie='wxuin=1610134497; devicetype=android-24; version=2607023a; lang=zh_CN; rewardsn=; wxtokenkey=777; pass_ticket=n7zaWPtBa5p3vItJykj3ZkhXHZ3HchLLwnoEsl+lH2ICQgOCN0EXBSUl85YaESOe; wap_sid2=COHn4v8FEooBeV9ITm1XYmY2bE9rWkpTZDZxbEljVTRpWWdQUkVNbFNxNk1SNURWQWlSVWpzbF9PbnVWb3piN1hERk9rVVBtQ0VHTEdxVVdObjNWZEptSkxVRk5SbDNubTBFdXRYRmIyYVcxazViTUgxOFFJNEkwTkNXVzl5SXhRblRiV3RGb3FzeXR4d1NBQUF+MPvxpf0FOA1AAQ=='

