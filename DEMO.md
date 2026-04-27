# DEMO 演示指南

**Cancer Epidemiology Research To Lancet — 完整功能演示**

本文档引导你通过平台的全部核心功能，从启动服务到生成论文。

---

## 前提条件

- Python 3.10+ (推荐 3.12)
- macOS / Linux
- 网络连接 (首次安装依赖需要)

---

## 第一步: 启动服务

```bash
# 方式一: 一键部署 (推荐)
cd ~/Desktop/OPC/oncology-global-data-to-lancet
chmod +x deploy.sh
./deploy.sh

# 方式二: 手动启动
python3.12 run.py
```

确认服务启动成功:
```bash
curl http://localhost:8002/health
# 返回: {"status": "healthy", "service": "oncology-to-lancet"}
```

---

## 第二步: 浏览器访问

打开浏览器访问以下地址:

| 页面       | URL                            |
|-----------|--------------------------------|
| 前端界面   | http://localhost:8002          |
| Swagger UI | http://localhost:8002/api/docs |
| ReDoc     | http://localhost:8002/api/redoc|

推荐先访问 Swagger UI (API 文档)，可以直接在浏览器中测试所有接口。

---

## 第三步: 运行 HCC 一键演示

这是最快捷的体验方式 — 一键执行完整的肝细胞癌 (HCC) 分析流程:

```bash
curl -X POST http://localhost:8002/api/demo/run | python3.12 -m json.tool
```

该接口自动执行以下步骤:
1. 创建 HCC 研究项目
2. 加载 GLOBOCAN 示例数据 (多国多年份)
3. 计算 6 个风险因素的 PAF
4. 生成 Lancet 风格 PAF 图表
5. 生成论文初稿 (Markdown)

预期返回:
```json
{
  "project_id": "demo_20260427_214821",
  "status": "completed",
  "data_records": 120,
  "paf_results": [
    {"risk_factor": "Hepatitis B", "paf": 0.632, ...},
    {"risk_factor": "Hepatitis C", "paf": 0.341, ...},
    {"risk_factor": "Alcohol", "paf": 0.248, ...},
    ...
  ],
  "charts": [...],
  "paper_path": "output/papers/demo_xxx_paper.md",
  "message": "演示流程完成！"
}
```

---

## 第四步: 查看生成的产物

### 图表
```bash
ls -la output/charts/
# 你会看到生成的 PNG 图片，如:
#   demo_xxx_paf.png         — PAF 条形图
#   demo_xxx_trend.png       — 趋势图
#   demo_xxx_risk_pie.png    — 风险因素饼图
```

### 论文
```bash
# 查看生成的论文
cat output/papers/demo_xxx_paper.md

# 用浏览器打开 HTML 版本
open output/papers/demo_xxx_paper.html
```

---

## 第五步: 手动创建研究项目

除了演示模式，你也可以手动创建自定义研究项目:

### 5.1 创建项目

```bash
curl -X POST http://localhost:8002/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Global Lung Cancer Burden 2000-2020",
    "cancer_types": ["lung"],
    "countries": ["China", "United States", "Japan", "India"],
    "time_range": {"start_year": 2000, "end_year": 2020},
    "risk_factors": ["smoking", "air_pollution"],
    "data_source": "GLOBOCAN",
    "description": "全球肺癌负担趋势分析"
  }'
```

记下返回的 `project_id`。

### 5.2 加载示例数据

```bash
curl -X POST http://localhost:8002/api/sample/load/YOUR_PROJECT_ID
```

### 5.3 运行分析

```bash
curl -X POST http://localhost:8002/api/projects/YOUR_PROJECT_ID/analysis \
  -H "Content-Type: application/json" \
  -d '{"project_id": "YOUR_PROJECT_ID", "analysis_type": "PAF"}'
```

### 5.4 生成可视化

```bash
curl -X POST http://localhost:8002/api/projects/YOUR_PROJECT_ID/visualize
```

### 5.5 生成论文

```bash
curl -X POST http://localhost:8002/api/projects/YOUR_PROJECT_ID/paper
```

### 5.6 下载所有产物

```bash
# 下载 ZIP 包
curl -o project_output.zip \
  http://localhost:8002/api/projects/YOUR_PROJECT_ID/export/download-all
```

---

## 第六步: 使用统计计算 API

### PAF 计算

```bash
# 单个风险因素
curl -X POST http://localhost:8002/api/analysis/paf \
  -H "Content-Type: application/json" \
  -d '{"exposure_rate": 0.08, "relative_risk": 22.3}'

# 批量计算
curl -X POST http://localhost:8002/api/analysis/paf/batch \
  -H "Content-Type: application/json" \
  -d '[
    {"name": "Hepatitis B", "exposure_rate": 0.08, "relative_risk": 22.3},
    {"name": "Hepatitis C", "exposure_rate": 0.03, "relative_risk": 17.3},
    {"name": "Alcohol", "exposure_rate": 0.30, "relative_risk": 2.1}
  ]'
```

### 趋势分析

```bash
curl -X POST http://localhost:8002/api/analysis/trend \
  -H "Content-Type: application/json" \
  -d '{
    "years": [2000, 2005, 2010, 2015, 2020],
    "values": [35.2, 38.1, 40.5, 39.2, 36.8]
  }'
```

### Joinpoint 回归

```bash
curl -X POST http://localhost:8002/api/analysis/joinpoint \
  -H "Content-Type: application/json" \
  -d '{
    "years": [2000, 2003, 2006, 2009, 2012, 2015, 2018, 2020],
    "values": [35.0, 37.2, 39.8, 41.0, 39.5, 37.8, 36.2, 35.5]
  }'
```

---

## 第七步: 查看系统信息

```bash
# 支持的统计方法
curl http://localhost:8002/api/statistics/methods

# 支持的数据库
curl http://localhost:8002/api/databases

# 查看示例数据
curl http://localhost:8002/api/sample/hcc
```

---

## 第八步: 前端界面操作

在浏览器中访问 http://localhost:8002 ，你可以:

1. **首页仪表盘** — 查看所有项目及其状态
2. **创建新项目** — 填写研究参数表单
3. **运行分析** — 选择分析类型并执行
4. **查看结果** — 浏览图表和统计结果
5. **生成论文** — 一键生成论文初稿
6. **导出下载** — 下载图表、论文或完整 ZIP 包

---

## 常见问题

### Q: 端口被占用怎么办?

```bash
# 查找占用端口的进程
lsof -ti:8002

# 杀掉进程后重启
kill $(lsof -ti:8002)
./deploy.sh quick
```

### Q: 如何更换端口?

```bash
# 方式一: 环境变量
PORT=9000 ./deploy.sh start

# 方式二: 修改 run.py 中的 port 参数
```

### Q: 依赖安装失败?

```bash
# 尝试不使用镜像
pip3.12 install --break-system-packages -r requirements.txt

# 或使用 venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Q: 图表中文显示为方块?

系统缺少中文字体。安装中文字体后重启服务:
```bash
# macOS
brew install font-noto-sans-cjk

# Ubuntu
sudo apt install fonts-noto-cjk
```

### Q: Word 导出失败?

Word 导出需要额外安装 python-docx:
```bash
pip3.12 install --break-system-packages python-docx
```

---

## 完整操作流程图

```
启动服务
  |
  v
访问 http://localhost:8002/api/docs
  |
  +--> POST /api/demo/run  (一键演示)
  |      |
  |      v
  |    查看 output/charts/  (图表)
  |    查看 output/papers/  (论文)
  |
  +--> 手动操作:
         |
         v
       POST /api/projects  (创建项目)
         |
         v
       POST /api/projects/{id}/data  (上传数据)
         |
         v
       POST /api/projects/{id}/analysis  (统计分析)
         |
         v
       POST /api/projects/{id}/visualize  (生成图表)
         |
         v
       POST /api/projects/{id}/paper  (生成论文)
         |
         v
       GET /api/projects/{id}/export/download-all  (下载)
```

---

## 停止服务

```bash
# 方式一
./deploy.sh stop

# 方式二
kill $(lsof -ti:8002)
```

---

**恭喜! 你已完成全部演示流程。**

如有问题，请查阅 [README.md](README.md) 或提交 Issue。
