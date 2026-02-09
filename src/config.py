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

# 基础配置
DEBUG = False  # 默认关闭调试模式
ENV = "production"  # 默认环境为生产环境

# 服务配置
PORT = 8080  # 服务开启端口

# 路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XS_DIR = os.path.join(BASE_DIR, "xs")  # 小说源文件放的位置
STATIC_DIR = os.path.join(BASE_DIR, "static")  # 静态文件目录
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")  # 模板文件目录
LOGS_DIR = os.path.join(BASE_DIR, "logs")  # 日志文件目录

# 日志配置
LOG_FILE_NAME = "server.log"  # 默认的日志文件名称
LOG_LEVEL = "INFO"  # 默认的日志级别

# 小说配置
TARGET = "飞卢小说"  # 小说目标
ENDSWITH = ".zip"  # 小说源文件的格式

# 小说规则配置
RULES = [
    {
        "name": "飞卢小说",
        "endswith": ".zip"
    }
]

# 确保必要的目录存在
for dir_path in [XS_DIR, LOGS_DIR, STATIC_DIR, TEMPLATES_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
