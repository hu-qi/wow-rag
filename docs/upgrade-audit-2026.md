# wow-rag 教程与运行环境更新盘点（2026）

## 背景

`wow-rag` 原教程和依赖环境已有一段时间，部分内容、依赖版本、启动方式和运行说明可能已经过时。为了重新捡起这个项目，先做一次系统性盘点，再根据问题拆分小 PR 更新教程、依赖和运行说明。

本分支用于第一阶段 audit，不直接改 `main`。

- 上游仓库：`datawhalechina/wow-rag`
- fork 仓库：`hu-qi/wow-rag`
- 当前工作分支：`chore/audit-2026`
- 分支基线：上游 `datawhalechina/wow-rag:main` 的干净基线

> 注意：fork 的 `main` 当前不作为工作基线，后续改动应从上游干净基线创建分支，避免把 fork main 中的额外历史带入。

## 目标

- 跑通当前 README 的快速开始流程
- 盘点 backend / frontend / docs / notebooks / tutorials 的过时内容
- 明确 Python、Node、依赖包和模型接入方式的可运行版本
- 修复启动、依赖、配置和教程中的不一致问题
- 整理可验证的新版教程与运行说明
- 稳定后按主题拆分 PR 贡献回上游

## 第一轮静态盘点结论

> 本节基于仓库文件静态阅读，尚未完成本地端到端运行复现。

### P0：后端存在硬编码 API Key 和固定公网 base URL

- 位置：`backend/engine.py`
- 现状：代码中直接写入 `api_key`、`base_url`、`chat_model`、`emb_model`，并且 `dotenv` 相关代码被注释。
- 影响：
  - 不利于公开仓库维护，存在密钥泄露风险。
  - 用户无法通过 `.env` 或环境变量切换自己的模型服务。
  - 教程复现依赖某个固定公网服务，稳定性和可持续性较弱。
- 建议：
  - 新增 `.env.example`。
  - 使用 `python-dotenv` 加载 `WOWRAG_API_KEY`、`WOWRAG_BASE_URL`、`WOWRAG_CHAT_MODEL`、`WOWRAG_EMBED_MODEL`。
  - README 中补充配置说明。
- 建议后续分支：`fix/backend-config-env`

### P0：依赖未锁版本，长期复现风险较高

- 位置：`backend/requirements.txt`
- 现状：依赖列表没有版本约束，例如 `openai`、`pydantic`、`llama-index-core`、`qdrant-client`、`fastapi`、`uvicorn` 等均未 pin 版本。
- 影响：
  - 2026 年重新安装时会默认安装最新版本，可能与教程编写时的 API 不兼容。
  - LlamaIndex、OpenAI SDK、Pydantic 都属于历史上发生过 breaking change 的依赖，复现风险较高。
- 建议：
  - 先本地复现当前未锁版本是否可运行。
  - 若不可运行，记录失败版本组合。
  - 产出一组推荐可运行版本，必要时拆分 `requirements.in` / `requirements.txt` 或增加 `uv.lock`。
- 建议后续分支：`fix/backend-deps`

### P1：README 快速开始偏 Windows，跨平台说明不足

- 位置：`README.md`
- 现状：快速开始中只给出 Windows 虚拟环境激活命令：`.\\rag-venv\\Scripts\\activate`。
- 影响：
  - macOS / Linux 用户需要自行推断激活命令。
  - README 待做清单中也提到“在Linux云电脑跑本教程的说明”，说明跨平台部署文档尚未完成。
- 建议：
  - README 增加 macOS / Linux 激活命令：`source rag-venv/bin/activate`。
  - 明确 Python 推荐版本，例如先以 `Python 3.10` 或本地验证后的版本为准。
  - 补充 Windows PowerShell、CMD、macOS/Linux 三种常见环境说明。
- 建议后续分支：`docs/update-quickstart`

### P1：前端 API 地址硬编码为本机 5000 端口

- 位置：`frontend/chat.html`
- 现状：前端请求地址写死为 `http://127.0.0.1:5000/stream_chat`。
- 影响：
  - 本地体验可以工作，但远程服务器、Docker、Codespaces、云电脑等场景需要手动改源码。
  - README 中没有说明如何修改 API base URL。
- 建议：
  - 短期在 README 中明确说明后端必须运行在 `127.0.0.1:5000`。
  - 中期给 `chat.html` 增加可配置 `API_BASE_URL` 常量。
  - 云部署场景单独说明 CORS、监听地址、浏览器访问地址。
- 建议后续分支：`fix/frontend-api-config`

### P1：README 中 Issue / Discussion 链接为空

- 位置：`README.md`
- 现状：参与贡献部分写了 `[Issue]()`、`[Discussion]()` 空链接。
- 影响：
  - 用户无法直接点击反馈问题或参与讨论。
  - 对开源协作不友好。
- 建议：
  - 将 Issue 链接补为 `https://github.com/datawhalechina/wow-rag/issues`。
  - 若未开启 Discussions，则删除 Discussion 链接或改为有效渠道。
- 建议后续分支：`docs/update-contributing-links`

### P1：后端启动时会在 import 阶段直接构建索引和请求 embedding

- 位置：`backend/main.py`、`backend/engine.py`
- 现状：`main.py` import `query_engine` 后，`engine.py` 会立即读取文档、连接 Qdrant、构建索引，并调用 embedding 获取维度。
- 影响：
  - `python main.py` 启动阶段就依赖模型服务和文档路径。
  - 用户配置错误时服务可能直接启动失败，错误定位不够清晰。
  - 后续增加测试或健康检查会比较困难。
- 建议：
  - 将 engine 初始化封装为显式函数，例如 `create_query_engine()`。
  - 增加配置检查和更友好的错误提示。
  - 后续再考虑缓存索引或延迟初始化。
- 建议后续分支：`refactor/backend-engine-init`

### P2：前端依赖全部来自 CDN，离线或网络受限环境复现风险较高

- 位置：`frontend/chat.html`
- 现状：Vue、Tailwind、Marked、字体和样式依赖均从 CDN 加载。
- 影响：
  - 快速体验简单，但网络受限环境可能无法打开或样式异常。
  - 不需要立即引入构建系统，但 README 应说明需要联网加载前端资源。
- 建议：
  - README 中说明前端页面依赖 CDN。
  - 若后续要做稳定产品化，再考虑引入 Vite / package.json。
- 建议后续分支：`docs/frontend-runtime-notes`

## 初步检查清单

### 1. 仓库结构

- [x] 检查 `README.md` 是否仍能指导用户完成快速开始
- [x] 检查 `backend/` 是否能按当前说明启动（静态检查完成，尚未本地运行）
- [x] 检查 `frontend/` 是否能按当前说明启动（静态检查完成，尚未浏览器验证）
- [ ] 检查 `docs/` 内容是否与实际代码一致
- [ ] 检查 `notebooks/` 是否能从头运行
- [ ] 检查 `tutorials/` 是否存在过时 API、链接或命令

### 2. 环境版本

待确认：

- [ ] Python 推荐版本
- [ ] Node.js 推荐版本（当前前端暂未发现 package.json，可能不需要 Node）
- [ ] 包管理器版本，例如 pip / uv / conda / npm / pnpm
- [ ] 操作系统差异，例如 macOS / Linux / Windows

### 3. 后端依赖

已发现：

- [x] `backend/requirements.txt` 未锁版本
- [x] `.env` 或配置文件缺少示例，且 `engine.py` 存在硬编码 API Key / base URL

待检查：

- [ ] FastAPI / Uvicorn 相关版本
- [ ] LlamaIndex 相关 API 是否有 breaking change
- [ ] OpenAI / DashScope / ZhipuAI 等模型 SDK 是否有接口变化

### 4. 前端依赖

已发现：

- [x] `frontend/chat.html` 写死 `http://127.0.0.1:5000/stream_chat`
- [x] 前端依赖 CDN，README 未明确说明

待检查：

- [ ] 是否确实不存在 `frontend/package.json`
- [ ] 启动命令是否仍有效
- [ ] README 中是否说明前后端联调方式

### 5. 教程内容

待检查：

- [ ] 教程章节顺序是否合理
- [ ] Notebook 是否能独立运行
- [ ] 教程中的依赖安装命令是否过时
- [ ] 教程中的模型 API 示例是否仍可用
- [ ] 截图、路径、命令是否与当前代码一致

## 建议 PR 拆分

后续建议不要把所有更新放在一个大 PR 中，而是按主题拆分：

1. `chore/audit-2026`
   - 只提交本盘点文档和复现记录
   - 不做大规模代码改动

2. `docs/update-quickstart`
   - 更新 README 快速开始
   - 明确环境、依赖、启动命令

3. `fix/backend-config-env`
   - 移除硬编码 API Key / base URL
   - 增加 `.env.example`
   - README 补充模型服务配置说明

4. `fix/backend-deps`
   - 修复后端依赖和启动问题
   - 必要时锁定可运行版本

5. `fix/frontend-api-config`
   - 说明或配置前端 API 地址
   - 补充前后端联调说明

6. `docs/update-tutorials`
   - 更新教程正文、notebook、路径、命令和截图

## 复现记录模板

后续本地复现时，可按以下格式记录问题：

```md
### 问题标题

- 位置：`path/to/file`
- 复现命令：
  ```bash
  command here
  ```
- 期望结果：
- 实际结果：
- 错误信息：
- 初步判断：
- 建议修复：
```

## 上游 issue 建议标题

```text
[Roadmap] 更新 wow-rag 教程与运行环境
```

## 上游 issue 建议正文

```md
## 背景

`wow-rag` 原教程和依赖环境已有一段时间，部分内容、依赖版本、启动方式和运行说明可能已经过时。准备重新捡起这个项目，先做一次系统性盘点，再根据问题拆分小 PR 更新教程、依赖和运行说明。

当前计划先在 fork 仓库中创建工作分支推进：

- fork: `hu-qi/wow-rag`
- branch: `chore/audit-2026`

> 说明：fork 的 `main` 目前不作为工作基线，后续改动会从上游 `datawhalechina/wow-rag:main` 的干净基线创建分支，避免把 fork main 中的额外历史带入。

## 目标

- 跑通当前 README 的快速开始流程
- 盘点 backend / frontend / docs / notebooks / tutorials 的过时内容
- 明确 Python、Node、依赖包和模型接入方式的可运行版本
- 修复启动、依赖、配置和教程中的不一致问题
- 整理可验证的新版教程与运行说明
- 稳定后按主题拆分 PR 贡献回上游

## 初步任务

- [ ] 确认上游 `datawhalechina/wow-rag:main` 最新基线
- [ ] 从上游干净基线创建 fork 工作分支，不直接改 fork 的 `main`
- [ ] 本地复现当前 README 快速开始流程
- [ ] 记录无法运行、依赖冲突、API 过时等问题
- [ ] 检查 backend 依赖和启动流程
- [ ] 检查 frontend 依赖和启动流程
- [ ] 检查 notebooks 是否仍可按教程运行
- [ ] 检查 tutorials 与实际代码是否一致
- [ ] 输出一份 upgrade audit 文档，作为后续拆分 PR 的依据

## 建议分支 / PR 拆分

- `chore/audit-2026`：只做运行盘点和升级清单
- `docs/update-quickstart`：更新 README 快速开始
- `fix/backend-config-env`：移除硬编码配置，增加 `.env.example`
- `fix/backend-deps`：修复后端依赖与启动问题
- `fix/frontend-api-config`：说明或配置前端 API 地址
- `docs/update-tutorials`：更新教程正文和截图/命令

## 验收标准

第一阶段完成时，至少应产出：

1. 一份可复现的运行盘点文档
2. 明确列出当前不能跑的步骤和原因
3. 明确列出推荐的环境版本
4. 后续每个修复任务都能关联到具体问题点
```
