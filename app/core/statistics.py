"""
肿瘤学全球数据到柳叶刀 - 统计分析引擎
实现 PAF、CDPAF、趋势分析、年龄标准化率等统计方法
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import List, Dict, Any, Optional, Tuple
import statsmodels.api as sm


class StatisticalEngine:
    """统计分析引擎"""
    
    @staticmethod
    def calculate_paf(
        exposure_rate: float,
        relative_risk: float,
        confidence_level: float = 0.95
    ) -> Dict[str, float]:
        """
        计算人群归因分数 (Population Attributable Fraction)
        
        PAF = (Pe × (RR - 1)) / (1 + Pe × (RR - 1))
        
        Args:
            exposure_rate: 暴露率 (Pe)
            relative_risk: 相对风险 (RR)
            confidence_level: 置信水平
            
        Returns:
            包含 PAF 值和置信区间的字典
        """
        if exposure_rate < 0 or exposure_rate > 1:
            raise ValueError("暴露率必须在 0-1 之间")
        if relative_risk < 0:
            raise ValueError("相对风险必须 >= 0")
        
        # 计算 PAF
        paf = (exposure_rate * (relative_risk - 1)) / (1 + exposure_rate * (relative_risk - 1))
        
        # 计算置信区间 (使用 Delta 方法)
        # 这里简化处理，实际应该使用更复杂的统计方法
        z = stats.norm.ppf((1 + confidence_level) / 2)
        
        # 假设相对风险的标准误约为 10%
        rr_se = relative_risk * 0.1
        pe_se = exposure_rate * 0.05
        
        # Delta 方法计算 PAF 的标准误
        paf_se = np.sqrt(
            ((relative_risk - 1) / (1 + exposure_rate * (relative_risk - 1)) ** 2) ** 2 * pe_se ** 2 +
            (exposure_rate / (1 + exposure_rate * (relative_risk - 1)) ** 2) ** 2 * rr_se ** 2
        )
        
        ci_lower = max(0, paf - z * paf_se)
        ci_upper = min(1, paf + z * paf_se)
        
        return {
            "paf": round(paf, 4),
            "ci_lower": round(ci_lower, 4),
            "ci_upper": round(ci_upper, 4),
            "exposure_rate": exposure_rate,
            "relative_risk": relative_risk
        }
    
    @staticmethod
    def calculate_paf_for_risk_factors(
        risk_factors: List[Dict[str, float]]
    ) -> List[Dict[str, Any]]:
        """
        计算多个风险因素的 PAF
        
        Args:
            risk_factors: 风险因素列表，每个包含 name, exposure_rate, relative_risk
            
        Returns:
            PAF 结果列表
        """
        results = []
        for rf in risk_factors:
            paf_result = StatisticalEngine.calculate_paf(
                exposure_rate=rf["exposure_rate"],
                relative_risk=rf["relative_risk"]
            )
            results.append({
                "risk_factor": rf["name"],
                **paf_result
            })
        return results
    
    @staticmethod
    def calculate_cdpaf(
        risk_factors: List[Dict[str, float]],
        correlation_matrix: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """
        计算相关性分解归因分数 (Correlation-Decomposed PAF)
        
        考虑多个风险因素之间的相关性，避免简单相加导致的高估
        
        Args:
            risk_factors: 风险因素列表
            correlation_matrix: 风险因素间的相关性矩阵
            
        Returns:
            CDPAF 结果
        """
        n = len(risk_factors)
        
        # 如果没有提供相关性矩阵，假设独立
        if correlation_matrix is None:
            correlation_matrix = np.eye(n)
        
        # 计算单个 PAF
        individual_pafs = []
        for rf in risk_factors:
            paf_result = StatisticalEngine.calculate_paf(
                exposure_rate=rf["exposure_rate"],
                relative_risk=rf["relative_risk"]
            )
            individual_pafs.append(paf_result["paf"])
        
        # 计算联合 PAF (考虑相关性)
        # 使用 Miettinen 的公式: PAF_joint = 1 - ∏(1 - PAF_i)
        # 但需要根据相关性进行调整
        
        # 简化版本：使用相关性矩阵调整
        paf_vector = np.array(individual_pafs)
        
        # 调整后的联合 PAF
        # 考虑正相关会增加联合效应，负相关会减少
        adjustment = 1 + np.dot(paf_vector, np.dot(correlation_matrix - np.eye(n), paf_vector)) / 2
        joint_paf = 1 - np.prod(1 - paf_vector) * adjustment
        
        # 确保在合理范围内
        joint_paf = max(0, min(1, joint_paf))
        
        return {
            "individual_pafs": dict(zip(
                [rf["name"] for rf in risk_factors],
                individual_pafs
            )),
            "joint_paf": round(joint_paf, 4),
            "sum_individual_pafs": round(sum(individual_pafs), 4),
            "correlation_adjustment": round(adjustment, 4),
            "n_risk_factors": n
        }
    
    @staticmethod
    def joinpoint_regression(
        years: List[int],
        rates: List[float],
        min_joinpoints: int = 0,
        max_joinpoints: int = 3
    ) -> Dict[str, Any]:
        """
        Joinpoint 回归分析
        
        识别时间趋势的转折点，计算年度百分比变化 (APC)
        
        Args:
            years: 年份列表
            rates: 对应的率值列表
            min_joinpoints: 最小转折点数
            max_joinpoints: 最大转折点数
            
        Returns:
            包含转折点和 APC 的结果
        """
        if len(years) != len(rates):
            raise ValueError("年份和率值列表长度必须相同")
        
        if len(years) < 4:
            raise ValueError("至少需要 4 个数据点进行 Joinpoint 分析")
        
        years = np.array(years)
        rates = np.array(rates)
        
        # 对率值取对数 (用于计算 APC)
        log_rates = np.log(rates + 1e-10)  # 避免 log(0)
        
        # 使用分段线性回归寻找最佳转折点
        best_model = None
        best_bic = np.inf
        
        for n_joinpoints in range(min_joinpoints, min(max_joinpoints + 1, len(years) // 2)):
            # 尝试所有可能的转折点位置
            if n_joinpoints == 0:
                # 无转折点，简单线性回归
                model = sm.OLS(log_rates, sm.add_constant(years)).fit()
                bic = model.bic
                if bic < best_bic:
                    best_bic = bic
                    best_model = {
                        "n_joinpoints": 0,
                        "joinpoints": [],
                        "segments": [(years[0], years[-1])],
                        "apcs": [model.params[1] * 100],  # 转换为百分比
                        "p_values": [model.pvalues[1]],
                        "r_squared": model.rsquared
                    }
            else:
                # 有转折点的情况
                # 这里简化处理，使用网格搜索
                from itertools import combinations
                
                # 可能的转折点位置 (排除首尾)
                possible_positions = list(range(2, len(years) - 2))
                
                for positions in combinations(possible_positions, n_joinpoints):
                    positions = sorted(positions)
                    
                    # 分段拟合
                    segments = []
                    apcs = []
                    p_values = []
                    total_sse = 0
                    
                    # 添加首尾位置
                    all_positions = [0] + list(positions) + [len(years)]
                    
                    for i in range(len(all_positions) - 1):
                        start = all_positions[i]
                        end = all_positions[i + 1]
                        
                        segment_years = years[start:end]
                        segment_rates = log_rates[start:end]
                        
                        if len(segment_years) < 2:
                            continue
                        
                        # 线性回归
                        X = sm.add_constant(segment_years)
                        model = sm.OLS(segment_rates, X).fit()
                        
                        segments.append((int(segment_years[0]), int(segment_years[-1])))
                        apcs.append(model.params[1] * 100)
                        p_values.append(model.pvalues[1])
                        total_sse += model.ssr
                    
                    # 计算 BIC
                    n = len(years)
                    k = n_joinpoints * 2 + 2  # 参数数量
                    bic = n * np.log(total_sse / n) + k * np.log(n)
                    
                    if bic < best_bic:
                        best_bic = bic
                        best_model = {
                            "n_joinpoints": n_joinpoints,
                            "joinpoints": [int(years[p]) for p in positions],
                            "segments": segments,
                            "apcs": [round(apc, 2) for apc in apcs],
                            "p_values": [round(p, 4) for p in p_values],
                            "r_squared": 1 - total_sse / np.sum((log_rates - np.mean(log_rates)) ** 2)
                        }
        
        if best_model is None:
            # 如果没有找到合适的模型，返回简单结果
            return {
                "n_joinpoints": 0,
                "joinpoints": [],
                "segments": [(int(years[0]), int(years[-1]))],
                "apcs": [0],
                "p_values": [1],
                "r_squared": 0,
                "message": "无法找到显著的趋势变化"
            }
        
        # 计算总体 APC
        overall_apc = np.mean(best_model["apcs"])
        
        return {
            **best_model,
            "overall_apc": round(overall_apc, 2),
            "bic": round(best_bic, 2)
        }
    
    @staticmethod
    def age_standardized_rate(
        age_specific_rates: List[float],
        age_specific_population: List[int],
        standard_population: Optional[List[int]] = None
    ) -> Dict[str, float]:
        """
        计算年龄标准化率 (Age-Standardized Rate)
        
        使用直接标准化方法
        
        Args:
            age_specific_rates: 各年龄组的率
            age_specific_population: 各年龄组的人口数
            standard_population: 标准人口分布 (默认使用世界标准人口)
            
        Returns:
            年龄标准化率及其置信区间
        """
        if len(age_specific_rates) != len(age_specific_population):
            raise ValueError("率值和人口数列表长度必须相同")
        
        # 默认使用世界标准人口 (WHO 2000-2025)
        if standard_population is None:
            # 18 个年龄组 (0-4, 5-9, ..., 80-84, 85+)
            standard_population = [
                8860, 8670, 8480, 8290, 8090,
                7890, 7680, 7460, 7230, 6980,
                6680, 6340, 5930, 5430, 4810,
                4040, 3070, 2000
            ]
        
        # 确保长度匹配
        n_groups = min(len(age_specific_rates), len(standard_population))
        rates = np.array(age_specific_rates[:n_groups])
        standard = np.array(standard_population[:n_groups], dtype=float)
        population = np.array(age_specific_population[:n_groups], dtype=float)
        
        # 计算标准化率
        # ASR = Σ(rate_i × standard_i) / Σ(standard_i)
        asr = np.sum(rates * standard) / np.sum(standard)
        
        # 计算方差 (用于置信区间)
        # Var(ASR) = Σ(standard_i^2 × rate_i / population_i) / (Σ(standard_i))^2
        variance = np.sum(standard ** 2 * rates / population) / (np.sum(standard)) ** 2
        se = np.sqrt(variance)
        
        # 95% 置信区间
        z = 1.96
        ci_lower = asr - z * se
        ci_upper = asr + z * se
        
        return {
            "asr": round(asr, 2),
            "se": round(se, 4),
            "ci_lower": round(max(0, ci_lower), 2),
            "ci_upper": round(ci_upper, 2),
            "n_age_groups": n_groups
        }
    
    @staticmethod
    def calculate_relative_risk(
        exposed_cases: int,
        exposed_total: int,
        unexposed_cases: int,
        unexposed_total: int
    ) -> Dict[str, float]:
        """
        计算相对风险 (Relative Risk)
        
        Args:
            exposed_cases: 暴露组病例数
            exposed_total: 暴露组总人数
            unexposed_cases: 非暴露组病例数
            unexposed_total: 非暴露组总人数
            
        Returns:
            相对风险及其置信区间
        """
        # 计算发病率
        rate_exposed = exposed_cases / exposed_total
        rate_unexposed = unexposed_cases / unexposed_total
        
        # 计算 RR
        rr = rate_exposed / rate_unexposed
        
        # 计算 ln(RR) 的标准误
        se_ln_rr = np.sqrt(
            1 / exposed_cases - 1 / exposed_total +
            1 / unexposed_cases - 1 / unexposed_total
        )
        
        # 95% 置信区间
        z = 1.96
        ln_rr = np.log(rr)
        ci_lower = np.exp(ln_rr - z * se_ln_rr)
        ci_upper = np.exp(ln_rr + z * se_ln_rr)
        
        # 计算 p 值 (使用卡方检验)
        # 2x2 列联表
        table = np.array([
            [exposed_cases, exposed_total - exposed_cases],
            [unexposed_cases, unexposed_total - unexposed_cases]
        ])
        chi2, p_value, _, _ = stats.chi2_contingency(table)
        
        return {
            "rr": round(rr, 4),
            "ci_lower": round(ci_lower, 4),
            "ci_upper": round(ci_upper, 4),
            "p_value": round(p_value, 6),
            "rate_exposed": round(rate_exposed, 6),
            "rate_unexposed": round(rate_unexposed, 6)
        }
    
    @staticmethod
    def trend_analysis(
        years: List[int],
        values: List[float]
    ) -> Dict[str, Any]:
        """
        简单趋势分析
        
        Args:
            years: 年份列表
            values: 对应的值
            
        Returns:
            趋势分析结果
        """
        if len(years) != len(values):
            raise ValueError("年份和值列表长度必须相同")
        
        years = np.array(years, dtype=float)
        values = np.array(values)
        
        # 线性回归
        X = sm.add_constant(years)
        model = sm.OLS(values, X).fit()
        
        # 计算 APC (Annual Percentage Change)
        # APC = (exp(b) - 1) * 100，其中 b 是回归系数
        slope = model.params[1]
        apc = (np.exp(slope) - 1) * 100
        
        # 预测值
        predicted = model.predict(X)
        
        return {
            "apc": round(apc, 2),
            "slope": round(slope, 6),
            "intercept": round(model.params[0], 4),
            "r_squared": round(model.rsquared, 4),
            "p_value": round(model.pvalues[1], 6),
            "trend_direction": "increasing" if slope > 0 else "decreasing",
            "predicted_values": predicted.tolist(),
            "residuals": (values - predicted).tolist()
        }


# 创建全局实例
statistical_engine = StatisticalEngine()
