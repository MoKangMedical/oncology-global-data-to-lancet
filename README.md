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
- [统计方法](#统计方法)
- [截图说明](#截图说明)
- [技术栈](#技术栈)
- [演示流程](#演示流程)
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

### 方式三：指定端口

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

### 系统接口

| 方法   | 路径              | 说明       |
|--------|-------------------|-----------|
| GET    | `/`               | 服务信息   |
| GET    | `/health`         | 健康检查   |

### 项目管理

| 方法     | 路径                            | 说明               |
|----------|--------------------------------|-------------------|
| POST     | `/api/projects`                | 创建研究项目        |
| GET      | `/api/projects`                | 获取所有项目列表    |
| GET      | `/api/projects/{id}`           | 获取单个项目详情    |
| DELETE   | `/api/projects/{id}`           | 删除项目           |

**创建项目请求体:**
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

### 数据管理

| 方法  | 路径                          | 说明             |
|-------|------------------------------|-----------------|
| POST  | `/api/projects/{id}/data`    | 上传数据文件      |
| GET   | `/api/projects/{id}/data`    | 获取项目数据摘要  |

支持格式: CSV, XLSX, XLS

### 统计分析

| 方法  | 路径                              | 说明                    |
|-------|----------------------------------|------------------------|
| POST  | `/api/analysis/paf`              | 计算 PAF                |
| POST  | `/api/analysis/paf/batch`        | 批量计算 PAF            |
| POST  | `/api/analysis/trend`            | 趋势分析 (APC)          |
| POST  | `/api/analysis/joinpoint`        | Joinpoint 回归分析      |
| POST  | `/api/projects/{id}/analysis`    | 运行项目完整分析        |

**PAF 计算示例:**
```bash
curl -X POST http://localhost:8002/api/analysis/paf \
  -H "Content-Type: application/json" \
  -d '{"exposure_rate": 0.08, "relative_risk": 22.3}'
```

**响应:**
```json
{
  "paf": 0.632,
  "paf_ci_lower": 0.521,
  "paf_ci_upper": 0.743,
  "exposure_rate": 0.08,
  "relative_risk": 22.3
}
```

**趋势分析示例:**
```bash
curl -X POST http://localhost:8002/api/analysis/trend \
  -H "Content-Type: application/json" \
  -d '{
    "years": [2000, 2005, 2010, 2015, 2020],
    "values": [35.2, 38.1, 40.5, 39.2, 36.8]
  }'
```

### 可视化

| 方法  | 路径                                | 说明           |
|-------|------------------------------------|---------------|
| POST  | `/api/projects/{id}/visualize`     | 生成项目图表   |

生成图表类型:
- PAF 条形图 (各风险因素的人群归因分数)
- 发病率趋势图 (含 95% 置信区间)
- 风险因素贡献饼图

### 论文

| 方法  | 路径                                       | 说明         |
|-------|-------------------------------------------|-------------|
| POST  | `/api/projects/{id}/paper`                 | 生成论文     |
| GET   | `/api/projects/{id}/paper/download`        | 下载论文     |

### 演示

| 方法  | 路径                    | 说明                   |
|-------|------------------------|-----------------------|
| POST  | `/api/demo/run`        | 运行完整 HCC 演示流程   |
| GET   | `/api/sample/hcc`      | 获取 HCC 示例数据       |
| POST  | `/api/sample/load/{id}`| 加载示例数据到项目      |

### 导出

| 方法  | 路径                                          | 说明                |
|-------|----------------------------------------------|--------------------|
| GET   | `/api/projects/{id}/export/summary`           | 导出摘要            |
| POST  | `/api/projects/{id}/export/charts`            | 导出图表            |
| POST  | `/api/projects/{id}/export/paper`             | 导出论文            |
| POST  | `/api/projects/{id}/export/package`           | 创建 ZIP 下载包     |
| GET   | `/api/projects/{id}/export/download/{file}`   | 下载单个文件        |
| GET   | `/api/projects/{id}/export/download-all`      | 下载全部 (ZIP)      |

### 元数据

| 方法  | 路径                         | 说明                 |
|-------|-----------------------------|---------------------|
| GET   | `/api/statistics/methods`    | 获取支持的统计方法    |
| GET   | `/api/databases`             | 获取支持的数据库信息  |

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

## 截图说明

### 1. 首页 - 项目管理

![首页](docs/screenshots/home.png)

首页展示所有研究项目，支持创建新项目、查看项目状态和快速启动演示。

### 2. 演示流程 - HCC 分析

![演示](docs/screenshots/demo.png)

一键运行 HCC (肝细胞癌) 完整分析演示:
- 自动生成 GLOBOCAN 样本数据
- 计算 6 个风险因素的 PAF
- 生成 Lancet 风格图表
- 输出论文初稿

### 3. PAF 分析结果

![PAF分析](docs/screenshots/paf_analysis.png)

展示各风险因素的人群归因分数，以条形图形式呈现，含 95% 置信区间。

### 4. 趋势分析

![趋势](docs/screenshots/trend_analysis.png)

时间趋势可视化，含置信区间带和 Joinpoint 转折点标注。

### 5. 论文输出

![论文](docs/screenshots/paper_output.png)

自动生成符合 Lancet 标准的论文初稿，支持 Markdown/HTML/Word 多格式导出。

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

## 演示流程

最快速的体验方式是运行内置 HCC 演示:

```bash
# 启动服务后
curl -X POST http://localhost:8002/api/demo/run
```

返回结果包含:
- 项目 ID
- 数据记录数
- PAF 分析结果 (6 个风险因素)
- 生成的图表路径
- 论文路径

详细演示步骤请参阅 [DEMO.md](DEMO.md)。

---

## 贡献指南

欢迎贡献! 请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

Copyright (c) 2024 MoKangMedical
