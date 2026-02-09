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
from functools import lru_cache
from typing import Optional, List, Dict, Any


def safe_join(base: str, *paths: str) -> Optional[str]:
    """
    安全地连接路径，防止目录遍历攻击
    
    Args:
        base: 基础路径
        *paths: 要连接的路径部分
        
    Returns:
        连接后的安全路径，如果路径不安全则返回None
    """
    try:
        # 规范化基础路径
        base = os.path.normpath(base)
        
        # 构建目标路径
        target_path = os.path.normpath(os.path.join(base, *paths))
        
        # 检查目标路径是否在基础路径内
        if os.path.commonpath([base, target_path]) != base:
            logging.warning(f"不安全的路径访问尝试: {target_path}")
            return None
        
        return target_path
        
    except Exception as e:
        logging.error(f"路径处理时出错: {str(e)}")
        return None


def validate_path(path: str) -> bool:
    """
    验证路径是否安全，防止目录遍历攻击
    
    Args:
        path: 要验证的路径
        
    Returns:
        如果路径安全则返回True，否则返回False
    """
    # 检查路径是否包含危险字符
    dangerous_patterns = ['..', '//', '\\\\', '~']
    
    for pattern in dangerous_patterns:
        if pattern in path:
            logging.warning(f"路径包含危险模式: {pattern}")
            return False
    
    return True


def validate_novel_name(name: str) -> bool:
    """
    验证小说名称是否合法
    
    Args:
        name: 小说名称
        
    Returns:
        如果名称合法则返回True，否则返回False
    """
    # 检查名称是否为空
    if not name or not name.strip():
        logging.warning("小说名称为空")
        return False
    
    # 检查名称长度
    if len(name) > 100:
        logging.warning(f"小说名称过长: {name}")
        return False
    
    # 检查名称是否包含危险字符
    dangerous_chars = ['<', '>', '"', "'", '&', '/', '\\', '|', '?', '*']
    
    for char in dangerous_chars:
        if char in name:
            logging.warning(f"小说名称包含危险字符: {char}")
            return False
    
    return True


# 缓存装饰器，用于缓存函数结果
def cached_function(maxsize: int = 128):
    """
    创建一个缓存装饰器
    
    Args:
        maxsize: 缓存大小
        
    Returns:
        缓存装饰器
    """
    def decorator(func):
        cached_func = lru_cache(maxsize=maxsize)(func)
        
        def wrapper(*args, **kwargs):
            try:
                return cached_func(*args, **kwargs)
            except Exception as e:
                logging.error(f"缓存函数执行时出错: {str(e)}")
                # 出错时直接执行原函数，不使用缓存
                return func(*args, **kwargs)
        
        # 保留原函数的元数据
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        
        return wrapper
    
    return decorator


def get_file_encoding(file_path: str) -> Optional[str]:
    """
    检测文件编码
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件编码，如果无法检测则返回None
    """
    encodings = ['utf-8', 'gbk', 'utf-16', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(1024)  # 读取一小部分进行测试
            return encoding
        except UnicodeDecodeError:
            continue
        except Exception as e:
            logging.error(f"检测文件编码时出错: {str(e)}")
            continue
    
    return None
