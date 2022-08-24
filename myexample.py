#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2022/8/12 14:55
# @File  : myexample.py
# @Author: 
# @Desc  :
import atexit
import json
import os
import time
import random
from tqdm import tqdm
from gevent import monkey
monkey.patch_all()
from myutils import read_article_id
from zhihu_crawler import search_crawler, set_cookie, set_proxy, common_crawler

def save_metafile(meta_data, meta_file):
    # 如果已经存在meta_file文件，那么读取后和现有meta_data合并
    if os.path.exists(meta_file):
        print(f"已存在{meta_file}文件，读取后和现有meta_data合并")
        with open(meta_file, 'r') as f:
            old_data = json.load(f)
        print(f"原有meta_data条数：{len(old_data)}, 现有meta_data条数：{len(meta_data)}")
        meta_data += old_data
    print(f"保存源数据到{meta_file},共{len(meta_data)}条")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta_data, f, ensure_ascii=False)
    return meta_data

def get_words():
    words_file = "/opt/lang/kg/words.json"
    with open(words_file, 'r') as f:
        data = json.load(f)
    words = []
    for one in data:
        words.append(one["english"])
    return words

def spider_by_words():
    meta_data = []
    words = get_words()
    # words = ["johnson7788"]
    start_idx = 98 # 从第几个单词开始搜索,98
    cnt = 0  # 记录总的爬取次数
    # 保存源数据
    atexit.register(save_metafile, meta_data, meta_file)
    for idx, word in enumerate(words):
        print(f"正在爬取关键字: {word}, 当前第{idx}个关键字")
        if idx < start_idx:
            continue
        # 可传入data_type 指定搜索类型, 获取数据类型 可选择（answer、article、zvideo） 默认三个类型都会采集
        current_word_cnt = 0
        for info in search_crawler(key_word=word, count=10, nums=10, data_type='article'):
            cnt += 1
            current_word_cnt += 1
            if "title" not in info or "article_id" not in info:
                print(f"warning: 注意，这个请求有问题，请检查爬虫")
                time.sleep(random.randint(1, 3))
                continue
            title = info["title"]
            article_id = info["article_id"]
            #  把content弹出来
            content = info.pop("content")
            # 根据id保存文章内容到文件
            article_file = os.path.join(save_dir, f"{article_id}.txt")
            with open(article_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"爬取到第{cnt}条数据，保存文章: {title}  到  {article_file}")
            # 源数据要保存起来
            meta_data.append(info)
            time.sleep(random.randrange(10,15))
            if current_word_cnt >= 10:
                break
    save_metafile(meta_data, meta_file)



def spider_by_articleid():
    meta_data = []
    sub_dir = "article"
    final_saved = os.path.join(save_dir, sub_dir)
    if not os.path.exists(final_saved):
        os.mkdir(final_saved)
    # 读取所有文章的id
    infos = read_article_id()
    # 保存源数据
    atexit.register(save_metafile, meta_data, meta_file)
    for info in tqdm(infos):
        title = info["title"]
        title = title.replace(" ",'_').replace(":",'_')
        url = info["url"]
        article_id = url.split('p/')[-1]
        spinfos = common_crawler(task_id=article_id, data_type="article")
        spinfo = list(spinfos)[0]
        # 根据id保存文章内容到文件
        content = spinfo.pop("content")
        article_file = os.path.join(final_saved, f"{title}.md")
        with open(article_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"保存文章: {title}  到  {article_file}")
        # 源数据要保存起来
        meta_data.append(spinfo)
        time.sleep(random.randrange(5, 10))
    save_metafile(meta_data, meta_file)

if __name__ == '__main__':
    # 设置代理; 如采集量较大，建议每次请求都切换代理
    # set_proxy({'http': 'http://127.0.0.1:8125', 'https': 'http://127.0.0.1:8125'})
    # 设置cookie, 通过浏览器的开发这空间，本地缓存中可以获取
    d_c0_cookie = "AMAeDzBA1RKPTpUMkBSgGfhCkOoy9YZajf8=|1616328659"
    set_cookie({'d_c0': d_c0_cookie})
    save_dir = "data"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    meta_file = os.path.join(save_dir, "meta.json")
    spider_by_articleid()
    # spider_by_words()


