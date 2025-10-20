# config/__init__.py
import os
import sys
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取当前环境变量
env = os.getenv("ENV", "development").lower()  # 默认为开发环境

# 检测是否为包的一部分，并调整路径
if __package__ is None:
    # 如果不是包的一部分，则手动设置包路径
    dir_path = os.path.dirname(os.path.abspath(__file__))
    package_name = os.path.basename(dir_path)
    parent_dir = os.path.dirname(dir_path)
    sys.path.append(parent_dir)
    __package__ = f"{package_name}"

# 动态加载对应环境的配置
try:
    if env == "production":
        from .prod import *  # 加载生产环境配置
    elif env == "testing":
        from .test import *  # 加载测试环境配置
    else:
        from .dev import *  # 加载开发环境配置
except ImportError as e:
    raise ImportError(f"Failed to load configuration for environment '{env}': {e}")

# 明确指定需要暴露的变量
__all__ = ["ENV", "LOG_FILE_DIR", "LOG_FILE_NAME", "LOG_LEVEL"]