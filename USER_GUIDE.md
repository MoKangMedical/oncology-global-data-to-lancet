# 用户手册

**Cancer Epidemiology Research To Lancet — 详细使用指南**

本手册面向研究人员和数据分析师，指导你充分利用平台的全部功能完成癌症流行病学研究。

---

## 目录

- [简介](#简介)
- [入门指南](#入门指南)
- [功能详解](#功能详解)
  - [项目管理](#项目管理)
  - [数据上传](#数据上传)
  - [统计分析](#统计分析)
  - [可视化生成](#可视化生成)
  - [论文生成](#论文生成)
  - [导出与下载](#导出与下载)
- [完整工作流](#完整工作流)
- [数据格式说明](#数据格式说明)
- [统计方法详解](#统计方法详解)
- [常见问题 (FAQ)](#常见问题-faq)
- [术语表](#术语表)

---

## 简介

Cancer Epidemiology Research To Lancet 是一个端到端的癌症流行病学研究平台。它帮助研究者:

1. **整合数据** — 从 GLOBOCAN、GBD、CI5 等权威数据库导入数据
2. **执行分析** — 计算 PAF、趋势分析、Joinpoint 回归等
3. **生成图表** — 自动创建符合 Lancet 标准的学术图表
4. **撰写论文** — AI 辅助生成论文初稿，节省 70% 以上写作时间
5. **导出成果** — 一键打包下载图表、论文和数据

### 典型用户

- 流行病学研究人员
- 肿瘤学研究者
- 公共卫生政策分析师
- 医学研究生

---

## 入门指南

### 前提条件

- Python 3.10+ (推荐 3.12)
- macOS 或 Linux 操作系统
- 浏览器 (Chrome/Firefox/Safari)

### 第一步：启动服务

```bash
cd oncology-global-data-to-lancet
chmod +x deploy.sh
./deploy.sh
```

看到 "Server started successfully!" 即表示启动成功。

### 第二步：访问界面

打开浏览器访问 http://localhost:8002

### 第三步：快速体验

点击页面上的 "运行演示" 按钮，或在终端执行:

```bash
curl -X POST http://localhost:8002/api/demo/run
```

系统将自动执行完整的 HCC (肝细胞癌) 分析流程，约 10-30 秒即可看到结果。

---

## 功能详解

### 项目管理

#### 创建新项目

每个研究项目是平台的核心组织单元。一个项目包含研究参数、数据、分析结果、图表和论文。

**方式一：前端界面**

1. 点击首页 "新建项目" 按钮
2. 填写表单:
   - **项目标题**: 简明描述研究目的，如 "全球肝癌负担分析 2000-2020"
   - **癌症类型**: 选择一种或多种 (肝癌、肺癌、乳腺癌等)
   - **目标国家**: 选择要分析的国家/地区
   - **时间范围**: 设置起止年份
   - **风险因素**: 选择要分析的风险因素
   - **数据源**: 选择数据来源
3. 点击 "创建"

**方式二：API 调用**

```bash
curl -X POST http://localhost:8002/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "title": "亚太地区肝癌趋势分析",
    "cancer_types": ["liver"],
    "countries": ["China", "Japan", "South Korea", "India"],
    "time_range": {"start_year": 2000, "end_year": 2020},
    "risk_factors": ["hepatitis_b", "hepatitis_c", "alcohol"],
    "data_source": "GLOBOCAN",
    "description": "分析亚太地区 HCC 的发病趋势及主要风险因素"
  }'
```

#### 查看项目列表

```bash
curl http://localhost:8002/api/projects
```

#### 删除项目

```bash
curl -X DELETE http://localhost:8002/api/projects/PROJECT_ID
```

> 注意: 删除项目会同时删除其关联的数据、分析结果、图表和论文，且不可恢复。

---

### 数据上传

#### 支持的数据格式

| 格式   | 扩展名          | 说明                    |
|--------|----------------|------------------------|
| CSV    | `.csv`          | 逗号分隔，UTF-8 编码     |
| Excel  | `.xlsx`, `.xls` | Microsoft Excel 格式    |

#### 上传方式

**前端界面:**

1. 进入项目详情页
2. 点击 "上传数据"
3. 选择文件并确认数据源

**API 调用:**

```bash
curl -X POST http://localhost:8002/api/projects/PROJECT_ID/data \
  -F "file=@your_data.csv" \
  -F "data_source=GLOBOCAN"
```

#### 数据列名映射

平台支持智能列名识别，自动映射中英文列名:

| 标准列名         | 中文识别        | 英文识别            |
|-----------------|----------------|-------------------|
| country         | 国家            | country, nation   |
| year            | 年份            | year              |
| cancer_type     | 癌症类型         | cancer_type, cancer|
| incidence       | 发病率           | incidence, rate   |
| mortality       | 死亡率           | mortality, death_rate |
| asr_incidence   | 标化发病率        | asr, age_standardized |
| population      | 人口            | population, pop   |
| cases           | 病例数           | cases, new_cases  |
| deaths          | 死亡数           | deaths            |

#### 使用内置示例数据

如果没有自己的数据，可以使用内置的 HCC 示例数据:

```bash
# 查看示例数据结构
curl http://localhost:8002/api/sample/hcc

# 加载示例数据到项目
curl -X POST http://localhost:8002/api/sample/load/PROJECT_ID
```

---

### 统计分析

#### 人群归因分数 (PAF)

PAF 表示可归因于特定风险因素的疾病比例，是流行病学中最常用的归因指标。

**单独计算 PAF:**

```bash
curl -X POST http://localhost:8002/api/analysis/paf \
  -H "Content-Type: application/json" \
  -d '{"exposure_rate": 0.08, "relative_risk": 22.3}'
```

**参数说明:**
- `exposure_rate` (暴露率): 人群中暴露于该风险因素的比例，取值 0-1
  - 例: 中国 HBV 携带率约 8%，则 exposure_rate = 0.08
- `relative_risk` (相对风险): 暴露组相对于非暴露组的发病风险倍数
  - 例: HBV 感染者肝癌风险是未感染者的 22.3 倍

**批量计算:**

同时计算多个风险因素的 PAF:

```bash
curl -X POST http://localhost:8002/api/analysis/paf/batch \
  -H "Content-Type: application/json" \
  -d '[
    {"name": "乙型肝炎", "exposure_rate": 0.08, "relative_risk": 22.3},
    {"name": "丙型肝炎", "exposure_rate": 0.03, "relative_risk": 17.3},
    {"name": "饮酒", "exposure_rate": 0.30, "relative_risk": 2.1},
    {"name": "肥胖", "exposure_rate": 0.15, "relative_risk": 1.8},
    {"name": "糖尿病", "exposure_rate": 0.10, "relative_risk": 2.5},
    {"name": "吸烟", "exposure_rate": 0.25, "relative_risk": 1.5}
  ]'
```

#### 趋势分析

分析指标随时间的变化趋势，计算 APC (年度百分比变化):

```bash
curl -X POST http://localhost:8002/api/analysis/trend \
  -H "Content-Type: application/json" \
  -d '{
    "years": [2000, 2005, 2010, 2015, 2020],
    "values": [35.2, 38.1, 40.5, 39.2, 36.8]
  }'
```

**解读结果:**
- APC > 0: 指标呈上升趋势
- APC < 0: 指标呈下降趋势
- p_value < 0.05: 趋势具有统计学意义

#### Joinpoint 回归

识别时间趋势中的转折点 (年份)，发现趋势发生显著变化的时刻:

```bash
curl -X POST http://localhost:8002/api/analysis/joinpoint \
  -H "Content-Type: application/json" \
  -d '{
    "years": [2000, 2003, 2006, 2009, 2012, 2015, 2018, 2020],
    "values": [35.0, 37.2, 39.8, 41.0, 39.5, 37.8, 36.2, 35.5]
  }'
```

**解读结果:**
- `joinpoints`: 转折点年份数组
- `segments`: 每段的起止年份和各自的 APC
- 例: 如果 joinpoints = [2009]，说明 2009 年前后趋势发生了显著变化

#### 运行项目完整分析

对整个项目执行综合分析:

```bash
curl -X POST http://localhost:8002/api/projects/PROJECT_ID/analysis \
  -H "Content-Type: application/json" \
  -d '{"project_id": "PROJECT_ID", "analysis_type": "PAF"}'
```

---

### 可视化生成

#### 生成图表

```bash
curl -X POST http://localhost:8002/api/projects/PROJECT_ID/visualize
```

系统自动生成三种图表:

**1. PAF 条形图 (paf_bar)**
- 展示各风险因素的 PAF 值
- 含 95% 置信区间误差线
- Lancet 风格配色

**2. 发病率趋势图 (trend)**
- 时间轴上的发病率变化曲线
- 95% 置信区间带 (阴影区域)
- 标注关键转折点

**3. 风险因素饼图 (pie)**
- 各风险因素对疾病的相对贡献
- 百分比标注

#### 图表质量

所有图表默认输出:
- 格式: PNG
- 分辨率: 300 DPI (适合学术出版)
- 配色: Lancet 期刊标准色板

---

### 论文生成

#### 生成论文

```bash
curl -X POST http://localhost:8002/api/projects/PROJECT_ID/paper
```

#### 论文结构

生成的论文遵循 Lancet 投稿标准:

| 章节          | 内容                                       |
|--------------|-------------------------------------------|
| Summary      | 研究背景、方法、主要发现和结论的简要概述      |
| Introduction | 研究背景、现有知识空白和研究目的              |
| Methods      | 数据来源、统计方法、分析流程的详细描述        |
| Results      | PAF 结果、趋势分析结果、主要发现             |
| Discussion   | 结果解读、与现有研究对比、局限性和政策意义    |

#### 查看论文

```bash
# 获取论文内容
curl http://localhost:8002/api/projects/PROJECT_ID/paper

# 下载 Markdown 版本
curl -o paper.md http://localhost:8002/api/projects/PROJECT_ID/paper/download?format=markdown

# 下载 HTML 版本 (可用浏览器打开)
curl -o paper.html http://localhost:8002/api/projects/PROJECT_ID/paper/download?format=html
```

#### 使用建议

- 生成的论文为初稿，需要研究者进一步修改和完善
- 特别关注 Results 和 Discussion 章节，可能需要根据实际数据补充细节
- 检查所有数据引用的准确性
- 根据目标期刊要求调整格式

---

### 导出与下载

#### 导出图表

```bash
# 导出 PNG 格式 (300 DPI)
curl -X POST http://localhost:8002/api/projects/PROJECT_ID/export/charts?format=png&dpi=300
```

#### 导出论文 (多格式)

```bash
# 导出所有格式 (Markdown + HTML + Word)
curl -X POST http://localhost:8002/api/projects/PROJECT_ID/export/paper?format=all
```

#### 打包下载

```bash
# 创建 ZIP 包 (包含图表和论文)
curl -X POST http://localhost:8002/api/projects/PROJECT_ID/export/package

# 下载 ZIP
curl -o output.zip http://localhost:8002/api/projects/PROJECT_ID/export/download-all
```

#### 前端操作

在浏览器中:
1. 进入项目详情页
2. 点击 "导出" 标签
3. 选择导出内容和格式
4. 点击 "下载"

---

## 完整工作流

### 流程一：快速演示 (推荐新手)

```
1. 启动服务          ./deploy.sh
2. 运行演示          curl -X POST http://localhost:8002/api/demo/run
3. 查看图表          ls output/charts/
4. 查看论文          cat output/papers/demo_*_paper.md
5. 下载打包          curl -o result.zip http://localhost:8002/api/projects/DEMO_ID/export/download-all
```

### 流程二：自定义研究

```
1. 创建项目          POST /api/projects
2. 上传数据          POST /api/projects/{id}/data
   或加载示例        POST /api/sample/load/{id}
3. 运行分析          POST /api/projects/{id}/analysis
4. 生成图表          POST /api/projects/{id}/visualize
5. 生成论文          POST /api/projects/{id}/paper
6. 导出下载          GET  /api/projects/{id}/export/download-all
```

### 流程三：仅做统计计算

```
1. 计算 PAF           POST /api/analysis/paf
2. 趋势分析           POST /api/analysis/trend
3. Joinpoint 回归     POST /api/analysis/joinpoint
```

---

## 数据格式说明

### CSV 数据示例

```csv
country,year,cancer_type,incidence,mortality,cases,deaths,population
China,2020,liver,39.2,33.8,150000,105000,1400000000
China,2015,liver,40.5,35.1,145000,102000,1370000000
Japan,2020,liver,22.1,18.5,45000,38000,126000000
South Korea,2020,liver,28.3,22.6,18000,14300,52000000
```

### Excel 数据要求

- 第一行为列标题
- 每行一条记录
- 推荐使用 `.xlsx` 格式
- 避免合并单元格

### 内置示例数据结构

HCC 示例数据包含以下字段:
- `country`: 国家 (China, Japan, South Korea 等)
- `year`: 年份 (2000-2020)
- `cancer_type`: 癌症类型 (liver)
- `incidence`: 发病率 (每 10 万人)
- `mortality`: 死亡率 (每 10 万人)
- `cases`: 新发病例数
- `deaths`: 死亡病例数

---

## 统计方法详解

### PAF 的实际意义

PAF = 0.632 意味着: 在研究人群中，63.2% 的肝癌病例可归因于该风险因素 (如 HBV 感染)。

**使用场景:**
- 评估疾病预防的潜在收益
- 为公共卫生政策提供依据
- 比较不同风险因素的相对重要性

### CDPAF 的优势

当多个风险因素同时作用时，简单将各个 PAF 相加会导致过度归因 (>100%)。CDPAF 通过考虑因素之间的相关性进行调整。

**使用场景:**
- 同时分析 3 个以上风险因素
- 风险因素之间存在已知相关性 (如肥胖和糖尿病)
- 需要估算所有风险因素的联合效应

### APC 的解读

- APC = 2.5%: 指标每年增长 2.5%
- APC = -1.2%: 指标每年下降 1.2%
- 统计学意义: p < 0.05

---

## 常见问题 (FAQ)

### Q: 端口 8002 被占用怎么办?

```bash
# 查找占用端口的进程
lsof -ti:8002

# 杀掉进程后重启
kill $(lsof -ti:8002)
./deploy.sh quick

# 或使用其他端口
PORT=9000 ./deploy.sh start
```

### Q: 依赖安装失败怎么办?

```bash
# 方案一: 使用虚拟环境
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 方案二: 不使用镜像源
pip3.12 install --break-system-packages -r requirements.txt

# 方案三: 逐个安装
pip3.12 install --break-system-packages fastapi uvicorn pandas numpy
```

### Q: 上传数据后分析报错?

检查数据格式:
1. 确保 CSV 文件使用 UTF-8 编码
2. 确保包含必需的列 (country, year, cancer_type 等)
3. 确保数值列不含非数字字符
4. 先使用示例数据验证系统功能正常

### Q: 图表中文显示为方块?

安装中文字体:

```bash
# macOS
brew install font-noto-sans-cjk

# Ubuntu/Debian
sudo apt install fonts-noto-cjk

# 安装后重启服务
./deploy.sh restart
```

### Q: Word 导出失败?

```bash
# 安装 python-docx
pip3.12 install --break-system-packages python-docx

# 验证安装
python3.12 -c "import docx; print('OK')"
```

### Q: 论文内容不准确?

生成的论文为 AI 辅助的初稿，需要:
1. 仔细核对所有数据和统计结果
2. 补充专业领域知识
3. 根据研究实际修改 Methods 和 Results
4. 完善 Discussion 中的文献引用

### Q: 如何更新到最新版本?

```bash
cd oncology-global-data-to-lancet
git pull origin main
./deploy.sh restart
```

### Q: 数据安全吗?

- 所有数据存储在本地服务器内存中
- 不会上传到任何外部服务
- 论文和图表生成在本地完成
- 重启服务后内存数据会清除

---

## 术语表

| 术语       | 英文                              | 说明                                      |
|-----------|----------------------------------|------------------------------------------|
| PAF       | Population Attributable Fraction | 人群归因分数，可归因于某风险因素的疾病比例      |
| CDPAF     | Correlation-Decomposed PAF       | 考虑因素相关性的调整 PAF                    |
| APC       | Annual Percentage Change         | 年度百分比变化，衡量时间趋势的方向和强度       |
| ASR       | Age-Standardized Rate            | 年龄标准化率，消除年龄结构差异的标准化指标     |
| RR        | Relative Risk                    | 相对风险，暴露组相对于非暴露组的风险倍数       |
| CI        | Confidence Interval              | 置信区间，参数估计的不确定性范围             |
| Joinpoint | -                                | 趋势分析中的转折点，趋势发生显著变化的年份    |
| GLOBOCAN  | Global Cancer Observatory        | 全球癌症统计数据库                          |
| GBD       | Global Burden of Disease         | 全球疾病负担研究数据库                       |
| CI5       | Cancer Incidence in Five Continents | 五大洲癌症发病率数据库                     |
| HCC       | Hepatocellular Carcinoma         | 肝细胞癌                                   |
| ASGI      | Asynchronous Server Gateway Interface | 异步服务器网关接口                     |

---

## 技术支持

如遇到本文档未覆盖的问题:

1. 查看 [DEMO.md](DEMO.md) 演示指南
2. 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 部署指南
3. 在 GitHub 提交 [Issue](https://github.com/MoKangMedical/oncology-global-data-to-lancet/issues)
4. 联系邮箱: contact@mokangmedical.com
