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


# 创建全局实例
visualization_generator = VisualizationGenerator()
