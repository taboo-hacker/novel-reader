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

import logging
from typing import List, Dict, Any


def novel_chapterizer(txt_content: str) -> List[Dict[str, Any]]:
    """
    将小说文本内容分章处理
    
    Args:
        txt_content: 小说文本内容
        
    Returns:
        分章后的章节列表，每个章节包含标题和内容
    """
    try:
        # 预处理文本，移除多余的回车和空格
        processed_content = txt_content.replace("\r", "").replace("\u3000", "")
        
        # 分割章节
        chapters_raw = processed_content.split("\n             ")
        
        chapters = []
        
        for i, chapter_raw in enumerate(chapters_raw):
            try:
                # 分割标题和内容
                parts = chapter_raw.split("\n ")
                
                if len(parts) >= 2:
                    title = parts[0].strip()
                    content_parts = parts[1:]
                    content = "\n".join(content_parts).split("\n")
                    # 过滤空行
                    content = [line.strip() for line in content if line.strip()]
                    
                    # 只添加内容不为空的章节
                    if content:
                        chapters.append({
                            "title": title,
                            "content": content
                        })
                else:
                    # 处理特殊情况，没有明确的标题和内容分隔
                    title = f"第{i+1}章"
                    content = chapter_raw.split("\n")
                    content = [line.strip() for line in content if line.strip()]
                    
                    # 只添加内容不为空的章节
                    if content:
                        chapters.append({
                            "title": title,
                            "content": content
                        })
                    
            except Exception as e:
                logging.error(f"处理章节时出错: {str(e)}")
                # 跳过错误章节，继续处理其他章节
                continue
        
        logging.info(f"成功解析{len(chapters)}个章节")
        return chapters
        
    except Exception as e:
        logging.error(f"分章处理时出错: {str(e)}")
        # 返回空列表作为错误处理
        return []
