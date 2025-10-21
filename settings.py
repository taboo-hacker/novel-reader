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

from config import *

print(f"环境：{ENV}")


def rule_set():
    if 'target' in globals():
        _endswith = globals().get('endswith')
        _rule = next(
            filter(lambda _rule: _rule["name"] == target and (_rule.get("endswith") == _endswith if _endswith else True),
                   rules),
            next(filter(lambda _rule: _rule["name"] == target, rules), dict()))
        if not _rule:
            _rule["name"] = "未知"
            _rule["endswith"] = _endswith if _endswith else "未知"
    return _rule


# 服务开启端口
port = 8080
# 小说源文件放的位置
xs_dir = "./xs"
# 小说目标
target = "飞卢小说"
# 小说源文件的格式
endswith = ".zip"
# 默认的日志文件路径
# LOG_FILE_DIR = "logs"
# 默认的日志文件名称
# LOG_FILE_NAME = "server.log"
# 默认的日志级别
# LOG_LEVEL = "INFO"

rules = [
    {
        "name": "飞卢小说",
        "endswith": ".zip"
    }
]

rule = rule_set()
if endswith != rule["endswith"] and not rule:
    endswith = rule["endswith"]
print("匹配规则：", rule)
