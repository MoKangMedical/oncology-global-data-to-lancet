"""
肿瘤学全球数据到柳叶刀 - 数据解析器
支持 GLOBOCAN、GBD、CI5 等数据源的 CSV/Excel 解析
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import io
import base64


class DataParser:
    """数据解析器基类"""
    
    # 标准列名映射
    STANDARD_COLUMNS = {
        'country': ['country', 'Country', 'COUNTRY', 'nation', 'Nation', 'area', 'Area'],
        'year': ['year', 'Year', 'YEAR', 'period', 'Period'],
        'cancer_type': ['cancer', 'Cancer', 'cancer_type', 'Cancer_Type', 'type', 'Type', 
                       'site', 'Site', 'neoplasm', 'Neoplasm'],
        'sex': ['sex', 'Sex', 'SEX', 'gender', 'Gender'],
        'incidence': ['incidence', 'Incidence', 'INCIDENCE', 'cases', 'Cases', 'new_cases'],
        'mortality': ['mortality', 'Mortality', 'MORTALITY', 'deaths', 'Deaths', 'death'],
        'prevalence': ['prevalence', 'Prevalence', 'PREVALENCE'],
        'asr_incidence': ['asr_incidence', 'ASR_incidence', 'asr_i', 'age_standardized_incidence'],
        'asr_mortality': ['asr_mortality', 'ASR_mortality', 'asr_m', 'age_standardized_mortality'],
        'population': ['population', 'Population', 'POPULATION', 'pop', 'Pop'],
        'cases': ['cases', 'Cases', 'CASES', 'new_cases', 'incident_cases'],
        'deaths': ['deaths', 'Deaths', 'DEATHS', 'mortal_cases'],
        'age_group': ['age', 'Age', 'AGE', 'age_group', 'Age_Group', 'age_range'],
    }
    
    # 癌症类型标准化映射
    CANCER_TYPE_MAPPING = {
        'liver': ['liver', 'Liver', 'LIVER', 'hepatic', 'Hepatic', '肝', '肝癌', '肝细胞癌', 'HCC',
                  'hepatocellular', 'Liver cancer'],
        'lung': ['lung', 'Lung', 'LUNG', 'pulmonary', 'Pulmonary', '肺', '肺癌', 'Lung cancer'],
        'breast': ['breast', 'Breast', 'BREAST', '乳腺', '乳腺癌', 'Breast cancer'],
        'colorectal': ['colorectal', 'Colorectal', 'COLORECTAL', 'colon', 'Colon', 'rectal', 'Rectal',
                       '结直肠', '结直肠癌', 'Colorectal cancer'],
        'stomach': ['stomach', 'Stomach', 'STOMACH', 'gastric', 'Gastric', '胃', '胃癌', 'Stomach cancer'],
        'prostate': ['prostate', 'Prostate', 'PROSTATE', '前列腺', '前列腺癌', 'Prostate cancer'],
        'thyroid': ['thyroid', 'Thyroid', 'THYROID', '甲状腺', '甲状腺癌', 'Thyroid cancer'],
        'esophagus': ['esophagus', 'Esophagus', 'ESOPHAGUS', 'esophageal', 'Esophageal',
                      '食管', '食管癌', 'Esophageal cancer'],
        'pancreas': ['pancreas', 'Pancreas', 'PANCREAS', 'pancreatic', 'Pancreatic',
                     '胰腺', '胰腺癌', 'Pancreatic cancer'],
        'bladder': ['bladder', 'Bladder', 'BLADDER', '膀胱', '膀胱癌', 'Bladder cancer'],
    }
    
    # 国家名称标准化映射
    COUNTRY_MAPPING = {
        'china': ['china', 'China', 'CHINA', '中国', 'People\'s Republic of China'],
        'united_states': ['united states', 'United States', 'USA', 'US', '美国'],
        'japan': ['japan', 'Japan', 'JAPAN', '日本'],
        'korea': ['korea', 'Korea', 'KOREA', '韩国', 'South Korea', 'Republic of Korea'],
        'india': ['india', 'India', 'INDIA', '印度'],
        'germany': ['germany', 'Germany', 'GERMANY', '德国'],
        'france': ['france', 'France', 'FRANCE', '法国'],
        'united_kingdom': ['united kingdom', 'United Kingdom', 'UK', '英国', 'Great Britain'],
        'brazil': ['brazil', 'Brazil', 'BRAZIL', '巴西'],
        'australia': ['australia', 'Australia', 'AUSTRALIA', '澳大利亚'],
    }
    
    @classmethod
    def normalize_column_name(cls, col_name: str) -> Optional[str]:
        """标准化列名"""
        col_lower = col_name.lower().strip()
        
        for standard_name, aliases in cls.STANDARD_COLUMNS.items():
            if col_name in aliases or col_lower in [a.lower() for a in aliases]:
                return standard_name
        
        return None
    
    @classmethod
    def normalize_cancer_type(cls, cancer_type: str) -> str:
        """标准化癌症类型"""
        cancer_lower = cancer_type.lower().strip()
        
        for standard_name, aliases in cls.CANCER_TYPE_MAPPING.items():
            if cancer_type in aliases or cancer_lower in [a.lower() for a in aliases]:
                return standard_name
        
        return cancer_lower
    
    @classmethod
    def normalize_country(cls, country: str) -> str:
        """标准化国家名称"""
        country_lower = country.lower().strip()
        
        for standard_name, aliases in cls.COUNTRY_MAPPING.items():
            if country in aliases or country_lower in [a.lower() for a in aliases]:
                return standard_name
        
        return country_lower
    
    @classmethod
    def parse_csv(
        cls,
        file_content: str,
        encoding: str = 'utf-8'
    ) -> pd.DataFrame:
        """
        解析 CSV 文件
        
        Args:
            file_content: CSV 文件内容
            encoding: 文件编码
            
        Returns:
            解析后的 DataFrame
        """
        # 尝试不同的分隔符
        for sep in [',', '\t', ';', '|']:
            try:
                df = pd.read_csv(
                    io.StringIO(file_content),
                    sep=sep,
                    encoding=encoding
                )
                if len(df.columns) > 1:
                    return df
            except:
                continue
        
        raise ValueError("无法解析 CSV 文件，请检查格式")
    
    @classmethod
    def parse_excel(
        cls,
        file_content: bytes,
        sheet_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        解析 Excel 文件
        
        Args:
            file_content: Excel 文件内容 (bytes)
            sheet_name: 工作表名称
            
        Returns:
            解析后的 DataFrame
        """
        try:
            # 尝试 xlsx 格式
            df = pd.read_excel(
                io.BytesIO(file_content),
                sheet_name=sheet_name or 0,
                engine='openpyxl'
            )
            return df
        except:
            try:
                # 尝试 xls 格式
                df = pd.read_excel(
                    io.BytesIO(file_content),
                    sheet_name=sheet_name or 0,
                    engine='xlrd'
                )
                return df
            except Exception as e:
                raise ValueError(f"无法解析 Excel 文件: {str(e)}")
    
    @classmethod
    def standardize_dataframe(
        cls,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        标准化 DataFrame 的列名和数据
        
        Args:
            df: 原始 DataFrame
            
        Returns:
            标准化后的 DataFrame
        """
        # 创建列名映射
        column_mapping = {}
        for col in df.columns:
            standard_name = cls.normalize_column_name(col)
            if standard_name:
                column_mapping[col] = standard_name
        
        # 重命名列
        df = df.rename(columns=column_mapping)
        
        # 标准化癌症类型
        if 'cancer_type' in df.columns:
            df['cancer_type'] = df['cancer_type'].apply(cls.normalize_cancer_type)
        
        # 标准化国家名称
        if 'country' in df.columns:
            df['country'] = df['country'].apply(cls.normalize_country)
        
        # 确保数值列是数字
        numeric_columns = ['incidence', 'mortality', 'prevalence', 'asr_incidence', 
                          'asr_mortality', 'population', 'cases', 'deaths']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 确保年份是整数
        if 'year' in df.columns:
            df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
        
        return df
    
    @classmethod
    def validate_dataframe(
        cls,
        df: pd.DataFrame,
        required_columns: List[str] = None
    ) -> Tuple[bool, List[str]]:
        """
        验证 DataFrame 的格式
        
        Args:
            df: 要验证的 DataFrame
            required_columns: 必需的列名
            
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        # 默认必需列
        if required_columns is None:
            required_columns = ['country', 'year', 'cancer_type']
        
        # 检查必需列
        for col in required_columns:
            if col not in df.columns:
                errors.append(f"缺少必需列: {col}")
        
        # 检查数据类型
        if 'year' in df.columns:
            if not pd.api.types.is_numeric_dtype(df['year']):
                errors.append("year 列必须是数值类型")
        
        # 检查缺失值
        for col in required_columns:
            if col in df.columns:
                missing_count = df[col].isna().sum()
                if missing_count > 0:
                    errors.append(f"{col} 列有 {missing_count} 个缺失值")
        
        # 检查数据范围
        if 'year' in df.columns:
            year_min = df['year'].min()
            year_max = df['year'].max()
            if year_min < 1900 or year_max > 2100:
                errors.append(f"年份范围异常: {year_min}-{year_max}")
        
        return len(errors) == 0, errors
    
    @classmethod
    def parse_and_standardize(
        cls,
        file_content: str,
        file_type: str = 'csv'
    ) -> Tuple[pd.DataFrame, List[str]]:
        """
        解析并标准化数据文件
        
        Args:
            file_content: 文件内容
            file_type: 文件类型 ('csv' 或 'excel')
            
        Returns:
            (标准化后的 DataFrame, 警告信息列表)
        """
        warnings = []
        
        # 解析文件
        if file_type == 'csv':
            df = cls.parse_csv(file_content)
        elif file_type == 'excel':
            # 如果是 base64 编码的内容
            if isinstance(file_content, str):
                file_content = base64.b64decode(file_content)
            df = cls.parse_excel(file_content)
        else:
            raise ValueError(f"不支持的文件类型: {file_type}")
        
        # 记录原始列名
        original_columns = list(df.columns)
        warnings.append(f"原始列名: {original_columns}")
        
        # 标准化
        df = cls.standardize_dataframe(df)
        
        # 记录标准化后的列名
        standardized_columns = list(df.columns)
        warnings.append(f"标准化后列名: {standardized_columns}")
        
        # 验证
        is_valid, errors = cls.validate_dataframe(df)
        if not is_valid:
            warnings.extend(errors)
        
        return df, warnings
    
    @classmethod
    def filter_data(
        cls,
        df: pd.DataFrame,
        countries: Optional[List[str]] = None,
        cancer_types: Optional[List[str]] = None,
        year_range: Optional[Tuple[int, int]] = None,
        sex: Optional[str] = None
    ) -> pd.DataFrame:
        """
        过滤数据
        
        Args:
            df: 数据 DataFrame
            countries: 国家列表
            cancer_types: 癌症类型列表
            year_range: 年份范围 (start, end)
            sex: 性别 ('male', 'female', 'both')
            
        Returns:
            过滤后的 DataFrame
        """
        filtered_df = df.copy()
        
        if countries and 'country' in filtered_df.columns:
            # 标准化国家名称
            normalized_countries = [cls.normalize_country(c) for c in countries]
            filtered_df = filtered_df[filtered_df['country'].isin(normalized_countries)]
        
        if cancer_types and 'cancer_type' in filtered_df.columns:
            # 标准化癌症类型
            normalized_types = [cls.normalize_cancer_type(ct) for ct in cancer_types]
            filtered_df = filtered_df[filtered_df['cancer_type'].isin(normalized_types)]
        
        if year_range and 'year' in filtered_df.columns:
            start_year, end_year = year_range
            filtered_df = filtered_df[
                (filtered_df['year'] >= start_year) & 
                (filtered_df['year'] <= end_year)
            ]
        
        if sex and 'sex' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['sex'].str.lower() == sex.lower()]
        
        return filtered_df
    
    @classmethod
    def get_summary_statistics(
        cls,
        df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        获取数据摘要统计
        
        Args:
            df: 数据 DataFrame
            
        Returns:
            摘要统计字典
        """
        summary = {
            "total_records": len(df),
            "columns": list(df.columns),
        }
        
        if 'country' in df.columns:
            summary["n_countries"] = df['country'].nunique()
            summary["countries"] = df['country'].unique().tolist()
        
        if 'year' in df.columns:
            summary["year_range"] = {
                "min": int(df['year'].min()),
                "max": int(df['year'].max())
            }
        
        if 'cancer_type' in df.columns:
            summary["n_cancer_types"] = df['cancer_type'].nunique()
            summary["cancer_types"] = df['cancer_type'].unique().tolist()
        
        # 数值列统计
        numeric_cols = ['incidence', 'mortality', 'asr_incidence', 'asr_mortality']
        for col in numeric_cols:
            if col in df.columns:
                summary[f"{col}_stats"] = {
                    "mean": round(df[col].mean(), 2),
                    "std": round(df[col].std(), 2),
                    "min": round(df[col].min(), 2),
                    "max": round(df[col].max(), 2)
                }
        
        return summary


# 创建全局实例
data_parser = DataParser()
