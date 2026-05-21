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
| #9 | `test: add backend smoke check` | `refactor/backend-engine-init` | 增加 `/health` 健康检查接口和后端 smoke check 文档。 | 依赖 #2 和 #7；先合前置 PR，再 retarget 到 `main` |
| #10 | `docs: add tutorial update plan` | `main` | 新增教程更新计划，梳理 README、Notebook、示例数据和后续教程任务。 | 可独立 review / merge |
| #11 | `docs: fix notebook path in README` | `main` | 修正 README 中 Notebook 路径，将 `learn.ipynb` 明确为 `backend/learn.ipynb`。 | 可独立 review / merge |

## 建议合并顺序

建议按以下顺序推进：

1. #1 — `docs: add 2026 upgrade audit plan`
2. #5 — `docs: fix contributing links`
3. #4 — `docs: clarify cross-platform quickstart`
4. #8 — `docs: note frontend CDN runtime requirements`
5. #10 — `docs: add tutorial update plan`
6. #11 — `docs: fix notebook path in README`
7. #3 — `fix: make frontend API base URL configurable`
8. #6 — `fix: constrain backend dependency versions`
9. #2 — `fix: load backend model config from env`
10. #7 — `refactor: initialize backend query engine explicitly`
11. #9 — `test: add backend smoke check`

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

### #9 依赖 #7，且间接依赖 #2

#9 增加后端 smoke check，依赖 #7 中的显式 query engine 初始化：

- #2 提供环境变量配置基础。
- #7 提供可检测的 query engine 初始化状态。
- #9 在此基础上增加 `/health` 接口和 smoke check 文档。

推荐流程：

1. Review 并 merge #2。
2. Retarget #7 到 `main`，review 并 merge #7。
3. Retarget #9 到 `main`。
4. 运行 `docs/backend-smoke-check.md` 中的验证流程。
5. 验证通过后再 merge #9。

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

### 后端 Smoke Check

在后端启动后，打开另一个终端执行：

```bash
curl http://127.0.0.1:5000/health
```

期望返回：

```json
{
  "status": "ok",
  "query_engine_ready": true
}
```

然后验证流式接口：

```bash
curl "http://127.0.0.1:5000/stream_chat?param=你好"
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

### 教程与 Notebook 验证

围绕 #10 / #11 后续拆分任务，建议验证：

- README 中提到的 `learn.ipynb` 是否已明确为 `backend/learn.ipynb`。
- `backend/learn.ipynb` 是否能在干净环境中从头运行。
- `docs/问答手册.txt` 是否仍适合作为快速体验示例数据。
- `backend/base.py` 中“替换 site-packages 源码”的做法是否需要改写为历史兼容说明。

## 后续工作建议

合并上述 PR 后，可以继续拆分以下任务：

- `docs/add-lesson-file-map`：增加课程章节和文件入口映射。
- `docs/review-learn-notebook`：检查并更新 `backend/learn.ipynb`。
- `docs/refresh-sample-data`：确认或替换 `docs/问答手册.txt` 示例数据。
- `chore/dependency-lock`：在完成本地验证后考虑增加更严格的锁文件。
- `frontend/local-assets-or-build`：若需要离线或产品化部署，再考虑引入本地依赖管理或前端构建流程。
