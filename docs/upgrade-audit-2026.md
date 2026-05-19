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

## 初步检查清单

### 1. 仓库结构

- [ ] 检查 `README.md` 是否仍能指导用户完成快速开始
- [ ] 检查 `backend/` 是否能按当前说明启动
- [ ] 检查 `frontend/` 是否能按当前说明启动
- [ ] 检查 `docs/` 内容是否与实际代码一致
- [ ] 检查 `notebooks/` 是否能从头运行
- [ ] 检查 `tutorials/` 是否存在过时 API、链接或命令

### 2. 环境版本

待确认：

- [ ] Python 推荐版本
- [ ] Node.js 推荐版本
- [ ] 包管理器版本，例如 pip / uv / conda / npm / pnpm
- [ ] 操作系统差异，例如 macOS / Linux / Windows

### 3. 后端依赖

待检查：

- [ ] `backend/requirements.txt`
- [ ] FastAPI / Uvicorn 相关版本
- [ ] LlamaIndex 相关 API 是否有 breaking change
- [ ] OpenAI / DashScope / ZhipuAI 等模型 SDK 是否有接口变化
- [ ] `.env` 或配置文件是否缺少示例

### 4. 前端依赖

待检查：

- [ ] `frontend/package.json`
- [ ] 启动命令是否仍有效
- [ ] API base URL 配置是否清晰
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

3. `fix/backend-deps`
   - 修复后端依赖和启动问题
   - 必要时锁定可运行版本

4. `fix/frontend-deps`
   - 修复前端依赖和启动问题
   - 补充前端启动说明

5. `docs/update-tutorials`
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
- `fix/backend-deps`：修复后端依赖与启动问题
- `fix/frontend-deps`：修复前端依赖与启动问题
- `docs/update-tutorials`：更新教程正文和截图/命令

## 验收标准

第一阶段完成时，至少应产出：

1. 一份可复现的运行盘点文档
2. 明确列出当前不能跑的步骤和原因
3. 明确列出推荐的环境版本
4. 后续每个修复任务都能关联到具体问题点
```
