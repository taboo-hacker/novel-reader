# config/test.py
from .base import *  # 导入基础配置

# 测试环境特定配置
DEBUG = True  # 开启调试模式
ENV = "测试环境"  # 设置为测试环境
LOG_LEVEL = "DEBUG"  # 设置日志级别为 DEBUG
# DATABASE_URI = "sqlite:///:memory:"  # 测试环境使用内存数据库