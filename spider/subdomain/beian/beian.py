# -*- coding: utf-8 -*-
# @Time    : 2023/1/20  21:24
# @Author  : Leslie
# @File    : beian.py
# @Software: PyCharm
# @Describe:
# -*- encoding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
import json
import math
from termcolor import cprint
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}

def chinazApi(domain):
    cprint('Load chinazApi: ', 'green')
    chinazNewDomains = []
    companyName = ""

    #获取公司名称
    url = "https://micp.chinaz.com/Handle/AjaxHandler.ashx?action=GetPermit&query={}&type=host".format(domain)
    # url = "https://micp.chinaz.com/?query={}".format(domain)
    # print(url)
    try:
        res = requests.get(url=url, headers=headers, allow_redirects=False, verify=False, timeout=10)
    except Exception as e:
        print('[error] request : {}\n{}'.format(url, e.args))
        return chinazNewDomains, companyName
    text = res.text
    # print(text)
    companyName = re.search('ComName:"(.*)",Typ:', text)
    if companyName:
        companyName = companyName.group(1)
        # print(companyName)
    else:
        print("[{}] 没有匹配到公司名".format(domain))
        return chinazNewDomains, companyName

    #获取备案号
    # 获取备案号
    url = 'https://micp.chinaz.com/Handle/AjaxHandler.ashx?action=GetBeiansl&query={}&type=host'.format(domain)
    try:
        res = requests.get(url=url, headers=headers, allow_redirects=False, verify=False, timeout=10)
    except Exception as e:
        print('[error] request : {}\n{}'.format(url, e.args))
        return chinazNewDomains, companyName
    text = res.text
    beianResult = re.findall('SiteLicense:"([^"]*)",SiteName:"([^"]*)",MainPage:"([^"]*)",VerifyTime:"([^"]*)"', text)
    if not beianResult:
        print("[{}] 没有查到备案信息".format(domain))
        return chinazNewDomains, companyName

    for _ in beianResult:
        # print(_)
        beianId, siteName, newDomain, time = _
        if newDomain.startswith('www.'):
            newDomain = newDomain.replace("www.", '')
        chinazNewDomains.append([beianId, siteName, newDomain, time])

    # print('chinazApi去重后共计{}个顶级域名'.format(len(chinazNewDomains)))

    return chinazNewDomains, companyName


def run_beian(domain):
    beian = []
    chinazNewDomains, companyName = chinazApi(domain)

    tempDict = {}
    for each in chinazNewDomains:
        if each[1] not in tempDict:
            tempDict[each[1]] = each
            beian.append(each)
    cprint('-' * 50 + '去重后共计{}个顶级域名'.format(len(beian)) + '-' * 50, 'green')
    for _ in beian:
        print(_)
    cprint('去重后共计{}个顶级域名'.format(len(beian)), 'red')
    # print(companyName)
    return beian, companyName



if __name__ == '__main__':
    domain = 'baidu.com'
    run_beian(domain)