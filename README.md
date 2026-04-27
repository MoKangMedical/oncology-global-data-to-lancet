# Cancer Epidemiology Research To Lancet

AI驱动的肿瘤学数据分析平台 — 从全球数据到Lancet论文

## 核心功能

- **数据整合**: 支持 GLOBOCAN、GBD、CI5 三大权威数据库
- **统计分析**: PAF、CDPAF、Joinpoint趋势分析、年龄标准化率
- **可视化**: 自动生成Lancet风格的图表
- **论文生成**: 符合Lancet标准的论文初稿自动生成

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python run.py

# 访问
# 前端界面: http://localhost:8000
# API文档: http://localhost:8000/api/docs
```

## API 接口

### 统计分析
- `POST /api/analysis/paf` - 计算人群归因分数
- `POST /api/analysis/trend` - 趋势分析
- `POST /api/analysis/joinpoint` - Joinpoint回归分析

### 项目管理
- `GET /api/projects` - 获取所有项目
- `POST /api/projects` - 创建项目
- `POST /api/projects/{id}/analysis` - 运行分析
- `POST /api/projects/{id}/visualize` - 生成图表
- `POST /api/projects/{id}/paper` - 生成论文

### 演示
- `POST /api/demo/run` - 运行完整HCC演示
- `GET /api/sample/hcc` - 获取示例数据

## 技术栈

- **后端**: Python 3.12 + FastAPI
- **统计**: NumPy, Pandas, SciPy, Statsmodels
- **可视化**: Matplotlib, Seaborn, Plotly
- **前端**: Tailwind CSS

## 项目结构

```
oncology-global-data-to-lancet/
├── app/
│   ├── main.py              # FastAPI 主应用
│   ├── core/
│   │   ├── statistics.py    # 统计分析引擎
│   │   ├── data_parser.py   # 数据解析器
│   │   ├── visualization.py # 可视化生成器
│   │   └── paper_generator.py # 论文生成器
│   ├── data/
│   │   └── hcc_sample.py    # HCC示例数据
│   └── templates/
│       └── index.html       # 前端页面
├── output/
│   ├── charts/              # 生成的图表
│   └── papers/              # 生成的论文
├── requirements.txt
├── run.py                   # 启动脚本
└── README.md
```

## 统计方法

### 人群归因分数 (PAF)
PAF = (Pe × (RR - 1)) / (1 + Pe × (RR - 1))

其中:
- Pe = 暴露率
- RR = 相对风险

### 趋势分析
- 年度百分比变化 (APC)
- Joinpoint回归识别趋势转折点

### 年龄标准化率 (ASR)
使用世界标准人口 (WHO 2000-2025) 进行直接标准化

## License

MIT License
