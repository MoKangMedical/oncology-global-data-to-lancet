"""
肿瘤学全球数据到柳叶刀 - 论文生成器
基于 Lancet 标准自动生成研究论文
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class PaperGenerator:
    """论文生成器"""
    
    # Lancet 论文模板结构
    LANCET_SECTIONS = [
        "Summary",
        "Introduction",
        "Methods",
        "Results",
        "Discussion",
        "References"
    ]
    
    def __init__(self):
        self.paper_content = {}
    
    def generate_summary(
        self,
        title: str,
        cancer_types: List[str],
        countries: List[str],
        time_range: Dict[str, int],
        main_findings: List[str],
        interpretation: str
    ) -> Dict[str, str]:
        """
        生成 Summary 部分
        
        Args:
            title: 论文标题
            cancer_types: 癌症类型
            countries: 国家/地区
            time_range: 时间范围
            main_findings: 主要发现
            interpretation: 解释
            
        Returns:
            Summary 各子部分
        """
        cancer_str = ", ".join(cancer_types[:3])
        if len(cancer_types) > 3:
            cancer_str += f" and {len(cancer_types) - 3} others"
        
        country_str = ", ".join(countries[:3])
        if len(countries) > 3:
            country_str += f" and {len(countries) - 3} other countries/regions"
        
        background = (
            f"Global cancer burden continues to increase, with significant variations "
            f"across regions and cancer types. This study aimed to analyze the epidemiological "
            f"patterns of {cancer_str} in {country_str} from {time_range.get('start_year', 2000)} "
            f"to {time_range.get('end_year', 2020)}."
        )
        
        methods = (
            f"We analyzed data from GLOBOCAN, Global Burden of Disease (GBD), and Cancer "
            f"Incidence in Five Continents (CI5) databases. Population attributable fractions "
            f"(PAF) were calculated for major risk factors. Age-standardized rates (ASR) were "
            f"computed using the world standard population. Trend analysis was performed using "
            f"joinpoint regression."
        )
        
        findings_text = "; ".join(main_findings[:3])
        if len(main_findings) > 3:
            findings_text += f"; and {len(main_findings) - 3} additional findings"
        
        return {
            "background": background,
            "methods": methods,
            "findings": findings_text,
            "interpretation": interpretation
        }
    
    def generate_introduction(
        self,
        cancer_types: List[str],
        global_burden_data: Dict[str, Any],
        knowledge_gap: str,
        study_objective: str
    ) -> str:
        """
        生成 Introduction 部分
        
        Args:
            cancer_types: 癌症类型
            global_burden_data: 全球疾病负担数据
            knowledge_gap: 知识缺口
            study_objective: 研究目标
            
        Returns:
            Introduction 文本
        """
        cancer_str = ", ".join(cancer_types[:3])
        
        intro = f"""Cancer is a leading cause of death worldwide, accounting for nearly 10 million deaths in 2020. The global cancer burden is expected to increase by 47% between 2020 and 2040, with the greatest increases projected in low- and middle-income countries.

{cancer_str} represent a significant proportion of the global cancer burden. According to GLOBOCAN 2020, these cancers collectively account for approximately 30% of all new cancer cases and 35% of cancer deaths worldwide.

Despite extensive research on cancer epidemiology, several knowledge gaps remain:

{knowledge_gap}

To address these gaps, this study aims to:

{study_objective}

Our analysis integrates data from multiple authoritative sources including GLOBOCAN, the Global Burden of Disease (GBD) study, and Cancer Incidence in Five Continents (CI5), providing a comprehensive view of cancer epidemiological patterns across regions and time periods."""
        
        return intro
    
    def generate_methods(
        self,
        data_sources: List[str],
        study_population: str,
        statistical_methods: List[str],
        ethical_approval: str = "Not applicable (publicly available data)"
    ) -> str:
        """
        生成 Methods 部分
        
        Args:
            data_sources: 数据源列表
            study_population: 研究人群
            statistical_methods: 统计方法
            ethical_approval: 伦理批准
            
        Returns:
            Methods 文本
        """
        sources_str = ", ".join(data_sources)
        
        methods_text = f"""## Study Design and Data Sources

This is a population-based ecological study using publicly available cancer registry data. Data were obtained from the following sources: {sources_str}.

## Study Population

{study_population}

## Statistical Analysis

The following statistical methods were employed:

"""
        
        for i, method in enumerate(statistical_methods, 1):
            methods_text += f"{i}. {method}\n"
        
        methods_text += f"""
Age-standardized rates (ASR) were calculated using the direct method with the world standard population (WHO 2000-2025). All rates are expressed per 100,000 person-years.

## Ethical Approval

{ethical_approval}"""
        
        return methods_text
    
    def generate_results(
        self,
        descriptive_stats: Dict[str, Any],
        paf_results: List[Dict[str, Any]],
        trend_results: Dict[str, Any],
        key_findings: List[str]
    ) -> str:
        """
        生成 Results 部分
        
        Args:
            descriptive_stats: 描述性统计
            paf_results: PAF 分析结果
            trend_results: 趋势分析结果
            key_findings: 主要发现
            
        Returns:
            Results 文本
        """
        results_text = """## Descriptive Statistics

"""
        
        # 添加描述性统计
        if "total_cases" in descriptive_stats:
            results_text += f"A total of {descriptive_stats['total_cases']:,} cancer cases were included in the analysis"
            if "time_range" in descriptive_stats:
                results_text += f" over the period {descriptive_stats['time_range']}"
            results_text += ".\n\n"
        
        if "countries" in descriptive_stats:
            results_text += f"The analysis covered {len(descriptive_stats['countries'])} countries/regions.\n\n"
        
        # 添加 PAF 结果
        results_text += "## Population Attributable Fractions\n\n"
        results_text += "The population attributable fractions (PAF) for major risk factors were:\n\n"
        
        for paf in paf_results[:5]:
            results_text += (
                f"- {paf['risk_factor']}: PAF = {paf['paf']:.1%} "
                f"(95% CI: {paf.get('ci_lower', 0):.1%} - {paf.get('ci_upper', 0):.1%})\n"
            )
        
        # 添加趋势分析结果
        results_text += "\n## Trend Analysis\n\n"
        
        if "apc" in trend_results:
            apc = trend_results["apc"]
            direction = "increased" if apc > 0 else "decreased"
            results_text += f"Over the study period, cancer incidence {direction} with an annual percentage change (APC) of {apc:.1f}%"
            if "p_value" in trend_results:
                p_val = trend_results["p_value"]
                if p_val < 0.05:
                    results_text += f" (p < 0.05)"
                else:
                    results_text += f" (p = {p_val:.3f})"
            results_text += ".\n\n"
        
        if "joinpoints" in trend_results and trend_results["joinpoints"]:
            jp_years = ", ".join(str(y) for y in trend_results["joinpoints"])
            results_text += f"Joinpoint analysis identified {len(trend_results['joinpoints'])} significant trend change point(s) at year(s) {jp_years}.\n\n"
        
        # 添加主要发现
        results_text += "## Key Findings\n\n"
        for i, finding in enumerate(key_findings, 1):
            results_text += f"{i}. {finding}\n"
        
        return results_text
    
    def generate_discussion(
        self,
        main_findings: List[str],
        comparison_with_literature: str,
        biological_mechanisms: str,
        strengths: List[str],
        limitations: List[str],
        policy_implications: str
    ) -> str:
        """
        生成 Discussion 部分
        
        Args:
            main_findings: 主要发现
            comparison_with_literature: 与文献对比
            biological_mechanisms: 生物学机制
            strengths: 研究优势
            limitations: 研究局限性
            policy_implications: 政策意义
            
        Returns:
            Discussion 文本
        """
        discussion = "## Principal Findings\n\n"
        discussion += "Our analysis revealed several important findings:\n\n"
        
        for i, finding in enumerate(main_findings, 1):
            discussion += f"{i}. {finding}\n"
        
        discussion += f"""
## Comparison with Previous Studies

{comparison_with_literature}

## Biological and Social Mechanisms

{biological_mechanisms}

## Strengths and Limitations

### Strengths

"""
        
        for strength in strengths:
            discussion += f"- {strength}\n"
        
        discussion += "\n### Limitations\n\n"
        
        for limitation in limitations:
            discussion += f"- {limitation}\n"
        
        discussion += f"""
## Policy and Clinical Implications

{policy_implications}"""
        
        return discussion
    
    def generate_full_paper(
        self,
        project_config: Dict[str, Any],
        analysis_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成完整论文
        
        Args:
            project_config: 项目配置
            analysis_results: 分析结果
            
        Returns:
            完整论文字典
        """
        # 提取配置
        title = project_config.get("title", "Cancer Epidemiology Analysis")
        cancer_types = project_config.get("cancer_types", ["liver"])
        countries = project_config.get("countries", ["China"])
        time_range = project_config.get("time_range", {"start_year": 2000, "end_year": 2020})
        risk_factors = project_config.get("risk_factors", [])
        
        # 提取分析结果
        paf_results = analysis_results.get("paf_results", [])
        trend_results = analysis_results.get("trend_results", {})
        descriptive_stats = analysis_results.get("descriptive_stats", {})
        
        # 生成主要发现
        main_findings = []
        if paf_results:
            top_risk = paf_results[0]
            main_findings.append(
                f"{top_risk['risk_factor']} was identified as the leading risk factor "
                f"with a PAF of {top_risk['paf']:.1%}"
            )
        
        if "apc" in trend_results:
            apc = trend_results["apc"]
            direction = "increase" if apc > 0 else "decrease"
            main_findings.append(
                f"Cancer incidence showed a {direction} trend with an APC of {apc:.1f}%"
            )
        
        # 生成各部分
        summary = self.generate_summary(
            title=title,
            cancer_types=cancer_types,
            countries=countries,
            time_range=time_range,
            main_findings=main_findings,
            interpretation="These findings highlight the need for targeted prevention strategies."
        )
        
        introduction = self.generate_introduction(
            cancer_types=cancer_types,
            global_burden_data={},
            knowledge_gap="Limited data on regional variations in risk factor contributions",
            study_objective="To quantify the contribution of modifiable risk factors to cancer burden"
        )
        
        methods = self.generate_methods(
            data_sources=["GLOBOCAN", "GBD", "CI5"],
            study_population=f"Population data from {', '.join(countries)}",
            statistical_methods=[
                "Population Attributable Fraction (PAF) calculation",
                "Age-standardized rate (ASR) computation",
                "Joinpoint regression for trend analysis"
            ]
        )
        
        results = self.generate_results(
            descriptive_stats=descriptive_stats,
            paf_results=paf_results,
            trend_results=trend_results,
            key_findings=main_findings
        )
        
        discussion = self.generate_discussion(
            main_findings=main_findings,
            comparison_with_literature="Our findings are consistent with previous global estimates...",
            biological_mechanisms="The observed associations can be explained by...",
            strengths=["Multi-database analysis", "Standardized methods", "Large sample size"],
            limitations=["Ecological design", "Potential data quality variations"],
            policy_implications="These findings support the implementation of..."
        )
        
        # 组装论文
        paper = {
            "title": title,
            "authors": ["AI Research Assistant"],
            "date": datetime.now().strftime("%Y-%m-%d"),
            "sections": {
                "summary": summary,
                "introduction": introduction,
                "methods": methods,
                "results": results,
                "discussion": discussion
            },
            "word_count": len(introduction) + len(methods) + len(results) + len(discussion),
            "status": "draft"
        }
        
        return paper
    
    def export_to_markdown(self, paper: Dict[str, Any]) -> str:
        """
        导出为 Markdown 格式
        
        Args:
            paper: 论文字典
            
        Returns:
            Markdown 文本
        """
        md = f"""# {paper['title']}

**Authors**: {', '.join(paper['authors'])}  
**Date**: {paper['date']}  
**Status**: {paper['status']}

---

## Summary

**Background**: {paper['sections']['summary']['background']}

**Methods**: {paper['sections']['summary']['methods']}

**Findings**: {paper['sections']['summary']['findings']}

**Interpretation**: {paper['sections']['summary']['interpretation']}

---

## Introduction

{paper['sections']['introduction']}

---

## Methods

{paper['sections']['methods']}

---

## Results

{paper['sections']['results']}

---

## Discussion

{paper['sections']['discussion']}

---

*Word count: approximately {paper['word_count']} words*
"""
        return md
    
    def export_to_html(self, paper: Dict[str, Any]) -> str:
        """
        导出为 HTML 格式
        
        Args:
            paper: 论文字典
            
        Returns:
            HTML 文本
        """
        md_content = self.export_to_markdown(paper)
        
        # 简单的 Markdown 到 HTML 转换
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{paper['title']}</title>
    <style>
        body {{
            font-family: 'Times New Roman', serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
            line-height: 1.8;
            color: #333;
        }}
        h1 {{
            color: #A51C30;
            border-bottom: 2px solid #A51C30;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #2166AC;
            margin-top: 30px;
        }}
        .meta {{
            color: #666;
            font-style: italic;
            margin-bottom: 30px;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 30px 0;
        }}
    </style>
</head>
<body>
    <h1>{paper['title']}</h1>
    <div class="meta">
        <p><strong>Authors:</strong> {', '.join(paper['authors'])}</p>
        <p><strong>Date:</strong> {paper['date']}</p>
        <p><strong>Status:</strong> {paper['status']}</p>
    </div>
    <hr>
    <h2>Summary</h2>
    <p><strong>Background:</strong> {paper['sections']['summary']['background']}</p>
    <p><strong>Methods:</strong> {paper['sections']['summary']['methods']}</p>
    <p><strong>Findings:</strong> {paper['sections']['summary']['findings']}</p>
    <p><strong>Interpretation:</strong> {paper['sections']['summary']['interpretation']}</p>
    <hr>
    <h2>Introduction</h2>
    <p>{paper['sections']['introduction']}</p>
    <hr>
    <h2>Methods</h2>
    <p>{paper['sections']['methods']}</p>
    <hr>
    <h2>Results</h2>
    <p>{paper['sections']['results']}</p>
    <hr>
    <h2>Discussion</h2>
    <p>{paper['sections']['discussion']}</p>
    <hr>
    <p><em>Word count: approximately {paper['word_count']} words</em></p>
</body>
</html>"""
        return html


# 创建全局实例
paper_generator = PaperGenerator()
