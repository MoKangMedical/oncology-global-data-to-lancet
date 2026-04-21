import { describe, expect, it } from "vitest";
import {
  calculatePAF,
  calculateMultipleRiskFactorPAF,
  calculateCombinedPAF,
  calculateRelativeRisk,
  analyzeTrend,
  calculateSummaryStatistics,
  type RiskFactorData,
  type TrendPoint,
} from "./analysis";

describe("calculatePAF", () => {
  it("calculates PAF correctly for typical values", () => {
    // Example: prevalence = 0.3, RR = 2.0
    // PAF = (0.3 * (2.0 - 1)) / (1 + 0.3 * (2.0 - 1)) = 0.3 / 1.3 ≈ 0.231
    const paf = calculatePAF(0.3, 2.0);
    expect(paf).toBeCloseTo(0.231, 2);
  });

  it("returns 0 when prevalence is 0", () => {
    const paf = calculatePAF(0, 2.0);
    expect(paf).toBe(0);
  });

  it("returns 0 when RR is 1", () => {
    const paf = calculatePAF(0.5, 1.0);
    expect(paf).toBe(0);
  });

  it("handles high prevalence and high RR", () => {
    const paf = calculatePAF(0.8, 5.0);
    expect(paf).toBeGreaterThan(0.7);
    expect(paf).toBeLessThanOrEqual(1.0);
  });

  it("throws error for invalid prevalence", () => {
    expect(() => calculatePAF(-0.1, 2.0)).toThrow("Prevalence must be between 0 and 1");
    expect(() => calculatePAF(1.5, 2.0)).toThrow("Prevalence must be between 0 and 1");
  });

  it("throws error for negative RR", () => {
    expect(() => calculatePAF(0.5, -1.0)).toThrow("Relative risk must be positive");
  });
});

describe("calculateMultipleRiskFactorPAF", () => {
  it("calculates PAF for multiple risk factors", () => {
    const riskFactors: RiskFactorData[] = [
      { factor: "Smoking", prevalence: 0.25, relativeRisk: 2.5 },
      { factor: "Obesity", prevalence: 0.30, relativeRisk: 1.8 },
      { factor: "Alcohol", prevalence: 0.15, relativeRisk: 1.5 },
    ];

    const totalCases = 10000;
    const results = calculateMultipleRiskFactorPAF(riskFactors, totalCases);

    expect(results).toHaveLength(3);
    
    // Check smoking
    expect(results[0].factor).toBe("Smoking");
    expect(results[0].paf).toBeGreaterThan(0);
    expect(results[0].cases).toBeGreaterThan(0);
    expect(results[0].percentage).toBeGreaterThan(0);

    // Check that all PAFs are between 0 and 1
    results.forEach(result => {
      expect(result.paf).toBeGreaterThanOrEqual(0);
      expect(result.paf).toBeLessThanOrEqual(1);
    });
  });
});

describe("calculateCombinedPAF", () => {
  it("calculates combined PAF correctly", () => {
    const individualPAFs = [0.2, 0.15, 0.1];
    // Combined PAF = 1 - (1-0.2)*(1-0.15)*(1-0.1) = 1 - 0.8*0.85*0.9 = 1 - 0.612 = 0.388
    const combined = calculateCombinedPAF(individualPAFs);
    expect(combined).toBeCloseTo(0.388, 2);
  });

  it("returns 0 for empty array", () => {
    const combined = calculateCombinedPAF([]);
    expect(combined).toBe(0);
  });

  it("returns single PAF for one-element array", () => {
    const combined = calculateCombinedPAF([0.3]);
    expect(combined).toBeCloseTo(0.3, 5);
  });
});

describe("calculateRelativeRisk", () => {
  it("calculates RR correctly", () => {
    // Exposed: 50 cases out of 200 (25%)
    // Unexposed: 20 cases out of 200 (10%)
    // RR = 0.25 / 0.10 = 2.5
    const result = calculateRelativeRisk(50, 200, 20, 200);
    expect(result.rr).toBeCloseTo(2.5, 1);
    expect(result.lower).toBeGreaterThan(0);
    expect(result.upper).toBeGreaterThan(result.rr);
  });

  it("returns RR of 1 for equal risks", () => {
    const result = calculateRelativeRisk(50, 200, 50, 200);
    expect(result.rr).toBeCloseTo(1.0, 1);
  });
});

describe("analyzeTrend", () => {
  it("detects increasing trend", () => {
    const data: TrendPoint[] = [
      { year: 2010, value: 100 },
      { year: 2011, value: 110 },
      { year: 2012, value: 120 },
      { year: 2013, value: 135 },
      { year: 2014, value: 150 },
    ];

    const result = analyzeTrend(data);
    expect(result.apc).toBeGreaterThan(0); // Positive trend
    expect(result.trends).toHaveLength(5);
  });

  it("detects decreasing trend", () => {
    const data: TrendPoint[] = [
      { year: 2010, value: 150 },
      { year: 2011, value: 140 },
      { year: 2012, value: 130 },
      { year: 2013, value: 120 },
      { year: 2014, value: 110 },
    ];

    const result = analyzeTrend(data);
    expect(result.apc).toBeLessThan(0); // Negative trend
  });

  it("throws error for insufficient data", () => {
    const data: TrendPoint[] = [{ year: 2010, value: 100 }];
    expect(() => analyzeTrend(data)).toThrow("Need at least 2 data points");
  });
});

describe("calculateSummaryStatistics", () => {
  it("calculates statistics correctly", () => {
    const values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
    const stats = calculateSummaryStatistics(values);

    expect(stats.mean).toBe(55);
    expect(stats.median).toBe(55);
    expect(stats.min).toBe(10);
    expect(stats.max).toBe(100);
    expect(stats.count).toBe(10);
    expect(stats.total).toBe(550);
    expect(stats.stdDev).toBeGreaterThan(0);
  });

  it("handles single value", () => {
    const values = [42];
    const stats = calculateSummaryStatistics(values);

    expect(stats.mean).toBe(42);
    expect(stats.median).toBe(42);
    expect(stats.min).toBe(42);
    expect(stats.max).toBe(42);
    expect(stats.stdDev).toBe(0);
  });

  it("throws error for empty array", () => {
    expect(() => calculateSummaryStatistics([])).toThrow(
      "Cannot calculate statistics for empty array"
    );
  });

  it("calculates median correctly for even number of values", () => {
    const values = [1, 2, 3, 4];
    const stats = calculateSummaryStatistics(values);
    expect(stats.median).toBe(2.5); // (2 + 3) / 2
  });

  it("calculates median correctly for odd number of values", () => {
    const values = [1, 2, 3, 4, 5];
    const stats = calculateSummaryStatistics(values);
    expect(stats.median).toBe(3);
  });
});
