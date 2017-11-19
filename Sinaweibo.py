import urllib.request
import json
import re
id = input('请输入id:')
file = input('请输入存储路径\nlike.D:\Python\上课代码a\Sinaweibo\weibo.txt：')
proxy_addr = '22.241.72.191:808'

def use_proxy(url,proxy_addr):
    req = urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Mobile Safari/537.36")
    proxy = urllib.request.ProxyHandler({'http':proxy_addr})
    opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(req).read().decode('utf-8','ignore')
    return data
def get_contaninerid(url):
    data = use_proxy(url,proxy_addr)
    content = json.loads(data)
    for data in content.get("tabsInfo").get("tabs"):
        if (data.get('tab_type') == 'weibo'):
            containerid = data.get('containerid')
    return containerid
def get_userInfo(id):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='+ id
    data = use_proxy(url,proxy_addr)
    content = json.loads(data)
    screen_name = content.get("userInfo").get("screen_name")
    followers_count = content.get("userInfo").get("followers_count")
    follow_count = content.get("userInfo").get("follow_count")
    statuses_count = content.get("userInfo").get("statuses_count")
    print("微博昵称：" + str(screen_name) + "\n" + "关注数：" + str(follow_count) + "\n" + "粉丝数：" + str(followers_count) + "\n" + "微博数：" + str(statuses_count) + "\n" )

def get_weibo(id,file):
    while True:
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
        data = use_proxy(url,proxy_addr)
        content = json.loads(data)
        follow_url = content.get("userInfo").get("follow_scheme")
        follow_url = follow_url.split("?")
        pattern = re.compile('followersrecomm')
        follow_url = re.sub(pattern, u'followers', follow_url[1])
        weibo_url = 'https://m.weibo.cn/api/container/getIndex?'+ follow_url
        print(weibo_url)
        try:
            data = use_proxy(weibo_url, proxy_addr)
            content = json.loads(data)
            cards = content.get('cards')
            if (len(cards)>0):
                for j in range(len(cards)):
                    card_type = cards[j].get('card_type')
                    if (card_type == 11 ):
                        card_group = cards[j].get('card_group')
                        if(len(card_group)>0):
                            for k in range(len(card_group)):
                                card_type = card_group[k].get('card_type')
                                if (card_type == 10):
                                    screen_name = card_group[k].get('user').get('screen_name')
                                    fid = card_group[k].get('user').get('id')
                                    with open(file,'a',encoding='utf-8') as fh:
                                        fh.write("关注人昵称：" + str(screen_name) + "\n" + "关注人id：" + str(fid))
            else:
                break
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__":
    get_userInfo(id)
    get_weibo(id,file)
