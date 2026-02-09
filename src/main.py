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

"""
小说阅读器主入口文件

该文件是小说阅读器的主入口，负责启动HTTP服务器并处理请求。
"""

from .server import start_server


if __name__ == "__main__":
    """
    主函数，启动小说阅读器服务器
    """
    try:
        start_server()
    except KeyboardInterrupt:
        print("服务器已手动关闭")
    except Exception as e:
        print(f"服务器启动失败: {str(e)}")
