# # -*- coding: utf-8 -*-

def novel_chapterizer(txt_content):
    t = txt_content.replace("\r", "").replace("\u3000", "").split("\n             ")
    ttt = [{
        "title": i.split("\n ")[0],
        "content": i.split("\n ")[1].split("\n")
    } for i in t]
    return ttt