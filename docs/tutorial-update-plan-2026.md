# wow-rag 教程更新计划（2026）

本文档用于记录教程、Notebook、示例数据和 README 描述之间的对应关系，并作为后续逐章更新教程的任务清单。

> 本 PR 只做教程更新前的文件盘点和计划整理，不直接改动 Notebook 或运行代码。

## 当前已确认的教程相关文件

| 文件 | 当前用途 | 初步问题 |
| --- | --- | --- |
| `README.md` | 项目入口、快速体验、课程章节列表 | “项目附属文件”中写的是 `learn.ipynb`，但实际文件位于 `backend/learn.ipynb`；课程章节只有标题，没有指向具体教程文件。 |
| `backend/learn.ipynb` | README 中提到的“所有运行代码”Notebook | Notebook 包含已执行输出和历史环境信息，后续需要确认是否能从空环境顺序运行。 |
| `docs/问答手册.txt` | 后端默认读取的示例文档 | 文件存在，但内容与“问答手册”名称不完全一致，后续需要确认是否仍适合作为 RAG 快速体验数据。 |
| `backend/base.py` | README 中提到可替换 LlamaIndex OpenAI embedding 源码的辅助文件 | 这种“替换 site-packages 源码”的方式维护风险较高，后续教程应尽量改为配置化或自定义 embedding 类。 |
| `frontend/chat.html` | 静态前端体验页面 | 依赖 CDN，适合快速体验；离线或产品化部署需要另行处理。 |

## README 与实际文件路径不一致

README 当前写法：

```text
learn.ipynb 本项目的所有运行代码。
```

实际文件路径：

```text
backend/learn.ipynb
```

建议后续在 README 中改为：

```text
backend/learn.ipynb 是本项目的示例运行代码 Notebook。
```

## 教程章节映射待补充

README 当前列出课程内容：

1. 第1课：手搓一个土得掉渣的RAG
2. 第2课：正式上路搞定模型
3. 第3课：初步体验问答引擎
4. 第4课：最脏最累的文档管理
5. 第5课：流式部署

但当前 README 没有说明每一课对应的文件、Notebook cell 范围或文档入口。建议后续补充一张章节映射表：

| 课程 | 建议补充内容 |
| --- | --- |
| 第1课 | 对应 Notebook cell 范围、示例文档、最小 RAG 流程说明 |
| 第2课 | 模型 API 配置、环境变量、OpenAI 兼容服务说明 |
| 第3课 | Query engine 构建方式、retriever / synthesizer 关系 |
| 第4课 | 文档加载、切分、索引、Qdrant 本地存储说明 |
| 第5课 | FastAPI 流式接口、前端 chat.html 联调、浏览器访问说明 |

## 后续建议拆分

### 1. `docs/fix-notebook-path`

目标：只修 README 中 `learn.ipynb` 的路径描述。

建议改动：

- 将 `learn.ipynb` 改为 `backend/learn.ipynb`。
- 简要说明 Notebook 适合学习运行，不等同于生产启动入口。

### 2. `docs/add-lesson-file-map`

目标：增加课程章节和文件入口映射。

建议改动：

- 在 README 的“课程内容”后增加“学习文件入口”。
- 标注每一课建议先看哪些文件。

### 3. `docs/review-learn-notebook`

目标：检查 `backend/learn.ipynb` 是否仍能从头运行。

建议检查：

- 是否包含过时的输出。
- 是否依赖已经废弃的 LlamaIndex API。
- 是否仍要求手动替换 `site-packages` 源码。
- 是否需要拆成更小的 lesson notebooks。

### 4. `docs/refresh-sample-data`

目标：确认 `docs/问答手册.txt` 是否适合作为快速体验示例数据。

建议检查：

- 文件内容是否与“问答手册”名称匹配。
- 是否应该替换为更清晰的中文问答型示例文档。
- 是否需要新增数据来源说明。

### 5. `docs/remove-site-packages-patch-guide`

目标：替换“手动修改 LlamaIndex 源码”的教程路径。

建议方向：

- 优先使用自定义 embedding 类或环境变量配置。
- 将 `backend/base.py` 降级为历史兼容说明，避免推荐新用户复制覆盖依赖源码。

## 验证建议

后续真正更新教程时，应至少完成：

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

并验证：

```bash
curl http://127.0.0.1:5000/health
curl "http://127.0.0.1:5000/stream_chat?param=你好"
```

前端验证：

```bash
cd frontend
python -m http.server 8080 --bind 0.0.0.0
```

浏览器访问：

```text
http://127.0.0.1:8080/chat.html
```
