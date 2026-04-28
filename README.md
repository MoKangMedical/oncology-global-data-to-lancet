# Cancer Epidemiology Research To Lancet

**AI驱动的肿瘤学数据分析平台 — 从全球数据到Lancet论文**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 目录

- [项目简介](#项目简介)
- [核心功能](#核心功能)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [API 文档](#api-文档)
  - [系统接口](#系统接口)
  - [项目管理](#项目管理)
  - [数据管理](#数据管理)
  - [示例数据](#示例数据)
  - [统计分析](#统计分析)
  - [可视化](#可视化)
  - [论文生成](#论文生成)
  - [导出功能](#导出功能)
  - [元数据接口](#元数据接口)
  - [演示接口](#演示接口)
  - [数据模型](#数据模型)
  - [错误码说明](#错误码说明)
- [统计方法](#统计方法)
- [技术栈](#技术栈)
- [相关文档](#相关文档)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 项目简介

**Cancer Epidemiology Research To Lancet** 是一个端到端的癌症流行病学研究平台，集成数据整合、统计分析、可视化和论文生成功能。平台自动处理来自 GLOBOCAN、GBD、CI5 等权威数据库的癌症统计数据，执行 PAF、CDPAF、Joinpoint 趋势分析等高级统计计算，生成符合 *The Lancet* 期刊标准的图表和论文初稿。

### 设计理念

```
原始数据 -> 数据解析 -> 统计分析 -> 可视化生成 -> 论文撰写 -> 导出下载
```

---

## 核心功能

### 数据整合
- 支持 **GLOBOCAN** (全球癌症统计)、**GBD** (全球疾病负担)、**CI5** (五大洲癌症发病率) 三大权威数据库
- CSV / Excel 文件智能解析与列名标准化
- 支持中英文列名自动映射
- 内置 HCC (肝细胞癌) 示例数据集

### 统计分析
- **PAF** (Population Attributable Fraction) — 人群归因分数
- **CDPAF** (Correlation-Decomposed PAF) — 考虑因素相关性的调整PAF
- **Joinpoint 回归** — 时间趋势转折点识别
- **APC** (Annual Percentage Change) — 年度百分比变化
- **ASR** (Age-Standardized Rate) — 年龄标准化率
- 批量风险因素分析

### 可视化
- Lancet 风格配色方案的静态图表 (Matplotlib/Seaborn)
- 交互式图表 (Plotly)
- PAF 条形图、趋势线图、风险因素饼图
- 300 DPI 高质量学术图片输出

### 论文生成
- 符合 Lancet 投稿标准的论文结构 (Summary/Introduction/Methods/Results/Discussion)
- 自动生成摘要、方法学描述、结果陈述
- 支持 Markdown 和 HTML 导出
- Word (.docx) 导出 (需 python-docx)

### 导出服务
- 图表批量导出 (PNG/SVG)
- 论文多格式导出 (Markdown/HTML/Word)
- 一键打包下载 (ZIP)

---

## 快速开始

### 方式一：一键部署 (推荐)

```bash
# 克隆项目
git clone https://github.com/MoKangMedical/oncology-global-data-to-lancet.git
cd oncology-global-data-to-lancet

# 赋予执行权限并运行
chmod +x deploy.sh
./deploy.sh
```

脚本自动完成: Python 环境检查 -> 依赖安装 -> 目录创建 -> 服务启动

### 方式二：手动启动

```bash
# 1. 安装依赖 (使用清华镜像加速)
pip3.12 install --break-system-packages \
  -i https://pypi.tuna.tsinghua.edu.cn/simple \
  -r requirements.txt

# 2. 启动服务
python3.12 run.py
```

### 方式三：虚拟环境 (推荐开发)

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### 方式四：指定端口

```bash
PORT=9000 ./deploy.sh start
```

### 验证安装

```bash
# 健康检查
curl http://localhost:8002/health

# 预期响应:
# {"status": "healthy", "service": "oncology-to-lancet"}
```

### 访问地址

| 服务       | 地址                           |
|-----------|-------------------------------|
| 前端界面   | http://localhost:8002          |
| API 文档   | http://localhost:8002/api/docs |
| ReDoc 文档 | http://localhost:8002/api/redoc|
| 健康检查   | http://localhost:8002/health   |

---

## 项目结构

```
oncology-global-data-to-lancet/
├── deploy.sh                  # 一键部署脚本
├── run.py                     # Python 启动入口 (端口 8002)
├── requirements.txt           # Python 依赖
├── README.md                  # 项目文档 (本文件)
├── DEMO.md                    # 演示指南
├── USER_GUIDE.md              # 用户手册
├── DEPLOYMENT.md              # 部署指南
├── CHANGELOG.md               # 更新日志
├── CONTRIBUTING.md            # 贡献指南
├── LICENSE                    # MIT 许可证
│
├── app/                       # 应用核心
│   ├── __init__.py
│   ├── main.py                # FastAPI 主应用 (全部路由)
│   ├── core/                  # 核心模块
│   │   ├── statistics.py      # 统计引擎 (PAF/CDPAF/Joinpoint/ASR)
│   │   ├── data_parser.py     # 数据解析器 (CSV/Excel, 多源标准化)
│   │   ├── visualization.py   # 可视化生成 (Lancet 风格)
│   │   ├── paper_generator.py # 论文生成器 (Lancet 结构)
│   │   └── export_service.py  # 导出服务 (图表/论文/ZIP)
│   ├── data/
│   │   └── hcc_sample.py      # HCC 示例数据集
│   ├── models/
│   │   └── schemas.py         # Pydantic 数据模型
│   ├── templates/
│   │   └── index.html         # 单页前端 (Tailwind CSS)
│   └── static/                # 静态资源
│
├── output/                    # 输出目录 (自动生成)
│   ├── charts/                # 生成的图表 (PNG/SVG)
│   ├── papers/                # 生成的论文 (MD/HTML)
│   └── exports/               # 导出包 (ZIP)
│
└── scripts/                   # 辅助脚本
    ├── deploy.sh              # 旧版部署脚本
    └── analyze.py             # 分析辅助脚本
```

---

## API 文档

**基础信息**

| 项目         | 值                                      |
|-------------|----------------------------------------|
| Base URL    | `http://localhost:8002`                 |
| API 前缀     | `/api`                                  |
| 文档地址     | `http://localhost:8002/api/docs` (Swagger UI) |
| ReDoc       | `http://localhost:8002/api/redoc`        |
| Content-Type | `application/json`                      |
| 编码         | `UTF-8`                                 |

---

### 系统接口

#### `GET /`

首页，返回 Web 前端 HTML 页面。

- **响应**: `text/html` — 单页应用 (Tailwind CSS)

---

#### `GET /api`

API 根路径，返回服务信息。

- **响应示例**:
```json
{
  "name": "肿瘤学全球数据到柳叶刀",
  "version": "2.0.0",
  "description": "AI驱动的肿瘤学数据分析平台",
  "docs": "/api/docs"
}
```

---

#### `GET /health`

健康检查端点，用于监控和负载均衡器探活。

- **响应示例**:
```json
{
  "status": "healthy",
  "service": "oncology-to-lancet"
}
```

---

### 项目管理

#### `POST /api/projects`

创建新的研究项目。

- **请求体**:

| 字段           | 类型       | 必填 | 说明                                      |
|---------------|-----------|------|------------------------------------------|
| title         | string    | 是   | 项目标题                                  |
| cancer_types  | string[]  | 是   | 癌症类型 (liver/lung/breast/colorectal/stomach/prostate/thyroid/esophagus/pancreas/bladder) |
| countries     | string[]  | 是   | 目标国家/地区                              |
| time_range    | object    | 是   | 时间范围，含 start_year 和 end_year        |
| risk_factors  | string[]  | 否   | 风险因素 (smoking/alcohol/obesity/hepatitis_b/hepatitis_c/diabetes/hpv/h_pylori/air_pollution/physical_inactivity) |
| data_source   | string    | 否   | 数据源 (GLOBOCAN/GBD/CI5/SEER/CUSTOM)，默认 GLOBOCAN |
| description   | string    | 否   | 项目描述                                  |

- **请求示例**:
```json
{
  "title": "Global HCC Burden Analysis",
  "cancer_types": ["liver"],
  "countries": ["China", "Japan", "South Korea"],
  "time_range": {"start_year": 2000, "end_year": 2020},
  "risk_factors": ["hepatitis_b", "hepatitis_c", "alcohol"],
  "data_source": "GLOBOCAN",
  "description": "亚太地区肝癌负担分析"
}
```

- **响应示例**:
```json
{
  "id": "proj_20260428_090000",
  "title": "Global HCC Burden Analysis",
  "cancer_types": ["liver"],
  "countries": ["China", "Japan", "South Korea"],
  "time_range": {"start_year": 2000, "end_year": 2020},
  "risk_factors": ["hepatitis_b", "hepatitis_c", "alcohol"],
  "data_source": "GLOBOCAN",
  "description": "亚太地区肝癌负担分析",
  "status": "created",
  "created_at": "2026-04-28T09:00:00.000000",
  "updated_at": "2026-04-28T09:00:00.000000"
}
```

---

#### `GET /api/projects`

获取所有项目列表。

- **响应示例**:
```json
{
  "projects": [
    {
      "id": "proj_20260428_090000",
      "title": "Global HCC Burden Analysis",
      "status": "created",
      "created_at": "2026-04-28T09:00:00",
      ...
    }
  ]
}
```

---

#### `GET /api/projects/{project_id}`

获取单个项目详情。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **响应**: 项目完整信息对象
- **错误**: `404` — 项目不存在

---

#### `DELETE /api/projects/{project_id}`

删除项目及其关联数据。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **响应示例**:
```json
{
  "message": "项目已删除"
}
```
- **错误**: `404` — 项目不存在

---

### 数据管理

#### `POST /api/projects/{project_id}/data`

上传数据文件到项目。使用 `multipart/form-data` 编码。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **表单字段**:
  - `file` (file, 必填) — 数据文件 (支持 CSV, XLSX, XLS)
  - `data_source` (string, 可选) — 数据来源标识，默认 "GLOBOCAN"

- **请求示例**:
```bash
curl -X POST http://localhost:8002/api/projects/PROJECT_ID/data \
  -F "file=@data.csv" \
  -F "data_source=GLOBOCAN"
```

- **响应示例**:
```json
{
  "data_id": "data_20260428_090001",
  "filename": "data.csv",
  "records": 120,
  "columns": ["country", "year", "cancer_type", "incidence", "mortality"],
  "warnings": []
}
```
- **错误**: `400` — 不支持的文件格式; `404` — 项目不存在

---

#### `GET /api/projects/{project_id}/data`

获取项目数据摘要。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **响应示例**:
```json
{
  "data_id": "data_20260428_090001",
  "filename": "data.csv",
  "data_source": "GLOBOCAN",
  "summary": {
    "total_records": 120,
    "columns": ["country", "year", "incidence"],
    "numeric_stats": { ... }
  },
  "warnings": []
}
```

---

### 示例数据

#### `GET /api/sample/hcc`

获取内置 HCC (肝细胞癌) 示例数据集信息。

- **响应示例**:
```json
{
  "globocan": {
    "records": 120,
    "columns": ["country", "year", "cancer_type", "incidence", "mortality", ...],
    "sample": [
      {"country": "China", "year": 2020, "incidence": 39.2, ...},
      ...
    ]
  }
}
```

---

#### `POST /api/sample/load/{project_id}`

加载内置 HCC 示例数据到指定项目。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **响应示例**:
```json
{
  "message": "示例数据加载成功",
  "data_id": "data_sample_20260428_090001",
  "records": 120
}
```
- **错误**: `404` — 项目不存在

---

### 统计分析

#### `POST /api/analysis/paf`

计算单个风险因素的人群归因分数 (PAF)。

- **请求体**:

| 字段            | 类型    | 必填 | 说明                              |
|----------------|--------|------|----------------------------------|
| exposure_rate  | float  | 是   | 暴露率 (0-1)，人群暴露于风险因素的比例 |
| relative_risk  | float  | 是   | 相对风险 (RR > 0)，暴露组相对于非暴露组的风险倍数 |

- **请求示例**:
```bash
curl -X POST http://localhost:8002/api/analysis/paf \
  -H "Content-Type: application/json" \
  -d '{"exposure_rate": 0.08, "relative_risk": 22.3}'
```

- **响应示例**:
```json
{
  "paf": 0.632,
  "paf_ci_lower": 0.521,
  "paf_ci_upper": 0.743,
  "exposure_rate": 0.08,
  "relative_risk": 22.3
}
```
- **错误**: `400` — 参数错误

---

#### `POST /api/analysis/paf/batch`

批量计算多个风险因素的 PAF。

- **请求体**: 风险因素数组

| 字段            | 类型    | 必填 | 说明         |
|----------------|--------|------|-------------|
| name           | string | 否   | 风险因素名称  |
| exposure_rate  | float  | 是   | 暴露率       |
| relative_risk  | float  | 是   | 相对风险      |

- **请求示例**:
```bash
curl -X POST http://localhost:8002/api/analysis/paf/batch \
  -H "Content-Type: application/json" \
  -d '[
    {"name": "Hepatitis B", "exposure_rate": 0.08, "relative_risk": 22.3},
    {"name": "Hepatitis C", "exposure_rate": 0.03, "relative_risk": 17.3},
    {"name": "Alcohol", "exposure_rate": 0.30, "relative_risk": 2.1}
  ]'
```

- **响应示例**:
```json
{
  "results": [
    {"risk_factor": "Hepatitis B", "paf": 0.632, "paf_ci_lower": 0.521, "paf_ci_upper": 0.743, ...},
    {"risk_factor": "Hepatitis C", "paf": 0.341, ...},
    {"risk_factor": "Alcohol", "paf": 0.248, ...}
  ]
}
```

---

#### `POST /api/analysis/trend`

时间趋势分析，计算 APC (年度百分比变化)。

- **请求体**:

| 字段    | 类型       | 必填 | 说明         |
|--------|-----------|------|-------------|
| years  | int[]     | 是   | 年份数组      |
| values | float[]   | 是   | 对应的数值数组 |

- **请求示例**:
```bash
curl -X POST http://localhost:8002/api/analysis/trend \
  -H "Content-Type: application/json" \
  -d '{"years": [2000, 2005, 2010, 2015, 2020], "values": [35.2, 38.1, 40.5, 39.2, 36.8]}'
```

- **响应示例**:
```json
{
  "apc": -1.2,
  "p_value": 0.003,
  "r_squared": 0.85,
  "trend_direction": "decreasing"
}
```

---

#### `POST /api/analysis/joinpoint`

Joinpoint 回归分析，识别时间趋势的转折点。

- **请求体**: 同趋势分析 (`years`, `values`)

- **请求示例**:
```bash
curl -X POST http://localhost:8002/api/analysis/joinpoint \
  -H "Content-Type: application/json" \
  -d '{"years": [2000, 2003, 2006, 2009, 2012, 2015, 2018, 2020], "values": [35.0, 37.2, 39.8, 41.0, 39.5, 37.8, 36.2, 35.5]}'
```

- **响应示例**:
```json
{
  "segments": [
    {"start_year": 2000, "end_year": 2009, "apc": 1.8, "p_value": 0.01},
    {"start_year": 2009, "end_year": 2020, "apc": -1.5, "p_value": 0.005}
  ],
  "joinpoints": [2009],
  "overall_apc": -0.2
}
```

---

#### `POST /api/projects/{project_id}/analysis`

运行项目的完整分析流程 (PAF + 趋势分析)。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **请求体**:

| 字段           | 类型    | 必填 | 说明                                 |
|---------------|--------|------|-------------------------------------|
| project_id    | string | 是   | 项目 ID (与路径参数一致)              |
| analysis_type | string | 否   | 分析类型 (PAF/CDPAF/TREND/ASR)，默认 "PAF" |
| parameters    | object | 否   | 额外参数                              |

- **响应示例**:
```json
{
  "analysis_id": "analysis_20260428_090002",
  "paf_results": [...],
  "trend_results": {"apc": -1.2, "p_value": 0.003}
}
```
- **错误**: `404` — 项目不存在

---

#### `GET /api/projects/{project_id}/analysis`

获取项目的已有分析结果。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **响应**: 分析结果对象，或 `{"message": "尚未运行分析"}`

---

### 可视化

#### `POST /api/projects/{project_id}/visualize`

为项目生成可视化图表 (Lancet 风格)。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **生成图表类型**:
  - PAF 条形图 (各风险因素的人群归因分数，含 95% CI)
  - 发病率趋势图 (含置信区间带)
  - 风险因素贡献饼图

- **响应示例**:
```json
{
  "project_id": "proj_20260428_090000",
  "charts": [
    {"type": "paf_bar", "title": "PAF by Risk Factor", "file_path": "output/charts/proj_xxx_paf.png"},
    {"type": "trend", "title": "Incidence Trend", "file_path": "output/charts/proj_xxx_trend.png"},
    {"type": "pie", "title": "Risk Factor Distribution", "file_path": "output/charts/proj_xxx_risk_pie.png"}
  ],
  "message": "生成了 3 个图表"
}
```
- **错误**: `404` — 项目不存在

---

### 论文生成

#### `POST /api/projects/{project_id}/paper`

生成符合 Lancet 标准的论文初稿。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **论文结构**:
  - Summary (摘要)
  - Introduction (引言)
  - Methods (方法)
  - Results (结果)
  - Discussion (讨论)

- **响应示例**:
```json
{
  "project_id": "proj_20260428_090000",
  "paper": {
    "title": "Global Burden of Hepatocellular Carcinoma...",
    "sections": [...],
    "word_count": 3500
  },
  "files": {
    "markdown": "output/papers/proj_xxx_paper.md",
    "html": "output/papers/proj_xxx_paper.html"
  },
  "message": "论文生成成功"
}
```

---

#### `GET /api/projects/{project_id}/paper`

获取项目的论文内容。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **查询参数**: 无

- **响应**: 论文内容 (Markdown 和结构化数据)

---

#### `GET /api/projects/{project_id}/paper/download`

下载论文文件。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **查询参数**:
  - `format` (string, 可选) — 文件格式: `markdown` 或 `html`，默认 `markdown`

- **响应**: 文件下载 (FileResponse)
- **错误**: `400` — 不支持的格式; `404` — 论文不存在

---

### 导出功能

#### `GET /api/projects/{project_id}/export/summary`

获取项目的导出文件摘要。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **响应**: 可用导出文件列表及统计

---

#### `POST /api/projects/{project_id}/export/charts`

批量导出项目图表。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **查询参数**:
  - `format` (string, 可选) — 图片格式: `png`/`svg`，默认 `png`
  - `dpi` (int, 可选) — 分辨率，默认 300

- **响应示例**:
```json
{
  "project_id": "proj_20260428_090000",
  "format": "png",
  "exported_files": ["output/charts/proj_xxx_paf.png", ...],
  "count": 3,
  "message": "成功导出 3 个图表"
}
```

---

#### `POST /api/projects/{project_id}/export/paper`

导出论文。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **查询参数**:
  - `format` (string, 可选) — 导出格式: `markdown`/`html`/`word`/`all`，默认 `markdown`

- **响应示例**:
```json
{
  "project_id": "proj_20260428_090000",
  "format": "all",
  "exported_files": ["output/papers/proj_xxx_paper.md", "output/papers/proj_xxx_paper.html"],
  "word_count": 3500,
  "message": "论文导出成功 (约 3500 词)"
}
```

---

#### `POST /api/projects/{project_id}/export/package`

创建 ZIP 下载包。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **查询参数**:
  - `include_charts` (bool, 可选) — 是否包含图表，默认 `true`
  - `include_paper` (bool, 可选) — 是否包含论文，默认 `true`
  - `include_data` (bool, 可选) — 是否包含数据，默认 `false`

- **响应示例**:
```json
{
  "project_id": "proj_20260428_090000",
  "zip_path": "output/exports/proj_xxx_package.zip",
  "files_count": {"charts": 3, "papers": 2, "data": 0},
  "message": "下载包创建成功"
}
```

---

#### `GET /api/projects/{project_id}/export/download/{filename}`

下载单个导出文件。

- **路径参数**:
  - `project_id` (string) — 项目 ID
  - `filename` (string) — 文件名

- **响应**: 文件下载 (FileResponse)
- **错误**: `404` — 文件不存在

---

#### `GET /api/projects/{project_id}/export/download-all`

下载全部导出文件 (ZIP)。

- **路径参数**:
  - `project_id` (string, 必填) — 项目 ID

- **响应**: ZIP 文件下载
- **错误**: `404` — 没有可下载的文件

---

### 演示接口

#### `POST /api/demo/run`

运行完整的 HCC 演示流程。自动执行: 创建项目 -> 加载数据 -> 统计分析 -> 生成图表 -> 撰写论文。

- **请求体**: 无

- **请求示例**:
```bash
curl -X POST http://localhost:8002/api/demo/run
```

- **响应示例**:
```json
{
  "project_id": "demo_20260428_090000",
  "status": "completed",
  "data_records": 120,
  "paf_results": [
    {"risk_factor": "Hepatitis B", "paf": 0.632, ...},
    {"risk_factor": "Hepatitis C", "paf": 0.341, ...},
    {"risk_factor": "Alcohol", "paf": 0.248, ...},
    {"risk_factor": "Obesity", "paf": 0.107, ...},
    {"risk_factor": "Diabetes", "paf": 0.130, ...},
    {"risk_factor": "Smoking", "paf": 0.111, ...}
  ],
  "charts": [...],
  "paper_path": "output/papers/demo_xxx_paper.md",
  "message": "演示流程完成！"
}
```

---

### 元数据接口

#### `GET /api/statistics/methods`

获取平台支持的所有统计方法。

- **响应示例**:
```json
{
  "methods": [
    {
      "name": "PAF",
      "full_name": "Population Attributable Fraction",
      "description": "人群归因分数 - 估计可归因于特定风险因素的疾病比例",
      "formula": "PAF = (Pe × (RR - 1)) / (1 + Pe × (RR - 1))"
    },
    {
      "name": "CDPAF",
      "full_name": "Correlation-Decomposed PAF",
      "description": "相关性分解归因分数 - 考虑多个风险因素间的相关性",
      "formula": "调整后的联合PAF"
    },
    {
      "name": "ASR",
      "full_name": "Age-Standardized Rate",
      "description": "年龄标准化率 - 使用标准人口进行年龄调整",
      "formula": "ASR = Σ(rate_i × standard_i) / Σ(standard_i)"
    },
    {
      "name": "Joinpoint",
      "full_name": "Joinpoint Regression",
      "description": "Joinpoint回归 - 识别时间趋势的转折点",
      "formula": "分段线性回归"
    },
    {
      "name": "APC",
      "full_name": "Annual Percentage Change",
      "description": "年度百分比变化 - 衡量时间趋势",
      "formula": "APC = (exp(b) - 1) × 100"
    }
  ]
}
```

---

#### `GET /api/databases`

获取平台支持的数据库信息。

- **响应示例**:
```json
{
  "databases": [
    {
      "name": "GLOBOCAN",
      "full_name": "Global Cancer Observatory",
      "description": "全球癌症统计数据库",
      "url": "https://gco.iarc.fr/",
      "coverage": "185个国家/地区",
      "cancer_types": "36种癌症"
    },
    {
      "name": "GBD",
      "full_name": "Global Burden of Disease",
      "description": "全球疾病负担研究数据库",
      "url": "http://ghdx.healthdata.org/gbd-results-tool",
      "coverage": "204个国家/地区"
    },
    {
      "name": "CI5",
      "full_name": "Cancer Incidence in Five Continents",
      "description": "五大洲癌症发病率数据库",
      "url": "https://ci5.iarc.fr/",
      "coverage": "60个国家/地区"
    }
  ]
}
```

---

### 数据模型

#### CancerType 枚举

| 值          | 说明     |
|------------|---------|
| liver      | 肝癌     |
| lung       | 肺癌     |
| breast     | 乳腺癌   |
| colorectal | 结直肠癌 |
| stomach    | 胃癌     |
| prostate   | 前列腺癌 |
| thyroid    | 甲状腺癌 |
| esophagus  | 食管癌   |
| pancreas   | 胰腺癌   |
| bladder    | 膀胱癌   |
| all        | 所有癌症 |

#### RiskFactor 枚举

| 值                  | 说明       |
|--------------------|-----------|
| smoking            | 吸烟       |
| alcohol            | 饮酒       |
| obesity            | 肥胖       |
| hepatitis_b        | 乙肝       |
| hepatitis_c        | 丙肝       |
| diabetes           | 糖尿病     |
| hpv                | 人乳头瘤病毒 |
| h_pylori           | 幽门螺杆菌 |
| air_pollution      | 空气污染   |
| physical_inactivity| 缺乏运动   |

#### 项目状态流转

```
created -> data_uploaded -> analyzed -> visualized -> paper_generated -> completed
```

---

### 错误码说明

| HTTP 状态码 | 说明                | 常见原因                       |
|------------|--------------------|-----------------------------|
| 200        | 成功                | 请求正常处理                    |
| 400        | 请求参数错误          | 输入数据格式不正确或超出有效范围    |
| 404        | 资源不存在            | 项目/文件/论文未找到             |
| 422        | 请求体验证失败         | 必填字段缺失或类型不匹配          |
| 500        | 服务器内部错误         | 服务端异常，请检查日志            |

---

## 统计方法

### 人群归因分数 (PAF)

估计可归因于特定风险因素的疾病比例:

```
PAF = (Pe × (RR - 1)) / (1 + Pe × (RR - 1))
```

- Pe = 暴露率 (人群暴露于风险因素的比例)
- RR = 相对风险 (暴露组相对于非暴露组的风险倍数)
- 输出含 Delta 方法计算的 95% 置信区间

### 相关性分解 PAF (CDPAF)

考虑多个风险因素之间的相关性，避免简单加和导致的重复归因:

```
CDPAF = 1 - ∏(1 - PAF_i × w_i)
```

其中 w_i 为基于因素相关性的调整权重。

### Joinpoint 回归

使用分段线性回归识别时间趋势的转折点:

- 识别趋势发生显著变化的年份
- 每段独立计算 APC (年度百分比变化)
- 支持多重检验校正

### 年龄标准化率 (ASR)

使用 WHO 2000-2025 标准人口进行直接标准化:

```
ASR = Σ(rate_i × standard_pop_i) / Σ(standard_pop_i)
```

### 年度百分比变化 (APC)

```
APC = (exp(b) - 1) × 100
```

其中 b 为对数线性回归的斜率系数。

---

## 技术栈

### 后端
- **Python 3.10+** — 运行时环境
- **FastAPI 0.104** — Web 框架 (异步, 自动文档)
- **Uvicorn** — ASGI 服务器

### 数据 & 统计
- **NumPy** — 数值计算
- **Pandas** — 数据处理
- **SciPy** — 统计检验
- **Statsmodels** — 回归分析

### 可视化
- **Matplotlib** — 静态图表
- **Seaborn** — 统计图表
- **Plotly** — 交互式图表

### 前端
- **Tailwind CSS** — 响应式 UI
- **Vanilla JavaScript** — 单页交互

### 可选
- **python-docx** — Word 文档导出

---

## 相关文档

| 文档            | 说明                           |
|----------------|-------------------------------|
| [README.md](README.md)           | 项目文档 (本文件)              |
| [DEMO.md](DEMO.md)               | 演示指南 — 完整功能演示        |
| [USER_GUIDE.md](USER_GUIDE.md)   | 用户手册 — 详细使用说明        |
| [DEPLOYMENT.md](DEPLOYMENT.md)   | 部署指南 — 多环境部署方案      |
| [CHANGELOG.md](CHANGELOG.md)     | 更新日志 — 版本变更记录        |
| [CONTRIBUTING.md](CONTRIBUTING.md)| 贡献指南 — 参与开发规范       |

---

## 贡献指南

欢迎贡献! 请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

Copyright (c) 2024 MoKangMedical
