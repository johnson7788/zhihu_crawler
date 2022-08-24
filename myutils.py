#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2022/8/24 10:05
# @File  : utils.py
# @Author: 
# @Desc  : 工具
import os
import json
def rename_txtfile(data_dir="data"):
    """
    把txt文件命名成标题的名字
    """
    meta_file = os.path.join(data_dir, "meta.json")
    with open(meta_file, 'r') as f:
        meta_data = json.load(f)
    for one in meta_data:
        article_id = one["article_id"]
        title = one["title"]
        title = title.replace(":",'_').replace('"','_').replace("'",'_').replace(".",'_').replace(" ",'_').replace("/",'_')
        source_file = os.path.join(data_dir, f"{article_id}.txt")
        destination_file = os.path.join(data_dir, f"{title}.md")
        # 如果源文件存在，那么重新命名
        if os.path.exists(source_file):
            os.rename(source_file, destination_file)
        print(f"重命名文件: {source_file}到{destination_file}")

def read_article_id():
    file = "/opt/salt-daily-check/notes/zhihu.md"
    lines = []
    with open(file, "r") as f:
        for line in f:
            lines.append(line.strip())
    print(f"共收集到{len(lines)}行")
    infos = []
    for i in range(0, len(lines), 4):
        name = lines[i]
        url = lines[i + 1]
        title = lines[i + 2]
        assert "https" in url, f"链接{url}不对"
        info = {
            "name":name,
            "url": url,
            "title": title
        }
        infos.append(info)
    return infos

if __name__ == '__main__':
    read_article_id()