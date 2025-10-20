# -*- coding: utf-8 -*-

from os import listdir
from urllib.parse import unquote
from settings import endswith, xs_dir


# 生成HTML内容
def generate_html(chapters=None, path="/"):
    html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>小说阅读器</title>
            <link rel="stylesheet" href="/style.css">  <!-- 引入外部CSS -->
        </head>
        <body>
            <div class="container">
                <h1>小说阅读器</h1>
        """
    if path == "/":
        lst = []
        html_content += "<ul class='chapter-list'>"
        for filename in listdir(xs_dir):
            if filename.endswith(endswith):
                lst.append(f"<li><a href=\'/{filename[:-18]}\'>{filename[:-18]}</a></li>")
        html_content += "".join(lst)
        html_content += "</ul>"
        html_content += "</div>"
    elif path.count("/") == 1:
        html_content += "<ul class='chapter-list'>"
        for chapter in chapters:
            html_content += f"<li><a href='{path}\\{chapter['title']}'>{chapter['title']}</a></li>" if chapter != chapters[0] else f"<li><h2>{chapter['title']}</h2></li>"
        html_content += "</ul>"
    else:
        for chapter in chapters:
            if chapter["title"] in unquote(path).split("/")[-1]:
                html_content += f"<h2>{chapter['title']}</h2>"
                html_content += f"<div class='chapter-content'>{'<br>'.join(c for c in chapter['content'])}</div>"
                break
    html_content += "</div></body></html>"
    return html_content
