# config/prod.py
from .base import *  # 导入基础配置

# 生产环境特定配置
DEBUG = False  # 关闭调试模式
ENV = "生产环境"  # 设置为生产环境
LOG_LEVEL = "INFO"  # 设置日志级别为 INFO
# DATABASE_URI = "mysql+pymysql://user:password@host:port/dbname"  # 生产环境使用的数据库