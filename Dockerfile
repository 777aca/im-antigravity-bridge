FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（如果某些 Python 包需要编译）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 优先复制依赖文件，利用 Docker 缓存层
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.org/simple

# 复制全部项目代码
COPY . .

# 暴露端口
EXPOSE 8000

# 直接启动 uvicorn 服务
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
