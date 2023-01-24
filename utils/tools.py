# -*- coding: utf-8 -*-
# @Time    : 2023/1/19  19:31
# @Author  : Leslie
# @File    : tools.py
# @Software: PyCharm
# @Describe:
# -*- encoding:utf-8 -*-

import re
import yaml
import os
import dns.resolver
from termcolor import cprint


def getRootPath():
    # 获取文件目录
    curPath = os.path.abspath(os.path.dirname(__file__))
    # 获取项目根路径，内容为当前项目的名字
    rootPath = curPath[:curPath.find('yscan')+len('yscan')]+'/'
    return  rootPath

#判断是否是泛解析
def checkPanAnalysis(domain):
    cprint('-' * 50 + 'check Pan-Analysis ...' + '-' * 50, 'green')
    panDomain = 'sadfsadnxzjlkcxjvlkasdfasdf.{}'.format(domain)
    try:
        dns_A_ips = [j for i in dns.resolver.query(panDomain, 'A').response.answer for j in i.items]
        print(dns_A_ips)
        cprint('[泛解析] {} -> {}'.format(panDomain, dns_A_ips), 'red')
        return True
    except Exception as e:
        cprint('[不是泛解析] :{}'.format(e.args), 'red')
        return False


def isIP(str):
    rule = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if rule.match(str):
        return True
    return False

# 打印脚本跑出了几个新的子域名，并返回最新最全的子域名列表  传递两个列表，old是前面收集好的子域名，new是刚跑完的脚本收集的子域名，进行比较.
def printGetNewSubdomains(old_subdomains, new_subdomains):
    if len(old_subdomains) > 0:
        newSubdomains = list(set(new_subdomains) - set(old_subdomains))
        print('[new :{}] {}'.format(len(newSubdomains), newSubdomains))
    return list(set(new_subdomains + old_subdomains))


