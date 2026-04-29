import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  FileText, 
  Database, 
  BarChart3, 
  FileCheck, 
  TrendingUp, 
  Globe,
  ArrowRight,
  CheckCircle2,
  ExternalLink
} from "lucide-react";
import { Link } from "wouter";
import { getLoginUrl } from "@/const";
import { useState } from "react";

export default function Home() {
  const { user, loading, isAuthenticated } = useAuth();
  const [activeTab, setActiveTab] = useState("gbd");

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Navigation Bar */}
      <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-6">
            <Link href="/">
              <span className="text-xl font-bold text-primary cursor-pointer">Cancer Research To Lancet</span>
            </Link>
            <div className="hidden md:flex items-center gap-6">
              <Link href="/databases">
                <a className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors cursor-pointer">
                  全球数据库
                </a>
              </Link>
              {isAuthenticated && (
                <Link href="/projects">
                  <a className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors cursor-pointer">
                    我的项目
                  </a>
                </Link>
              )}
            </div>
          </div>
          <div>
            {isAuthenticated ? (
              <Link href="/projects/new">
                <Button size="sm">创建项目</Button>
              </Link>
            ) : (
              <Button asChild size="sm">
                <a href={getLoginUrl()}>登录</a>
              </Button>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="container py-16 md:py-24">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6">
            Cancer Epidemiology Research
            <span className="block text-primary mt-2">To Lancet</span>
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            从数据收集到论文撰写的全流程自动化处理。整合Global Burden of Disease (GBD)、GLOBOCAN、Cancer Incidence in Five Continents (CI5)三大权威数据库，自动生成统计分析和符合Lancet标准的研究论文。
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            {isAuthenticated ? (
              <Link href="/projects">
                <Button size="lg" className="gap-2">
                  进入我的项目
                  <ArrowRight className="w-5 h-5" />
                </Button>
              </Link>
            ) : (
              <Button asChild size="lg" className="gap-2">
                <a href={getLoginUrl()}>
                  开始使用
                  <ArrowRight className="w-5 h-5" />
                </a>
              </Button>
            )}
            <Link href="/databases">
              <Button variant="outline" size="lg">
                了解数据库
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="container py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-foreground mb-4">核心功能</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            专业的癌症流行病学研究自动化工具，帮助研究人员提高效率，确保学术标准
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Feature 1 */}
          <Card className="border-2 hover:border-primary transition-colors">
            <CardHeader>
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <FileText className="w-6 h-6 text-primary" />
              </div>
              <CardTitle>研究方案解析</CardTitle>
              <CardDescription>
                上传研究方案文档，系统自动提取癌症类型、地区、时间范围、风险因素等关键参数
              </CardDescription>
            </CardHeader>
          </Card>

          {/* Feature 2 */}
          <Card className="border-2 hover:border-primary transition-colors">
            <CardHeader>
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <Database className="w-6 h-6 text-primary" />
              </div>
              <CardTitle>多数据源整合</CardTitle>
              <CardDescription>
                支持GLOBOCAN、GBD、CI5数据库的数据上传和自动下载，统一标准化处理
              </CardDescription>
            </CardHeader>
          </Card>

          {/* Feature 3 */}
          <Card className="border-2 hover:border-primary transition-colors">
            <CardHeader>
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <BarChart3 className="w-6 h-6 text-primary" />
              </div>
              <CardTitle>统计分析引擎</CardTitle>
              <CardDescription>
                实现PAF、CDPAF、相对风险计算、Joinpoint趋势分析等核心流行病学方法
              </CardDescription>
            </CardHeader>
          </Card>

          {/* Feature 4 */}
          <Card className="border-2 hover:border-primary transition-colors">
            <CardHeader>
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <TrendingUp className="w-6 h-6 text-primary" />
              </div>
              <CardTitle>数据可视化</CardTitle>
              <CardDescription>
                自动生成地理热力图、风险因素贡献图、趋势分析图表，支持高分辨率导出
              </CardDescription>
            </CardHeader>
          </Card>

          {/* Feature 5 */}
          <Card className="border-2 hover:border-primary transition-colors">
            <CardHeader>
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <FileCheck className="w-6 h-6 text-primary" />
              </div>
              <CardTitle>论文自动生成</CardTitle>
              <CardDescription>
                基于分析结果自动撰写符合Lancet标准的5000词以上英文论文，包含完整章节
              </CardDescription>
            </CardHeader>
          </Card>

          {/* Feature 6 */}
          <Card className="border-2 hover:border-primary transition-colors">
            <CardHeader>
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <Globe className="w-6 h-6 text-primary" />
              </div>
              <CardTitle>全球数据覆盖</CardTitle>
              <CardDescription>
                支持全球185个国家和地区的癌症数据分析，提供区域和国家级别的深度洞察
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </div>

      {/* Workflow Section */}
      <div className="container py-16">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-4">工作流程</h2>
            <p className="text-muted-foreground">
              简单四步，完成从数据到论文的全流程
            </p>
          </div>

          <div className="space-y-6">
            {[
              {
                step: 1,
                title: "创建研究项目",
                description: "上传研究方案或手动输入研究参数，系统自动解析关键信息",
              },
              {
                step: 2,
                title: "上传和整合数据",
                description: "上传GLOBOCAN、GBD数据文件，系统自动下载CI5数据并标准化处理",
              },
              {
                step: 3,
                title: "运行统计分析",
                description: "一键运行PAF计算、趋势分析等统计方法，生成可视化图表",
              },
              {
                step: 4,
                title: "生成研究论文",
                description: "自动撰写符合Lancet标准的完整论文，支持Word和PDF格式导出",
              },
            ].map((item) => (
              <Card key={item.step} className="border-l-4 border-l-primary">
                <CardContent className="flex items-start gap-4 p-6">
                  <div className="w-10 h-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold text-lg flex-shrink-0">
                    {item.step}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold mb-1">{item.title}</h3>
                    <p className="text-muted-foreground">{item.description}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>

      {/* Database Introduction Section */}
      <div className="container py-16 bg-gradient-to-br from-primary/5 to-background">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-4">三大权威癌症数据库</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              整合全球最权威的癌症流行病学数据库，为您的研究提供坚实的数据基础
            </p>
          </div>

          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-3 mb-8">
              <TabsTrigger value="gbd">Global Burden of Disease</TabsTrigger>
              <TabsTrigger value="globocan">GLOBOCAN</TabsTrigger>
              <TabsTrigger value="ci5">CI5</TabsTrigger>
            </TabsList>

            {/* GBD Tab */}
            <TabsContent value="gbd" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    Global Burden of Disease (GBD)
                    <a href="https://vizhub.healthdata.org/gbd-results/" target="_blank" rel="noopener noreferrer" className="text-primary hover:text-primary/80">
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </CardTitle>
                  <CardDescription>
                    由美国华盛顿大学健康指标与评估研究所（IHME）主导的全球疾病负担研究项目
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-semibold mb-2">核心指标</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <div className="text-2xl font-bold text-primary">369</div>
                        <div className="text-xs text-muted-foreground">疾病和伤害</div>
                      </div>
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <div className="text-2xl font-bold text-primary">204</div>
                        <div className="text-xs text-muted-foreground">国家和地区</div>
                      </div>
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <div className="text-2xl font-bold text-primary">1990-2021</div>
                        <div className="text-xs text-muted-foreground">时间跨度</div>
                      </div>
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <div className="text-2xl font-bold text-primary">87</div>
                        <div className="text-xs text-muted-foreground">风险因素</div>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">数据覆盖范围</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• 癌症发病率、死亡率、患病率、伤残调整生命年（DALYs）</li>
                      <li>• 按年龄、性别、地区分层的详细数据</li>
                      <li>• 87种风险因素的归因分析</li>
                      <li>• 支持全球、区域、国家级别的数据查询</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">代表性论文</h4>
                    <div className="space-y-2 text-sm">
                      <div className="p-3 bg-muted/30 rounded-lg">
                        <div className="font-medium">Global Burden of Disease 2021 Cancer Collaboration</div>
                        <div className="text-muted-foreground">The Lancet (2024) | 引用次数: 1,200+</div>
                      </div>
                      <div className="p-3 bg-muted/30 rounded-lg">
                        <div className="font-medium">Global burden of 369 diseases and injuries in 204 countries</div>
                        <div className="text-muted-foreground">The Lancet (2020) | 引用次数: 25,000+</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* GLOBOCAN Tab */}
            <TabsContent value="globocan" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    GLOBOCAN
                    <a href="https://gco.iarc.fr/" target="_blank" rel="noopener noreferrer" className="text-primary hover:text-primary/80">
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </CardTitle>
                  <CardDescription>
                    由国际癌症研究机构（IARC）维护的全球癌症观察站数据库
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-semibold mb-2">核心指标</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <div className="text-2xl font-bold text-primary">36</div>
                        <div className="text-xs text-muted-foreground">癌症类型</div>
                      </div>
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <div className="text-2xl font-bold text-primary">185</div>
                        <div className="text-xs text-muted-foreground">国家和地区</div>
                      </div>
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <div className="text-2xl font-bold text-primary">2022</div>
                        <div className="text-xs text-muted-foreground">最新数据年份</div>
                      </div>
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <div className="text-2xl font-bold text-primary">20M+</div>
                        <div className="text-xs text-muted-foreground">年新增病例</div>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">数据覆盖范围</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• 癌症发病率、死亡率、5年患病率估计</li>
                      <li>• 按性别、年龄组分层的详细数据</li>
                      <li>• 全球、区域、国家级别的癌症统计</li>
                      <li>• 未来癌症负担预测（2025-2050）</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">代表性论文</h4>
                    <div className="space-y-2 text-sm">
                      <div className="p-3 bg-muted/30 rounded-lg">
                        <div className="font-medium">Global cancer statistics 2022: GLOBOCAN estimates</div>
                        <div className="text-muted-foreground">CA: A Cancer Journal for Clinicians (2024) | IF: 503.1</div>
                      </div>
                      <div className="p-3 bg-muted/30 rounded-lg">
                        <div className="font-medium">Global cancer statistics 2020: GLOBOCAN estimates</div>
                        <div className="text-muted-foreground">CA: A Cancer Journal for Clinicians (2021) | 引用次数: 15,000+</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* CI5 Tab */}
            <TabsContent value="ci5" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    Cancer Incidence in Five Continents (CI5)
                    <a href="https://ci5.iarc.fr/" target="_blank" rel="noopener noreferrer" className="text-primary hover:text-primary/80">
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </CardTitle>
                  <CardDescription>
                    由IARC编制的全球癌症登记数据汇编，被认为是癌症发病率数据的金标准
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-semibold mb-2">核心指标</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <div className="text-2xl font-bold text-primary">XII</div>
                        <div className="text-xs text-muted-foreground">最新卷次</div>
                      </div>
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <div className="text-2xl font-bold text-primary">290+</div>
                        <div className="text-xs text-muted-foreground">癌症登记处</div>
                      </div>
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <div className="text-2xl font-bold text-primary">2013-2017</div>
                        <div className="text-xs text-muted-foreground">数据时间段</div>
                      </div>
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <div className="text-2xl font-bold text-primary">60+</div>
                        <div className="text-xs text-muted-foreground">年出版历史</div>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">数据覆盖范围</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• 基于人群的癌症登记数据，数据质量最高</li>
                      <li>• 详细的癌症发病率数据，按ICD-10分类</li>
                      <li>• 按年龄、性别、组织学类型分层</li>
                      <li>• 涵盖五大洲的代表性癌症登记处</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">代表性论文</h4>
                    <div className="space-y-2 text-sm">
                      <div className="p-3 bg-muted/30 rounded-lg">
                        <div className="font-medium">Cancer Incidence in Five Continents Vol. XII</div>
                        <div className="text-muted-foreground">IARC Scientific Publication (2021)</div>
                      </div>
                      <div className="p-3 bg-muted/30 rounded-lg">
                        <div className="font-medium">International variation in prostate cancer incidence</div>
                        <div className="text-muted-foreground">The Lancet Oncology (2023) | 引用次数: 800+</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          {/* Comparison Table */}
          <Card className="mt-8">
            <CardHeader>
              <CardTitle>三大数据库对比</CardTitle>
              <CardDescription>快速了解各数据库的特点和适用场景</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left p-3 font-semibold">特征</th>
                      <th className="text-left p-3 font-semibold">GBD</th>
                      <th className="text-left p-3 font-semibold">GLOBOCAN</th>
                      <th className="text-left p-3 font-semibold">CI5</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="border-b">
                      <td className="p-3 font-medium">数据来源</td>
                      <td className="p-3 text-muted-foreground">多源数据建模估计</td>
                      <td className="p-3 text-muted-foreground">癌症登记+建模估计</td>
                      <td className="p-3 text-muted-foreground">高质量癌症登记数据</td>
                    </tr>
                    <tr className="border-b">
                      <td className="p-3 font-medium">地理覆盖</td>
                      <td className="p-3 text-muted-foreground">204个国家和地区</td>
                      <td className="p-3 text-muted-foreground">185个国家和地区</td>
                      <td className="p-3 text-muted-foreground">290+癌症登记处</td>
                    </tr>
                    <tr className="border-b">
                      <td className="p-3 font-medium">时间跨度</td>
                      <td className="p-3 text-muted-foreground">1990-2021（年度）</td>
                      <td className="p-3 text-muted-foreground">2022（最新）</td>
                      <td className="p-3 text-muted-foreground">2013-2017（5年）</td>
                    </tr>
                    <tr className="border-b">
                      <td className="p-3 font-medium">核心优势</td>
                      <td className="p-3 text-muted-foreground">长时间趋势分析</td>
                      <td className="p-3 text-muted-foreground">全球最新估计</td>
                      <td className="p-3 text-muted-foreground">数据质量最高</td>
                    </tr>
                    <tr>
                      <td className="p-3 font-medium">适用场景</td>
                      <td className="p-3 text-muted-foreground">疾病负担、趋势分析</td>
                      <td className="p-3 text-muted-foreground">全球癌症概况</td>
                      <td className="p-3 text-muted-foreground">国际比较研究</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>

          <div className="mt-8 text-center">
            <Link href="/databases">
              <Button size="lg" variant="outline" className="gap-2">
                查看详细介绍和论文图表
                <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Benefits Section */}
      <div className="container py-16">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl">为什么选择我们的平台？</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  "节省数据处理和分析时间，提高研究效率",
                  "确保统计方法的准确性和学术标准",
                  "自动生成符合顶级期刊要求的论文",
                  "提供完整的分析代码，保证研究可重复性",
                  "支持多数据源整合，数据更全面",
                  "实时追踪分析进度，随时掌握项目状态",
                ].map((benefit, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <CheckCircle2 className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                    <span className="text-sm">{benefit}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* CTA Section */}
      <div className="container py-16">
        <Card className="max-w-3xl mx-auto text-center bg-gradient-to-br from-primary to-primary/80 text-primary-foreground border-0">
          <CardContent className="py-12">
            <h2 className="text-3xl font-bold mb-4">准备开始您的研究？</h2>
            <p className="text-primary-foreground/90 mb-8 text-lg">
              立即创建您的第一个癌症流行病学研究项目
            </p>
            {isAuthenticated ? (
              <Link href="/projects/new">
                <Button size="lg" variant="secondary" className="gap-2">
                  创建新项目
                  <ArrowRight className="w-5 h-5" />
                </Button>
              </Link>
            ) : (
              <Button asChild size="lg" variant="secondary" className="gap-2">
                <a href={getLoginUrl()}>
                  开始使用
                  <ArrowRight className="w-5 h-5" />
                </a>
              </Button>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
