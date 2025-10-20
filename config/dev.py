# config/dev.py
from .base import *  # 导入基础配置

# 开发环境特定配置
DEBUG = True  # 开启调试模式
ENV = "开发环境"  # 设置为开发环境
LOG_LEVEL = "DEBUG"  # 设置日志级别为 DEBUG
# DATABASE_URI = "sqlite:///dev_example.db"  # 开发环境使用的数据库
