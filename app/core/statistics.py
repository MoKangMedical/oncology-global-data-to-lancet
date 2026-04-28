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


    # ==================== 生存分析 (Survival Analysis) ====================

    @staticmethod
    def kaplan_meier_estimate(
        times: List[float],
        events: List[int],
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        Kaplan-Meier 生存分析估计

        非参数方法估计生存函数 S(t) = P(T > t)

        Args:
            times: 观察时间列表
            events: 事件指示列表 (1=事件发生, 0=删失)
            confidence_level: 置信水平

        Returns:
            包含生存曲线数据、中位生存时间等的字典
        """
        if len(times) != len(events):
            raise ValueError("时间和事件列表长度必须相同")
        if len(times) == 0:
            raise ValueError("数据不能为空")

        times = np.array(times, dtype=float)
        events = np.array(events, dtype=int)

        # 获取所有事件时间点（去重且排序）
        event_times = np.sort(np.unique(times[events == 1]))

        if len(event_times) == 0:
            return {
                "time_points": [],
                "survival_prob": [],
                "ci_lower": [],
                "ci_upper": [],
                "median_survival": None,
                "n_at_risk": [],
                "n_events": [],
                "n_censored": [],
                "total_subjects": len(times),
                "total_events": int(np.sum(events)),
                "message": "没有观察到任何事件"
            }

        # Kaplan-Meier 估计（Nelson-Aalen 变体用于方差）
        z = stats.norm.ppf((1 + confidence_level) / 2)

        km_times = []
        km_survival = []
        km_ci_lower = []
        km_ci_upper = []
        km_n_risk = []
        km_n_events = []
        km_n_censored = []

        survival = 1.0
        variance_sum = 0.0  # 累积方差用于 Greenwood 公式

        for t in event_times:
            # 在时间 t 之前仍处于风险中的个体数
            n_at_risk = np.sum(times >= t)
            # 在时间 t 发生事件的个体数
            n_events = np.sum((times == t) & (events == 1))
            # 在时间 t 删失的个体数
            n_censored = np.sum((times == t) & (events == 0))

            if n_at_risk == 0:
                continue

            # 更新生存概率
            survival *= (1 - n_events / n_at_risk)

            # Greenwood 公式计算方差
            if n_at_risk > n_events:
                variance_sum += n_events / (n_at_risk * (n_at_risk - n_events))

            # 标准误
            se = survival * np.sqrt(variance_sum) if variance_sum > 0 else 0

            km_times.append(float(t))
            km_survival.append(round(float(survival), 6))
            km_ci_lower.append(round(float(max(0, survival - z * se)), 6))
            km_ci_upper.append(round(float(min(1, survival + z * se)), 6))
            km_n_risk.append(int(n_at_risk))
            km_n_events.append(int(n_events))
            km_n_censored.append(int(n_censored))

        # 中位生存时间
        median_survival = None
        for i, s in enumerate(km_survival):
            if s <= 0.5:
                median_survival = km_times[i]
                break

        return {
            "time_points": km_times,
            "survival_prob": km_survival,
            "ci_lower": km_ci_lower,
            "ci_upper": km_ci_upper,
            "median_survival": median_survival,
            "n_at_risk": km_n_risk,
            "n_events": km_n_events,
            "n_censored": km_n_censored,
            "total_subjects": len(times),
            "total_events": int(np.sum(events)),
            "confidence_level": confidence_level
        }

    @staticmethod
    def cox_regression(
        times: List[float],
        events: List[int],
        covariates: Dict[str, List[float]],
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        Cox 比例风险回归模型

        h(t|X) = h0(t) * exp(β1*X1 + β2*X2 + ... + βp*Xp)

        使用 Newton-Raphson 迭代求解偏似然方程

        Args:
            times: 观察时间列表
            events: 事件指示列表 (1=事件发生, 0=删失)
            covariates: 协变量字典 {变量名: 值列表}
            confidence_level: 置信水平

        Returns:
            包含回归系数、风险比(HR)、置信区间等的字典
        """
        if len(times) != len(events):
            raise ValueError("时间和事件列表长度必须相同")

        n = len(times)
        times = np.array(times, dtype=float)
        events = np.array(events, dtype=int)

        # 构建设计矩阵
        cov_names = list(covariates.keys())
        p = len(cov_names)

        if p == 0:
            raise ValueError("至少需要一个协变量")

        X = np.column_stack([np.array(covariates[name], dtype=float) for name in cov_names])

        if X.shape[0] != n:
            raise ValueError("协变量长度与时间/事件长度不匹配")

        # 标准化协变量（提高数值稳定性）
        X_mean = X.mean(axis=0)
        X_std = X.std(axis=0)
        X_std[X_std == 0] = 1.0
        X_scaled = (X - X_mean) / X_std

        # 排序（按时间降序，用于 Breslow 偏似然）
        order = np.argsort(-times)
        times_sorted = times[order]
        events_sorted = events[order]
        X_sorted = X_scaled[order]

        # Newton-Raphson 迭代求解 Cox 偏似然
        beta = np.zeros(p)
        max_iter = 50
        tol = 1e-6

        for iteration in range(max_iter):
            # 计算 exp(X * beta)
            risk_scores = np.exp(X_sorted @ beta)

            # 计算梯度和 Hessian
            gradient = np.zeros(p)
            hessian = np.zeros((p, p))

            for i in range(n):
                if events_sorted[i] == 0:
                    continue

                # 风险集（时间 >= 当前时间的个体）
                risk_set_mask = times_sorted >= times_sorted[i]
                risk_set_risk = risk_scores[risk_set_mask]
                risk_set_X = X_sorted[risk_set_mask]

                # 加权平均
                denom = np.sum(risk_set_risk)
                if denom == 0:
                    continue

                weighted_x = (risk_set_risk[:, np.newaxis] * risk_set_X).sum(axis=0) / denom

                # 梯度
                gradient += X_sorted[i] - weighted_x

                # Hessian
                weighted_xx = (risk_set_risk[:, np.newaxis, np.newaxis] *
                              (risk_set_X[:, :, np.newaxis] * risk_set_X[:, np.newaxis, :])).sum(axis=0) / denom
                hessian -= weighted_xx - np.outer(weighted_x, weighted_x)

            # 更新 beta
            try:
                delta = np.linalg.solve(hessian, gradient)
            except np.linalg.LinAlgError:
                break

            beta -= delta

            if np.max(np.abs(delta)) < tol:
                break

        # 计算方差-协方差矩阵
        try:
            var_cov = np.linalg.inv(-hessian)
            se = np.sqrt(np.diag(var_cov))
        except np.linalg.LinAlgError:
            se = np.full(p, np.nan)

        # 还原到原始尺度的风险比
        z = stats.norm.ppf((1 + confidence_level) / 2)

        results = []
        for j, name in enumerate(cov_names):
            # HR = exp(beta_original) = exp(beta_scaled / X_std)
            beta_orig = beta[j] / X_std[j]
            hr = np.exp(beta_orig)
            se_orig = se[j] / X_std[j]
            hr_ci_lower = np.exp(beta_orig - z * se_orig)
            hr_ci_upper = np.exp(beta_orig + z * se_orig)

            # Wald 检验 p 值
            if not np.isnan(se[j]) and se[j] > 0:
                wald_stat = (beta[j] / se[j]) ** 2
                p_value = 1 - stats.chi2.cdf(wald_stat, 1)
            else:
                wald_stat = np.nan
                p_value = np.nan

            results.append({
                "variable": name,
                "coef": round(float(beta_orig), 6),
                "hr": round(float(hr), 4),
                "hr_ci_lower": round(float(hr_ci_lower), 4),
                "hr_ci_upper": round(float(hr_ci_upper), 4),
                "se": round(float(se_orig), 6),
                "wald_statistic": round(float(wald_stat), 4) if not np.isnan(wald_stat) else None,
                "p_value": round(float(p_value), 6) if not np.isnan(p_value) else None,
                "significant": bool(p_value < 0.05) if not np.isnan(p_value) else None
            })

        # 计算 -2 log likelihood 用于模型评估
        risk_scores_full = np.exp(X_sorted @ beta)
        log_lik = 0.0
        cum_risk = 0.0
        for i in range(n):
            cum_risk += risk_scores_full[i]
            if events_sorted[i] == 1:
                log_lik += X_sorted[i] @ beta - np.log(cum_risk)

        return {
            "coefficients": results,
            "converged": bool(np.max(np.abs(delta)) < tol),
            "iterations": iteration + 1,
            "n_subjects": n,
            "n_events": int(np.sum(events)),
            "log_likelihood": round(float(log_lik), 4),
            "confidence_level": confidence_level
        }

    # ==================== Meta 分析 (Meta-Analysis) ====================

    @staticmethod
    def heterogeneity_test(
        effects: List[float],
        variances: List[float]
    ) -> Dict[str, Any]:
        """
        异质性检验

        计算 Cochran's Q 检验和 I² 统计量

        Q = Σ(wi * (yi - y_bar)^2)
        I² = max(0, (Q - df) / Q × 100%)

        Args:
            effects: 各研究的效应量列表
            variances: 各研究的方差列表

        Returns:
            Q 统计量、I² 统计量、p 值等
        """
        if len(effects) != len(variances):
            raise ValueError("效应量和方差列表长度必须相同")
        if len(effects) < 2:
            raise ValueError("至少需要两个研究")

        effects = np.array(effects, dtype=float)
        variances = np.array(variances, dtype=float)

        k = len(effects)
        df = k - 1

        # 权重（固定效应模型的权重 = 1/variance）
        weights = 1.0 / variances

        # 加权平均效应量
        pooled_effect = np.sum(weights * effects) / np.sum(weights)

        # Cochran's Q 统计量
        Q = np.sum(weights * (effects - pooled_effect) ** 2)

        # Q 的 p 值（卡方分布）
        p_value = 1 - stats.chi2.cdf(Q, df)

        # I² 统计量
        I_squared = max(0, (Q - df) / Q * 100) if Q > 0 else 0

        # H² 统计量
        H_squared = Q / df if df > 0 else 1

        # τ² (tau-squared) - 研究间方差 (DerSimonian-Leard)
        C = np.sum(weights) - np.sum(weights ** 2) / np.sum(weights)
        tau_squared = max(0, (Q - df) / C) if C > 0 else 0

        # 异质性程度判断
        if I_squared < 25:
            heterogeneity_level = "low"
        elif I_squared < 50:
            heterogeneity_level = "moderate"
        elif I_squared < 75:
            heterogeneity_level = "substantial"
        else:
            heterogeneity_level = "considerable"

        return {
            "Q": round(float(Q), 4),
            "Q_df": int(df),
            "Q_p_value": round(float(p_value), 6),
            "I_squared": round(float(I_squared), 2),
            "H_squared": round(float(H_squared), 4),
            "tau_squared": round(float(tau_squared), 6),
            "heterogeneity_level": heterogeneity_level,
            "n_studies": k,
            "significant_heterogeneity": bool(p_value < 0.10)
        }

    @staticmethod
    def meta_analysis_fixed_effect(
        effects: List[float],
        variances: List[float],
        study_names: Optional[List[str]] = None,
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        固定效应 Meta 分析 (Inverse Variance Method)

        合并效应量: θ_hat = Σ(wi * yi) / Σ(wi)
        其中 wi = 1 / vi (方差的倒数)

        Args:
            effects: 各研究的效应量列表 (如 log-OR, log-RR, mean diff)
            variances: 各研究效应量的方差列表
            study_names: 各研究名称列表
            confidence_level: 置信水平

        Returns:
            合并效应量、置信区间、各研究权重等
        """
        effects = np.array(effects, dtype=float)
        variances = np.array(variances, dtype=float)
        k = len(effects)

        if study_names is None:
            study_names = [f"Study_{i+1}" for i in range(k)]

        # 权重
        weights = 1.0 / variances
        total_weight = np.sum(weights)

        # 合并效应量
        pooled_effect = np.sum(weights * effects) / total_weight

        # 合并效应量的方差和标准误
        pooled_var = 1.0 / total_weight
        pooled_se = np.sqrt(pooled_var)

        # 置信区间
        z = stats.norm.ppf((1 + confidence_level) / 2)
        ci_lower = pooled_effect - z * pooled_se
        ci_upper = pooled_effect + z * pooled_se

        # Z 检验
        z_stat = pooled_effect / pooled_se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        # 各研究的贡献
        study_results = []
        for i in range(k):
            ci_l = effects[i] - z * np.sqrt(variances[i])
            ci_u = effects[i] + z * np.sqrt(variances[i])
            study_results.append({
                "study": study_names[i],
                "effect": round(float(effects[i]), 6),
                "variance": round(float(variances[i]), 6),
                "se": round(float(np.sqrt(variances[i])), 6),
                "ci_lower": round(float(ci_l), 6),
                "ci_upper": round(float(ci_u), 6),
                "weight": round(float(weights[i] / total_weight * 100), 2),
                "weight_raw": round(float(weights[i]), 6)
            })

        return {
            "method": "fixed_effect_inverse_variance",
            "pooled_effect": round(float(pooled_effect), 6),
            "pooled_se": round(float(pooled_se), 6),
            "ci_lower": round(float(ci_lower), 6),
            "ci_upper": round(float(ci_upper), 6),
            "z_statistic": round(float(z_stat), 4),
            "p_value": round(float(p_value), 6),
            "significant": bool(p_value < 0.05),
            "n_studies": k,
            "studies": study_results,
            "confidence_level": confidence_level
        }

    @staticmethod
    def meta_analysis_random_effect(
        effects: List[float],
        variances: List[float],
        study_names: Optional[List[str]] = None,
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        随机效应 Meta 分析 (DerSimonian-Laird 方法)

        使用 DerSimonian-Laird 估计器估计 τ²，然后用
        wi* = 1 / (vi + τ²) 作为新的权重

        Args:
            effects: 各研究的效应量列表
            variances: 各研究效应量的方差列表
            study_names: 各研究名称列表
            confidence_level: 置信水平

        Returns:
            合并效应量、τ²、置信区间等
        """
        effects = np.array(effects, dtype=float)
        variances = np.array(variances, dtype=float)
        k = len(effects)

        if study_names is None:
            study_names = [f"Study_{i+1}" for i in range(k)]

        df = k - 1

        # 第一步：固定效应权重
        w_fe = 1.0 / variances
        pooled_fe = np.sum(w_fe * effects) / np.sum(w_fe)

        # 第二步：计算 Q 统计量
        Q = np.sum(w_fe * (effects - pooled_fe) ** 2)

        # 第三步：DerSimonian-Laird 估计 τ²
        C = np.sum(w_fe) - np.sum(w_fe ** 2) / np.sum(w_fe)
        tau_squared = max(0, (Q - df) / C) if C > 0 else 0

        # 第四步：随机效应权重
        w_re = 1.0 / (variances + tau_squared)
        total_weight = np.sum(w_re)

        # 合并效应量
        pooled_effect = np.sum(w_re * effects) / total_weight

        # 合并效应量的方差和标准误
        pooled_var = 1.0 / total_weight
        pooled_se = np.sqrt(pooled_var)

        # 置信区间
        z = stats.norm.ppf((1 + confidence_level) / 2)
        ci_lower = pooled_effect - z * pooled_se
        ci_upper = pooled_effect + z * pooled_se

        # Z 检验
        z_stat = pooled_effect / pooled_se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        # 预测区间 (prediction interval)
        if df > 0:
            t_crit = stats.t.ppf((1 + confidence_level) / 2, df)
            pred_lower = pooled_effect - t_crit * np.sqrt(pooled_var + tau_squared)
            pred_upper = pooled_effect + t_crit * np.sqrt(pooled_var + tau_squared)
        else:
            pred_lower = None
            pred_upper = None

        # 各研究的贡献
        study_results = []
        for i in range(k):
            ci_l = effects[i] - z * np.sqrt(variances[i])
            ci_u = effects[i] + z * np.sqrt(variances[i])
            study_results.append({
                "study": study_names[i],
                "effect": round(float(effects[i]), 6),
                "variance": round(float(variances[i]), 6),
                "se": round(float(np.sqrt(variances[i])), 6),
                "ci_lower": round(float(ci_l), 6),
                "ci_upper": round(float(ci_u), 6),
                "weight": round(float(w_re[i] / total_weight * 100), 2),
                "weight_raw": round(float(w_re[i]), 6)
            })

        return {
            "method": "random_effect_derSimonian_laird",
            "pooled_effect": round(float(pooled_effect), 6),
            "pooled_se": round(float(pooled_se), 6),
            "ci_lower": round(float(ci_lower), 6),
            "ci_upper": round(float(ci_upper), 6),
            "z_statistic": round(float(z_stat), 4),
            "p_value": round(float(p_value), 6),
            "significant": bool(p_value < 0.05),
            "tau_squared": round(float(tau_squared), 6),
            "tau": round(float(np.sqrt(tau_squared)), 6),
            "prediction_interval_lower": round(float(pred_lower), 6) if pred_lower is not None else None,
            "prediction_interval_upper": round(float(pred_upper), 6) if pred_upper is not None else None,
            "n_studies": k,
            "studies": study_results,
            "confidence_level": confidence_level
        }

    @staticmethod
    def meta_analysis(
        effects: List[float],
        variances: List[float],
        study_names: Optional[List[str]] = None,
        method: str = "both",
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        综合 Meta 分析（同时进行异质性检验和固定/随机效应分析）

        Args:
            effects: 各研究的效应量列表
            variances: 各研究效应量的方差列表
            study_names: 各研究名称列表
            method: "fixed", "random", 或 "both"
            confidence_level: 置信水平

        Returns:
            包含异质性检验和合并效应的完整结果
        """
        result = {}

        # 异质性检验
        heterogeneity = StatisticalEngine.heterogeneity_test(effects, variances)
        result["heterogeneity"] = heterogeneity

        # 固定效应分析
        if method in ["fixed", "both"]:
            fe_result = StatisticalEngine.meta_analysis_fixed_effect(
                effects, variances, study_names, confidence_level
            )
            result["fixed_effect"] = fe_result

        # 随机效应分析
        if method in ["random", "both"]:
            re_result = StatisticalEngine.meta_analysis_random_effect(
                effects, variances, study_names, confidence_level
            )
            result["random_effect"] = re_result

        # 推荐模型
        if method == "both":
            if heterogeneity["significant_heterogeneity"]:
                result["recommended_model"] = "random_effect"
                result["recommendation_reason"] = (
                    f"存在显著异质性 (I²={heterogeneity['I_squared']}%, "
                    f"Q p={heterogeneity['Q_p_value']})，推荐使用随机效应模型"
                )
            else:
                result["recommended_model"] = "fixed_effect"
                result["recommendation_reason"] = (
                    f"无显著异质性 (I²={heterogeneity['I_squared']}%, "
                    f"Q p={heterogeneity['Q_p_value']})，推荐使用固定效应模型"
                )

        return result

    # ==================== 敏感性分析 (Sensitivity Analysis) ====================

    @staticmethod
    def sensitivity_analysis_leave_one_out(
        effects: List[float],
        variances: List[float],
        study_names: Optional[List[str]] = None,
        model: str = "random",
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        敏感性分析 - 逐一剔除法 (Leave-One-Out)

        依次剔除每个研究，重新进行 Meta 分析，
        评估单个研究对合并结果的影响

        Args:
            effects: 各研究的效应量列表
            variances: 各研究效应量的方差列表
            study_names: 各研究名称列表
            model: 使用的模型 ("fixed" 或 "random")
            confidence_level: 置信水平

        Returns:
            逐一剔除分析结果
        """
        effects = np.array(effects, dtype=float)
        variances = np.array(variances, dtype=float)
        k = len(effects)

        if study_names is None:
            study_names = [f"Study_{i+1}" for i in range(k)]

        # 全部研究的合并结果
        if model == "random":
            full_result = StatisticalEngine.meta_analysis_random_effect(
                effects.tolist(), variances.tolist(), study_names, confidence_level
            )
        else:
            full_result = StatisticalEngine.meta_analysis_fixed_effect(
                effects.tolist(), variances.tolist(), study_names, confidence_level
            )

        full_pooled = full_result["pooled_effect"]

        # 逐一剔除
        leave_one_out_results = []
        for i in range(k):
            mask = np.ones(k, dtype=bool)
            mask[i] = False

            remaining_effects = effects[mask].tolist()
            remaining_variances = variances[mask].tolist()
            remaining_names = [study_names[j] for j in range(k) if j != i]

            if model == "random":
                loo_result = StatisticalEngine.meta_analysis_random_effect(
                    remaining_effects, remaining_variances, remaining_names, confidence_level
                )
            else:
                loo_result = StatisticalEngine.meta_analysis_fixed_effect(
                    remaining_effects, remaining_variances, remaining_names, confidence_level
                )

            # 计算影响（剔除前后差异）
            effect_change = loo_result["pooled_effect"] - full_pooled
            relative_change = abs(effect_change / full_pooled * 100) if full_pooled != 0 else 0

            leave_one_out_results.append({
                "excluded_study": study_names[i],
                "excluded_effect": round(float(effects[i]), 6),
                "pooled_effect_without": round(float(loo_result["pooled_effect"]), 6),
                "ci_lower_without": round(float(loo_result["ci_lower"]), 6),
                "ci_upper_without": round(float(loo_result["ci_upper"]), 6),
                "p_value_without": round(float(loo_result["p_value"]), 6),
                "effect_change": round(float(effect_change), 6),
                "relative_change_pct": round(float(relative_change), 2),
                "n_remaining_studies": k - 1
            })

        # 识别有影响力的研究
        max_change = max(r["relative_change_pct"] for r in leave_one_out_results)
        influential_studies = [
            r["excluded_study"] for r in leave_one_out_results
            if r["relative_change_pct"] > 10  # 变化超过10%视为有影响力
        ]

        # 汇总效应量范围
        pooled_effects = [r["pooled_effect_without"] for r in leave_one_out_results]

        return {
            "model": model,
            "full_pooled_effect": round(float(full_pooled), 6),
            "full_ci_lower": round(float(full_result["ci_lower"]), 6),
            "full_ci_upper": round(float(full_result["ci_upper"]), 6),
            "leave_one_out": leave_one_out_results,
            "pooled_effect_range": {
                "min": round(float(min(pooled_effects)), 6),
                "max": round(float(max(pooled_effects)), 6),
                "range": round(float(max(pooled_effects) - min(pooled_effects)), 6)
            },
            "max_relative_change_pct": round(float(max_change), 2),
            "influential_studies": influential_studies,
            "n_studies": k,
            "conclusion": (
                f"合并效应量在 {round(min(pooled_effects), 4)} ~ {round(max(pooled_effects), 4)} 之间，"
                f"最大相对变化为 {round(max_change, 1)}%。"
                + (f" 有影响力的研究: {', '.join(influential_studies)}。" if influential_studies else " 无单一研究具有显著影响力。")
            )
        }


# 创建全局实例
statistical_engine = StatisticalEngine()
