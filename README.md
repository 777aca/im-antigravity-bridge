# IM Antigravity Bridge - 飞书机器人版

基于 FastAPI 和 Antigravity Python SDK 打造的飞书机器人代理网关。该服务通过飞书 Webhook 接收用户消息，调度智能 Agent 执行任务，并将结果回传至飞书。

## 核心特性

- **飞书原生接入**：支持飞书 URL Challenge 校验及 `im.message.receive_v1` 文本消息订阅。
- **智能调度**：集成 Antigravity SDK，支持上下文传递及工具调用。
- **开箱即用**：内置 Docker 容器化支持与 GitHub Actions CI 工作流。
- **自动化构建**：内置自动安装依赖及服务重启脚本。

## 快速开始

### 1. 准备工作
- Python 3.12+ 运行环境。
- 在 [飞书开发者后台](https://open.feishu.cn/) 创建应用，获取 `App ID` 与 `App Secret`，并开启机器人能力。

### 2. 环境变量配置
在项目根目录创建或修改 `.env` 文件，填入飞书凭证：
```ini
FEISHU_APP_ID=你的APP_ID
FEISHU_APP_SECRET=你的APP_SECRET
# 下列配置按需使用
# FEISHU_VERIFICATION_TOKEN=your_token
# FEISHU_ENCRYPT_KEY=your_key
```

### 3. 本地运行
使用提供的 Node 脚本启动服务（脚本会自动处理 Python 依赖并调用 Uvicorn）：
```bash
node scripts/start.js
```
服务将在 `http://0.0.0.0:8000` 启动。

> **测试提示**：本地调试请使用内网穿透工具（如 `localtunnel`），将映射后的公网地址（带 `/webhook` 后缀）填入飞书后台的“事件订阅”请求地址中。

---

## 生产部署 (Docker)

项目已提供 `Dockerfile` 及 `docker-compose.yml`，推荐使用 Docker 进行生产环境部署。

```bash
# 后台构建并运行
docker-compose up -d --build

# 查看运行日志
docker-compose logs -f
```

## GitHub CI 集成

项目包含 `.github/workflows/docker-build.yml`。当你向 `main` 分支提交代码或发起 PR 时，GitHub Actions 将自动执行 Docker 镜像构建测试，确保环境一致性。
