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
import logging
from os import listdir, path, makedirs
from urllib.parse import unquote
from webbrowser import open as op
from settings import port, xs_dir, LOG_FILE_DIR, LOG_FILE_NAME, LOG_LEVEL
from http.server import HTTPServer, BaseHTTPRequestHandler
from __init__ import generate_html, novel_chapterizer, extract_txt_from_zip


# 设置日志
log_dir = LOG_FILE_DIR
if not path.exists(log_dir):
    makedirs(log_dir)  # 如果日志目录不存在，创建它

log_file = str(path.join(log_dir, LOG_FILE_NAME))  # 日志文件名
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)  # 设置日志级别

# 创建文件处理器，将日志写入文件
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter("%(message)s"))

# 创建流处理器，将日志输出到控制台
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(message)s"))

# 将处理器添加到日志器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

if not path.exists(xs_dir):
    makedirs(xs_dir)  # 如果小说目录不存在，创建它

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # 自定义日志格式，记录到文件中
        logging.info(f"{self.client_address[0]} - - [{self.log_date_time_string()}] {format % args}")

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if self.path == "/":
                html_content = generate_html()
                self.wfile.write(html_content.encode('utf-8'))
                # logging.info(f"请求主页成功: {self.path}")
            elif self.path == "/style.css":  # 处理外部CSS请求
                with open(".\\css\\style.css", "rb") as css_file:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/css')
                    self.end_headers()
                    self.wfile.write(css_file.read())
                    # logging.info(f"请求CSS文件成功: {self.path}")
            else:
                for filename in listdir(xs_dir):
                    if filename.endswith('.zip') and unquote(self.path).split("/")[1] in filename:#:
                        txt_content = extract_txt_from_zip(xs_dir + "/" + filename)
                        if txt_content:
                            chapters = novel_chapterizer(txt_content)
                            html_content = generate_html(chapters, self.path)
                            self.wfile.write(html_content.encode('utf-8'))
                            # logging.info(f"请求小说内容成功: {self.path}")
                            break
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"404 Not Found")
                    # logging.warning(f"请求未找到: {self.path}")
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"500 Internal Server Error")
            # logging.error(f"请求处理失败: {self.path} - {str(e)}")


def main():
    server_address = ('', port)
    true_address = f"http://127.0.0.1{'' if port == 80 else ':' + str(server_address[1])}"
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    # print(f"正在启动服务器，地址为 {true_address} ……")
    logging.info(f"服务器启动成功，地址为 {true_address}")
    op(true_address)
    httpd.serve_forever()

if __name__ == '__main__':
    main()
