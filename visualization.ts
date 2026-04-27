/**
 * Data Visualization Generation Module
 * Generates chart configurations for cancer epidemiology data
 */

export interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    backgroundColor?: string | string[];
    borderColor?: string | string[];
    borderWidth?: number;
  }[];
}

export interface HeatmapData {
  countries: string[];
  values: number[];
  min: number;
  max: number;
}

export interface TableData {
  headers: string[];
  rows: (string | number)[][];
}

/**
 * Generate bar chart configuration for risk factor contributions
 */
export function generateRiskFactorBarChart(
  factors: { name: string; value: number; percentage: number }[]
): ChartData {
  return {
    labels: factors.map(f => f.name),
    datasets: [
      {
        label: "Attributable Cases",
        data: factors.map(f => f.value),
        backgroundColor: [
          "rgba(255, 99, 132, 0.7)",
          "rgba(54, 162, 235, 0.7)",
          "rgba(255, 206, 86, 0.7)",
          "rgba(75, 192, 192, 0.7)",
          "rgba(153, 102, 255, 0.7)",
          "rgba(255, 159, 64, 0.7)",
          "rgba(199, 199, 199, 0.7)",
          "rgba(83, 102, 255, 0.7)",
          "rgba(255, 99, 255, 0.7)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
          "rgba(199, 199, 199, 1)",
          "rgba(83, 102, 255, 1)",
          "rgba(255, 99, 255, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };
}

/**
 * Generate pie chart configuration for risk factor proportions
 */
export function generateRiskFactorPieChart(
  factors: { name: string; percentage: number }[]
): ChartData {
  return {
    labels: factors.map(f => `${f.name} (${f.percentage.toFixed(1)}%)`),
    datasets: [
      {
        label: "PAF %",
        data: factors.map(f => f.percentage),
        backgroundColor: [
          "rgba(255, 99, 132, 0.8)",
          "rgba(54, 162, 235, 0.8)",
          "rgba(255, 206, 86, 0.8)",
          "rgba(75, 192, 192, 0.8)",
          "rgba(153, 102, 255, 0.8)",
          "rgba(255, 159, 64, 0.8)",
          "rgba(199, 199, 199, 0.8)",
          "rgba(83, 102, 255, 0.8)",
          "rgba(255, 99, 255, 0.8)",
        ],
        borderColor: "#ffffff",
        borderWidth: 2,
      },
    ],
  };
}

/**
 * Generate line chart configuration for trend analysis
 */
export function generateTrendLineChart(
  trends: {
    year: number;
    value: number;
    lower?: number;
    upper?: number;
  }[],
  metric: string
): ChartData {
  const datasets: ChartData["datasets"] = [
    {
      label: metric,
      data: trends.map(t => t.value),
      borderColor: "rgba(75, 192, 192, 1)",
      backgroundColor: "rgba(75, 192, 192, 0.2)",
      borderWidth: 2,
    },
  ];

  // Add confidence interval if available
  if (trends[0]?.lower !== undefined && trends[0]?.upper !== undefined) {
    datasets.push({
      label: "Lower CI",
      data: trends.map(t => t.lower || 0),
      borderColor: "rgba(75, 192, 192, 0.3)",
      backgroundColor: "transparent",
      borderWidth: 1,
    });
    datasets.push({
      label: "Upper CI",
      data: trends.map(t => t.upper || 0),
      borderColor: "rgba(75, 192, 192, 0.3)",
      backgroundColor: "transparent",
      borderWidth: 1,
    });
  }

  return {
    labels: trends.map(t => t.year.toString()),
    datasets,
  };
}

/**
 * Generate heatmap data for geographic distribution
 */
export function generateGeographicHeatmap(
  data: { country: string; value: number }[]
): HeatmapData {
  const values = data.map(d => d.value);
  return {
    countries: data.map(d => d.country),
    values,
    min: Math.min(...values),
    max: Math.max(...values),
  };
}

/**
 * Generate stacked bar chart for multiple regions/groups
 */
export function generateStackedBarChart(
  categories: string[],
  series: { name: string; data: number[] }[]
): ChartData {
  const colors = [
    "rgba(255, 99, 132, 0.7)",
    "rgba(54, 162, 235, 0.7)",
    "rgba(255, 206, 86, 0.7)",
    "rgba(75, 192, 192, 0.7)",
    "rgba(153, 102, 255, 0.7)",
    "rgba(255, 159, 64, 0.7)",
  ];

  return {
    labels: categories,
    datasets: series.map((s, i) => ({
      label: s.name,
      data: s.data,
      backgroundColor: colors[i % colors.length],
      borderColor: colors[i % colors.length].replace("0.7", "1"),
      borderWidth: 1,
    })),
  };
}

/**
 * Generate table data for statistical results
 */
export function generateStatisticsTable(
  data: {
    region: string;
    incidenceRate: number;
    mortalityRate: number;
    cases: number;
    deaths: number;
  }[]
): TableData {
  return {
    headers: [
      "Region",
      "Incidence Rate (per 100,000)",
      "Mortality Rate (per 100,000)",
      "New Cases",
      "Deaths",
    ],
    rows: data.map(d => [
      d.region,
      d.incidenceRate.toFixed(2),
      d.mortalityRate.toFixed(2),
      d.cases.toLocaleString(),
      d.deaths.toLocaleString(),
    ]),
  };
}

/**
 * Generate PAF table
 */
export function generatePAFTable(
  pafResults: {
    factor: string;
    paf: number;
    cases: number;
    percentage: number;
  }[]
): TableData {
  return {
    headers: [
      "Risk Factor",
      "PAF",
      "Attributable Cases",
      "Percentage (%)",
    ],
    rows: pafResults.map(r => [
      r.factor,
      r.paf.toFixed(4),
      r.cases.toLocaleString(),
      r.percentage.toFixed(2),
    ]),
  };
}

/**
 * Generate trend analysis table
 */
export function generateTrendTable(
  trends: {
    metric: string;
    apc: number;
    aapc: number;
    pValue: number;
    significant: boolean;
  }[]
): TableData {
  return {
    headers: [
      "Metric",
      "APC (%)",
      "AAPC (%)",
      "P-value",
      "Significant",
    ],
    rows: trends.map(t => [
      t.metric,
      t.apc.toFixed(2),
      t.aapc.toFixed(2),
      t.pValue.toFixed(4),
      t.significant ? "Yes" : "No",
    ]),
  };
}

/**
 * Color palette for consistent styling
 */
export const colorPalette = {
  primary: "rgba(75, 192, 192, 1)",
  secondary: "rgba(54, 162, 235, 1)",
  success: "rgba(75, 192, 75, 1)",
  warning: "rgba(255, 206, 86, 1)",
  danger: "rgba(255, 99, 132, 1)",
  info: "rgba(153, 102, 255, 1)",
  light: "rgba(199, 199, 199, 1)",
  dark: "rgba(51, 51, 51, 1)",
};

/**
 * Generate color gradient for heatmaps
 */
export function generateColorGradient(
  value: number,
  min: number,
  max: number
): string {
  const normalized = (value - min) / (max - min);
  
  // Color gradient from light yellow to dark red
  const r = Math.floor(255);
  const g = Math.floor(255 * (1 - normalized));
  const b = Math.floor(100 * (1 - normalized));
  
  return `rgba(${r}, ${g}, ${b}, 0.8)`;
}
