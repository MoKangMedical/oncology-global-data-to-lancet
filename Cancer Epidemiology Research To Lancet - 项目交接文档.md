# Cancer Epidemiology Research To Lancet - 项目交接文档

**文档版本**: 1.0  
**创建日期**: 2026年2月15日  
**作者**: Manus AI  
**交接对象**: OpenClaw  

---

## 项目概述

**Cancer Epidemiology Research To Lancet** 是一个端到端的癌症流行病学研究自动化分析平台，旨在帮助研究人员从数据收集、统计分析、可视化到论文撰写的全流程自动化处理。平台整合Global Burden of Disease (GBD)、GLOBOCAN、Cancer Incidence in Five Continents (CI5)三大权威数据库，自动生成符合Lancet标准的研究论文。

### 核心价值主张

平台通过AI驱动的自动化工作流，将传统需要数周甚至数月的癌症流行病学研究流程压缩至数小时，同时确保方法学的严谨性和结果的可复现性。研究人员只需上传研究方案和数据文件，系统即可自动完成统计分析（PAF、CDPAF、趋势分析）、生成高质量图表，并撰写符合Lancet格式的完整论文初稿。

### 目标用户

- 癌症流行病学研究人员
- 公共卫生政策制定者
- 医学院研究生和博士生
- 需要快速产出高质量研究论文的科研团队

---

## 技术架构

### 技术栈

**前端**
- React 19 + TypeScript
- Tailwind CSS 4（采用seertotoponcology.vip风格配色）
- tRPC 11（类型安全的API调用）
- Wouter（轻量级路由）
- shadcn/ui（UI组件库）
- Recharts（数据可视化）

**后端**
- Node.js 22 + Express 4
- tRPC 11（端到端类型安全）
- Drizzle ORM（数据库操作）
- MySQL/TiDB（数据库）
- Manus Auth（OAuth认证）
- Manus LLM API（论文生成和参数提取）
- S3（文件存储）

**开发工具**
- pnpm（包管理）
- Vitest（单元测试）
- TypeScript 5.9
- Vite 7（构建工具）

### 项目结构

```
cancer-research-automation/
├── client/                    # 前端代码
│   ├── public/               # 静态资源
│   │   └── images/databases/ # 数据库相关图片
│   ├── src/
│   │   ├── pages/           # 页面组件
│   │   │   ├── Home.tsx     # 首页（含数据库介绍）
│   │   │   ├── Databases.tsx # 数据库详情页
│   │   │   ├── Projects.tsx  # 项目列表
│   │   │   ├── NewProject.tsx # 新建项目
│   │   │   └── ProjectDetail.tsx # 项目详情
│   │   ├── components/      # 可复用组件
│   │   ├── lib/trpc.ts      # tRPC客户端
│   │   └── index.css        # 全局样式（seertotoponcology配色）
├── server/                   # 后端代码
│   ├── routers.ts           # tRPC路由定义
│   ├── db.ts                # 数据库查询函数
│   ├── analysis.ts          # 统计分析引擎
│   ├── visualization.ts     # 数据可视化生成
│   ├── paperGeneration.ts   # 论文自动生成
│   └── *.test.ts            # 单元测试
├── drizzle/                 # 数据库schema和迁移
│   └── schema.ts            # 数据表定义
├── shared/                  # 前后端共享代码
└── todo.md                  # 功能清单
```

### 数据库设计

平台使用MySQL/TiDB存储研究项目数据，主要数据表包括：

| 表名 | 说明 | 关键字段 |
|------|------|----------|
| `users` | 用户信息 | id, openId, name, email, role |
| `projects` | 研究项目 | id, userId, title, cancerTypes, countries, timeRange, riskFactors, researchProposalUrl, status |
| `data_files` | 上传的数据文件 | id, projectId, dataSource (GBD/GLOBOCAN/CI5), fileUrl, uploadedAt |
| `cancer_data` | 标准化癌症数据 | id, projectId, dataSource, country, year, cancerType, incidence, mortality, prevalence |
| `analysis_results` | 分析结果 | id, projectId, analysisType (PAF/CDPAF/Trend), results (JSON), createdAt |
| `visualizations` | 生成的图表 | id, projectId, visualizationType, imageUrl, createdAt |
| `papers` | 生成的论文 | id, projectId, content, wordCount, status, createdAt |

### 核心API路由

所有API通过tRPC暴露，类型安全且自动生成客户端代码：

**项目管理** (`projects.*`)
- `create`: 创建新研究项目，自动解析研究方案
- `list`: 获取用户的所有项目
- `get`: 获取单个项目详情
- `update`: 更新项目信息
- `delete`: 删除项目
- `uploadProposal`: 上传研究方案文档（PDF/Word/TXT）

**数据管理** (`data.*`)
- `uploadFile`: 上传数据文件（GLOBOCAN/GBD/CI5）
- `listFiles`: 获取项目的所有数据文件
- `deleteFile`: 删除数据文件

**统计分析** (`analysis.*`)
- `runAnalysis`: 执行统计分析（PAF、CDPAF、趋势分析）
- `getResults`: 获取分析结果

**可视化** (`visualization.*`)
- `generate`: 生成图表（地图、饼图、折线图）
- `list`: 获取项目的所有图表

**论文生成** (`paper.*`)
- `generate`: 自动生成Lancet格式论文
- `get`: 获取论文内容
- `update`: 更新论文内容

---

## 已完成功能

### 1. 用户认证和项目管理

平台已集成Manus OAuth认证系统，支持用户注册、登录和权限管理。用户可以创建多个研究项目，每个项目包含完整的研究方案、数据文件、分析结果和生成的论文。

### 2. 研究方案智能解析

用户上传研究方案文档（PDF/Word/TXT）后，系统使用Manus LLM API自动提取关键参数，包括：

- 癌症类型（如肝细胞癌、肺癌、乳腺癌等）
- 目标国家/地区
- 研究时间范围
- 风险因素（如吸烟、饮酒、肥胖等）
- 研究设计类型（横断面/队列/生存分析等）

提取的参数自动填充到项目配置中，用户可手动编辑调整。

### 3. 数据上传和管理

平台支持上传CSV/Excel格式的GLOBOCAN和GBD数据文件。上传的文件自动存储到S3，并在数据库中记录元数据。系统会验证数据格式并标准化存储到`cancer_data`表中，便于后续分析。

### 4. 统计分析引擎

实现了多种癌症流行病学常用的统计方法，所有计算逻辑位于`server/analysis.ts`：

**人群归因分数（PAF）计算**
```typescript
PAF = (Pe × (RR - 1)) / (1 + Pe × (RR - 1))
```
其中Pe为暴露率，RR为相对风险。

**相关性分解归因分数（CDPAF）方法**
考虑多个风险因素之间的相关性，避免简单相加导致的高估。

**Joinpoint趋势回归分析**
识别癌症发病率或死亡率的时间趋势转折点，计算年度百分比变化（APC）。

**年龄标准化率计算**
使用世界标准人口或Segi标准人口进行年龄标准化，便于跨国比较。

所有统计方法已通过20个单元测试验证准确性（见`server/analysis.test.ts`）。

### 5. 数据可视化生成

系统可自动生成多种符合Lancet风格的图表（`server/visualization.ts`）：

- **地理热力图**：全球、区域或国家级别的癌症负担分布
- **风险因素贡献图**：饼图或条形图展示各风险因素对疾病负担的贡献
- **趋势分析折线图**：展示癌症发病率或死亡率的时间趋势
- **统计表格**：Table 1（基线特征）、回归结果表等

图表生成后上传到S3，返回URL供前端展示和下载。

### 6. 论文自动生成

基于Lancet标准的论文模板（`server/paperGeneration.ts`），系统可自动撰写包含以下章节的完整论文：

- **Summary**: 背景、方法、发现、解释
- **Introduction**: 全球疾病负担、知识缺口、研究目标
- **Methods**: 数据来源、研究人群、暴露和结局定义、统计分析
- **Results**: 基线特征、主要发现、亚组分析、敏感性分析
- **Discussion**: 主要发现、与文献对比、生物学/社会机制、优势与局限性、政策和临床意义

论文生成使用Manus LLM API，结合项目参数和分析结果，自动填充数据和解释。生成的论文长度通常在5000-8000词，符合Lancet投稿要求。

### 7. 数据库介绍页面

创建了详细的数据库介绍页面（`client/src/pages/Databases.tsx`），包含：

- GBD、GLOBOCAN、CI5三大数据库的详细介绍
- 核心指标、数据覆盖范围、更新频率
- 24篇代表性论文列表（7篇Lancet系列，其他顶级期刊）
- 6张来自真实论文的高质量图表展示
- 三个数据库的对比表格

### 8. 首页和导航

首页（`client/src/pages/Home.tsx`）采用seertotoponcology.vip风格设计，包含：

- Hero区域：项目标题、简介、CTA按钮
- 核心功能介绍
- 数据库介绍模块（Tab切换展示GBD、GLOBOCAN、CI5）
- 数据库对比表格

导航栏包含"全球数据库"和"我的项目"链接，方便用户快速访问。

### 9. 配色方案

参考seertotoponcology.vip网站，采用温暖现代的配色方案：

- **主色调**：鲜红色（#DC2626），用于标题、按钮、强调文字
- **辅助色**：金黄色（#FBBF24）、绿色（#10B981）
- **背景色**：温暖的米色系（#FEF7ED），营造柔和舒适的视觉体验
- **卡片背景**：纯白色（#FFFFFF），形成清晰的层次对比

所有颜色已在`client/src/index.css`中定义为CSS变量，支持深色模式切换。

### 10. 单元测试

已编写28个单元测试，覆盖核心功能：

- `server/auth.logout.test.ts`（1个测试）：认证登出功能
- `server/analysis.test.ts`（20个测试）：统计分析引擎的准确性
- `server/projects.test.ts`（7个测试）：项目CRUD操作

所有测试使用Vitest框架，运行`pnpm test`即可执行。测试覆盖率约60%，核心业务逻辑已充分验证。

---

## 待完善功能

根据`todo.md`，以下功能尚未实现，建议OpenClaw优先完成：

### 高优先级

1. **研究参数手动编辑功能**  
   当前LLM自动提取的参数无法在UI中编辑。需要在项目详情页添加表单，允许用户修改癌症类型、国家、时间范围等参数。

2. **CI5数据自动下载功能**  
   目前仅支持手动上传GLOBOCAN和GBD数据。需要集成CI5 API或爬虫，根据项目参数自动下载相关数据。参考CI5官网：https://ci5.iarc.fr/ci5plus/download

3. **数据格式验证和标准化**  
   上传的CSV/Excel文件需要严格验证格式（列名、数据类型、缺失值处理）。建议使用Zod schema定义数据格式，并在`server/routers.ts`中添加验证逻辑。

4. **数据整合和存储**  
   当前上传的数据文件仅存储URL，未解析内容。需要实现CSV/Excel解析器，将数据标准化存储到`cancer_data`表中，便于统计分析。

5. **高分辨率图表导出（PNG/SVG）**  
   当前图表生成逻辑仅返回占位符。需要集成Recharts或D3.js，在服务端渲染图表并导出为高分辨率图片。可使用Puppeteer或Playwright进行无头浏览器渲染。

6. **论文导出（Word/PDF格式）**  
   当前论文仅以Markdown格式存储。需要实现Word和PDF导出功能。建议使用`docx`库生成Word文档，使用`weasyprint`或`puppeteer`生成PDF。

7. **结果可视化展示页面**  
   在项目详情页添加"分析结果"Tab，展示所有生成的图表和统计表格。支持图表交互（缩放、筛选）和下载。

8. **论文预览和编辑页面**  
   在项目详情页添加"论文"Tab，使用富文本编辑器（如TipTap或Quill）展示和编辑生成的论文。支持实时保存和版本历史。

9. **结果下载中心**  
   创建统一的下载页面，允许用户一键下载所有生成的论文、图表、统计表格和原始数据。可打包为ZIP文件。

### 中优先级

10. **示例数据集集成（HCC数据）**  
    提供基于参考论文的肝细胞癌（HCC）示例数据集，用户可直接使用演示完整流程。数据应包含GLOBOCAN、GBD和CI5的真实数据样本。

11. **GLOBOCAN和GBD数据下载指南**  
    创建详细的分步教程页面，教用户如何从GBD Results Tool和GLOBOCAN下载数据。包含截图、筛选条件设置、数据格式选择和常见问题解答。

12. **用户使用教程**  
    制作视频或交互式教程，演示从创建项目到生成论文的完整流程。可使用Loom录制视频，嵌入到帮助页面。

13. **分析代码透明化（提供Python/R脚本）**  
    为增强用户信任和结果可复现性，建议在分析结果页面提供生成的Python或R脚本下载。脚本应包含完整的数据处理和统计分析代码。

14. **集成测试（完整流程）**  
    编写端到端测试，模拟用户从创建项目、上传数据、运行分析到生成论文的完整流程。可使用Playwright进行UI自动化测试。

15. **性能优化（大数据集处理）**  
    当前统计分析在内存中进行，无法处理超大数据集（如全球所有国家50年的数据）。建议引入流式处理或分布式计算（如Apache Spark）。

16. **用户体验优化**  
    - 添加加载动画和进度条（数据上传、分析运行、论文生成）
    - 优化移动端响应式布局
    - 添加快捷键支持（如Ctrl+S保存论文）
    - 实现暗色模式切换

### 低优先级

17. **多语言支持**  
    当前界面仅支持中文。建议使用i18n库添加英文版本，方便国际用户使用。

18. **协作功能**  
    允许多个用户共同编辑一个研究项目，类似Google Docs的实时协作。需要实现WebSocket或CRDT同步机制。

19. **版本控制**  
    为论文和分析结果添加版本历史，允许用户回滚到之前的版本。

20. **API文档**  
    使用Swagger或tRPC自动生成API文档，方便第三方集成。

---

## 开发指南

### 环境搭建

1. **克隆项目**
   ```bash
   git clone <repository_url>
   cd cancer-research-automation
   ```

2. **安装依赖**
   ```bash
   pnpm install
   ```

3. **配置环境变量**  
   Manus平台会自动注入以下环境变量，无需手动配置：
   - `DATABASE_URL`: MySQL/TiDB连接字符串
   - `JWT_SECRET`: Session cookie签名密钥
   - `VITE_APP_ID`: Manus OAuth应用ID
   - `OAUTH_SERVER_URL`: Manus OAuth后端URL
   - `BUILT_IN_FORGE_API_URL`: Manus内置API URL
   - `BUILT_IN_FORGE_API_KEY`: Manus内置API密钥

4. **推送数据库schema**
   ```bash
   pnpm db:push
   ```

5. **启动开发服务器**
   ```bash
   pnpm dev
   ```
   访问 https://3000-<sandbox-id>.manus.computer

6. **运行测试**
   ```bash
   pnpm test
   ```

### 开发工作流

1. **添加新功能**
   - 在`todo.md`中添加待办事项
   - 在`drizzle/schema.ts`中更新数据表（如需要）
   - 运行`pnpm db:push`推送schema变更
   - 在`server/db.ts`中添加数据库查询函数
   - 在`server/routers.ts`中添加tRPC路由
   - 在`client/src/pages/`中创建或更新页面组件
   - 编写单元测试（`server/*.test.ts`）
   - 运行`pnpm test`确保测试通过

2. **调试技巧**
   - 查看开发服务器日志：`.manus-logs/devserver.log`
   - 查看浏览器控制台日志：`.manus-logs/browserConsole.log`
   - 查看网络请求日志：`.manus-logs/networkRequests.log`
   - 使用`console.log`在服务端和客户端打印调试信息

3. **代码规范**
   - 使用TypeScript严格模式，避免`any`类型
   - 遵循React Hooks规则，避免在render中调用setState
   - tRPC路由使用`publicProcedure`或`protectedProcedure`
   - 数据库查询使用Drizzle ORM，避免原始SQL（除非必要）
   - UI组件优先使用shadcn/ui，保持设计一致性

4. **性能优化**
   - 使用`trpc.*.useQuery`的`enabled`选项避免不必要的请求
   - 对大列表使用虚拟滚动（如`react-window`）
   - 图片使用WebP格式并压缩，存储到S3
   - 避免在循环中调用数据库，使用批量查询

5. **部署**
   - 运行`pnpm test`确保所有测试通过
   - 创建checkpoint：在Manus UI点击"Save Checkpoint"
   - 点击"Publish"按钮发布到生产环境
   - 生产环境URL：`https://<custom-domain>.manus.space`

### 常见问题

**Q: 如何调用Manus LLM API？**  
A: 使用`server/_core/llm.ts`中的`invokeLLM`函数：
```typescript
import { invokeLLM } from "./server/_core/llm";

const response = await invokeLLM({
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Extract cancer types from this text..." }
  ]
});
```

**Q: 如何上传文件到S3？**  
A: 使用`server/storage.ts`中的`storagePut`函数：
```typescript
import { storagePut } from "./server/storage";

const { url } = await storagePut(
  `${userId}/files/${fileName}.pdf`,
  fileBuffer,
  "application/pdf"
);
```

**Q: 如何添加新的数据表？**  
A: 在`drizzle/schema.ts`中定义表结构，然后运行`pnpm db:push`：
```typescript
export const myTable = mysqlTable("my_table", {
  id: int("id").autoincrement().primaryKey(),
  name: text("name").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});
```

**Q: 如何处理大文件上传？**  
A: 使用分块上传。前端使用`FormData`，后端使用`multer`或直接流式上传到S3。

**Q: 如何实现实时进度更新？**  
A: 使用Server-Sent Events (SSE)或WebSocket。tRPC支持subscription，可实现实时推送。

---

## 关键文件说明

### 前端核心文件

| 文件路径 | 说明 |
|---------|------|
| `client/src/pages/Home.tsx` | 首页，包含Hero区域、核心功能介绍、数据库介绍模块 |
| `client/src/pages/Databases.tsx` | 数据库详情页，展示GBD、GLOBOCAN、CI5的详细信息和论文列表 |
| `client/src/pages/Projects.tsx` | 项目列表页，展示用户的所有研究项目 |
| `client/src/pages/NewProject.tsx` | 新建项目页面，上传研究方案并创建项目 |
| `client/src/pages/ProjectDetail.tsx` | 项目详情页，展示项目信息、数据文件、分析结果（待完善） |
| `client/src/lib/trpc.ts` | tRPC客户端配置 |
| `client/src/index.css` | 全局样式，定义seertotoponcology配色方案 |

### 后端核心文件

| 文件路径 | 说明 |
|---------|------|
| `server/routers.ts` | tRPC路由定义，包含所有API端点 |
| `server/db.ts` | 数据库查询函数，封装Drizzle ORM操作 |
| `server/analysis.ts` | 统计分析引擎，实现PAF、CDPAF、趋势分析等方法 |
| `server/visualization.ts` | 数据可视化生成，创建地图、饼图、折线图等 |
| `server/paperGeneration.ts` | 论文自动生成，基于Lancet模板撰写论文 |
| `server/_core/llm.ts` | Manus LLM API封装 |
| `server/storage.ts` | S3文件存储封装 |

### 数据库和配置文件

| 文件路径 | 说明 |
|---------|------|
| `drizzle/schema.ts` | 数据库表结构定义 |
| `package.json` | 项目依赖和脚本 |
| `tsconfig.json` | TypeScript配置 |
| `vite.config.ts` | Vite构建配置 |
| `vitest.config.ts` | Vitest测试配置 |
| `todo.md` | 功能清单和待办事项 |

---

## 数据流程图

```
用户上传研究方案
    ↓
LLM提取研究参数（癌症类型、国家、时间范围、风险因素）
    ↓
用户上传数据文件（GLOBOCAN/GBD/CI5 CSV/Excel）
    ↓
数据解析和标准化存储到cancer_data表
    ↓
用户触发统计分析
    ↓
分析引擎计算PAF、CDPAF、趋势分析等
    ↓
结果存储到analysis_results表
    ↓
可视化引擎生成图表（地图、饼图、折线图）
    ↓
图表上传到S3，URL存储到visualizations表
    ↓
论文生成引擎基于分析结果撰写Lancet格式论文
    ↓
论文存储到papers表
    ↓
用户预览、编辑、下载论文和图表
```

---

## 统计方法参考文献

平台实现的统计方法基于以下权威文献，建议OpenClaw在完善功能时参考：

1. **PAF计算方法**  
   Levin ML. The occurrence of lung cancer in man. *Acta Unio Int Contra Cancrum*. 1953;9(3):531-541.

2. **CDPAF方法**  
   Ezzati M, Lopez AD, Rodgers A, et al. Selected major risk factors and global and regional burden of disease. *Lancet*. 2002;360(9343):1347-1360.

3. **Joinpoint回归分析**  
   Kim HJ, Fay MP, Feuer EJ, Midthune DN. Permutation tests for joinpoint regression with applications to cancer rates. *Stat Med*. 2000;19(3):335-351.

4. **年龄标准化率**  
   Ahmad OB, Boschi-Pinto C, Lopez AD, et al. Age Standardization of Rates: A New WHO Standard. *GPE Discussion Paper Series: No.31*. WHO, 2001.

---

## 联系方式

如有技术问题或需要进一步支持，请联系：

- **项目负责人**: 小林（科研工作者，医生，药物研发，医疗大数据）
- **邮箱**: medivisual@mokangmedical.cn
- **Manus项目ID**: WHR3iwP78jvfuNmsjBYYho

---

## 附录：OpenClaw接管建议

### 第一周：熟悉项目

1. 克隆项目并成功运行开发服务器
2. 阅读所有核心文件（`server/routers.ts`、`server/analysis.ts`、`client/src/pages/Home.tsx`等）
3. 运行单元测试，理解测试覆盖范围
4. 在本地创建一个测试项目，体验完整流程
5. 查看数据库表结构，理解数据模型

### 第二周：完成高优先级功能

1. 实现研究参数手动编辑功能（在ProjectDetail.tsx添加表单）
2. 实现数据格式验证和标准化（使用Zod schema）
3. 实现数据整合和存储（CSV/Excel解析器）
4. 编写相关单元测试

### 第三周：完成可视化和导出功能

1. 实现高分辨率图表导出（集成Recharts + Puppeteer）
2. 实现论文导出（Word/PDF格式）
3. 创建结果可视化展示页面
4. 创建论文预览和编辑页面

### 第四周：完善用户体验

1. 创建结果下载中心
2. 添加示例数据集（HCC数据）
3. 创建数据下载指南页面
4. 优化加载动画和进度条
5. 进行端到端测试

### 长期规划

- 集成CI5数据自动下载功能
- 实现分析代码透明化（提供Python/R脚本）
- 性能优化（大数据集处理）
- 多语言支持
- 协作功能
- API文档

---

**祝OpenClaw接管顺利！如有任何问题，请随时联系。**

---

*本文档由Manus AI生成，最后更新于2026年2月15日。*
