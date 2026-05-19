# wow-rag 2026 更新 PR 计划

本文档用于记录当前 fork 中围绕 `wow-rag` 教程与运行环境更新拆分出的 PR，以及建议的 review / merge 顺序。

## 当前 PR 列表

| PR | 标题 | Base | 说明 | 建议状态 |
| --- | --- | --- | --- | --- |
| #1 | `docs: add 2026 upgrade audit plan` | `main` | 新增 2026 更新盘点文档，作为后续工作的路线图入口。 | 可先 review / merge |
| #2 | `fix: load backend model config from env` | `main` | 移除后端硬编码 API Key / base URL，改为环境变量配置。 | 后端修复基础 PR，建议优先 merge |
| #3 | `fix: make frontend API base URL configurable` | `main` | 前端 API 地址抽为可覆盖配置，默认保持本地 `127.0.0.1:5000`。 | 可独立 review / merge |
| #4 | `docs: clarify cross-platform quickstart` | `main` | 整理 README 快速开始，补充 Windows / macOS / Linux 说明。 | 可独立 review / merge |
| #5 | `docs: fix contributing links` | `main` | 修复 README 中空的 Issue / Discussion 链接。 | 可独立 review / merge |
| #6 | `fix: constrain backend dependency versions` | `main` | 为后端依赖增加版本范围，降低重新安装环境时的复现风险。 | 可独立 review / merge，但建议本地安装验证后再 merge |
| #7 | `refactor: initialize backend query engine explicitly` | `fix/backend-config-env` | 将 query engine 初始化从 import 阶段移到 FastAPI startup。 | 依赖 #2；先合 #2，再 retarget 到 `main` |
| #8 | `docs: note frontend CDN runtime requirements` | `main` | 说明当前前端依赖 CDN，离线或网络受限环境可能影响页面表现。 | 可独立 review / merge |

## 建议合并顺序

建议按以下顺序推进：

1. #1 — `docs: add 2026 upgrade audit plan`
2. #5 — `docs: fix contributing links`
3. #4 — `docs: clarify cross-platform quickstart`
4. #8 — `docs: note frontend CDN runtime requirements`
5. #3 — `fix: make frontend API base URL configurable`
6. #6 — `fix: constrain backend dependency versions`
7. #2 — `fix: load backend model config from env`
8. #7 — `refactor: initialize backend query engine explicitly`

## 依赖关系说明

### #7 依赖 #2

#7 是叠加在 #2 之上的后续重构：

- #2 先移除硬编码 API Key / base URL，并引入 `.env.example`。
- #7 再基于 #2 的环境变量配置，重构 query engine 初始化流程。

因此 #7 不应直接独立合入当前 `main`。推荐流程：

1. Review 并 merge #2。
2. 将 #7 的 base 从 `fix/backend-config-env` 改为 `main`。
3. 重新检查 diff，确认只剩初始化重构相关改动。
4. 完成 backend startup 验证后再 merge #7。

## 验证建议

在正式 merge runtime 相关 PR 前，建议至少完成以下验证：

### 后端依赖验证

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows 使用 .venv\\Scripts\\activate
pip install -r requirements.txt
```

### 后端启动验证

```bash
cp .env.example .env
# 填入自己的 WOWRAG_API_KEY
python main.py
```

### 前端联调验证

```bash
cd frontend
python -m http.server 8080 --bind 0.0.0.0
```

然后访问：

```text
http://127.0.0.1:8080/chat.html
```

### 前端 CDN 验证

打开浏览器开发者工具，确认下列资源可以正常加载：

- Vue
- Tailwind
- Marked
- Font Awesome
- Google Fonts / 项目样式资源

如果处于离线或网络受限环境，需要预期页面样式、交互或 Markdown 渲染可能不完整。

## 后续工作建议

合并上述 PR 后，可以继续拆分以下任务：

- `docs/update-tutorials`：逐章更新教程、notebook、命令和截图。
- `test/backend-smoke-check`：增加最小后端 smoke test 或健康检查。
- `chore/dependency-lock`：在完成本地验证后考虑增加更严格的锁文件。
- `frontend/local-assets-or-build`：若需要离线或产品化部署，再考虑引入本地依赖管理或前端构建流程。
