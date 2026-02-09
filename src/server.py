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
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
from webbrowser import open as op

from src.config import PORT, XS_DIR, STATIC_DIR, LOGS_DIR, LOG_FILE_NAME, LOG_LEVEL, ENDSWITH
from src.parsers.zip_parser import extract_txt_from_zip
from src.parsers.novel_parser import novel_chapterizer
from src.generators.html_generator import generate_html
from src.utils.helpers import safe_join, validate_path, validate_novel_name, cached_function

# 配置日志
log_file = os.path.join(LOGS_DIR, LOG_FILE_NAME)
logger = logging.getLogger()
logger.setLevel(getattr(logging, LOG_LEVEL))

# 创建文件处理器，将日志写入文件
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# 创建流处理器，将日志输出到控制台
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# 将处理器添加到日志器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 缓存装饰器，用于缓存小说解析结果
@cached_function(maxsize=32)
def extract_and_parse_novel(zip_path: str):
    """
    提取并解析小说内容，使用缓存提高性能
    
    Args:
        zip_path: ZIP文件路径
        
    Returns:
        解析后的章节列表
    """
    txt_content = extract_txt_from_zip(zip_path)
    if txt_content:
        return novel_chapterizer(txt_content)
    return []

class NovelHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    小说阅读器的HTTP请求处理器
    """
    
    def log_message(self, format, *args):
        """
        自定义日志格式，记录到文件中
        """
        logging.info(f"{self.client_address[0]} - - [{self.log_date_time_string()}] {format % args}")
    
    def do_GET(self):
        """
        处理GET请求
        """
        try:
            # 处理静态文件请求
            if self.path.startswith('/static/'):
                self._handle_static_file()
                return
            
            # 处理根路径请求
            if self.path == "/":
                self._handle_root()
                return
            
            # 处理小说和章节请求
            self._handle_novel_request()
            
        except Exception as e:
            logging.error(f"请求处理时出错: {str(e)}")
            self._send_error(500, "Internal Server Error")
    
    def _handle_static_file(self):
        """
        处理静态文件请求
        """
        try:
            # 获取静态文件路径
            static_file_path = self.path[len('/static/'):]
            
            # 验证路径安全性
            if not validate_path(static_file_path):
                self._send_error(403, "Forbidden")
                return
            
            # 构建完整文件路径
            file_path = safe_join(STATIC_DIR, static_file_path)
            
            if not file_path or not os.path.exists(file_path):
                self._send_error(404, "Not Found")
                return
            
            # 确定文件MIME类型
            content_type = self._get_content_type(file_path)
            
            # 发送文件
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
            
            logging.info(f"成功返回静态文件: {self.path}")
            
        except Exception as e:
            logging.error(f"处理静态文件时出错: {str(e)}")
            self._send_error(500, "Internal Server Error")
    
    def _handle_root(self):
        """
        处理根路径请求，返回小说列表
        """
        try:
            html_content = generate_html()
            self._send_html(html_content)
            logging.info("成功返回小说列表页面")
            
        except Exception as e:
            logging.error(f"处理根路径时出错: {str(e)}")
            self._send_error(500, "Internal Server Error")
    
    def _handle_novel_request(self):
        """
        处理小说和章节请求
        """
        try:
            # 解析路径
            path_parts = unquote(self.path).strip('/').split('/')
            
            if not path_parts or not path_parts[0]:
                self._handle_root()
                return
            
            novel_name = path_parts[0]
            
            # 验证小说名称
            if not validate_novel_name(novel_name):
                self._send_error(400, "Invalid Novel Name")
                return
            
            # 查找对应的ZIP文件
            zip_file = None
            if os.path.exists(XS_DIR):
                for filename in os.listdir(XS_DIR):
                    if filename.endswith(ENDSWITH) and novel_name in filename:
                        zip_file = os.path.join(XS_DIR, filename)
                        break
            
            if not zip_file:
                self._send_error(404, "Novel Not Found")
                return
            
            # 提取并解析小说内容
            chapters = extract_and_parse_novel(zip_file)
            
            if not chapters:
                self._send_error(404, "No Chapters Found")
                return
            
            # 处理章节请求
            if len(path_parts) > 1:
                # 章节详情页面
                html_content = generate_html(chapters, self.path)
            else:
                # 章节列表页面
                html_content = generate_html(chapters, self.path)
            
            self._send_html(html_content)
            logging.info(f"成功返回小说内容: {self.path}")
            
        except Exception as e:
            logging.error(f"处理小说请求时出错: {str(e)}")
            self._send_error(500, "Internal Server Error")
    
    def _send_html(self, html_content: str):
        """
        发送HTML内容
        
        Args:
            html_content: HTML内容
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def _send_error(self, status_code: int, message: str):
        """
        发送错误响应
        
        Args:
            status_code: HTTP状态码
            message: 错误消息
        """
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        error_html = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{status_code} - {message}</title>
            <link rel="stylesheet" href="/static/css/style.css">
        </head>
        <body>
            <div class="container">
                <h1>{status_code} - {message}</h1>
                <p>抱歉，请求处理时发生错误。</p>
                <a href="/">返回首页</a>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(error_html.encode('utf-8'))
    
    def _get_content_type(self, file_path: str):
        """
        根据文件扩展名获取内容类型
        
        Args:
            file_path: 文件路径
            
        Returns:
            内容类型字符串
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        content_types = {
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.html': 'text/html',
            '.txt': 'text/plain',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif'
        }
        
        return content_types.get(ext, 'application/octet-stream')

def start_server():
    """
    启动HTTP服务器
    """
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, NovelHTTPRequestHandler)
    
    server_url = f"http://127.0.0.1:{PORT}"
    logging.info(f"服务器启动成功，地址为: {server_url}")
    
    # 自动打开浏览器
    try:
        op(server_url)
        logging.info("已自动打开浏览器")
    except Exception as e:
        logging.warning(f"无法自动打开浏览器: {str(e)}")
    
    # 启动服务器
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("服务器正在关闭...")
        httpd.shutdown()
        logging.info("服务器已关闭")
