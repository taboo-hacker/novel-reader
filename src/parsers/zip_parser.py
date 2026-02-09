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

import zipfile
import logging
from typing import Optional


def extract_txt_from_zip(zip_path: str) -> Optional[str]:
    """
    从ZIP文件中提取文本内容
    
    Args:
        zip_path: ZIP文件路径
        
    Returns:
        提取的文本内容，如果失败则返回None
        
    Raises:
        FileNotFoundError: 如果ZIP文件不存在
        zipfile.BadZipFile: 如果ZIP文件无效
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 获取ZIP文件中的所有TXT文件
            txt_files = [f for f in zip_ref.namelist() if f.endswith('.txt')]
            
            if not txt_files:
                logging.warning(f"ZIP文件中未找到TXT文件: {zip_path}")
                return None
            
            # 移除VIP文件
            txt_files = [f for f in txt_files if f != "Vip╙├╗º▒╪╢┴.txt" and f != "Vip用户必读.txt"]
            
            if not txt_files:
                logging.warning(f"ZIP文件中仅包含VIP文件: {zip_path}")
                return None
            
            # 优先选择带有"-飞卢小说网.txt"的文件
            feilu_files = [f for f in txt_files if "-飞卢小说网.txt" in f]
            if feilu_files:
                txt_file = feilu_files[0]
            else:
                # 如果没有找到，选择第一个文件
                txt_file = txt_files[0]
            
            # 尝试使用不同编码解码文件
            encodings = ['gbk', 'utf-8', 'utf-16', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    content = zip_ref.read(txt_file).decode(encoding)
                    logging.info(f"使用{encoding}编码成功解码文件: {txt_file}")
                    
                    # 对于带有"-飞卢小说网.txt"的文件，跳过第一行（小说标题）
                    if "-飞卢小说网.txt" in txt_file:
                        lines = content.split('\n')
                        if len(lines) > 1:
                            # 跳过第一行，重新组合内容
                            content = '\n'.join(lines[1:])
                            logging.info(f"跳过了文件{txt_file}的第一行小说标题")
                    
                    return content
                except UnicodeDecodeError:
                    continue
            
            logging.error(f"无法解码TXT文件: {txt_file}")
            return None
            
    except FileNotFoundError:
        logging.error(f"ZIP文件不存在: {zip_path}")
        return None
    except zipfile.BadZipFile:
        logging.error(f"无效的ZIP文件: {zip_path}")
        return None
    except Exception as e:
        logging.error(f"提取TXT文件时出错: {str(e)}")
        return None
