# 后端 Smoke Check

本文档用于快速验证后端依赖安装、环境变量配置和 FastAPI 服务启动是否正常。

> 本检查依赖后端环境变量配置和显式 query engine 初始化改造。建议在合并相关后端 PR 后执行。

## 1. 创建并激活虚拟环境

在项目根目录执行：

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows 可使用：

```bat
.venv\Scripts\activate.bat
```

## 2. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

## 3. 配置环境变量

```bash
cp .env.example .env
```

然后编辑 `backend/.env`，至少填入：

```text
WOWRAG_API_KEY=your_api_key_here
```

如需使用其他 OpenAI 兼容服务，可继续配置：

```text
WOWRAG_BASE_URL=https://open.bigmodel.cn/api/paas/v4
WOWRAG_CHAT_MODEL=glm-4-flash
WOWRAG_EMBED_MODEL=embedding-3
```

## 4. 启动后端服务

确保当前目录为 `backend`，执行：

```bash
python main.py
```

服务默认监听：

```text
http://127.0.0.1:5000
```

## 5. 检查健康状态

打开另一个终端，执行：

```bash
curl http://127.0.0.1:5000/health
```

期望返回类似：

```json
{
  "status": "ok",
  "query_engine_ready": true
}
```

如果返回 `query_engine_ready: false` 或请求失败，请优先检查：

- `backend/.env` 是否存在
- `WOWRAG_API_KEY` 是否已填写
- `WOWRAG_BASE_URL` 是否可访问
- `WOWRAG_DOCS_PATH` 指向的文件是否存在
- 依赖是否安装成功

## 6. 检查流式问答接口

```bash
curl "http://127.0.0.1:5000/stream_chat?param=你好"
```

如果接口能够持续返回文本，说明后端最小链路已经跑通。
