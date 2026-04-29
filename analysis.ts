/**
 * Statistical Analysis Engine for Cancer Epidemiology Research
 * Implements PAF, CDPAF, RR calculations and trend analysis
 */

export interface RiskFactorData {
  factor: string;
  prevalence: number; // 0-1
  relativeRisk: number; // RR
}

export interface PAFResult {
  factor: string;
  paf: number; // Population Attributable Fraction (0-1)
  cases: number; // Attributable cases
  percentage: number; // Percentage of total cases
}

export interface CDPAFResult {
  factor: string;
  cdpaf: number; // Correlation-Decomposed PAF
  cases: number;
  percentage: number;
}

export interface TrendPoint {
  year: number;
  value: number;
  lower?: number;
  upper?: number;
}

export interface TrendAnalysisResult {
  metric: string;
  trends: TrendPoint[];
  apc: number; // Annual Percent Change
  aapc: number; // Average Annual Percent Change
  pValue: number;
  significant: boolean;
}

/**
 * Calculate Population Attributable Fraction (PAF)
 * Formula: PAF = (P * (RR - 1)) / (1 + P * (RR - 1))
 * where P = prevalence, RR = relative risk
 */
export function calculatePAF(prevalence: number, relativeRisk: number): number {
  if (prevalence < 0 || prevalence > 1) {
    throw new Error("Prevalence must be between 0 and 1");
  }
  if (relativeRisk < 0) {
    throw new Error("Relative risk must be positive");
  }

  const paf = (prevalence * (relativeRisk - 1)) / (1 + prevalence * (relativeRisk - 1));
  return Math.max(0, Math.min(1, paf)); // Clamp to [0, 1]
}

/**
 * Calculate PAF for multiple risk factors
 */
export function calculateMultipleRiskFactorPAF(
  riskFactors: RiskFactorData[],
  totalCases: number
): PAFResult[] {
  const results: PAFResult[] = [];

  for (const factor of riskFactors) {
    const paf = calculatePAF(factor.prevalence, factor.relativeRisk);
    const attributableCases = totalCases * paf;
    const percentage = paf * 100;

    results.push({
      factor: factor.factor,
      paf,
      cases: Math.round(attributableCases),
      percentage,
    });
  }

  return results;
}

/**
 * Calculate Correlation-Decomposed PAF (CDPAF)
 * This method adjusts for correlations between risk factors
 * 
 * Simplified implementation using correlation matrix
 * In practice, this would use more sophisticated methods like
 * the method described in the reference paper
 */
export function calculateCDPAF(
  riskFactors: RiskFactorData[],
  correlationMatrix: number[][],
  totalCases: number
): CDPAFResult[] {
  // First calculate individual PAFs
  const individualPAFs = calculateMultipleRiskFactorPAF(riskFactors, totalCases);

  // Adjust for correlations
  const results: CDPAFResult[] = [];

  for (let i = 0; i < riskFactors.length; i++) {
    const factor = riskFactors[i];
    const individualPAF = individualPAFs[i].paf;

    // Calculate adjustment factor based on correlations
    let adjustmentFactor = 1.0;
    for (let j = 0; j < riskFactors.length; j++) {
      if (i !== j) {
        const correlation = correlationMatrix[i][j] || 0;
        const otherPAF = individualPAFs[j].paf;
        // Reduce PAF based on correlation with other factors
        adjustmentFactor -= correlation * otherPAF * 0.5;
      }
    }

    adjustmentFactor = Math.max(0.5, Math.min(1.0, adjustmentFactor));

    const cdpaf = individualPAF * adjustmentFactor;
    const attributableCases = totalCases * cdpaf;
    const percentage = cdpaf * 100;

    results.push({
      factor: factor.factor,
      cdpaf,
      cases: Math.round(attributableCases),
      percentage,
    });
  }

  return results;
}

/**
 * Calculate combined PAF for multiple risk factors
 * Formula: Combined PAF = 1 - ∏(1 - PAF_i)
 */
export function calculateCombinedPAF(individualPAFs: number[]): number {
  let product = 1.0;
  for (const paf of individualPAFs) {
    product *= (1 - paf);
  }
  return 1 - product;
}

/**
 * Calculate Age-Standardized Rate (ASR)
 * Uses world standard population weights
 */
export function calculateASR(
  ageSpecificRates: { ageGroup: string; rate: number; population: number }[],
  standardPopulation: { ageGroup: string; weight: number }[]
): number {
  let weightedSum = 0;
  let totalWeight = 0;

  for (const ageData of ageSpecificRates) {
    const standardWeight = standardPopulation.find(
      sp => sp.ageGroup === ageData.ageGroup
    )?.weight || 0;

    weightedSum += ageData.rate * standardWeight;
    totalWeight += standardWeight;
  }

  return totalWeight > 0 ? weightedSum / totalWeight : 0;
}

/**
 * Simplified Joinpoint regression for trend analysis
 * Returns linear trend (APC) and average APC
 */
export function analyzeTrend(dataPoints: TrendPoint[]): TrendAnalysisResult {
  if (dataPoints.length < 2) {
    throw new Error("Need at least 2 data points for trend analysis");
  }

  // Sort by year
  const sorted = [...dataPoints].sort((a, b) => a.year - b.year);

  // Calculate linear regression for APC
  const n = sorted.length;
  const sumX = sorted.reduce((sum, p) => sum + p.year, 0);
  const sumY = sorted.reduce((sum, p) => sum + Math.log(p.value + 0.001), 0); // log transform
  const sumXY = sorted.reduce((sum, p) => sum + p.year * Math.log(p.value + 0.001), 0);
  const sumX2 = sorted.reduce((sum, p) => sum + p.year * p.year, 0);

  const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
  const apc = (Math.exp(slope) - 1) * 100; // Convert to percentage

  // Calculate AAPC (for single segment, same as APC)
  const aapc = apc;

  // Simple significance test (t-test approximation)
  const meanX = sumX / n;
  const meanY = sumY / n;
  const ssX = sorted.reduce((sum, p) => sum + Math.pow(p.year - meanX, 2), 0);
  const ssY = sorted.reduce((sum, p) => sum + Math.pow(Math.log(p.value + 0.001) - meanY, 2), 0);
  const ssXY = sorted.reduce((sum, p) => sum + (p.year - meanX) * (Math.log(p.value + 0.001) - meanY), 0);

  const r = ssXY / Math.sqrt(ssX * ssY);
  const tStat = r * Math.sqrt(n - 2) / Math.sqrt(1 - r * r);
  const pValue = 2 * (1 - normalCDF(Math.abs(tStat))); // Approximate p-value

  return {
    metric: "trend",
    trends: sorted,
    apc,
    aapc,
    pValue,
    significant: pValue < 0.05,
  };
}

/**
 * Normal cumulative distribution function (approximation)
 */
function normalCDF(x: number): number {
  const t = 1 / (1 + 0.2316419 * Math.abs(x));
  const d = 0.3989423 * Math.exp(-x * x / 2);
  const p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
  return x > 0 ? 1 - p : p;
}

/**
 * Calculate confidence intervals for rates
 * Uses Poisson approximation
 */
export function calculateConfidenceInterval(
  cases: number,
  population: number,
  confidenceLevel: number = 0.95
): { lower: number; upper: number } {
  const rate = (cases / population) * 100000; // per 100,000
  const z = 1.96; // 95% CI

  if (cases === 0) {
    return { lower: 0, upper: 0 };
  }

  const se = Math.sqrt(cases) / population * 100000;
  const lower = Math.max(0, rate - z * se);
  const upper = rate + z * se;

  return { lower, upper };
}

/**
 * Calculate relative risk (RR) from case-control or cohort data
 */
export function calculateRelativeRisk(
  exposedCases: number,
  exposedTotal: number,
  unexposedCases: number,
  unexposedTotal: number
): { rr: number; lower: number; upper: number } {
  const riskExposed = exposedCases / exposedTotal;
  const riskUnexposed = unexposedCases / unexposedTotal;

  const rr = riskExposed / riskUnexposed;

  // Calculate 95% CI using log transformation
  const seLogRR = Math.sqrt(
    (1 / exposedCases) - (1 / exposedTotal) +
    (1 / unexposedCases) - (1 / unexposedTotal)
  );

  const z = 1.96;
  const lower = Math.exp(Math.log(rr) - z * seLogRR);
  const upper = Math.exp(Math.log(rr) + z * seLogRR);

  return { rr, lower, upper };
}

/**
 * Generate summary statistics for a dataset
 */
export interface SummaryStatistics {
  mean: number;
  median: number;
  min: number;
  max: number;
  stdDev: number;
  q25: number;
  q75: number;
  total: number;
  count: number;
}

export function calculateSummaryStatistics(values: number[]): SummaryStatistics {
  if (values.length === 0) {
    throw new Error("Cannot calculate statistics for empty array");
  }

  const sorted = [...values].sort((a, b) => a - b);
  const n = sorted.length;
  const total = sorted.reduce((sum, v) => sum + v, 0);
  const mean = total / n;

  const median = n % 2 === 0
    ? (sorted[n / 2 - 1] + sorted[n / 2]) / 2
    : sorted[Math.floor(n / 2)];

  const variance = sorted.reduce((sum, v) => sum + Math.pow(v - mean, 2), 0) / n;
  const stdDev = Math.sqrt(variance);

  const q25Index = Math.floor(n * 0.25);
  const q75Index = Math.floor(n * 0.75);

  return {
    mean,
    median,
    min: sorted[0],
    max: sorted[n - 1],
    stdDev,
    q25: sorted[q25Index],
    q75: sorted[q75Index],
    total,
    count: n,
  };
}
