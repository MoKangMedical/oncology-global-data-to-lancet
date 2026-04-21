# OpenClaw 项目接管指令

**一键复制此指令给OpenClaw，帮助其快速理解项目并开始开发**

---

## 指令内容

```
你好OpenClaw！我需要你接管并继续开发一个癌症流行病学研究自动化分析平台项目。这是一个基于React + TypeScript + tRPC + MySQL的全栈Web应用，已完成核心框架和部分功能，现在需要你完善剩余功能。

### 项目背景

项目名称：**Cancer Epidemiology Research To Lancet**
项目路径：`/home/ubuntu/cancer-research-automation`
当前版本：271543c7
在线预览：https://3000-i5qn379xdp17gd6nuejhz-c0da2d78.us2.manus.computer

这是一个端到端的癌症流行病学研究自动化分析平台，帮助研究人员从数据收集、统计分析、可视化到论文撰写的全流程自动化处理。平台整合GBD、GLOBOCAN、CI5三大权威数据库，自动生成符合Lancet标准的研究论文。

### 技术栈

- 前端：React 19 + TypeScript + Tailwind CSS 4 + tRPC 11 + shadcn/ui + Recharts
- 后端：Node.js 22 + Express 4 + tRPC 11 + Drizzle ORM + MySQL/TiDB
- 认证：Manus Auth (OAuth)
- AI：Manus LLM API（论文生成和参数提取）
- 存储：S3（文件存储）
- 测试：Vitest（已有28个单元测试通过）

### 已完成功能

✅ 用户认证和项目管理
✅ 研究方案智能解析（LLM自动提取参数）
✅ 数据上传和管理（GLOBOCAN/GBD CSV/Excel）
✅ 统计分析引擎（PAF、CDPAF、Joinpoint趋势分析、年龄标准化率）
✅ 数据可视化生成（地图、饼图、折线图、统计表格）
✅ 论文自动生成（Lancet格式，5000-8000词）
✅ 数据库介绍页面（GBD/GLOBOCAN/CI5详细介绍和24篇论文列表）
✅ 首页和导航（seertotoponcology.vip风格配色）
✅ 28个单元测试（覆盖核心业务逻辑）

### 你需要完成的高优先级功能

请按以下顺序完成：

1. **研究参数手动编辑功能**
   - 在ProjectDetail.tsx添加表单，允许用户修改癌症类型、国家、时间范围、风险因素等参数
   - 使用shadcn/ui的Form组件
   - 调用`trpc.projects.update`保存修改

2. **数据格式验证和标准化**
   - 使用Zod schema定义CSV/Excel数据格式
   - 在`server/routers.ts`的`data.uploadFile`中添加验证逻辑
   - 验证列名、数据类型、缺失值处理

3. **数据整合和存储**
   - 实现CSV/Excel解析器（使用`xlsx`或`csv-parser`库）
   - 将解析的数据标准化存储到`cancer_data`表
   - 在`server/db.ts`添加批量插入函数

4. **高分辨率图表导出（PNG/SVG）**
   - 集成Recharts在服务端渲染图表
   - 使用Puppeteer或Playwright无头浏览器渲染
   - 图表上传到S3并返回URL

5. **论文导出（Word/PDF格式）**
   - 使用`docx`库生成Word文档
   - 使用`weasyprint`或`puppeteer`生成PDF
   - 添加下载按钮到论文预览页面

6. **结果可视化展示页面**
   - 在ProjectDetail.tsx添加"分析结果"Tab
   - 展示所有生成的图表和统计表格
   - 支持图表交互（缩放、筛选）和下载

7. **论文预览和编辑页面**
   - 在ProjectDetail.tsx添加"论文"Tab
   - 使用TipTap或Quill富文本编辑器
   - 支持实时保存和版本历史

8. **结果下载中心**
   - 创建统一的下载页面
   - 允许用户一键下载所有生成的论文、图表、统计表格和原始数据
   - 打包为ZIP文件

9. **CI5数据自动下载功能**
   - 集成CI5 API或爬虫
   - 根据项目参数自动下载相关数据
   - 参考CI5官网：https://ci5.iarc.fr/ci5plus/download

### 开发规范

1. **代码风格**
   - 使用TypeScript严格模式，避免`any`类型
   - 遵循React Hooks规则
   - tRPC路由使用`publicProcedure`或`protectedProcedure`
   - 数据库查询使用Drizzle ORM

2. **测试要求**
   - 为每个新功能编写单元测试
   - 测试文件命名：`server/*.test.ts`
   - 运行`pnpm test`确保所有测试通过

3. **UI设计**
   - 使用shadcn/ui组件库
   - 遵循seertotoponcology.vip配色方案（鲜红色#DC2626、米色背景#FEF7ED）
   - 确保移动端响应式布局

4. **文件存储**
   - 使用`server/storage.ts`中的`storagePut`上传文件到S3
   - 媒体文件必须上传到S3，不要存储在本地

5. **开发流程**
   - 在`todo.md`中标记完成的功能为`[x]`
   - 添加新功能前先在`todo.md`添加待办事项
   - 修改数据库schema后运行`pnpm db:push`
   - 完成功能后运行`pnpm test`确保测试通过

### 关键文件位置

- 前端页面：`client/src/pages/`
- tRPC路由：`server/routers.ts`
- 数据库查询：`server/db.ts`
- 统计分析：`server/analysis.ts`
- 可视化生成：`server/visualization.ts`
- 论文生成：`server/paperGeneration.ts`
- 数据库schema：`drizzle/schema.ts`
- 全局样式：`client/src/index.css`
- 功能清单：`todo.md`

### 常用命令

```bash
pnpm dev          # 启动开发服务器
pnpm test         # 运行单元测试
pnpm db:push      # 推送数据库schema变更
pnpm build        # 构建生产版本
```

### 调试技巧

- 开发服务器日志：`.manus-logs/devserver.log`
- 浏览器控制台日志：`.manus-logs/browserConsole.log`
- 网络请求日志：`.manus-logs/networkRequests.log`

### 重要提示

1. **媒体文件处理**：所有图片、PDF等媒体文件必须上传到S3，使用`manus-upload-file`命令或`storagePut`函数，不要存储在项目本地目录。

2. **LLM调用**：使用`server/_core/llm.ts`中的`invokeLLM`函数调用Manus LLM API，无需配置API密钥。

3. **数据库操作**：使用Drizzle ORM进行数据库操作，避免原始SQL（除非必要）。

4. **类型安全**：tRPC提供端到端类型安全，前端调用API时会自动获得类型提示。

5. **checkpoint保存**：完成功能后使用`webdev_save_checkpoint`保存检查点，便于回滚和版本管理。

### 第一步行动

请先执行以下操作：

1. 读取`/home/ubuntu/HANDOVER_TO_OPENCLAW.md`了解完整的项目文档
2. 读取`/home/ubuntu/cancer-research-automation/todo.md`查看详细的功能清单
3. 运行`pnpm test`确保当前所有测试通过
4. 访问在线预览URL体验现有功能
5. 开始实现第一个高优先级功能：研究参数手动编辑功能

如有任何问题，请随时询问。祝开发顺利！
```

---

## 补充说明

此指令已包含OpenClaw接管项目所需的所有关键信息。如果OpenClaw需要更详细的技术文档，请引导其阅读`/home/ubuntu/HANDOVER_TO_OPENCLAW.md`文件。

---

*本指令由Manus AI生成，最后更新于2026年2月15日。*
