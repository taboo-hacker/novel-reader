# -*- coding: utf-8 -*-
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

import os
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import unquote
from src.config import XS_DIR, ENDSWITH, TEMPLATES_DIR


def generate_html(chapters: Optional[List[Dict[str, Any]]] = None, path: str = "/") -> str:
    """
    生成HTML内容
    
    Args:
        chapters: 章节列表，如果为None则显示小说列表
        path: 请求路径
        
    Returns:
        生成的HTML内容
    """
    try:
        # 基础HTML结构
        html_content = """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>小说阅读器</title>
            <link rel="stylesheet" href="/static/css/style.css">
            <script src="/static/js/app.js"></script>
        </head>
        <body>
            <div class="container">
                <header class="header">
                    <h1>小说阅读器</h1>
                    <div class="header-controls">
                        <button id="dark-mode-toggle">深色模式</button>
                        <button id="font-decrease">字体减小</button>
                        <button id="font-increase">字体增大</button>
                        <button id="add-bookmark">添加书签</button>
                    </div>
                </header>
                <main class="main-content">
        """
        
        if path == "/":
            # 显示小说列表
            html_content += '<section class="novel-list">'
            html_content += '<h2>小说列表</h2>'
            html_content += '<ul class="novel-list">'
            
            # 获取小说列表
            novels = []
            if os.path.exists(XS_DIR):
                for filename in os.listdir(XS_DIR):
                    if filename.endswith(ENDSWITH):
                        novel_name = filename[:-18]  # 移除后缀
                        novel_path = f"/{novel_name}"
                        novels.append((novel_name, novel_path))
            
            if novels:
                for novel_name, novel_path in novels:
                    html_content += f"<li><a href='{novel_path}'>{novel_name}</a></li>"
            else:
                html_content += '<li>暂无小说，请将小说ZIP文件放入xs目录</li>'
            
            html_content += '</ul>'
            html_content += '</section>'
            
        elif path.count("/") == 1:
            # 显示章节列表
            html_content += '<section class="chapter-list">'
            html_content += '<h2>章节列表</h2>'
            html_content += '<ul class="chapter-list">'
            
            if chapters and len(chapters) > 0:
                for i, chapter in enumerate(chapters):
                    chapter_path = f"{path}/{chapter['title']}"
                    html_content += f"<li><a href='{chapter_path}'>{chapter['title']}</a></li>"
            else:
                html_content += '<li>暂无章节内容</li>'
            
            html_content += '</ul>'
            html_content += '</section>'
            
        else:
            # 显示章节内容
            html_content += '<section class="chapter-content">'
            
            if chapters and len(chapters) > 0:
                # 提取章节标题
                chapter_title = unquote(path).split("/")[-1]
                
                # 查找对应章节
                target_chapter = None
                for chapter in chapters:
                    if chapter["title"] == chapter_title:
                        target_chapter = chapter
                        break
                
                if target_chapter:
                    html_content += f"<h2>{target_chapter['title']}</h2>"
                    html_content += '<div class="content">'
                    
                    for paragraph in target_chapter['content']:
                        if paragraph:
                            html_content += f"<p>{paragraph}</p>"
                    
                    html_content += '</div>'
                    
                    # 添加章节导航
                    chapter_index = chapters.index(target_chapter)
                    html_content += '<div class="chapter-navigation">'
                    
                    # 返回首页
                    html_content += '<a href="/" class="home-link">返回首页</a>'
                    
                    # 上一章
                    if chapter_index > 0:
                        prev_chapter = chapters[chapter_index - 1]
                        prev_path = f"{path.rsplit('/', 1)[0]}/{prev_chapter['title']}"
                        html_content += f"<a href='{prev_path}' class='prev-chapter'>上一章</a>"
                    
                    # 返回目录
                    novel_path = path.rsplit('/', 1)[0]
                    html_content += f"<a href='{novel_path}' class='toc-link'>返回目录</a>"
                    
                    # 下一章
                    if chapter_index < len(chapters) - 1:
                        next_chapter = chapters[chapter_index + 1]
                        next_path = f"{path.rsplit('/', 1)[0]}/{next_chapter['title']}"
                        html_content += f"<a href='{next_path}' class='next-chapter'>下一章</a>"
                    
                    html_content += '</div>'
                else:
                    html_content += '<h2>章节未找到</h2>'
                    html_content += '<p>抱歉，未找到该章节内容。</p>'
            else:
                html_content += '<h2>章节内容</h2>'
                html_content += '<p>暂无章节内容</p>'
            
            html_content += '</section>'
        
        # 结束HTML结构
        html_content += """
                </main>
                <footer class="footer">
                    <p>© 2025 小说阅读器</p>
                </footer>
            </div>
        </body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        logging.error(f"生成HTML时出错: {str(e)}")
        # 返回错误页面
        error_html = """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>错误 - 小说阅读器</title>
            <link rel="stylesheet" href="/static/css/style.css">
        </head>
        <body>
            <div class="container">
                <h1>错误</h1>
                <p>页面生成时出错，请稍后重试。</p>
                <a href="/">返回首页</a>
            </div>
        </body>
        </html>
        """
        return error_html
