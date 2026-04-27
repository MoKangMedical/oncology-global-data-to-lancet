"""
HCC (肝细胞癌) 示例数据集
基于真实流行病学数据创建的示例数据
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any


def generate_hcc_sample_data() -> Dict[str, pd.DataFrame]:
    """
    生成 HCC 示例数据集
    
    Returns:
        包含多个 DataFrame 的字典
    """
    np.random.seed(42)
    
    # 1. GLOBOCAN 数据 (全球癌症统计)
    countries = [
        'China', 'Japan', 'South Korea', 'United States', 'Germany',
        'France', 'United Kingdom', 'Brazil', 'India', 'Australia',
        'Egypt', 'Nigeria', 'Thailand', 'Vietnam', 'Italy'
    ]
    
    globocan_data = []
    for country in countries:
        # 基础发病率 (每10万人)
        base_incidence = np.random.uniform(5, 30)
        base_mortality = base_incidence * np.random.uniform(0.6, 0.9)
        
        for year in range(2000, 2021):
            # 添加年度趋势
            year_factor = 1 + (year - 2000) * np.random.uniform(-0.02, 0.03)
            
            for sex in ['Male', 'Female']:
                # 男性发病率更高
                sex_factor = 2.5 if sex == 'Male' else 1.0
                
                incidence = base_incidence * year_factor * sex_factor * np.random.uniform(0.9, 1.1)
                mortality = base_mortality * year_factor * sex_factor * np.random.uniform(0.9, 1.1)
                
                globocan_data.append({
                    'country': country,
                    'year': year,
                    'cancer_type': 'Liver',
                    'sex': sex,
                    'incidence': round(incidence, 2),
                    'mortality': round(mortality, 2),
                    'asr_incidence': round(incidence * 0.8, 2),
                    'asr_mortality': round(mortality * 0.8, 2),
                    'cases': int(incidence * np.random.uniform(1000, 10000)),
                    'deaths': int(mortality * np.random.uniform(800, 8000))
                })
    
    globocan_df = pd.DataFrame(globocan_data)
    
    # 2. 风险因素数据
    risk_factors = {
        'Hepatitis B': {'prevalence': 0.08, 'rr': 22.3},
        'Hepatitis C': {'prevalence': 0.03, 'rr': 17.3},
        'Alcohol': {'prevalence': 0.30, 'rr': 2.1},
        'Obesity': {'prevalence': 0.15, 'rr': 1.8},
        'Diabetes': {'prevalence': 0.10, 'rr': 2.5},
        'Smoking': {'prevalence': 0.25, 'rr': 1.5},
        'Aflatoxin': {'prevalence': 0.05, 'rr': 3.5}
    }
    
    risk_data = []
    for factor, values in risk_factors.items():
        for country in countries:
            # 不同国家的风险因素暴露率不同
            country_factor = np.random.uniform(0.5, 2.0)
            exposure = min(0.95, values['prevalence'] * country_factor)
            rr = values['rr'] * np.random.uniform(0.8, 1.2)
            
            risk_data.append({
                'country': country,
                'risk_factor': factor,
                'exposure_rate': round(exposure, 4),
                'relative_risk': round(rr, 2),
                'rr_ci_lower': round(rr * 0.7, 2),
                'rr_ci_upper': round(rr * 1.3, 2)
            })
    
    risk_df = pd.DataFrame(risk_data)
    
    # 3. 时间趋势数据 (中国 HCC)
    years = list(range(2000, 2021))
    china_hcc_trend = []
    
    # 基础发病率
    base_rate = 35.0
    
    for year in years:
        # 2000-2010: 上升趋势 (乙肝疫苗效果未显现)
        # 2010-2015: 稳定
        # 2015-2020: 下降趋势 (疫苗接种效果 + 抗病毒治疗)
        if year < 2010:
            trend = 1 + (year - 2000) * 0.01
        elif year < 2015:
            trend = 1.1
        else:
            trend = 1.1 - (year - 2015) * 0.02
        
        rate = base_rate * trend * np.random.uniform(0.95, 1.05)
        
        china_hcc_trend.append({
            'year': year,
            'country': 'China',
            'cancer_type': 'Liver',
            'asr_incidence': round(rate, 2),
            'asr_mortality': round(rate * 0.7, 2),
            'cases': int(rate * 1400),  # 约14万/10万人口
            'deaths': int(rate * 0.7 * 1400)
        })
    
    trend_df = pd.DataFrame(china_hcc_trend)
    
    # 4. 年龄分布数据
    age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34',
                  '35-39', '40-44', '45-49', '50-54', '55-59', '60-64',
                  '65-69', '70-74', '75-79', '80-84', '85+']
    
    # HCC 年龄分布 (发病率随年龄增加)
    age_incidence = [0.1, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0,
                     35.0, 50.0, 60.0, 55.0, 45.0, 35.0, 25.0, 15.0]
    
    age_data = []
    for i, age_group in enumerate(age_groups):
        age_data.append({
            'age_group': age_group,
            'incidence_rate': age_incidence[i],
            'population_weight': [8.86, 8.67, 8.48, 8.29, 8.09, 7.89, 7.68,
                                  7.46, 7.23, 6.98, 6.68, 6.34, 5.93, 5.43,
                                  4.81, 4.04, 3.07, 2.00][i]
        })
    
    age_df = pd.DataFrame(age_data)
    
    return {
        'globocan': globocan_df,
        'risk_factors': risk_df,
        'trend': trend_df,
        'age_distribution': age_df
    }


def get_sample_analysis_results() -> Dict[str, Any]:
    """
    获取示例分析结果
    
    Returns:
        分析结果字典
    """
    return {
        'paf_results': [
            {'risk_factor': 'Hepatitis B', 'paf': 0.32, 'ci_lower': 0.25, 'ci_upper': 0.39,
             'exposure_rate': 0.08, 'relative_risk': 22.3},
            {'risk_factor': 'Hepatitis C', 'paf': 0.18, 'ci_lower': 0.12, 'ci_upper': 0.24,
             'exposure_rate': 0.03, 'relative_risk': 17.3},
            {'risk_factor': 'Alcohol', 'paf': 0.15, 'ci_lower': 0.10, 'ci_upper': 0.20,
             'exposure_rate': 0.30, 'relative_risk': 2.1},
            {'risk_factor': 'Obesity', 'paf': 0.08, 'ci_lower': 0.05, 'ci_upper': 0.11,
             'exposure_rate': 0.15, 'relative_risk': 1.8},
            {'risk_factor': 'Diabetes', 'paf': 0.07, 'ci_lower': 0.04, 'ci_upper': 0.10,
             'exposure_rate': 0.10, 'relative_risk': 2.5},
            {'risk_factor': 'Smoking', 'paf': 0.06, 'ci_lower': 0.03, 'ci_upper': 0.09,
             'exposure_rate': 0.25, 'relative_risk': 1.5},
            {'risk_factor': 'Aflatoxin', 'paf': 0.05, 'ci_lower': 0.02, 'ci_upper': 0.08,
             'exposure_rate': 0.05, 'relative_risk': 3.5}
        ],
        'trend_results': {
            'apc': -1.2,
            'p_value': 0.003,
            'r_squared': 0.85,
            'trend_direction': 'decreasing',
            'joinpoints': [2012],
            'segments': [
                {'start': 2000, 'end': 2012, 'apc': 0.5},
                {'start': 2012, 'end': 2020, 'apc': -2.8}
            ]
        },
        'descriptive_stats': {
            'total_cases': 1500000,
            'total_deaths': 1050000,
            'time_range': '2000-2020',
            'countries': ['China', 'Japan', 'South Korea', 'United States', 'Germany',
                         'France', 'United Kingdom', 'Brazil', 'India', 'Australia',
                         'Egypt', 'Nigeria', 'Thailand', 'Vietnam', 'Italy'],
            'asr_incidence_mean': 15.2,
            'asr_mortality_mean': 10.6
        }
    }


def get_sample_project_config() -> Dict[str, Any]:
    """
    获取示例项目配置
    
    Returns:
        项目配置字典
    """
    return {
        'title': 'Global Epidemiology of Hepatocellular Carcinoma: Risk Factors and Trends (2000-2020)',
        'cancer_types': ['liver'],
        'countries': ['China', 'Japan', 'South Korea', 'United States', 'Germany',
                     'France', 'United Kingdom', 'Brazil', 'India', 'Australia',
                     'Egypt', 'Nigeria', 'Thailand', 'Vietnam', 'Italy'],
        'time_range': {
            'start_year': 2000,
            'end_year': 2020
        },
        'risk_factors': ['hepatitis_b', 'hepatitis_c', 'alcohol', 'obesity', 'diabetes', 'smoking'],
        'data_source': 'GLOBOCAN',
        'description': 'A comprehensive analysis of HCC epidemiology across 15 countries, examining the contribution of major risk factors and temporal trends over two decades.'
    }


# 导出
__all__ = [
    'generate_hcc_sample_data',
    'get_sample_analysis_results',
    'get_sample_project_config'
]
