#!/bin/bash

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖项
pip install -r requirements.txt

# 运行应用程序
python app.py
