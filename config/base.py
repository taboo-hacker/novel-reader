# config/base.py

# 基础配置
DEBUG = False  # 默认关闭调试模式
ENV = "production"  # 默认环境为生产环境
# DATABASE_URI = "sqlite:///example.db"  # 默认数据库连接字符串
# API_KEY = "default_api_key"  # 默认的 API 密钥
# API_URL = "https://api.example.com"  # 默认的 API 服务地址
LOG_FILE_DIR = "logs"  # 默认的日志文件路径
LOG_FILE_NAME = "server.log"  # 默认的日志文件名称
LOG_LEVEL = "INFO"  # 默认的日志级别
# SECRET_KEY = "default_secret_key"  # 默认的密钥
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]  # 默认允许访问的主机列表
ALLOWED_PORTS = [8080]  # 默认允许访问的主机列表