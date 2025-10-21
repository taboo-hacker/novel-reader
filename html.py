# # -*- coding: utf-8 -*-
# Copyright (C) 2025 taboo-hacker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
