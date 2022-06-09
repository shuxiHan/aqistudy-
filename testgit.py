# -*- encoding:utf-8 -*-
"""
@文件        :testgit.py
@说明        :
@时间        :22/06/08/0008 19:36
@作者        :eleven
@软件        :PyCharm
"""
# -*- coding: utf-8 -*-
import re
import csv
import Util
import json
import time
import base64
import execjs
import hashlib
import requests
from urllib.parse import urljoin
from getUrl import getUrl
from getDate import getdate
from getCities import getcities


def des_js(js_str, date, city):
    keys = re.findall(f'DES\.encrypt\((\w+)\s?,\s?(\w+)\s?,\s?(\w+)\)', js_str)
    text_name, key_name, iv_name = keys[0]
    key = re.findall(f'const\s+?{key_name}\s+?=.*?"(.*?)"', js_str)[0]
    iv = re.findall(f'const\s+?{iv_name}\s+?=.*?"(.*?)"', js_str)[0]
    appid_name = re.findall("appId:.*?(\w+),", js_str)[0]
    appId = re.findall(f"var\s?{appid_name}\s?=.*?'(.*?)'", js_str)[0]
    param_name = re.findall("data:\s?\{\s?(\w+):.*?}", js_str)[0]

    des_keys = re.findall(f'DES\.decrypt\(data,\s?(\w+),\s?(\w+)\);', js_str)
    des_dec_key_name, des_dec_iv_name = des_keys[0]

    des_dec_key = re.findall(f'const\s+?{des_dec_key_name}\s+?=.*?"(.*?)"', js_str)[0]
    des_dec_iv = re.findall(f'const\s+?{des_dec_iv_name}\s+?=.*?"(.*?)"', js_str)[0]

    aes_keys = re.findall(f'AES\.decrypt\(data,\s?(\w+),\s?(\w+)\);', js_str)
    aes_dec_key_name, aes_dec_iv_name = aes_keys[0]
    aes_dec_key = re.findall(f'const\s+?{aes_dec_key_name}\s+?=.*?"(.*?)"', js_str)[0]
    aes_dec_iv = re.findall(f'const\s+?{aes_dec_iv_name}\s+?=.*?"(.*?)"', js_str)[0]

    method = "GETDAYDATA"
    obj = {"city": city, "month": date}
    timestamp = int(time.time() * 1000)
    clienttype = 'WEB'
    form_data = {
        "appId": appId,
        "method": method,
        "timestamp": timestamp,
        "clienttype": clienttype,
        "object": obj,
        "secret": hashlib.md5(
            f'{appId}{method}{timestamp}{clienttype}{str(obj)}'.replace("'", '"').replace(' ', '').encode(
                'utf-8')).hexdigest()
    }
    base64_d = base64.b64encode(str(form_data).replace("'", '"').replace(' ', '').encode('utf-8')).decode('utf-8')
    result = js.call("des_encrypt", base64_d, key, iv)
    print(data := {param_name: result})
    url = "https://www.aqistudy.cn/historydata/api/historyapi.php"
    resp = requests.post(url=url, proxies=Util.Get(), headers=headers, data=data)
    print(resp.text)
    dec_data = js.call('dec_func', resp.text, des_dec_key, des_dec_iv, aes_dec_key, aes_dec_iv)
    # print(json.loads(dec_data))
    return json.loads(dec_data)


def aes_js(js_str, date, city):
    keys = re.findall(f'AES\.encrypt\((\w+)\s?,\s?(\w+)\s?,\s?(\w+)\)', js_str)
    text_name, key_name, iv_name = keys[1]
    key = re.findall(f'const\s+?{key_name}\s+?=.*?"(.*?)"', js_str)[0]
    iv = re.findall(f'const\s+?{iv_name}\s+?=.*?"(.*?)"', js_str)[0]
    appid_name = re.findall("appId:.*?(\w+),", js_str)[0]
    appId = re.findall(f"var\s?{appid_name}\s?=.*?'(.*?)'", js_str)[0]
    param_name = re.findall("data:\s?\{\s?(\w+):.*?}", js_str)[0]

    des_keys = re.findall(f'DES\.decrypt\(data,\s?(\w+),\s?(\w+)\);', js_str)
    des_dec_key_name, des_dec_iv_name = des_keys[0]

    des_dec_key = re.findall(f'const\s+?{des_dec_key_name}\s+?=.*?"(.*?)"', js_str)[0]
    des_dec_iv = re.findall(f'const\s+?{des_dec_iv_name}\s+?=.*?"(.*?)"', js_str)[0]

    aes_keys = re.findall(f'AES\.decrypt\(data,\s?(\w+),\s?(\w+)\);', js_str)
    aes_dec_key_name, aes_dec_iv_name = aes_keys[0]
    aes_dec_key = re.findall(f'const\s+?{aes_dec_key_name}\s+?=.*?"(.*?)"', js_str)[0]
    aes_dec_iv = re.findall(f'const\s+?{aes_dec_iv_name}\s+?=.*?"(.*?)"', js_str)[0]

    method = "GETDAYDATA"
    obj = {"city": city, "month": date}
    timestamp = int(time.time() * 1000)
    clienttype = 'WEB'
    form_data = {
        "appId": appId,
        "method": method,
        "timestamp": timestamp,
        "clienttype": clienttype,
        "object": obj,
        "secret": hashlib.md5(
            f'{appId}{method}{timestamp}{clienttype}{str(obj)}'.replace("'", '"').replace(' ', '').encode(
                'utf-8')).hexdigest()
    }

    base64_d = base64.b64encode(str(form_data).replace("'", '"').replace(' ', '').encode('utf-8')).decode('utf-8')

    result = js.call("aes_encrypt", base64_d, key, iv)
    print(data := {param_name: result})

    url = "https://www.aqistudy.cn/historydata/api/historyapi.php"

    resp = requests.post(url=url, proxies=Util.Get(), headers=headers, data=data)

    dec_data = js.call('dec_func', resp.text, des_dec_key, des_dec_iv, aes_dec_key, aes_dec_iv)
    # print(json.loads(dec_data))
    return json.loads(dec_data)


def bs64_js(js_str, date, city):
    appid_name = re.findall("appId:.*?(\w+),", js_str)[0]
    appId = re.findall(f"var\s?{appid_name}\s?=.*?'(.*?)'", js_str)[0]
    param_name = re.findall("data:\s?\{\s?(\w+):.*?}", js_str)[0]

    method = "GETDAYDATA"
    obj = {"city": city, "month": date}
    timestamp = int(time.time() * 1000)
    clienttype = 'WEB'
    form_data = {
        "appId": appId,
        "method": method,
        "timestamp": timestamp,
        "clienttype": clienttype,
        "object": obj,
        "secret": hashlib.md5(
            f'{appId}{method}{timestamp}{clienttype}{str(obj)}'.replace("'", '"').replace(' ', '').encode(
                'utf-8')).hexdigest()
    }

    base64_d = base64.b64encode(str(form_data).replace("'", '"').replace(' ', '').encode('utf-8')).decode('utf-8')

    data = {param_name: base64_d}

    url = "https://www.aqistudy.cn/historydata/api/historyapi.php"

    resp = requests.post(url=url, proxies=Util.Get(), headers=headers, data=data)

    des_keys = re.findall(f'DES\.decrypt\(data,\s?(\w+),\s?(\w+)\);', js_str)
    des_dec_key_name, des_dec_iv_name = des_keys[0]

    des_dec_key = re.findall(f'const\s+?{des_dec_key_name}\s?=.*?"(.*?)"', js_str)[0]
    des_dec_iv = re.findall(f'const\s+?{des_dec_iv_name}\s?=.*?"(.*?)"', js_str)[0]

    aes_keys = re.findall(f'AES\.decrypt\(data,\s?(\w+),\s?(\w+)\);', js_str)
    aes_dec_key_name, aes_dec_iv_name = aes_keys[0]
    aes_dec_key = re.findall(f'const\s+?{aes_dec_key_name}\s?=.*?"(.*?)"', js_str)[0]
    aes_dec_iv = re.findall(f'const\s+?{aes_dec_iv_name}\s?=.*?"(.*?)"', js_str)[0]

    dec_data = js.call('dec_func', resp.text, des_dec_key, des_dec_iv, aes_dec_key, aes_dec_iv)
    # print(json.loads(dec_data))
    return json.loads(dec_data)


if __name__ == '__main__':
    cities = getcities('HotCities.txt')
    date = getdate()
    for city in cities[6:]:
        header = ['aqi', 'co', 'no2', 'o3', 'pm10', 'pm2_5', 'quality', 'rank', 'so2', 'time_point']
        name = city + '.csv'
        with open(name, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
            writer.writeheader()  # 写入列名
        for da in date:
            print(da)
            url = getUrl(city, da)
            # url = "https://www.aqistudy.cn/historydata/daydata.php?city=%E4%B8%8A%E6%B5%B7&month=202201"
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/88.0.4324.192 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://www.aqistudy.cn",
                "Referer": "https://www.aqistudy.cn/historydata/daydata.php?city=%E4%B8%8A%E6%B5%B7&month=202201",
            }
            req = requests.get(url, proxies=Util.Get(), headers=headers)
            js_url = re.findall(r'src="(resource/js/.*?.min.js\?v=\d+)"', req.text)[0]
            js_req = requests.get(url=urljoin(url, js_url), proxies=Util.Get(), headers=headers)
            print(js_req.url)  # 输出一个js请求网站

            js_code = open('air_history.js', 'r').read()
            js_bs64_bs64_code = js_req.text[5:-2]
            js_code = js_code.replace('jscode_pattern', js_bs64_bs64_code)
            js = execjs.compile(js_code)
            res = js.call("get_full_js", js_bs64_bs64_code)
            type_len = len(re.findall("dweklxde", res))
            print(type_len)  # 返回状态值 下做判断

            base64_str = re.findall("'(.*?)'", res)[0]
            lastData = {}
            if type_len == 2:
                target_js = base64.b64decode(base64.b64decode(base64_str)).decode('utf-8')
                lastData = des_js(js_str=target_js, date=da, city=city)
            elif type_len == 1:
                target_js = base64.b64decode(base64_str).decode('utf-8')
                lastData = aes_js(js_str=target_js, date=da, city=city)
            elif type_len == 0:
                lastData = bs64_js(js_str=res, date=da, city=city)
            print(lastData)
            lastData = lastData['result']
            lastData = lastData['data']
            lastData = lastData['items']
            print(lastData)
            a = []
            dict = lastData[0]
            for headers in sorted(dict.keys()):  # 把字典的键取出来
                a.append(headers)
            header = a  # 把列名给提取出来，用列表形式呈现
            print(header)
            with open(name, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
                writer.writerows(lastData)  # 写入数据
            print(da + "数据已经写入成功！！！")
    print("所有数据写入完成！")
