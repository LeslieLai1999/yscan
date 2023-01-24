# -*- coding: utf-8 -*-
# @Time    : 2023/1/21  16:00
# @Author  : Leslie
# @File    : ksubdomain.py
# @Software: PyCharm
# @Describe:
# -*- encoding:utf-8 -*-
import os
from utils.tools import getRootPath
def ksubdomain(domain):
    ksubdomains = []
    ksubdomain_folder = getRootPath()+"spider/subdomain/ksubdomain/"
    ksubdomain_file = '{}/{}.txt'.format(ksubdomain_folder, domain)
    os.system("chmod 777"+ksubdomain_folder+"ksubdomain.exe")
    os.system(ksubdomain_folder+"ksubdomain.exe"+" -d {} -o {}".format(domain, ksubdomain_file))
    try:
        with open(ksubdomain_file, 'rt') as f:
            for each_line in f.readlines():
                each_line_split = each_line.split('=>')
                subdomain = each_line_split[0].strip()                  # 子域名
                ksubdomains.append(subdomain)
        os.remove(ksubdomain_file)
    except Exception as e:
        ksubdomains = []

    return list(set(ksubdomains))


if __name__ == '__main__':
    ksubdomain("zjhu.edu.cn")
