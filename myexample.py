#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2022/8/12 14:55
# @File  : myexample.py
# @Author: 
# @Desc  :
from gevent import monkey
monkey.patch_all()
from zhihu_crawler import search_crawler, set_cookie, set_proxy

if __name__ == '__main__':
    # 设置代理; 如采集量较大，建议每次请求都切换代理
    # set_proxy({'http': 'http://127.0.0.1:8125', 'https': 'http://127.0.0.1:8125'})
    # 设置cookie, 通过浏览器的开发这空间，本地缓存中可以获取
    d_c0_cookie = "AMAeDzBA1RKPTpUMkBSgGfhCkOoy9YZajf8=|1616328659"
    set_cookie({'d_c0': d_c0_cookie})

    # 可传入data_type 指定搜索类型, 获取数据类型 可选择（answer、article、zvideo） 默认三个类型都会采集
    for info in search_crawler(key_word='多模态', count=3, data_type='article'):
        print(info)
