import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { ExternalLink, Database, Globe, BarChart3, TrendingUp, Map, BookOpen } from "lucide-react";

export default function Databases() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-rose-50 to-pink-50">
      {/* Header */}
      <div className="bg-white border-b border-border">
        <div className="container py-12">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
              全球癌症数据库
            </h1>
            <p className="text-xl text-muted-foreground">
              三大权威数据源支撑您的流行病学研究
            </p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container py-12">
        <Tabs defaultValue="gbd" className="space-y-8">
          <TabsList className="grid w-full max-w-3xl mx-auto grid-cols-3 bg-white">
            <TabsTrigger value="gbd">GBD</TabsTrigger>
            <TabsTrigger value="globocan">GLOBOCAN</TabsTrigger>
            <TabsTrigger value="ci5">CI5</TabsTrigger>
          </TabsList>

          {/* GBD Tab */}
          <TabsContent value="gbd" className="space-y-8">
            <div className="max-w-5xl mx-auto">
              {/* Overview Card */}
              <Card className="border-2 border-primary/20">
                <CardHeader>
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                      <Globe className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <CardTitle className="text-2xl">Global Burden of Disease (GBD)</CardTitle>
                      <CardDescription className="text-base">
                        Institute for Health Metrics and Evaluation (IHME)
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="prose max-w-none">
                    <p className="text-base leading-relaxed">
                      <strong>Global Burden of Disease (GBD)</strong> 研究是由华盛顿大学健康指标与评估研究所（IHME）主导的全球最全面的流行病学研究项目。该研究系统性地量化了全球204个国家和地区的疾病负担，涵盖369种疾病和伤害、87种风险因素。GBD数据库提供了从1990年至今的长期趋势数据，是评估全球健康状况变化的金标准。
                    </p>
                    
                    <h3 className="text-lg font-semibold mt-6 mb-3">核心指标</h3>
                    <ul className="space-y-2">
                      <li><strong>发病率 (Incidence)</strong>：新发病例数及年龄标准化发病率</li>
                      <li><strong>患病率 (Prevalence)</strong>：现患病例数及比例</li>
                      <li><strong>死亡率 (Mortality)</strong>：死亡人数及年龄标准化死亡率</li>
                      <li><strong>伤残调整生命年 (DALYs)</strong>：综合衡量疾病负担的指标</li>
                      <li><strong>风险因素归因 (Risk Attribution)</strong>：各风险因素对疾病负担的贡献</li>
                    </ul>

                    <h3 className="text-lg font-semibold mt-6 mb-3">数据覆盖范围</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 not-prose">
                      <Card>
                        <CardContent className="pt-6">
                          <div className="text-center">
                            <p className="text-3xl font-bold text-primary">204</p>
                            <p className="text-sm text-muted-foreground mt-1">国家和地区</p>
                          </div>
                        </CardContent>
                      </Card>
                      <Card>
                        <CardContent className="pt-6">
                          <div className="text-center">
                            <p className="text-3xl font-bold text-primary">30+</p>
                            <p className="text-sm text-muted-foreground mt-1">癌症类型</p>
                          </div>
                        </CardContent>
                      </Card>
                      <Card>
                        <CardContent className="pt-6">
                          <div className="text-center">
                            <p className="text-3xl font-bold text-primary">1990-2023</p>
                            <p className="text-sm text-muted-foreground mt-1">时间跨度</p>
                          </div>
                        </CardContent>
                      </Card>
                    </div>
                  </div>

                  {/* Visualization */}
                  <div className="mt-8">
                    <h3 className="text-lg font-semibold mb-4">数据可视化示例</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="rounded-lg overflow-hidden border border-border">
                        <img
                          src="/images/databases/gbd-disease-burden-map.png"
                          alt="GBD Disease Burden Rates from All Cancers"
                          className="w-full h-auto"
                        />
                        <p className="text-xs text-muted-foreground p-2 bg-muted/30">
                          全球癌症疾病负担率分布图（2021）
                        </p>
                      </div>
                      <div className="rounded-lg overflow-hidden border border-border">
                        <img
                          src="/images/databases/gbd-cancer-burden-chart.png"
                          alt="GBD Global Burden of Cancer by Risk Factors"
                          className="w-full h-auto"
                        />
                        <p className="text-xs text-muted-foreground p-2 bg-muted/30">
                          全球癌症负担与风险因素分析
                        </p>
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground mt-3 text-center">
                      来源：Global Burden of Disease Study, IHME | Our World in Data
                    </p>
                  </div>

                  {/* Key Publications */}
                  <div className="mt-8">
                    <div className="flex items-center gap-2 mb-4">
                      <BookOpen className="w-5 h-5 text-primary" />
                      <h3 className="text-lg font-semibold">代表性论文</h3>
                    </div>
                    
                    <Accordion type="single" collapsible className="w-full">
                      {/* Lancet Series */}
                      <AccordionItem value="lancet">
                        <AccordionTrigger className="text-base font-semibold">
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-1 bg-primary/10 text-primary text-xs rounded">Lancet系列</span>
                            <span>5篇论文</span>
                          </div>
                        </AccordionTrigger>
                        <AccordionContent>
                          <div className="space-y-3 pt-2">
                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  The global, regional, and national burden of cancer, 1990-2023, with forecasts to 2050: a systematic analysis for the Global Burden of Disease Study 2023
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>The Lancet</em>, 2025 | DOI: 10.1016/S0140-6736(25)01635-6 | 引用: 56+
                                </p>
                                <p className="text-xs mt-2">
                                  GBD 2023最新癌症负担报告，涵盖204个国家和地区47种癌症类型，预测至2050年
                                </p>
                              </CardContent>
                            </Card>
                            
                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  The current and future global burden of cancer among adolescents and young adults
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>The Lancet Oncology</em>, 2024 | DOI: 10.1016/S1470-2045(24)00523-0 | 引用: 38+
                                </p>
                                <p className="text-xs mt-2">
                                  青少年和年轻成人癌症负担的全球评估
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Global burden of 87 risk factors in 204 countries and territories, 1990–2019: a systematic analysis for the Global Burden of Disease Study 2019
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>The Lancet</em>, 2020 | DOI: 10.1016/S0140-6736(20)30752-2
                                </p>
                                <p className="text-xs mt-2">
                                  GBD 2019风险因素系统分析，包括癌症相关风险因素
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Cancer in sub-Saharan Africa: a Lancet Oncology Commission
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>The Lancet Oncology</em>, 2021 | DOI: 10.1016/S1470-2045(21)00720-8
                                </p>
                                <p className="text-xs mt-2">
                                  撒哈拉以南非洲癌症负担专题报告
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Global burden of cancer attributable to infections in 2018: a worldwide incidence analysis
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>The Lancet Global Health</em>, 2020 | DOI: 10.1016/S2214-109X(19)30488-7
                                </p>
                                <p className="text-xs mt-2">
                                  全球感染相关癌症负担分析
                                </p>
                              </CardContent>
                            </Card>
                          </div>
                        </AccordionContent>
                      </AccordionItem>

                      {/* Other Top Journals */}
                      <AccordionItem value="other">
                        <AccordionTrigger className="text-base font-semibold">
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">其他顶级期刊</span>
                            <span>5篇论文</span>
                          </div>
                        </AccordionTrigger>
                        <AccordionContent>
                          <div className="space-y-3 pt-2">
                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  The global burden of cancer 2013
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>JAMA Oncology</em>, 2015 | DOI: 10.1001/jamaoncol.2015.0735
                                </p>
                                <p className="text-xs mt-2">
                                  GBD 2013全球癌症负担综合报告
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  The Global Burden of Disease Study at 30 years
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>Nature Medicine</em>, 2022 | DOI: 10.1038/s41591-022-01990-1
                                </p>
                                <p className="text-xs mt-2">
                                  GBD研究30年回顾与展望
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Global Disparities of Cancer and Its Projected Burden in 2050
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>JAMA Network Open</em>, 2024 | DOI: 10.1001/jamanetworkopen.2024.25637 | 引用: 213+
                                </p>
                                <p className="text-xs mt-2">
                                  基于GBD数据的2050年癌症负担预测
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Global burden of cancer and associated risk factors in 204 countries and territories, 1980–2021: a systematic analysis for the GBD 2021
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>Journal of Hematology & Oncology</em>, 2024 | DOI: 10.1186/s13045-024-01640-8
                                </p>
                                <p className="text-xs mt-2">
                                  GBD 2021癌症负担和风险因素系统分析
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Global burden of cancer in women, 1990–2021: a systematic analysis from the GBD 2021 study
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>Frontiers in Oncology</em>, 2024
                                </p>
                                <p className="text-xs mt-2">
                                  女性癌症负担的全球时空趋势分析
                                </p>
                              </CardContent>
                            </Card>
                          </div>
                        </AccordionContent>
                      </AccordionItem>
                    </Accordion>
                  </div>

                  {/* Access Button */}
                  <div className="flex gap-3 mt-8">
                    <Button asChild size="lg" className="gap-2">
                      <a href="https://vizhub.healthdata.org/gbd-results/" target="_blank" rel="noopener noreferrer">
                        <Database className="w-5 h-5" />
                        访问GBD数据库
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    </Button>
                    <Button asChild variant="outline" size="lg" className="gap-2">
                      <a href="https://www.healthdata.org/research-analysis/gbd" target="_blank" rel="noopener noreferrer">
                        了解更多
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* GLOBOCAN Tab */}
          <TabsContent value="globocan" className="space-y-8">
            <div className="max-w-5xl mx-auto">
              <Card className="border-2 border-primary/20">
                <CardHeader>
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                      <Map className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <CardTitle className="text-2xl">GLOBOCAN</CardTitle>
                      <CardDescription className="text-base">
                        Global Cancer Observatory - International Agency for Research on Cancer (IARC)
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="prose max-w-none">
                    <p className="text-base leading-relaxed">
                      <strong>GLOBOCAN</strong> 是由世界卫生组织国际癌症研究机构（IARC）开发和维护的全球癌症统计数据库。该数据库提供了185个国家和地区36种癌症类型的发病率、死亡率和患病率估计。GLOBOCAN每两年更新一次，是全球癌症流行病学研究的重要参考来源，被广泛应用于政策制定和资源分配。
                    </p>

                    <h3 className="text-lg font-semibold mt-6 mb-3">核心特点</h3>
                    <ul className="space-y-2">
                      <li><strong>全球覆盖</strong>：185个国家和地区的癌症数据</li>
                      <li><strong>多维度分析</strong>：按性别、年龄、癌症类型分层</li>
                      <li><strong>标准化方法</strong>：统一的估算方法确保数据可比性</li>
                      <li><strong>交互式可视化</strong>：在线工具支持自定义数据查询和图表生成</li>
                      <li><strong>定期更新</strong>：每两年发布最新全球癌症统计数据</li>
                    </ul>

                    <h3 className="text-lg font-semibold mt-6 mb-3">2022年全球癌症概况</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 not-prose">
                      <Card className="bg-primary/5">
                        <CardContent className="pt-6">
                          <div className="text-center">
                            <p className="text-3xl font-bold text-primary">20.0M</p>
                            <p className="text-sm text-muted-foreground mt-1">新发癌症病例</p>
                            <p className="text-xs text-muted-foreground mt-2">
                              较2020年增长10%
                            </p>
                          </div>
                        </CardContent>
                      </Card>
                      <Card className="bg-primary/5">
                        <CardContent className="pt-6">
                          <div className="text-center">
                            <p className="text-3xl font-bold text-primary">9.7M</p>
                            <p className="text-sm text-muted-foreground mt-1">癌症死亡人数</p>
                            <p className="text-xs text-muted-foreground mt-2">
                              全球第二大死因
                            </p>
                          </div>
                        </CardContent>
                      </Card>
                    </div>
                  </div>

                  {/* Visualization */}
                  <div className="mt-8">
                    <h3 className="text-lg font-semibold mb-4">全球癌症地图与统计</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="rounded-lg overflow-hidden border border-border">
                        <img
                          src="/images/databases/globocan-world-map.png"
                          alt="GLOBOCAN Global Cancer Incidence Map"
                          className="w-full h-auto"
                        />
                        <p className="text-xs text-muted-foreground p-2 bg-muted/30">
                          全球癌症发病率地理分布
                        </p>
                      </div>
                      <div className="rounded-lg overflow-hidden border border-border">
                        <img
                          src="/images/databases/globocan-women-cancer.jpg"
                          alt="Global Burden of Cancer in Women"
                          className="w-full h-auto"
                        />
                        <p className="text-xs text-muted-foreground p-2 bg-muted/30">
                          女性癌症负担全球分布（1990-2021）
                        </p>
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground mt-3 text-center">
                      来源：GLOBOCAN 2022, Global Cancer Observatory (IARC) | Frontiers in Oncology
                    </p>
                  </div>

                  {/* Key Publications */}
                  <div className="mt-8">
                    <div className="flex items-center gap-2 mb-4">
                      <BookOpen className="w-5 h-5 text-primary" />
                      <h3 className="text-lg font-semibold">代表性论文</h3>
                    </div>
                    
                    <Accordion type="single" collapsible className="w-full">
                      {/* CA Journal */}
                      <AccordionItem value="ca-journal">
                        <AccordionTrigger className="text-base font-semibold">
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-1 bg-amber-100 text-amber-800 text-xs rounded">CA: A Cancer Journal for Clinicians (IF&gt;500)</span>
                            <span>3篇论文</span>
                          </div>
                        </AccordionTrigger>
                        <AccordionContent>
                          <div className="space-y-3 pt-2">
                            <Card className="bg-amber-50/50 border-amber-200">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Global cancer statistics 2022: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>CA: A Cancer Journal for Clinicians</em>, 2024 | DOI: 10.3322/caac.21834 | 引用: 27,588+
                                </p>
                                <p className="text-xs mt-2">
                                  GLOBOCAN 2022最新全球癌症统计，2000万新发病例
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-amber-50/50 border-amber-200">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Global cancer statistics 2020: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>CA: A Cancer Journal for Clinicians</em>, 2021 | DOI: 10.3322/caac.21660 | 引用: 124,565+
                                </p>
                                <p className="text-xs mt-2">
                                  GLOBOCAN 2020全球癌症统计
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-amber-50/50 border-amber-200">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Global cancer statistics 2018: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>CA: A Cancer Journal for Clinicians</em>, 2018 | DOI: 10.3322/CAAC.21492 | 引用: 100,522+
                                </p>
                                <p className="text-xs mt-2">
                                  GLOBOCAN 2018全球癌症统计，被引用超过10万次
                                </p>
                              </CardContent>
                            </Card>
                          </div>
                        </AccordionContent>
                      </AccordionItem>

                      {/* Lancet Series */}
                      <AccordionItem value="lancet">
                        <AccordionTrigger className="text-base font-semibold">
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-1 bg-primary/10 text-primary text-xs rounded">Lancet系列</span>
                            <span>1篇论文</span>
                          </div>
                        </AccordionTrigger>
                        <AccordionContent>
                          <div className="space-y-3 pt-2">
                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Global incidence of childhood cancer by subtype in 2022
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>eClinicalMedicine (The Lancet Discovery Science)</em>, 2025 | DOI: 10.1016/S2589-5370(25)00504-8
                                </p>
                                <p className="text-xs mt-2">
                                  基于GLOBOCAN 2022的儿童癌症发病率分析
                                </p>
                              </CardContent>
                            </Card>
                          </div>
                        </AccordionContent>
                      </AccordionItem>

                      {/* Other Journals */}
                      <AccordionItem value="other">
                        <AccordionTrigger className="text-base font-semibold">
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">其他顶级期刊</span>
                            <span>5篇论文</span>
                          </div>
                        </AccordionTrigger>
                        <AccordionContent>
                          <div className="space-y-3 pt-2">
                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Estimating the global cancer incidence and mortality in 2018: GLOBOCAN sources and methods
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>International Journal of Cancer</em>, 2019 | DOI: 10.1002/ijc.31937
                                </p>
                                <p className="text-xs mt-2">
                                  GLOBOCAN 2018数据来源和方法详解
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Cancer incidence and mortality worldwide: sources, methods and major patterns in GLOBOCAN 2012
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>International Journal of Cancer</em>, 2015 | DOI: 10.1002/ijc.29210
                                </p>
                                <p className="text-xs mt-2">
                                  GLOBOCAN 2012方法学和主要模式
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Gastrointestinal cancer statistics in 2022 and projection to 2050: GLOBOCAN estimates across 185 countries
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>Cancer</em>, 2025 | DOI: 10.1002/cncr.70245
                                </p>
                                <p className="text-xs mt-2">
                                  消化道癌症统计和2050年预测
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Estimates of esophageal squamous cell carcinoma and esophageal adenocarcinoma incidence and mortality in 2020 and projections to 2040
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>Gastroenterology</em>, 2022 | DOI: 10.1053/j.gastro.2022.02.036
                                </p>
                                <p className="text-xs mt-2">
                                  食管癌发病率和死亡率估计及预测
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Socioeconomic inequalities in cancer incidence and mortality: An analysis of GLOBOCAN 2022
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>Chinese Medical Journal</em>, 2024 | DOI: 10.1097/CM9.0000000000003140
                                </p>
                                <p className="text-xs mt-2">
                                  基于GLOBOCAN 2022的癌症社会经济不平等分析
                                </p>
                              </CardContent>
                            </Card>
                          </div>
                        </AccordionContent>
                      </AccordionItem>
                    </Accordion>
                  </div>

                  {/* Access Button */}
                  <div className="flex gap-3 mt-8">
                    <Button asChild size="lg" className="gap-2">
                      <a href="https://gco.iarc.fr/" target="_blank" rel="noopener noreferrer">
                        <Map className="w-5 h-5" />
                        访问GLOBOCAN
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    </Button>
                    <Button asChild variant="outline" size="lg" className="gap-2">
                      <a href="https://gco.iarc.fr/today/home" target="_blank" rel="noopener noreferrer">
                        Cancer Today工具
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* CI5 Tab */}
          <TabsContent value="ci5" className="space-y-8">
            <div className="max-w-5xl mx-auto">
              <Card className="border-2 border-primary/20">
                <CardHeader>
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                      <TrendingUp className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <CardTitle className="text-2xl">Cancer Incidence in Five Continents (CI5)</CardTitle>
                      <CardDescription className="text-base">
                        International Agency for Research on Cancer (IARC)
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="prose max-w-none">
                    <p className="text-base leading-relaxed">
                      <strong>Cancer Incidence in Five Continents (CI5)</strong> 是IARC自1966年以来持续发布的权威癌症登记数据汇编。该系列数据库收集了全球高质量人群基础癌症登记处的详细发病率数据，是研究全球癌症发病率地理差异和时间趋势的金标准数据源。CI5数据以其严格的质量控制标准和详细的分层数据而闻名。
                    </p>

                    <h3 className="text-lg font-semibold mt-6 mb-3">核心特点</h3>
                    <ul className="space-y-2">
                      <li><strong>高质量数据</strong>：仅纳入符合严格质量标准的癌症登记处数据</li>
                      <li><strong>详细分层</strong>：按性别、年龄组（5岁组）、癌症部位和组织学类型分层</li>
                      <li><strong>长期趋势</strong>：跨越60多年的历史数据，支持时间趋势分析</li>
                      <li><strong>国际可比</strong>：统一的编码标准（ICD-O）确保数据可比性</li>
                      <li><strong>开放获取</strong>：CI5plus在线数据库提供免费数据查询和下载</li>
                    </ul>

                    <h3 className="text-lg font-semibold mt-6 mb-3">CI5系列卷册</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 not-prose">
                      <Card>
                        <CardContent className="pt-6">
                          <div className="text-center">
                            <p className="text-3xl font-bold text-primary">XII</p>
                            <p className="text-sm text-muted-foreground mt-1">最新卷册</p>
                            <p className="text-xs text-muted-foreground mt-2">
                              2013-2017年数据
                            </p>
                          </div>
                        </CardContent>
                      </Card>
                      <Card>
                        <CardContent className="pt-6">
                          <div className="text-center">
                            <p className="text-3xl font-bold text-primary">600+</p>
                            <p className="text-sm text-muted-foreground mt-1">癌症登记处</p>
                            <p className="text-xs text-muted-foreground mt-2">
                              覆盖五大洲
                            </p>
                          </div>
                        </CardContent>
                      </Card>
                      <Card>
                        <CardContent className="pt-6">
                          <div className="text-center">
                            <p className="text-3xl font-bold text-primary">60+</p>
                            <p className="text-sm text-muted-foreground mt-1">年份跨度</p>
                            <p className="text-xs text-muted-foreground mt-2">
                              1960s至今
                            </p>
                          </div>
                        </CardContent>
                      </Card>
                    </div>
                  </div>

                  {/* Visualization */}
                  <div className="mt-8">
                    <h3 className="text-lg font-semibold mb-4">CI5数据库与癌症登记网络</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="rounded-lg overflow-hidden border border-border">
                        <img
                          src="/images/databases/ci5-vol12-cover.jpg"
                          alt="CI5 Volume XII Cover"
                          className="w-full h-auto"
                        />
                        <p className="text-xs text-muted-foreground p-2 bg-muted/30">
                          CI5 Vol. XII封面（2013-2017数据）
                        </p>
                      </div>
                      <div className="rounded-lg overflow-hidden border border-border">
                        <img
                          src="/images/databases/ci5-registry-map.png"
                          alt="Population-Based Cancer Registries Map"
                          className="w-full h-auto"
                        />
                        <p className="text-xs text-muted-foreground p-2 bg-muted/30">
                          全球人群基础癌症登记处分布
                        </p>
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground mt-3 text-center">
                      来源：Cancer Incidence in Five Continents Vol. XII (IARC) | American Cancer Society Cancer Atlas
                    </p>
                  </div>

                  {/* Key Publications */}
                  <div className="mt-8">
                    <div className="flex items-center gap-2 mb-4">
                      <BookOpen className="w-5 h-5 text-primary" />
                      <h3 className="text-lg font-semibold">代表性论文</h3>
                    </div>
                    
                    <Accordion type="single" collapsible className="w-full">
                      {/* Lancet Series */}
                      <AccordionItem value="lancet">
                        <AccordionTrigger className="text-base font-semibold">
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-1 bg-primary/10 text-primary text-xs rounded">Lancet系列</span>
                            <span>1篇论文</span>
                          </div>
                        </AccordionTrigger>
                        <AccordionContent>
                          <div className="space-y-3 pt-2">
                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Cancer survival in five continents: a worldwide population-based study (CONCORD)
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>The Lancet Oncology</em>, 2008 | DOI: 10.1016/S1470-2045(08)70179-7 | 引用: 1,937+
                                </p>
                                <p className="text-xs mt-2">
                                  基于CI5数据的全球癌症生存率研究
                                </p>
                              </CardContent>
                            </Card>
                          </div>
                        </AccordionContent>
                      </AccordionItem>

                      {/* Other Journals */}
                      <AccordionItem value="other">
                        <AccordionTrigger className="text-base font-semibold">
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">其他顶级期刊</span>
                            <span>4篇论文</span>
                          </div>
                        </AccordionTrigger>
                        <AccordionContent>
                          <div className="space-y-3 pt-2">
                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Cancer Incidence in Five Continents: Inclusion criteria, highlights from Volume X and the global status of cancer registration
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>International Journal of Cancer</em>, 2015 | DOI: 10.1002/ijc.29670 | 引用: 659+
                                </p>
                                <p className="text-xs mt-2">
                                  CI5 Volume X纳入标准和全球癌症登记状况
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Fifty years of cancer incidence: CI5 I–IX
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>International Journal of Cancer</em>, 2010 | DOI: 10.1002/ijc.25517
                                </p>
                                <p className="text-xs mt-2">
                                  CI5前九卷50年数据回顾
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Patterns of cancer incidence, mortality, and prevalence across five continents: defining priorities to reduce cancer disparities
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>Journal of Clinical Oncology</em>, 2006 | DOI: 10.1200/JCO.2005.05.2308
                                </p>
                                <p className="text-xs mt-2">
                                  基于CI5的五大洲癌症模式分析
                                </p>
                              </CardContent>
                            </Card>

                            <Card className="bg-muted/30">
                              <CardContent className="pt-4">
                                <p className="text-sm font-medium mb-1">
                                  Global cancer incidence and mortality rates and trends—an update
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  <em>Cancer Epidemiology, Biomarkers & Prevention</em>, 2016 | DOI: 10.1158/1055-9965.EPI-15-0578
                                </p>
                                <p className="text-xs mt-2">
                                  基于CI5的全球癌症发病率和死亡率趋势更新
                                </p>
                              </CardContent>
                            </Card>
                          </div>
                        </AccordionContent>
                      </AccordionItem>
                    </Accordion>
                  </div>

                  {/* Access Button */}
                  <div className="flex gap-3 mt-8">
                    <Button asChild size="lg" className="gap-2">
                      <a href="https://ci5.iarc.fr/" target="_blank" rel="noopener noreferrer">
                        <BarChart3 className="w-5 h-5" />
                        访问CI5数据库
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    </Button>
                    <Button asChild variant="outline" size="lg" className="gap-2">
                      <a href="https://ci5.iarc.fr/ci5plus/download" target="_blank" rel="noopener noreferrer">
                        CI5plus在线工具
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>

        {/* Comparison Section */}
        <div className="max-w-5xl mx-auto mt-12">
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">数据库对比</CardTitle>
              <CardDescription>
                选择最适合您研究需求的数据源
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-border">
                      <th className="text-left p-3 font-semibold">特征</th>
                      <th className="text-left p-3 font-semibold">GBD</th>
                      <th className="text-left p-3 font-semibold">GLOBOCAN</th>
                      <th className="text-left p-3 font-semibold">CI5</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="border-b border-border">
                      <td className="p-3 font-medium">数据类型</td>
                      <td className="p-3">发病、死亡、DALYs、风险归因</td>
                      <td className="p-3">发病、死亡、患病</td>
                      <td className="p-3">发病率（详细分层）</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-3 font-medium">地理覆盖</td>
                      <td className="p-3">204个国家/地区</td>
                      <td className="p-3">185个国家/地区</td>
                      <td className="p-3">600+癌症登记处</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-3 font-medium">时间范围</td>
                      <td className="p-3">1990-2023</td>
                      <td className="p-3">2022（每2年更新）</td>
                      <td className="p-3">1960s-2017</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-3 font-medium">数据来源</td>
                      <td className="p-3">综合估算（多源数据建模）</td>
                      <td className="p-3">估算（基于登记和建模）</td>
                      <td className="p-3">实际登记数据</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-3 font-medium">适用场景</td>
                      <td className="p-3">疾病负担、风险因素、趋势分析</td>
                      <td className="p-3">全球癌症概况、国家比较</td>
                      <td className="p-3">详细发病率、地区差异、时间趋势</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-3 font-medium">代表性论文</td>
                      <td className="p-3">10篇（5篇Lancet系列）</td>
                      <td className="p-3">9篇（1篇Lancet系列，3篇CA期刊）</td>
                      <td className="p-3">5篇（1篇Lancet系列）</td>
                    </tr>
                    <tr>
                      <td className="p-3 font-medium">数据质量</td>
                      <td className="p-3">建模估算，覆盖全面</td>
                      <td className="p-3">标准化估算</td>
                      <td className="p-3">高质量实测数据</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Publication Summary */}
        <div className="max-w-5xl mx-auto mt-8">
          <Card className="bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
            <CardContent className="py-8">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold mb-2">论文发表统计</h3>
                <p className="text-muted-foreground">三大数据库在顶级期刊的影响力</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-4xl font-bold text-primary mb-2">24</div>
                  <div className="text-sm text-muted-foreground mb-1">代表性论文总数</div>
                  <div className="text-xs text-muted-foreground">覆盖多个顶级期刊</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold text-primary mb-2">6</div>
                  <div className="text-sm text-muted-foreground mb-1">Lancet系列论文</div>
                  <div className="text-xs text-muted-foreground">最权威的医学期刊</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold text-primary mb-2">250K+</div>
                  <div className="text-sm text-muted-foreground mb-1">总引用次数</div>
                  <div className="text-xs text-muted-foreground">GLOBOCAN 2018单篇超10万</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* CTA Section */}
        <div className="max-w-3xl mx-auto mt-12">
          <Card className="bg-gradient-to-br from-primary to-primary/80 text-primary-foreground border-0">
            <CardContent className="py-12 text-center">
              <h2 className="text-3xl font-bold mb-4">开始您的研究</h2>
              <p className="text-primary-foreground/90 mb-8 text-lg">
                利用三大数据库，自动化完成从数据收集到论文撰写的全流程
              </p>
              <Button asChild size="lg" variant="secondary" className="gap-2">
                <a href="/projects/new">
                  创建研究项目
                  <ExternalLink className="w-5 h-5" />
                </a>
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
