# -*- encoding:utf-8 -*-
"""
@文件        :getUrl.py
@说明        :
@时间        :22/06/08/0008 20:10
@作者        :eleven
@软件        :PyCharm
"""
import getCities
import getDate


# 只要哈尔滨数据
def getUrls():
    url = "https://www.aqistudy.cn/historydata/daydata.php?city="
    urls = []
    cities = getCities.getcities('HotCities.txt')
    date = getDate.getdate()
    for city in cities:
        for da in date:
            data = url + city + "&month=" + da
            urls.append(data)
    return urls[0:102]


def getUrl(city, date):
    url = "https://www.aqistudy.cn/historydata/daydata.php?city="
    url = url + city + "&month=" + date
    return url


if __name__ == "__main__":
    print(getUrl('哈尔滨', '2019-01'))
