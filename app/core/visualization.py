"""
肿瘤学全球数据到柳叶刀 - 可视化生成器
生成符合 Lancet 风格的图表
"""

import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import json

# 设置 Lancet 风格的配色方案
LANCET_COLORS = {
    'primary': '#A51C30',  # 深红色
    'secondary': '#2166AC',  # 蓝色
    'accent1': '#B2182B',  # 红色
    'accent2': '#D6604D',  # 浅红色
    'accent3': '#4393C3',  # 浅蓝色
    'accent4': '#92C5DE',  # 更浅的蓝色
    'background': '#FFFFFF',
    'text': '#333333',
    'grid': '#E5E5E5'
}

# 分类颜色
CATEGORY_COLORS = [
    '#A51C30', '#2166AC', '#B2182B', '#D6604D', '#4393C3',
    '#92C5DE', '#F4A582', '#FDDBC7', '#D1E5F0', '#92C5DE'
]


class VisualizationGenerator:
    """可视化生成器"""
    
    def __init__(self, output_dir: str = "output/charts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置 matplotlib 样式
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.facecolor'] = 'white'
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.edgecolor'] = '#333333'
        plt.rcParams['axes.labelcolor'] = '#333333'
        plt.rcParams['text.color'] = '#333333'
    
    def create_bar_chart(
        self,
        data: Dict[str, float],
        title: str,
        xlabel: str = "",
        ylabel: str = "",
        filename: str = "bar_chart.png",
        orientation: str = 'vertical',
        figsize: Tuple[int, int] = (10, 6)
    ) -> str:
        """
        创建条形图
        
        Args:
            data: 数据字典 {标签: 值}
            title: 图表标题
            xlabel: X 轴标签
            ylabel: Y 轴标签
            filename: 输出文件名
            orientation: 方向 ('vertical' 或 'horizontal')
            figsize: 图表大小
            
        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        labels = list(data.keys())
        values = list(data.values())
        
        if orientation == 'horizontal':
            bars = ax.barh(labels, values, color=LANCET_COLORS['primary'])
            ax.set_xlabel(ylabel)  # 注意：水平条形图的轴标签交换
        else:
            bars = ax.bar(labels, values, color=LANCET_COLORS['primary'])
            ax.set_ylabel(ylabel)
            plt.xticks(rotation=45, ha='right')
        
        ax.set_title(title, fontsize=14, fontweight='bold', color=LANCET_COLORS['primary'])
        
        # 添加数值标签
        for bar in bars:
            if orientation == 'horizontal':
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2.,
                       f'{width:.1f}', ha='left', va='center')
            else:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def create_line_chart(
        self,
        data: Dict[str, List[float]],
        x_values: List[Any],
        title: str,
        xlabel: str = "",
        ylabel: str = "",
        filename: str = "line_chart.png",
        figsize: Tuple[int, int] = (10, 6)
    ) -> str:
        """
        创建折线图
        
        Args:
            data: 数据字典 {系列名: 值列表}
            x_values: X 轴值
            title: 图表标题
            xlabel: X 轴标签
            ylabel: Y 轴标签
            filename: 输出文件名
            figsize: 图表大小
            
        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        for i, (series_name, values) in enumerate(data.items()):
            color = CATEGORY_COLORS[i % len(CATEGORY_COLORS)]
            ax.plot(x_values, values, marker='o', label=series_name, 
                   color=color, linewidth=2, markersize=6)
        
        ax.set_title(title, fontsize=14, fontweight='bold', color=LANCET_COLORS['primary'])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def create_pie_chart(
        self,
        data: Dict[str, float],
        title: str,
        filename: str = "pie_chart.png",
        figsize: Tuple[int, int] = (8, 8)
    ) -> str:
        """
        创建饼图
        
        Args:
            data: 数据字典 {标签: 值}
            title: 图表标题
            filename: 输出文件名
            figsize: 图表大小
            
        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        labels = list(data.keys())
        values = list(data.values())
        
        # 过滤掉小于 2% 的值
        total = sum(values)
        threshold = total * 0.02
        filtered_labels = []
        filtered_values = []
        other_sum = 0
        
        for label, value in zip(labels, values):
            if value >= threshold:
                filtered_labels.append(label)
                filtered_values.append(value)
            else:
                other_sum += value
        
        if other_sum > 0:
            filtered_labels.append('Other')
            filtered_values.append(other_sum)
        
        wedges, texts, autotexts = ax.pie(
            filtered_values, 
            labels=filtered_labels,
            autopct='%1.1f%%',
            colors=CATEGORY_COLORS[:len(filtered_labels)],
            pctdistance=0.85,
            wedgeprops=dict(width=0.5)  # 环形图
        )
        
        ax.set_title(title, fontsize=14, fontweight='bold', 
                    color=LANCET_COLORS['primary'], pad=20)
        
        plt.tight_layout()
        
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def create_heatmap(
        self,
        data: pd.DataFrame,
        title: str,
        xlabel: str = "",
        ylabel: str = "",
        filename: str = "heatmap.png",
        figsize: Tuple[int, int] = (12, 8),
        cmap: str = "YlOrRd"
    ) -> str:
        """
        创建热力图
        
        Args:
            data: 数据 DataFrame
            title: 图表标题
            xlabel: X 轴标签
            ylabel: Y 轴标签
            filename: 输出文件名
            figsize: 图表大小
            cmap: 颜色映射
            
        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.heatmap(
            data,
            annot=True,
            fmt='.1f',
            cmap=cmap,
            ax=ax,
            linewidths=0.5,
            linecolor='white'
        )
        
        ax.set_title(title, fontsize=14, fontweight='bold', 
                    color=LANCET_COLORS['primary'])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        plt.tight_layout()
        
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def create_grouped_bar_chart(
        self,
        data: Dict[str, Dict[str, float]],
        title: str,
        xlabel: str = "",
        ylabel: str = "",
        filename: str = "grouped_bar_chart.png",
        figsize: Tuple[int, int] = (12, 6)
    ) -> str:
        """
        创建分组条形图
        
        Args:
            data: 数据字典 {类别: {组: 值}}
            title: 图表标题
            xlabel: X 轴标签
            ylabel: Y 轴标签
            filename: 输出文件名
            figsize: 图表大小
            
        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        categories = list(data.keys())
        groups = list(list(data.values())[0].keys())
        
        x = np.arange(len(categories))
        width = 0.8 / len(groups)
        
        for i, group in enumerate(groups):
            values = [data[cat][group] for cat in categories]
            offset = (i - len(groups)/2 + 0.5) * width
            ax.bar(x + offset, values, width, label=group, 
                  color=CATEGORY_COLORS[i % len(CATEGORY_COLORS)])
        
        ax.set_title(title, fontsize=14, fontweight='bold', 
                    color=LANCET_COLORS['primary'])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.legend()
        
        plt.tight_layout()
        
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def create_trend_chart_with_ci(
        self,
        years: List[int],
        values: List[float],
        ci_lower: List[float],
        ci_upper: List[float],
        title: str,
        xlabel: str = "Year",
        ylabel: str = "",
        filename: str = "trend_ci.png",
        figsize: Tuple[int, int] = (10, 6)
    ) -> str:
        """
        创建带置信区间的趋势图
        
        Args:
            years: 年份列表
            values: 值列表
            ci_lower: 置信区间下限
            ci_upper: 置信区间上限
            title: 图表标题
            xlabel: X 轴标签
            ylabel: Y 轴标签
            filename: 输出文件名
            figsize: 图表大小
            
        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # 绘制置信区间
        ax.fill_between(years, ci_lower, ci_upper, 
                        alpha=0.3, color=LANCET_COLORS['secondary'])
        
        # 绘制趋势线
        ax.plot(years, values, marker='o', color=LANCET_COLORS['primary'], 
               linewidth=2, markersize=6, label='Observed')
        
        ax.set_title(title, fontsize=14, fontweight='bold', 
                    color=LANCET_COLORS['primary'])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def create_paf_chart(
        self,
        paf_results: List[Dict[str, Any]],
        title: str = "Population Attributable Fraction by Risk Factor",
        filename: str = "paf_chart.png"
    ) -> str:
        """
        创建 PAF 结果图表
        
        Args:
            paf_results: PAF 结果列表
            title: 图表标题
            filename: 输出文件名
            
        Returns:
            图表文件路径
        """
        risk_factors = [r['risk_factor'] for r in paf_results]
        pafs = [r['paf'] * 100 for r in paf_results]  # 转换为百分比
        
        # 按 PAF 值排序
        sorted_indices = np.argsort(pafs)[::-1]
        risk_factors = [risk_factors[i] for i in sorted_indices]
        pafs = [pafs[i] for i in sorted_indices]
        
        return self.create_bar_chart(
            data=dict(zip(risk_factors, pafs)),
            title=title,
            ylabel="PAF (%)",
            filename=filename,
            orientation='horizontal',
            figsize=(10, max(6, len(risk_factors) * 0.5))
        )
    
    def create_comparison_chart(
        self,
        data: Dict[str, Dict[str, float]],
        title: str = "Cancer Incidence Comparison",
        filename: str = "comparison_chart.png"
    ) -> str:
        """
        创建比较图表
        
        Args:
            data: 数据字典 {国家: {癌症类型: 发病率}}
            title: 图表标题
            filename: 输出文件名
            
        Returns:
            图表文件路径
        """
        return self.create_grouped_bar_chart(
            data=data,
            title=title,
            ylabel="Age-Standardized Rate (per 100,000)",
            filename=filename
        )

    # ==================== Meta 分析相关图表 ====================

    def create_forest_plot(
        self,
        studies: List[Dict[str, Any]],
        pooled_effect: Optional[float] = None,
        pooled_ci_lower: Optional[float] = None,
        pooled_ci_upper: Optional[float] = None,
        title: str = "Forest Plot",
        xlabel: str = "Effect Size",
        xlog: bool = False,
        filename: str = "forest_plot.png",
        figsize: Tuple[int, int] = (10, 8)
    ) -> str:
        """
        创建森林图 (Forest Plot)

        用于展示各研究效应量及置信区间，以及合并效应量

        Args:
            studies: 各研究数据列表 [{study, effect, ci_lower, ci_upper, weight}]
            pooled_effect: 合并效应量
            pooled_ci_lower: 合并效应量置信区间下限
            pooled_ci_upper: 合并效应量置信区间上限
            title: 图表标题
            xlabel: X 轴标签
            xlog: 是否使用对数刻度
            filename: 输出文件名
            figsize: 图表大小

        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=figsize)

        n_studies = len(studies)
        y_positions = list(range(n_studies, 0, -1))

        # 绘制各研究
        for i, study in enumerate(studies):
            effect = study["effect"]
            ci_lower = study["ci_lower"]
            ci_upper = study["ci_upper"]
            weight = study.get("weight", 5)

            # 点的大小与权重成比例
            marker_size = max(4, min(20, weight * 0.6))

            # 绘制置信区间线
            ax.plot(
                [ci_lower, ci_upper],
                [y_positions[i], y_positions[i]],
                color=LANCET_COLORS['secondary'],
                linewidth=1.5,
                solid_capstyle='round'
            )

            # 绘制效应量点
            ax.plot(
                effect,
                y_positions[i],
                's',  # 方形标记
                color=LANCET_COLORS['primary'],
                markersize=marker_size,
                markeredgecolor='white',
                markeredgewidth=0.5
            )

        # 绘制合并效应量（菱形）
        if pooled_effect is not None and pooled_ci_lower is not None and pooled_ci_upper is not None:
            diamond_y = 0
            diamond_height = 0.4

            # 菱形的四个顶点
            diamond_x = [pooled_ci_lower, pooled_effect, pooled_ci_upper, pooled_effect]
            diamond_y_pts = [diamond_y, diamond_y + diamond_height, diamond_y, diamond_y - diamond_height]

            ax.fill(diamond_x, diamond_y_pts, color=LANCET_COLORS['primary'], alpha=0.8, zorder=5)
            ax.plot(diamond_x + [diamond_x[0]], diamond_y_pts + [diamond_y_pts[0]],
                   color='white', linewidth=1, zorder=6)

        # 绘制无效线 (null line at 0 for mean differences, or 1 for odds ratios)
        null_value = 1 if xlog else 0
        ax.axvline(x=null_value, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)

        # 设置 Y 轴标签
        study_labels = [s["study"] for s in studies] + ["Pooled"]
        y_ticks = list(y_positions) + [0]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(study_labels, fontsize=9)

        if xlog:
            ax.set_xscale('log')

        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_title(title, fontsize=14, fontweight='bold', color=LANCET_COLORS['primary'])

        # 添加权重和数值注释
        for i, study in enumerate(studies):
            effect = study["effect"]
            ci_lower = study["ci_lower"]
            ci_upper = study["ci_upper"]
            weight = study.get("weight", 0)
            label = f"{effect:.2f} [{ci_lower:.2f}, {ci_upper:.2f}] ({weight:.1f}%)"
            ax.annotate(
                label,
                xy=(1.02, y_positions[i]),
                xycoords=('axes fraction', 'data'),
                va='center',
                fontsize=7,
                color='#555555'
            )

        # 添加合并效应量注释
        if pooled_effect is not None:
            label = f"{pooled_effect:.2f} [{pooled_ci_lower:.2f}, {pooled_ci_upper:.2f}]"
            ax.annotate(
                label,
                xy=(1.02, 0),
                xycoords=('axes fraction', 'data'),
                va='center',
                fontsize=7,
                fontweight='bold',
                color=LANCET_COLORS['primary']
            )

        # 右侧标注栏位标题
        ax.annotate(
            "Effect [95% CI] (Weight)",
            xy=(1.02, n_studies + 0.5),
            xycoords=('axes fraction', 'data'),
            va='center',
            fontsize=7,
            fontweight='bold',
            color='#333333'
        )

        ax.grid(True, axis='x', alpha=0.2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        plt.subplots_adjust(right=0.72)

        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        return str(filepath)

    def create_funnel_plot(
        self,
        effects: List[float],
        variances: List[float],
        study_names: Optional[List[str]] = None,
        pooled_effect: Optional[float] = None,
        title: str = "Funnel Plot",
        filename: str = "funnel_plot.png",
        figsize: Tuple[int, int] = (10, 8)
    ) -> str:
        """
        创建漏斗图 (Funnel Plot)

        用于评估 Meta 分析中的发表偏倚

        X 轴: 效应量
        Y 轴: 标准误 (倒置，小标准误在上方)

        Args:
            effects: 各研究的效应量列表
            variances: 各研究的方差列表
            study_names: 各研究名称列表
            pooled_effect: 合并效应量
            title: 图表标题
            filename: 输出文件名
            figsize: 图表大小

        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=figsize)

        effects = np.array(effects, dtype=float)
        se = np.sqrt(np.array(variances, dtype=float))

        if study_names is None:
            study_names = [f"Study_{i+1}" for i in range(len(effects))]

        # 绘制散点
        for i in range(len(effects)):
            ax.scatter(
                effects[i], se[i],
                s=80,
                color=LANCET_COLORS['primary'],
                edgecolors='white',
                linewidth=0.5,
                zorder=5
            )
            # 标注研究名称
            ax.annotate(
                study_names[i],
                (effects[i], se[i]),
                textcoords="offset points",
                xytext=(5, 3),
                fontsize=7,
                color='#555555'
            )

        # 绘制合并效应量线
        if pooled_effect is not None:
            ax.axvline(x=pooled_effect, color=LANCET_COLORS['primary'],
                      linestyle='-', linewidth=1.5, label=f'Pooled: {pooled_effect:.3f}')

        # 绘制伪95%置信区间漏斗
        se_range = np.linspace(0.001, max(se) * 1.2, 100)
        z = 1.96

        if pooled_effect is not None:
            funnel_left = pooled_effect - z * se_range
            funnel_right = pooled_effect + z * se_range
        else:
            mid = np.mean(effects)
            funnel_left = mid - z * se_range
            funnel_right = mid + z * se_range

        ax.plot(funnel_left, se_range, '--', color='gray', linewidth=0.8, alpha=0.6)
        ax.plot(funnel_right, se_range, '--', color='gray', linewidth=0.8, alpha=0.6)

        # 填充漏斗区域
        ax.fill_betweenx(se_range, funnel_left, funnel_right,
                         alpha=0.05, color='gray')

        # 反转 Y 轴（小标准误在上方 = 更精确的研究）
        ax.invert_yaxis()

        ax.set_xlabel("Effect Size", fontsize=11)
        ax.set_ylabel("Standard Error", fontsize=11)
        ax.set_title(title, fontsize=14, fontweight='bold', color=LANCET_COLORS['primary'])

        if pooled_effect is not None:
            ax.legend(loc='lower right', fontsize=9)

        ax.grid(True, alpha=0.2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()

        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        return str(filepath)

    # ==================== 生存分析相关图表 ====================

    def create_survival_curve(
        self,
        km_data: Dict[str, Any],
        title: str = "Kaplan-Meier Survival Curve",
        xlabel: str = "Time",
        ylabel: str = "Survival Probability",
        filename: str = "survival_curve.png",
        figsize: Tuple[int, int] = (10, 7),
        groups: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        创建生存曲线图 (Kaplan-Meier Plot)

        Args:
            km_data: Kaplan-Meier 分析结果数据
                包含 time_points, survival_prob, ci_lower, ci_upper, n_at_risk
            title: 图表标题
            xlabel: X 轴标签
            ylabel: Y 轴标签
            filename: 输出文件名
            figsize: 图表大小
            groups: 多组生存数据列表 [{name, km_data}, ...]

        Returns:
            图表文件路径
        """
        # 创建上下两个子图：生存曲线 + 风险表
        if km_data.get("n_at_risk") and len(km_data["n_at_risk"]) > 0:
            fig, (ax_main, ax_table) = plt.subplots(
                2, 1,
                figsize=figsize,
                gridspec_kw={'height_ratios': [4, 1]},
                sharex=True
            )
            has_risk_table = True
        else:
            fig, ax_main = plt.subplots(figsize=figsize)
            ax_table = None
            has_risk_table = False

        # 绘制生存曲线
        if groups is not None and len(groups) > 0:
            # 多组比较
            for g_idx, group in enumerate(groups):
                g_data = group["km_data"]
                color = CATEGORY_COLORS[g_idx % len(CATEGORY_COLORS)]

                times = g_data["time_points"]
                surv = g_data["survival_prob"]

                # 添加起始点 (time=0, survival=1)
                step_times = [0] + times
                step_surv = [1.0] + surv

                ax_main.step(step_times, step_surv, where='post',
                           color=color, linewidth=2, label=group["name"])

                # 置信区间
                if g_data.get("ci_lower") and g_data.get("ci_upper"):
                    ci_lower = [1.0] + g_data["ci_lower"]
                    ci_upper = [1.0] + g_data["ci_upper"]
                    ax_main.fill_between(
                        step_times, ci_lower, ci_upper,
                        step='post', alpha=0.15, color=color
                    )

                # 删失标记
                if g_data.get("n_censored") and g_data.get("time_points"):
                    for t_idx, t in enumerate(g_data["time_points"]):
                        if g_data["n_censored"][t_idx] > 0:
                            ax_main.plot(t, g_data["survival_prob"][t_idx],
                                       'x', color=color, markersize=8, markeredgewidth=2)

            ax_main.legend(loc='lower left', fontsize=9, framealpha=0.9)

        else:
            # 单组
            times = km_data["time_points"]
            surv = km_data["survival_prob"]

            step_times = [0] + times
            step_surv = [1.0] + surv

            ax_main.step(step_times, step_surv, where='post',
                        color=LANCET_COLORS['primary'], linewidth=2)

            # 置信区间
            if km_data.get("ci_lower") and km_data.get("ci_upper"):
                ci_lower = [1.0] + km_data["ci_lower"]
                ci_upper = [1.0] + km_data["ci_upper"]
                ax_main.fill_between(
                    step_times, ci_lower, ci_upper,
                    step='post', alpha=0.2, color=LANCET_COLORS['secondary'],
                    label='95% CI'
                )

            # 删失标记
            if km_data.get("n_censored") and km_data.get("time_points"):
                for t_idx, t in enumerate(km_data["time_points"]):
                    if km_data["n_censored"][t_idx] > 0:
                        ax_main.plot(t, km_data["survival_prob"][t_idx],
                                   'x', color=LANCET_COLORS['accent2'],
                                   markersize=8, markeredgewidth=2)

            ax_main.legend(loc='lower left', fontsize=9, framealpha=0.9)

        # 中位生存时间线
        if km_data.get("median_survival"):
            ax_main.axhline(y=0.5, color='gray', linestyle=':', linewidth=0.8, alpha=0.5)
            ax_main.axvline(x=km_data["median_survival"], color='gray', linestyle=':',
                          linewidth=0.8, alpha=0.5)

        ax_main.set_ylabel(ylabel, fontsize=11)
        ax_main.set_ylim(-0.02, 1.05)
        ax_main.set_title(title, fontsize=14, fontweight='bold', color=LANCET_COLORS['primary'])
        ax_main.grid(True, alpha=0.2)
        ax_main.spines['top'].set_visible(False)
        ax_main.spines['right'].set_visible(False)

        # 风险表 (Number at Risk)
        if has_risk_table and ax_table is not None:
            ax_table.set_xlim(ax_main.get_xlim())

            times_for_table = km_data["time_points"]
            n_at_risk = km_data["n_at_risk"]

            # 选择部分时间点展示（避免过于拥挤）
            max_labels = 10
            if len(times_for_table) > max_labels:
                step = len(times_for_table) // max_labels
                indices = list(range(0, len(times_for_table), step))
                if indices[-1] != len(times_for_table) - 1:
                    indices.append(len(times_for_table) - 1)
            else:
                indices = list(range(len(times_for_table)))

            display_times = [times_for_table[i] for i in indices]
            display_risks = [n_at_risk[i] for i in indices]

            ax_table.set_xticks(display_times)
            ax_table.set_xticklabels([f"{t:.0f}" for t in display_times], fontsize=8)
            ax_table.set_xlabel(xlabel, fontsize=11)

            # 隐藏 Y 轴
            ax_table.set_yticks([])
            ax_table.spines['top'].set_visible(False)
            ax_table.spines['right'].set_visible(False)
            ax_table.spines['left'].set_visible(False)

            # 添加 "Number at Risk" 标签
            ax_table.set_ylabel("No. at Risk", fontsize=9, rotation=0, labelpad=50, va='center')

            for i, t in enumerate(display_times):
                ax_table.text(t, 0.5, str(display_risks[i]),
                            ha='center', va='center', fontsize=8, fontweight='bold')
        else:
            ax_main.set_xlabel(xlabel, fontsize=11)

        plt.tight_layout()

        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        return str(filepath)

    def create_heatmap_plotly(
        self,
        data: pd.DataFrame,
        title: str = "Heatmap",
        filename: str = "heatmap_plotly.html",
        colorscale: str = "RdYlBu_r",
        show_values: bool = True
    ) -> str:
        """
        创建交互式热力图 (使用 Plotly)

        Args:
            data: 数据 DataFrame
            title: 图表标题
            filename: 输出文件名 (.html)
            colorscale: 颜色方案
            show_values: 是否显示数值

        Returns:
            图表文件路径
        """
        fig = go.Figure(data=go.Heatmap(
            z=data.values,
            x=data.columns.tolist(),
            y=data.index.tolist(),
            colorscale=colorscale,
            text=data.values if show_values else None,
            texttemplate="%{text:.2f}" if show_values else None,
            textfont={"size": 10},
            hoverongaps=False,
            colorbar=dict(
                title="",
                thickness=15,
                len=0.5
            )
        ))

        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=16, color=LANCET_COLORS['primary'], family="DejaVu Sans")
            ),
            xaxis=dict(
                tickfont=dict(size=10),
                tickangle=-45
            ),
            yaxis=dict(
                tickfont=dict(size=10),
                autorange='reversed'
            ),
            width=max(600, len(data.columns) * 60 + 200),
            height=max(400, len(data.index) * 40 + 200),
            margin=dict(l=120, r=50, t=60, b=80),
            template='plotly_white'
        )

        filepath = self.output_dir / filename
        fig.write_html(str(filepath))

        # 同时保存静态图片
        png_path = self.output_dir / filename.replace('.html', '.png')
        try:
            fig.write_image(str(png_path), width=fig.layout.width, height=fig.layout.height, scale=2)
        except Exception:
            pass  # kaleido 可能未安装

        return str(filepath)

    def create_heatmap_numpy(
        self,
        data: np.ndarray,
        row_labels: List[str],
        col_labels: List[str],
        title: str = "Heatmap",
        xlabel: str = "",
        ylabel: str = "",
        filename: str = "heatmap_np.png",
        figsize: Tuple[int, int] = (12, 8),
        cmap: str = "YlOrRd",
        annot: bool = True,
        center: Optional[float] = None
    ) -> str:
        """
        创建热力图 (使用 numpy 数组输入)

        Args:
            data: 二维 numpy 数组
            row_labels: 行标签
            col_labels: 列标签
            title: 图表标题
            xlabel: X 轴标签
            ylabel: Y 轴标签
            filename: 输出文件名
            figsize: 图表大小
            cmap: 颜色映射
            annot: 是否标注数值
            center: 颜色中心值

        Returns:
            图表文件路径
        """
        df = pd.DataFrame(data, index=row_labels, columns=col_labels)
        return self.create_heatmap(
            data=df,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            filename=filename,
            figsize=figsize,
            cmap=cmap
        )


# 创建全局实例
visualization_generator = VisualizationGenerator()
