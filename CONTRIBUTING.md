# 贡献指南

感谢您对 Cancer Epidemiology Research To Lancet 项目的关注！我们欢迎任何形式的贡献。

---

## 目录

- [如何贡献](#如何贡献)
- [开发环境设置](#开发环境设置)
- [项目架构](#项目架构)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [Pull Request 指南](#pull-request-指南)
- [Issue 规范](#issue-规范)
- [行为准则](#行为准则)

---

## 如何贡献

### 贡献方式

| 类型          | 说明                                        |
|--------------|--------------------------------------------|
| 报告 Bug      | 提交 Issue 描述问题                          |
| 功能建议       | 提交 Issue 描述需求                          |
| 代码贡献       | Fork -> Branch -> PR                       |
| 文档完善       | 修正错误、补充说明、翻译                       |
| 数据贡献       | 提供新的癌症数据集或数据源                      |
| 统计方法       | 实现新的统计分析方法                           |

### 报告问题

1. 查看 [Issues](https://github.com/MoKangMedical/oncology-global-data-to-lancet/issues) 确保问题未被报告
2. 创建新的 Issue，使用提供的 Bug Report 模板
3. 包含以下信息:
   - 操作系统和 Python 版本
   - 复现步骤
   - 期望行为与实际行为
   - 错误日志 (如有)
   - 截图 (如有 UI 问题)

### 提交代码

```bash
# 1. Fork 本仓库到你的 GitHub 账户

# 2. 克隆你的 Fork
git clone https://github.com/YOUR_USERNAME/oncology-global-data-to-lancet.git
cd oncology-global-data-to-lancet

# 3. 添加上游仓库
git remote add upstream https://github.com/MoKangMedical/oncology-global-data-to-lancet.git

# 4. 创建特性分支
git checkout -b feature/your-feature-name

# 5. 进行开发...

# 6. 提交更改
git add .
git commit -m "feat(scope): description of your changes"

# 7. 同步上游
git fetch upstream
git rebase upstream/main

# 8. 推送到你的 Fork
git push origin feature/your-feature-name

# 9. 在 GitHub 上创建 Pull Request
```

---

## 开发环境设置

### 环境要求

- Python 3.10+ (推荐 3.12)
- Git 2.0+
- macOS / Linux

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/MoKangMedical/oncology-global-data-to-lancet.git
cd oncology-global-data-to-lancet

# 2. 创建虚拟环境
python3.12 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 验证安装
python run.py
# 访问 http://localhost:8002/health 确认正常

# 5. 运行演示验证功能
curl -X POST http://localhost:8002/api/demo/run
```

### 项目结构

```
oncology-global-data-to-lancet/
├── app/                       # 应用核心
│   ├── main.py                # FastAPI 主应用 (所有路由)
│   ├── core/
│   │   ├── statistics.py      # 统计引擎
│   │   ├── data_parser.py     # 数据解析器
│   │   ├── visualization.py   # 可视化生成
│   │   ├── paper_generator.py # 论文生成器
│   │   └── export_service.py  # 导出服务
│   ├── data/
│   │   └── hcc_sample.py      # 示例数据
│   ├── models/
│   │   └── schemas.py         # Pydantic 数据模型
│   └── templates/
│       └── index.html         # 前端页面
├── run.py                     # 启动脚本
├── deploy.sh                  # 部署脚本
└── requirements.txt           # 依赖列表
```

---

## 项目架构

### 核心模块

| 模块               | 文件                  | 职责                        |
|-------------------|----------------------|----------------------------|
| Web 层            | `app/main.py`         | 路由定义、请求处理、响应格式化   |
| 统计引擎           | `app/core/statistics.py` | PAF/CDPAF/APC/Joinpoint 计算 |
| 数据解析           | `app/core/data_parser.py` | CSV/Excel 解析、列名标准化    |
| 可视化             | `app/core/visualization.py` | 图表生成 (Lancet 风格)     |
| 论文生成           | `app/core/paper_generator.py` | 论文结构组装和内容生成     |
| 导出服务           | `app/core/export_service.py` | 文件导出和打包           |
| 数据模型           | `app/models/schemas.py` | Pydantic 模型定义           |
| 示例数据           | `app/data/hcc_sample.py` | 内置 HCC 数据集             |

### 数据流

```
请求 -> main.py (路由) -> core/* (业务逻辑) -> 响应
                                        |
                                  output/* (文件输出)
```

---

## 代码规范

### Python 风格

- 遵循 [PEP 8](https://peps.python.org/pep-0008/) 规范
- 使用 4 空格缩进
- 行宽限制 120 字符
- 使用类型注解 (Type Hints)

### 命名规范

```python
# 模块/文件名: 小写+下划线
statistics.py, data_parser.py

# 类名: 大驼峰
class StatisticalEngine, class DataParser

# 函数/方法: 小写+下划线
def calculate_paf(), def parse_csv()

# 常量: 大写+下划线
MAX_RETRY_COUNT = 3
DEFAULT_PORT = 8002

# 变量: 小写+下划线
risk_factors = []
exposure_rate = 0.08
```

### 注释规范

```python
def calculate_paf(exposure_rate: float, relative_risk: float) -> dict:
    """
    计算人群归因分数 (PAF)。

    使用 Levin 公式: PAF = (Pe × (RR - 1)) / (1 + Pe × (RR - 1))

    Args:
        exposure_rate: 暴露率 (0-1)，人群暴露于风险因素的比例
        relative_risk: 相对风险 (RR > 0)，暴露组相对于非暴露组的风险倍数

    Returns:
        dict: 包含 PAF 值、95% 置信区间等信息

    Raises:
        ValueError: 当参数超出有效范围时
    """
```

### 导入顺序

```python
# 1. 标准库
import os
import json
from pathlib import Path
from typing import List, Dict

# 2. 第三方库
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException

# 3. 本地模块
from app.core.statistics import statistical_engine
from app.models.schemas import PAFResult
```

---

## 提交规范

### Commit Message 格式

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### 类型 (type)

| 类型       | 说明                              |
|-----------|----------------------------------|
| feat      | 新功能                             |
| fix       | 修复 Bug                           |
| docs      | 文档更新                            |
| style     | 代码格式调整 (不影响功能)             |
| refactor  | 代码重构 (不是新功能也不是修复)       |
| perf      | 性能优化                           |
| test      | 测试相关                           |
| chore     | 构建/工具链变更                     |
| ci        | CI/CD 相关                        |

### 范围 (scope)

可选，表示影响范围:

- `api` — API 接口
- `stats` — 统计引擎
- `viz` — 可视化
- `paper` — 论文生成
- `parser` — 数据解析
- `export` — 导出服务
- `deploy` — 部署相关
- `docs` — 文档

### 示例

```
feat(stats): 添加 CDPAF 相关性分解计算

- 实现考虑因素相关性的 PAF 调整算法
- 添加批量 CDPAF 计算接口
- 更新相关单元测试

Closes #42
```

```
fix(parser): 修复 Excel 文件中文列名识别失败的问题

- 改进列名标准化映射逻辑
- 添加中文列名到英文列名的自动转换

Fixes #38
```

```
docs(readme): 更新 API 文档，添加完整端点说明
```

---

## Pull Request 指南

### 提交前检查清单

- [ ] 代码符合项目规范 (PEP 8 + 类型注解)
- [ ] 所有现有测试通过
- [ ] 新功能添加了相应测试
- [ ] 文档已更新 (API 文档、README 等)
- [ ] Commit message 符合规范
- [ ] 没有引入新的 linting 警告
- [ ] 不包含调试代码或敏感信息

### PR 描述模板

```markdown
## 变更内容

简要描述此 PR 的更改内容。

## 变更类型

- [ ] 新功能 (feat)
- [ ] Bug 修复 (fix)
- [ ] 文档更新 (docs)
- [ ] 代码重构 (refactor)
- [ ] 性能优化 (perf)
- [ ] 其他: ___

## 相关 Issue

Closes #___

## 测试情况

描述如何测试这些更改:

1. ...
2. ...

## 截图 (如适用)

(如有 UI 变更，请添加截图)

## 检查清单

- [ ] 代码自测通过
- [ ] 文档已更新
- [ ] 没有破坏现有功能
```

### PR 流程

1. 创建 PR 后，自动 CI 检查将运行
2. 至少一位维护者 review
3. 根据 review 意见修改代码
4. 维护者批准后合并
5. 合并后自动更新 CHANGELOG.md

---

## Issue 规范

### Bug Report 模板

```markdown
## Bug 描述

简要描述问题。

## 复现步骤

1. 启动服务 '...'
2. 调用接口 '...'
3. 传入参数 '...'
4. 出现错误

## 期望行为

描述你期望发生的情况。

## 实际行为

描述实际发生的情况。

## 环境信息

- OS: [如 macOS 14.0]
- Python: [如 3.12.0]
- 项目版本: [如 2.0.0]

## 错误日志

(粘贴相关错误日志)

## 补充信息

(其他有助于定位问题的信息)
```

### Feature Request 模板

```markdown
## 功能描述

简要描述你希望添加的功能。

## 使用场景

描述这个功能解决什么问题或满足什么需求。

## 期望方案

描述你期望的实现方式。

## 替代方案

描述你考虑过的其他替代方案。

## 补充信息

(其他相关信息)
```

---

## 行为准则

### 我们的承诺

为了营造一个开放和友好的环境，我们承诺:

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 不可接受的行为

- 使用性化的语言或图像
- 人身攻击或侮辱性评论
- 公开或私下骚扰
- 未经许可发布他人的私人信息
- 其他不道德或不专业的行为

---

## 开发技巧

### 添加新的统计方法

1. 在 `app/core/statistics.py` 中添加计算函数
2. 在 `app/models/schemas.py` 中定义请求/响应模型
3. 在 `app/main.py` 中添加 API 路由
4. 更新 `app/data/hcc_sample.py` 中的示例数据 (如适用)
5. 在 `GET /api/statistics/methods` 中注册新方法
6. 更新文档

### 添加新的可视化类型

1. 在 `app/core/visualization.py` 中添加图表生成函数
2. 使用 Lancet 风格配色 (参考现有图表)
3. 在 `app/main.py` 的可视化路由中调用
4. 确保输出 300 DPI PNG

### 添加新的数据源

1. 在 `app/core/data_parser.py` 中添加解析逻辑
2. 在 `app/models/schemas.py` 的 `DataSource` 枚举中注册
3. 实现列名映射

---

## 许可证

参与本项目即表示您同意您的贡献将在 [MIT License](LICENSE) 下发布。

---

## 联系方式

如有任何问题，请通过以下方式联系我们:

- 项目 Issues: https://github.com/MoKangMedical/oncology-global-data-to-lancet/issues
- 邮箱: contact@mokangmedical.com

感谢您的贡献！
