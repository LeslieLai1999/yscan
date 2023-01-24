# -*- coding: utf-8 -*-
# @Time    : 2023/1/22  0:21
# @Author  : Leslie
# @File    : githubSubdomain.py
# @Software: PyCharm
# @Describe:
# -*- encoding:utf-8 -*-
import configparser
import re
import time
from queue import Queue
from threading import Thread

import requests
from termcolor import cprint

from utils.tools import getRootPath

def init(domain,proxies):
    global cmp, per_page, query, headers, raw_url_emails, requests_proxies
    conf = configparser.ConfigParser()
    conf.read(getRootPath()+"conf/config.ini",encoding='utf-8')
    github_token = conf.get('github api', 'GITHUB_TOKEN')  # github的api token
    regexp = r'[0-9a-zA-Z_\-\.]+\.' + domain.replace('.', '\.')             # 正则语法
    cmp = re.compile(regexp)                                                # 模式对象
    per_page = 30                                                           # 每页的结果个数
    headers = {"Authorization": "token " + github_token}                    # api的请求头
    raw_url_emails = {}
    requests_proxies = proxies

def githubApiSearchCode(domain,page):
    url  = 'https://api.github.com/search/code?s=indexed&type=Code&o=desc&q="{}"&page={}&per_page={}'.format(domain, page, per_page)
    print(url)
    try:
        res = requests.get(url=url,headers=headers,proxies=requests_proxies,timeout=10)
        if res.status_code == 401:
            cprint("[!] github api 失效", "red")
        json_text = res.json()
        return json_text
    except Exception as e:
        print('[-] curl api error.')
        return False
def get_subdomain(raw_q, i, github_subdomains, save_fold_path, domain):
    while not raw_q.empty():
        raw_url = raw_q.get()
        try:
            res = requests.get(url=raw_url,headers=headers,proxies=requests_proxies,timeout=10)
            text = res.text
            subdomains = cmp.findall(text)
            if subdomains:
                # print(subdomains)
                for subdomain in subdomains:
                    github_subdomains.add(subdomain)

            with open('{}/{}_github.txt'.format(save_fold_path,domain),'at') as f:
                f.write('[------------------] {} [------------------] \n'.format(raw_url))
                f.write('{}\n'.format(text))

            raw_url_split = raw_url.split('/')
            username = raw_url_split[3]
            repository = raw_url_split[4]
            tags_url = "https://api.github.com/repos/{}/{}/tags".format(username, repository)
            res = requests.get(url=tags_url, headers=headers, proxies=requests_proxies,timeout=10)

            allEmails = []
            for each in eval(res.text):
                commit_url = each["commit"]["url"]
                commit_url_res = requests.get(url = commit_url,headers = headers,proxies=requests_proxies,timeout =10)
                commit_url_text = commit_url_res.text

                emails = re.findall('"email":"(.*?)",', commit_url_text)
                print(emails)
                if emails:
                    allEmails.extend(emails)
                time.sleep(1)
            allEmails = list(set(allEmails))
            raw_url_emails[raw_url] = allEmails




        except Exception as e:
            print('[-] {} errors: {}'.format(raw_url, e.args))




def githubSubdomain(domain, save_fold_path,proxies):
    init(domain,proxies)
    github_subdomains = set()
    json_text = githubApiSearchCode(domain,1)
    try:
        total_count = json_text['total_count']
    except Exception as e:
        return [],{}

    total_count = 300 if total_count>300 else total_count
    pages = total_count // per_page           # 每页的数据是30个
    print("pages:{}".format(pages))

    for page in range(1,pages):
        print('请求 page{}'.format(page))
        json_text = githubApiSearchCode(domain,page)
        if json_text and 'items' in json_text.keys():
            raw_q = Queue(-1)
            items = json_text['items']
            for item in items:
                raw_url = item['html_url'].replace('https://github.com/', 'https://raw.githubusercontent.com/').replace('/blob/', '/')
                raw_q.put(raw_url)

            threads = []
            for i in range(per_page):
                t = Thread(target=get_subdomain, args=(raw_q, i, github_subdomains, save_fold_path, domain))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
        print('子域名个数: {}'.format(len(github_subdomains)))
        github_subdomains = list(github_subdomains)
        print(raw_url_emails)
        return github_subdomains, raw_url_emails