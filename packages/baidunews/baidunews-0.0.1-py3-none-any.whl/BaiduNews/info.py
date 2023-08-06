#coding=utf-8

# import logging
# logging.basicConfig(filename='logging.log',
#                     format='%(asctime)s %(message)s',
#                     filemode="w", level=logging.DEBUG)

# 更新：



loginParam={

    "home": {
        "action": "home",
        "__biz": "MzU2MDEwMTIwMg==",
        "scene": "126",
        "bizpsid": "0",
        "devicetype": "android-24",
        "version": "2607023a",
        "lang": "zh_CN",
        "nettype": "WIFI",
        "a8scene": "3",
        "pass_ticket": "Vkwp3yVwhHlxsXI%2FWobAEiwAtIJMiL0b51OrjPT6VMb8oqLWFv0WuSYlcq6s8Zw7",
        "wx_header": "1"
    },

    "news": {
        "rtt": "1",
        "bsst": "1",
        "cl": "2",
        "tn": "news",
        "rsv_dl": "ns_pc",
        "word": "中国银行%20电子银行",
        "x_bfe_rqs": "03E80",
        "x_bfe_tjscore": "0.000000",
        "tngroupname": "organic_news",
        "newVideo": "12",
        "pn": 10
    },



}

loginUrls =  {
    'proxyWeb': 'https://www.xicidaili.com/nn/',
    'proxies': {
        # "http": 'http://127.0.0.1:80',
        "https": 'https://127.0.0.1:80'
    },
    "home":"https://mp.weixin.qq.com/mp/profile_ext?",
    "news":"https://www.baidu.com/s?",


}
loginHeaders = {
    "home":{
        "Host": "mp.weixin.qq.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; BLN-AL40 Build/HONORBLN-AL40; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2692 MMWEBSDK/23 Mobile Safari/537.36 MicroMessenger/6.7.2.1340(0x2607023A) NetType/WIFI Language/zh_CN",
        "Sec-Fetch-User": "?1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/tpg,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "x-wechat-key": "c202bf1b0f3945b142c8e98a33cc7ab2b2c28214047bd5a94a27d596d150a50885267c410097889f77fd8092f3e2aa4802c95defb12b04749d5ec50afdc0126904e6f6989a35e9ac463f0c510072f38f7cae66d7803c7ee78efbe92db982ec5d225bfcda21cc9216d259f1a8d70e91ca062f4a941f210d713e26b30e3d3286e4",
        "x-wechat-uin": "MTYxMDEzNDQ5Nw%3D%3D",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "wxuin=1610134497; devicetype=android-24; version=2607023a; lang=zh_CN; rewardsn=; wxtokenkey=777; pass_ticket=Vkwp3yVwhHlxsXI/WobAEiwAtIJMiL0b51OrjPT6VMb8oqLWFv0WuSYlcq6s8Zw7; wap_sid2=COHn4v8FEooBeV9IQ2tPNG9FVzlWX1E4OHBUYTJPNzVRdnRHUG5YYkhGVFp2aHdwLU91R1lIbXZqYmFRS215MUFWaVoxOU9qMmd6UE1YZ0NwYmZ1LUJyWDgwRHAtMUtZdFVqNVp1WFppYkpxdEV3QUZDdjVabTgxdmVscUhjSEl5S2xFd2VDSEhfMEJod1NBQUF+MPjwsP0FOA1AlU4="
    },
    "news": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "BIDUPSID=07A5EF20F795C6F28A1664BF003C4348; PSTM=1598845012; BAIDUID=07A5EF20F795C6F20E6FDCA63C2A7B4B",
        "Host": "www.baidu.com",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    },

}

loginMsg='''

https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E4%B8%AD%E5%9B%BD%E9%93%B6%E8%A1%8C+%E7%94%B5%E5%AD%90%E9%93%B6%E8%A1%8C&x_bfe_rqs=03E80&x_bfe_tjscore=0.000000&tngroupname=organic_news&newVideo=12&pn=10


'''

loginCookie='wxuin=1610134497; devicetype=android-24; version=2607023a; lang=zh_CN; rewardsn=; wxtokenkey=777; pass_ticket=n7zaWPtBa5p3vItJykj3ZkhXHZ3HchLLwnoEsl+lH2ICQgOCN0EXBSUl85YaESOe; wap_sid2=COHn4v8FEooBeV9ITm1XYmY2bE9rWkpTZDZxbEljVTRpWWdQUkVNbFNxNk1SNURWQWlSVWpzbF9PbnVWb3piN1hERk9rVVBtQ0VHTEdxVVdObjNWZEptSkxVRk5SbDNubTBFdXRYRmIyYVcxazViTUgxOFFJNEkwTkNXVzl5SXhRblRiV3RGb3FzeXR4d1NBQUF+MPvxpf0FOA1AAQ=='

