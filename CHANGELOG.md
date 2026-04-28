# 更新日志

所有项目的更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [未发布]

### 计划中
- 数据库持久化 (PostgreSQL/SQLite) 替代内存存储
- 用户认证与权限管理
- 更多癌症类型数据集
- 实时协作编辑论文
- 支持更多导出格式 (LaTeX, PDF)
- 单元测试覆盖率达 80%+

---

## [2.0.0] - 2026-04-28

### 新增
- 完整的 RESTful API 接口体系 (25+ 端点)
- 项目管理功能: 创建、查看、删除研究项目
- 数据上传: 支持 CSV/Excel 文件上传及智能列名映射
- PAF (人群归因分数) 单因素和批量计算
- 趋势分析: APC 计算及统计显著性检验
- Joinpoint 回归: 时间趋势转折点识别
- 可视化引擎: Lancet 风格图表 (PAF 条形图、趋势图、饼图)
- 论文生成器: 符合 Lancet 投稿标准的论文自动撰写
- 导出服务: 多格式导出 (Markdown/HTML/Word) 及 ZIP 打包
- 内置 HCC (肝细胞癌) 示例数据集
- 一键演示流程 (POST /api/demo/run)
- 元数据接口: 统计方法和数据库信息查询
- Web 前端界面 (Tailwind CSS 单页应用)
- 自动 API 文档 (Swagger UI + ReDoc)
- 300 DPI 高质量学术图表输出

### 变更
- 迁移到 FastAPI 0.104 框架
- 升级 Python 最低版本至 3.10
- 重构项目结构，模块化核心组件
- 统一 API 响应格式

### 文档
- 完整的 README.md 项目文档
- API 接口详细文档
- 用户手册 (USER_GUIDE.md)
- 部署指南 (DEPLOYMENT.md)
- 演示指南 (DEMO.md)
- 贡献指南 (CONTRIBUTING.md)
- 更新日志 (CHANGELOG.md)

---

## [1.0.0] - 2024-01-01

### 新增
- 初始版本发布
- 基础 PAF 计算功能
- 简单数据解析 (CSV)
- 基础可视化 (Matplotlib)
- API 接口初版
- 基础文档

### 修复
- 初始版本，无修复记录

---

## 版本说明

### 版本号格式

本项目使用语义化版本号：`主版本号.次版本号.修订号`

- **主版本号**: 当你做了不兼容的 API 修改
- **次版本号**: 当你做了向下兼容的功能性新增
- **修订号**: 当你做了向下兼容的问题修正

### 发布周期

- **主版本**: 重大功能更新或架构变更
- **次版本**: 新功能发布，每月 1-2 次
- **修订版**: Bug 修复，根据需要发布

### 支持版本

| 版本   | 支持状态   | 说明               |
|-------|-----------|-------------------|
| 2.0.x | 支持      | 当前稳定版本         |
| 1.0.x | 维护模式   | 仅安全修复           |
| < 1.0 | 不支持     | 旧版本，请升级        |

---

## 贡献

欢迎提交 Pull Request 来完善更新日志。请遵循以下格式：

```markdown
## [版本号] - YYYY-MM-DD

### 新增
- 新功能描述

### 修复
- Bug 修复描述

### 变更
- 变更描述

### 移除
- 移除功能描述
```

---

## 链接

- [GitHub Releases](https://github.com/MoKangMedical/oncology-global-data-to-lancet/releases)
- [GitHub Issues](https://github.com/MoKangMedical/oncology-global-data-to-lancet/issues)
- [GitHub Pull Requests](https://github.com/MoKangMedical/oncology-global-data-to-lancet/pulls)
