#!/usr/bin/python
# -*- coding: UTF-8 -*-

from urllib.request import *
from bs4 import BeautifulSoup
import lxml
import json
import re
rankUrl = ['https://www.bilibili.com/ranking/origin/1/0/3',
           'https://www.bilibili.com/ranking/origin/3/0/3',
           'https://www.bilibili.com/ranking/origin/129/0/3',
           'https://www.bilibili.com/ranking/origin/4/0/3',
           'https://www.bilibili.com/ranking/origin/36/0/3',
           'https://www.bilibili.com/ranking/origin/188/0/3',
           'https://www.bilibili.com/ranking/origin/160/0/3',
           'https://www.bilibili.com/ranking/origin/119/0/3',
           'https://www.bilibili.com/ranking/origin/155/0/3',
           'https://www.bilibili.com/ranking/origin/5/0/3',
           'https://www.bilibili.com/ranking/origin/181/0/3',]
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
           'Host':'api.bilibili.com',
           'Referer': '',
           'Origin':'https://www.bilibili.com'}
class video:
    '''
    data : score view danmaku reply favorite coin share like
    '''
    def __init__(self, avId,score):
        self.avId = avId     #av号
        self.data = [score]
    def generateUrl(self):
        return {'url':'https://api.bilibili.com/x/web-interface/archive/stat?aid=' + self.avId,
                'Referer':'https://www.bilibili.com/video/av' + self.avId}
    def getDetial(self):
        url = self.generateUrl()
        headers['Referer'] = url['Referer']
        req = Request(url=url['url'], headers=headers)
        originData = urlopen(req).read()
        data = json.loads(originData)['data']
        self.data.append(data['view'])
        self.data.append(data['danmaku'])
        self.data.append(data['reply'])
        self.data.append(data['favorite'])
        self.data.append(data['coin'])
        self.data.append(data['share'])
        self.data.append(data['like'])
        for v in self.data:
            print('%10d ' %(v), end='')
        print('')
if __name__ == '__main__':

    mainHeaders = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    vList = []
    for url in rankUrl:
        req = Request(url=url, headers=mainHeaders)
        try:
            originData = urlopen(req).read()
        except Exception as e:
            originData = e.partial
        data = BeautifulSoup(originData, "lxml")
        rankList = data.find_all("div", "content")

        for item in rankList:
            info = item.contents[1].contents
            href, score = info[0], info[3]
            avId = re.search('av\d*',href['href']).group()[2:]
            score = int(score.div.string)
            vList.append(video(avId, score))
        print('%10s %10s %10s %10s %10s %10s %10s %10s'\
              %('score' ,'view' ,'danmaku' ,'reply' ,'favorite' ,'coin' ,'share', 'like'))
        for v in vList:
            v.getDetial()



