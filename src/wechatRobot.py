# -*- coding: utf-8 -*-

# @Time    : 2019/11/27 23:00
# @Author  : Leon
# @Email   : 1446684220@qq.com
# @File    : test.py
# @Desc    :
# @Software: PyCharm

from WechatPCAPI import WechatPCAPI
import time
import logging
from queue import Queue
import threading
from selenium import webdriver
import time
import selenium.webdriver
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from urllib import parse
import requests
import os
import schedule
import random
import ssl
import re



logging.basicConfig(level=logging.INFO)
queue_recved_message = Queue()


def on_message(message):
    queue_recved_message.put(message)


# 消息处理示例 仅供参考
def thread_handle_message(wx_inst):
    while True:
        # schedule.run_pending()
        message = queue_recved_message.get()
        print(message)

        if 'msg' in message.get('type'):
            # 这里是判断收到的是消息 不是别的响应
            msg_content = message.get('data', {}).get('msg', '')
            send_or_recv = message.get('data', {}).get('send_or_recv', '')
            from_wxid = message.get('data',{}).get('from_wxid','')
            from_chatroom_wxid = message.get('data',{}).get('from_chatroom_wxid','')
            member_wxid = message.get('data', {}).get('from_member_wxid', '')
            if send_or_recv[0] == '0':
                # 0是收到的消息 1是发出的 对于1不要再回复了 不然会无限循环回复
                # wx_inst.send_text('filehelper', '收到消息:{}'.format(msg_content))

                # 判断是群聊or私聊
                if (from_wxid):
                    toUser = from_wxid
                else:
                    toUser = from_chatroom_wxid


                #点歌功能
                if(msg_content[0:2] == "点歌"):
                    # print(msg_content[2:])
                    #异常处理
                    try:
                        result = send_song(msg_content[2:])
                        wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, '点歌失败QAQ')


                #百科功能
                if (msg_content[0:2] == "百科"):
                    #异常处理
                    try:
                        result = Baike(msg_content[2:])
                        wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, '查询百科出错QAQ')


                #百度知道
                if (msg_content[0:2] == "百度"):
                    print(msg_content[2:])
                    # 异常处理
                    try:
                        result = Zhidao(msg_content[2:])
                        wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, '呜呜呜百度找不到{}'.format(msg_content[2:]))

                #无内鬼
                global jishuqi
                if (msg_content == "无内鬼"):
                    # 异常处理
                    try:
                        for i in range(0,5):
                            img = imglist[jishuqi+i]
                            wx_inst.send_img(toUser, str(img))
                        jishuqi += 5
                    except:
                        wx_inst.send_text(toUser, '我真的一张都没有了,每晚十点半更新图库噢！')
                        # imglist = walkFile('C:\WechatRobot\src\wng/')
                        # jishuqi = int(0)

                #更新图库
                if (msg_content == "更新图库"):
                    # 异常处理
                    try:
                        wuneigui()
                        wx_inst.send_text(toUser, '更新成功！')
                    except:
                        wx_inst.send_text(toUser, '更新失败！')


                #微博热搜
                if (msg_content[0:3] == "看热搜"):
                    # 异常处理
                    # result = Get_Wbhot(msg_content[3:])
                    # wx_inst.send_text(toUser, '{}'.format(result))
                    try:
                        result = Get_Wbhot()
                        wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, "热搜异常")


                #热搜详情
                if (msg_content[0:4] == "热搜详情"):
                    # 异常处理
                    # result = Get_Wbhot(msg_content[3:])
                    # wx_inst.send_text(toUser, '{}'.format(result))
                    try:
                        result = Get_Wbhot_detail(msg_content[4:])
                        wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, "热搜异常")


                #看新闻
                if (msg_content[0:3] == "看新闻"):
                    # 异常处理
                    try:
                        result = get_news(msg_content[3:])
                        wx_inst.send_text(toUser, '{}'.format(result[0]))
                    except:
                        wx_inst.send_text(toUser, '很抱歉！没有找到与{}有关的新闻噢(⊙o⊙)！'.format(msg_content[3:]))

                #周公解梦
                if (msg_content[0:2] == "梦到"):
                    # 异常处理
                    try:
                        result = get_dream(msg_content[2:])
                        wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, '解梦功能异常')
                #简单聊天
                if (msg_content[0:4] == "@工具人"):
                    # 异常处理
                    try:
                        result = chat(msg_content[4:])
                        wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, '聊天功能异常！')

                #舔狗日记
                if (msg_content == "舔狗日记"):
                    # 异常处理
                    try:
                        result = dog_diary()
                        wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, '舔狗异常！')

                #搜题
                if (msg_content[0:2] == "搜题"):
                    # 异常处理
                    try:
                        result = search_answer(msg_content[2:])
                        wx_inst.send_text(toUser, '{}'.format(result))

                    except:
                        wx_inst.send_text(toUser, '很抱歉！没有找到与{}相关的题目噢(⊙o⊙)！'.format(msg_content[3:]))

                #文案
                if (msg_content[0:2] == "文案"):
                    # 异常处理
                    try:
                        result = get_moment()
                        wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, '今日次数已用光！')

                #毒鸡汤
                if (msg_content[0:3] == "毒鸡汤"):
                    # 异常处理
                    try:
                        result = get_dujitang()
                        wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, '今日次数已用光！')

                #彩虹屁
                if (msg_content[0:2] == "夸我"):
                    # 异常处理
                    try:
                        result = get_chp()
                        if("XXX" in result):
                            wx_inst.send_text(toUser, '{}'.format(result.split("XXX")[0]))
                            wx_inst.send_text(toUser, '{}'.format(result.split("XXX")[1]), member_wxid)
                        else:
                            wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, '今日次数已用光！')

                #知乎
                if (msg_content[0:2] == "知乎"):
                    # 异常处理
                    try:
                        result = zhihu(msg_content[2:])
                        wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, '我有问题？')

                #天气
                if (msg_content[0:3] == "看天气"):
                    # 异常处理
                    try:
                        result = weather(msg_content[3:])
                        wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, 'error')
                #搜歌
                if (msg_content[0:2] == "搜歌"):
                    # 异常处理
                    try:
                        result = download_song(msg_content[2:])
                        wx_inst.send_text(toUser, '{}'.format(result))
                    except:
                        wx_inst.send_text(toUser, '服务器繁忙，请稍后再试！')


# def thread_timer_message(wx_inst):
#     while True:
#         # schedule.every(1).to(10).days.do(job, name)
#         # schedule.every().monday.do(job, name)

#         schedule.run_pending()

def main():
    # 初始化wx实例

    wx_inst = WechatPCAPI(on_message=on_message)

    # 启动微信 目前仅支持微信V2.7.1.82
    wx_inst.start_wechat(block=True)

    # 等待登陆成功，此时需要人为扫码登录微信
    while not wx_inst.get_myself():
        time.sleep(5)
    # 登录成功了
    print(wx_inst.get_myself())

    # schedule.every().day.at("22:30").do(job)
    # schedule.every(1).minutes.do(weather_lpf, wx_inst)
    threading.Thread(target=thread_handle_message, args=(wx_inst,)).start()
    # schedule.every().day.at("09:00").do(weather_lpf, wx_inst)
    # schedule.every().day.at("22:30").do(wuneigui)
    # threading.Thread(target=thread_timer_message, args=(wx_inst,)).start()

    # 这个是获取群具体成员信息的，成员结果信息也从上面的回调返回
    # wx_inst.get_member_of_chatroom('22941059407@chatroom')
    #
    # # 新增@群里的某人的功能
    # wx_inst.send_text(to_user='22941059407@chatroom', msg='test for at someone', at_someone='wxid_6ij99jtd6s4722')

    # 这个是更新所有好友、群、公众号信息的，结果信息也从上面的回调返回
    # wx_inst.update_frinds()



#舔狗日记
def dog_diary():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://api.ixiaowai.cn/tgrj/" # 进行url编码
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    request = urllib.request.Request(url, headers=headers)  # 请求，修改，模拟http.
    data = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(data, "html5lib").getText()
    week = int(time.strftime('%w'))
    week_chn = ['星期一','星期二','星期三','星期三','星期四','星期五','星期六','星期日']
    weather = ['晴','阴','多云','雨','暴雨']
    str1 = time.strftime('%Y{y}%m{m}%d{d}\t').format(y='年', m='月', d='日')+week_chn[week]+"\t"+weather[random.randint(0, len(weather)-1)]+"\n"+soup
    return str1


#点歌
def send_song(songname):
    url = "https://weixin.sogou.com/weixinwap?query=%E9%9F%B3%E4%B9%90+%E6%AD%8C%E6%9B%B2+" + urllib.parse.quote(songname) + "&ie=utf8&s_from=input&type=2&t=1598101509501&pg=webSearchList&_sug_=n&_sug_type_="
    option = selenium.webdriver.ChromeOptions()
    option.add_argument('headless')
    # 打开chrome浏览器
    driver = webdriver.Chrome(chrome_options=option)
    driver.get(url)
    button = driver.find_element_by_css_selector('#sogou_vr_11002601_box_0 > div.list-txt > h4 > a')
    driver.switch_to.window(driver.window_handles[-1])
    sreach_window3 = driver.current_window_handle
    button.click()
    time.sleep(0.5)
    url = driver.current_url
    title = driver.find_element_by_xpath('//*[@id="activity-name"]').text
    str = title + ":" + "\n==点击下方链接即可播放歌曲(>__<)==\n" + url
    driver.close()
    return str



#百科
def Baike(query):
    url = "https://baike.baidu.com/item/" + parse.quote(query) #进行url编码
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    request = urllib.request.Request(url, headers=headers)  # 请求，修改，模拟http.
    data = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(data, "html5lib")
    for i in soup.select('sup'):
        i.decompose()
    mydata = soup.select('div[class="lemma-summary"]')
    #取到的数据含有解析不了的utf代码，将其用空格替代
    return mydata[0].get_text().replace(u'\u200b', u' ')


#百度知道
def Zhidao(query):
    url = "https://zhidao.baidu.com/index/?fr=new_search_top&word=" + parse.quote(query)
    # url = "https://www.52pojie.cn/"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    request = urllib.request.Request(url, headers=headers)  # 请求，修改，模拟http.
    data = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(data, "html5lib")
    mydata = soup.select('div[class="main-con-box"]')
    url = "https://zhidao.baidu.com/" + mydata[0].a.attrs['data-url']
    # print(url)
    headers = {"User-Agent":"Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"}
    request = urllib.request.Request(url, headers=headers)  # 请求，修改，模拟http.
    data = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(data, "html5lib")
    mydata = soup.select('div[class="full-content"]')
    result = mydata[0].get_text()
    result = result.replace('  ', '').replace('\n', '').replace('展开全部', '').replace('已赞过', '').replace('你对这个回答的评价是？评论收起','').replace('已踩过','')
    print(len(result))
    if(len(result)>250):
        result = result[0:240] + "..."
    return result

#简单聊天
def chat(info):
    url = "https://api.ownthink.com/bot?appid=xiaosi&userid=df71d0c341f61aa8f4cece811b510da3&spoken=" + info
    r = requests.get(url)
    # print("stata code: " + str(r.status_code))
    # 将API响应存储在一个变量中
    response_dict = r.json()
    # 处理结果
    return response_dict['data']['info']['text']

#微博热搜
def Get_Wbhot():
    url = "https://s.weibo.com/top/summary?Refer=top_hot"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    request = urllib.request.Request(url, headers=headers)  # 请求，修改，模拟http.

    data = urllib.request.urlopen(request).read().decode('utf-8')
    soup = BeautifulSoup(data, "html5lib")
    hotlist = soup.find_all("td", class_="td-02")
    result = "#微博热搜榜 ("+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+")\n"

    global href_list
    href_list = []
    i=1

    for line in hotlist[1:20]:
        if(i>10):
            break

        soup2 = BeautifulSoup(str(line),"lxml")
        soup2.span.extract()
        result += str(i)+"."+soup2.select('a')[0].get_text()+"\n"
        if(soup2.select('a')[0].attrs['href']=="javascript:void(0);"):
            # print("我有问题")
            continue
        href_list.append("https://s.weibo.com/"+ soup2.select('a')[0].attrs['href'])

        print(i)
        i+=1
        # print("https://s.weibo.com/"+ soup2.select('a')[0].attrs['href'])
    # print(href_list[0])
    # print(result)
    # print(result)
    return result

def Get_Wbhot_detail(index):
    # 看详情
    global href_list
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    url = href_list[int(index) - 1]
    request = urllib.request.Request(url, headers=headers)  # 请求，修改，模拟http.
    data = urllib.request.urlopen(request).read().decode('utf-8',"ignore")
    soup = BeautifulSoup(data, "html5lib")
    # 获取发布者
    user = soup.select_one('div.content > div.info > div:nth-child(2)').text.replace(' ', '').replace('\n', '').replace(u'\u200b', u' ')
    # 获取正文
    content = soup.select_one('div.content > p.txt').text.replace(' ', '').replace(u'\u200b', u' ')
    result = ""
    result += user + ":" + content
    return result



#周公解梦
def get_dream(keyword):
    url = "http://api.avatardata.cn/ZhouGongJieMeng/LookUp?key=ad499362b3fa4a2c8acc7bbebf775290&keyword=" + keyword
    r = requests.get(url)
    # print("stata code: " + str(r.status_code))
    # 将API响应存储在一个变量中
    response_dict = r.json()
    # 处理结果
    result = ""
    # print(response_dict.keys())
    if(response_dict['total'] != 0):

        result = response_dict['result'][0]['title'] + ":\n"
        result += response_dict['result'][0]['content'].replace('<div>','').replace('</div>','').replace('<br/>','\n')

    else:
        result = "很遗憾，周公解不了这个梦噢"
    return result


#天气
def weather():
    url = "https://yiketianqi.com/api?version=v61&appid=24723754&appsecret=EHsst4lC&version=v61&cityid=101282102"
    r = requests.get(url)
    # print("stata code: " + str(r.status_code))
    # 将API响应存储在一个变量中
    response_dict = r.json()
    # 处理结果
    # print(response_dict.keys())
    # print(response_dict['city'])
    # for key in response_dict.keys():
    #     print(str(key)+":"+str(response_dict[key]))
    # for key in response_dict['aqi'].keys():
    #     print(str(key)+":"+str(response_dict['aqi'][key]))
    #日期
    output = "#今日晨报#\n"
    output += str(response_dict['date'])+"\t"+str(response_dict['week'])+"\n"
    output += str(response_dict['city'])+",今天" + str(response_dict['wea'])+",温度："+str(response_dict['tem1'])+"℃~"+str(response_dict['tem2'])
    output += "℃,当前温度:" + str(response_dict['tem'])+"，空气质量:"+str(response_dict['air_level'])+","+str(response_dict['air_tips'])
    output += str(response_dict['aqi']['yundong'])+","+str(response_dict['aqi']['kaichuang'])+"。"

    return output


#看新闻
def get_news(keyword):
    url = "http://api.avatardata.cn/ActNews/Query?key=a4b1af8967524790a1c49bfe89113433&keyword=" + keyword
    r = requests.get(url)
    # print("stata code: " + str(r.status_code))
    # 将API响应存储在一个变量中
    response_dict = r.json()
    # 处理结果
    print(response_dict.keys())
    result = []
    for i in response_dict['result']:
        result.append(i['title'].replace('<em>','').replace('</em>','')+"\n"+i['content'].replace('<em>','').replace('</em>','')+"\n"+i['pdate'].replace('<em>','').replace('</em>',''))
    return result


#更新图库
def job():
    for i in walkFile("C:\WechatRobot\src\wng/"):
        del_file(i)
    url_list = get_url()
    src1 = get_src(url_list[0])
    src2 = get_src(url_list[1])

    download_img(src1,1)
    download_img(src2,2)

    global jishuqi
    jishuqi = int(0)
    global imglist
    imglist = walkFile("C:\WechatRobot\src\wng/")


#爬取前俩个a标签的url
def get_url():
    url = "https://www.mzitu.com"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    request = urllib.request.Request(url, headers=headers)  # 请求，修改，模拟http.
    data = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(data, "html5lib")
    mydata1 = soup.select_one('ul#pins > li:nth-child(1) > a').attrs['href']
    mydata2 = soup.select_one('ul#pins > li:nth-child(2) > a').attrs['href']
    return mydata1,mydata2
#爬取每一张图片的src
def get_src(url):
    # url = "https://www.mzitu.com/245789"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    request = urllib.request.Request(url, headers=headers)  # 请求，修改，模拟http.
    data = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(data, "html5lib")
    mydata = str(soup.select_one('div.main-image>p>a>img').attrs['src'])
    sum = soup.select_one('body > div.main > div.content > div.pagenavi > a:nth-child(7) >span').get_text()
    sum = int(sum)
    img_src = []
    img_src.append(mydata)
    # print(sum)
    print(url)
    for i in range(2,sum):
        url2 = url+"/"+str(i)
        request = urllib.request.Request(url2, headers=headers)  # 请求，修改，模拟http.
        data = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(data, "html5lib")
        mydata = str(soup.select_one('div.main-image>p>a>img').attrs['src'])
        img_src.append(mydata)
    return img_src


def download_img(img_src,dir_name):
    # print(img_src)
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Referer": "https://www.mzitu.com/"} # 设置http header，视情况加需要的条目，这里的token是用来鉴权的一种方式
    i = 1
    for src in img_src:
        # print(i)
        r = requests.get(src, headers=header, stream=True)
        # print(r.status_code)  # 返回状态码
        if r.status_code == 200:
            open('wng/' + str(dir_name)+ "/" + str(i) + '.jpg', 'wb').write(r.content)  # 将内容写入图片
            # print("done")
        del r
        i += 1

def del_file(path):
    os.remove(path)

def walkFile(file):
    img = []
    for root, dirs, files in os.walk(file+"1"):
        for f in files:
            img.append(os.path.join(root, f))
    for root, dirs, files in os.walk(file+"2"):
        for f in files:
            img.append(os.path.join(root, f))
    return img


def walkFile2(file):
    img = []
    for root, dirs, files in os.walk(file):
        for f in files:
            img.append(os.path.join(root, f))
    return img

def wuneigui():
    global jishuqi
    jishuqi = int(0)
    global imglist
    imglist = walkFile("C:\WechatRobot\src\wng/")


def search_answer(query):
    url = "https://www.baidu.com/s?wd=" + parse.quote(query) + "+site:tiku.baidu.com"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"}
    request = urllib.request.Request(url, headers=headers)  # 请求，修改，模拟http.
    data = urllib.request.urlopen(request).read().decode('utf-8')
    # print(data)
    # print(data)
    soup = BeautifulSoup(data, "html5lib")
    newurl = soup.select('div#content_left>div>h3>a')[0].attrs['href']

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(newurl)

    data = driver.page_source
    driver.close()
    # print(data)
    soup = BeautifulSoup(data, "html5lib")
    question = soup.select_one('#undefined > div > div > div.que-stem > div').text
    answer = soup.select_one('div.exam-answer > div > div').text
    analysis = soup.select_one('div.exam-analysis.exam-info > div').text
    result = "题:"+question+"\n"
    result+= "正确答案:"+answer+"\n"
    result+="解析："+analysis

    return result

#朋友圈文案
def get_moment():
    url = "http://api.tianapi.com/txapi/pyqwenan/index?key=59d742124cc4567eb1c74be38343cc3a"
    r = requests.get(url)
    # print("stata code: " + str(r.status_code))
    # 将API响应存储在一个变量中
    response_dict = r.json()
    # 处理结果
    # print(response_dict.keys())
    content = response_dict['newslist'][0]['content']
    source = response_dict['newslist'][0]['source']

    str = content+"\t——"+source
    # print(str)
    return str


#毒鸡汤
def get_dujitang():
    url = "http://api.tianapi.com/txapi/dujitang/index?key=59d742124cc4567eb1c74be38343cc3a"
    r = requests.get(url)
    # print("stata code: " + str(r.status_code))
    # 将API响应存储在一个变量中
    response_dict = r.json()
    # 处理结果
    # print(response_dict.keys())
    content = response_dict['newslist'][0]['content']

    str = content
    # print(str)
    return str

#彩虹屁
def get_chp():
    url = "http://api.tianapi.com/txapi/caihongpi/index?key=59d742124cc4567eb1c74be38343cc3a"
    r = requests.get(url)
    # print("stata code: " + str(r.status_code))
    # 将API响应存储在一个变量中
    response_dict = r.json()
    # 处理结果
    # print(response_dict.keys())
    content = response_dict['newslist'][0]['content']
    str = ""
    str = content
    print(str)
    return str

#知乎
def zhihu(query):
    url = "https://www.baidu.com/s?wd="+parse.quote(query)+"+site:www.zhihu.com"

    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"}
    request = urllib.request.Request(url, headers=headers)  # 请求，修改，模拟http.
    time.sleep(1)
    data = urllib.request.urlopen(request).read().decode('utf-8')
    # print(data)
    soup = BeautifulSoup(data, "html5lib")
    newurl = soup.select('div#content_left>div>h3>a')[0].attrs['href']

    # print(mydata)
    # url = "https://www.zhihu.com/question/316608391/answer/1483888117"
    request = urllib.request.Request(newurl, headers=headers)  # 请求，修改，模拟http.
    data = urllib.request.urlopen(request).read().decode('utf-8')
    soup = BeautifulSoup(data, "html5lib")

    title = soup.select_one('div.QuestionHeader-main > h1')
    result = "题："+title.text+"\n答："
    mydata = soup.select_one('div.RichContent-inner>span')
    # print(mydata)
    for e in mydata:
        result+=e.text
    return result




#天气实况
def weather(city):
    url = "https://geoapi.qweather.com/v2/city/lookup?location="+city+"&key=3ab4d9124c334a37b0e83c07bf249879"
    r = requests.get(url)
    # print("stata code: " + str(r.status_code))
    # 将API响应存储在一个变量中
    response_dict = r.json()
    # 处理结果
    # print(response_dict.keys())
    print(response_dict['location'][0]['id'])
    city_id = response_dict['location'][0]['id']
    city_name = response_dict['location'][0]['name']
    url =  "https://devapi.qweather.com/v7/weather/now?location="+city_id+"&key=3ab4d9124c334a37b0e83c07bf249879"
    r = requests.get(url)
    # print("stata code: " + str(r.status_code))
    # 将API响应存储在一个变量中
    response_dict = r.json()
    # print(response_dict['now'])
    result = ""
    result += (city_name+"天气实况:")+"\n"
    result += ("实况温度：" + response_dict['now']['temp']+"℃")+"\n"
    result += ("实况体感温度：" + response_dict['now']['feelsLike']+"℃")+"\n"
    result += ("天气状态：" + response_dict['now']['text'])+"\n"
    result += ("实况风向	：" + response_dict['now']['windDir'])+"\n"
    result += ("实况风力等级	：" + response_dict['now']['windScale'])
    return result


def download_song(query):
    url = "https://www.musicenc.com/search.php?q="+parse.quote(query)+"&Submit=%E6%90%9C%E7%B4%A2"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.find_element_by_css_selector('body > div.article > div.lbox > div.whitebg.bloglist > ul > li:nth-child(1) > h3 > a').click()

    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    song = driver.find_element_by_css_selector('body > div.article > div.lbox > div.content_box.whitebg > h1').text
    driver.find_element_by_css_selector('#downs').click()
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    link = driver.current_url
    result = song + "\n点击链接用浏览器打开即可下载！\n" + link
    return result


if __name__ == '__main__':
    jishuqi = int(0)
    imglist = walkFile('C:\WechatRobot\src\wng/')
    JM = int(0)
    JMlist = walkFile2('C:\WechatRobot\src\JM/')
    ZH = int(0)
    ZHlist = walkFile2('C:\WechatRobot\src\ZH/')
    YWQ = int(0)
    YWQlist = walkFile2('C:\WechatRobot\src\YWQ/')
    main()
