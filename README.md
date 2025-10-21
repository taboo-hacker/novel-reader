<div align="center">
  <h1>小说阅读器</h1>
  <p>一个轻量级的本地小说阅读器 Web 应用，基于 Python 标准库实现，无需额外依赖，支持自动解析 ZIP 压缩包中的飞卢小说文本，提供智能分章处理和响应式 Web 阅读界面，适配多种设备。</p>
</div>

![Python](https://img.shields.io/badge/Python-3.13+-blue)
![License](https://img.shields.io/badge/License-MIT-green)



## 📦 项目结构

```
novel-reader/
├── xs/                  # 存放小说 ZIP 文件的目录
├── css/                 # 样式表文件目录
│   └── style.css        # 样式表文件
├── main.py              # 主程序入口
├── novel.py             # 小说章节解析器
├── zip.py               # ZIP 文件处理器
├── html.py              # HTML 生成器
├── settings.py          # 配置文件
└── __init__.py          # 模块导出文件
```

## 🛠️ 技术栈

- **后端**：Python 3.7+（仅使用标准库 `http.server`）
- **前端**：纯 HTML5 + CSS3
- **文件处理**：`zipfile` 标准库

## 🚀 安装与使用

### 前置要求

- Python 3.7+
- 飞卢小说 ZIP 文件（需放在项目目录的 `xs/` 文件夹下）

### 快速启动

1. **克隆仓库**：

   ```bash
   git clone https://github.com/taboo-hacker/novel-reader.git
   cd novel-reader
   ```

2. **放入小说文件**：

   将飞卢小说 ZIP 文件放入 `xs/` 目录，文件名格式应为小说名.zip。

3. **启动服务**：

   ```bash
   python main.py
   ```

4. **浏览器访问**：

   打开浏览器，访问 [http://localhost:8080](http://localhost:8080) 即可开始阅读。

## ⚡ 功能特性

- **自动分章**：智能识别小说章节结构，自动将小说内容分章展示。
- **即点即读**：点击章节名称即可立即阅读对应章节内容。
- **日志记录**：完整记录访问日志，方便开发者调试和用户了解访问情况。
- **跨平台**：支持 Windows/Linux/macOS 等主流操作系统，无需额外配置。
- **无数据库**：纯文件系统存储，无需依赖数据库，简化了部署和维护过程。

## 📝 配置选项

通过修改 `settings.py` 文件，可以自定义以下配置：

- **服务端口**：`port`，默认为 8080。
- **小说存储目录**：`xs_dir`，默认为 `./xs`。
- **支持的小说平台**：`target`，目前仅支持“飞卢小说”。
- **支持的文件格式**：`endswith`，默认为 `.zip`。

## 📜 开源协议

本项目根据 [GNU General Public License v3.0](LICENSE) 授权。详情请参阅 [LICENSE](LICENSE) 文件。

## 📞 联系方式

如有任何问题或建议，欢迎通过以下方式联系我们：

- 邮箱：leo43991314520@outlook.com
- GitHub：[@taboo-hacker](https://github.com/taboo-hacker)
