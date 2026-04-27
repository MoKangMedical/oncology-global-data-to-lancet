/**
 * Academic Paper Generation Module
 * Generates Lancet-standard research papers from analysis results
 */

import { invokeLLM } from "./_core/llm";

export interface PaperSection {
  title: string;
  content: string;
  wordCount: number;
}

export interface PaperMetadata {
  title: string;
  abstract: string;
  keywords: string[];
  wordCount: number;
}

export interface AnalysisData {
  cancerType: string;
  countries: string[];
  timeRange: { start: number; end: number };
  totalCases: number;
  totalDeaths: number;
  riskFactors: {
    name: string;
    paf: number;
    cases: number;
    percentage: number;
  }[];
  trends: {
    metric: string;
    apc: number;
    aapc: number;
    significant: boolean;
  }[];
  regionalData: {
    region: string;
    incidenceRate: number;
    mortalityRate: number;
  }[];
}

/**
 * Generate complete research paper
 */
export async function generateCompletePaper(
  projectData: AnalysisData,
  visualizations: { title: string; description: string }[]
): Promise<{
  metadata: PaperMetadata;
  sections: {
    introduction: PaperSection;
    methods: PaperSection;
    results: PaperSection;
    discussion: PaperSection;
    conclusion: PaperSection;
  };
  references: string[];
  fullContent: string;
}> {
  // Generate each section
  const [metadata, introduction, methods, results, discussion, conclusion, references] = await Promise.all([
    generateMetadata(projectData),
    generateIntroduction(projectData),
    generateMethods(projectData),
    generateResults(projectData, visualizations),
    generateDiscussion(projectData),
    generateConclusion(projectData),
    generateReferences(projectData),
  ]);

  // Combine all sections
  const fullContent = `# ${metadata.title}

## Abstract
${metadata.abstract}

**Keywords:** ${metadata.keywords.join(", ")}

---

## Introduction
${introduction.content}

## Methods
${methods.content}

## Results
${results.content}

## Discussion
${discussion.content}

## Conclusion
${conclusion.content}

## References
${references.map((ref, i) => `${i + 1}. ${ref}`).join("\n")}
`;

  return {
    metadata,
    sections: {
      introduction,
      methods,
      results,
      discussion,
      conclusion,
    },
    references,
    fullContent,
  };
}

/**
 * Generate paper metadata (title, abstract, keywords)
 */
async function generateMetadata(data: AnalysisData): Promise<PaperMetadata> {
  const prompt = `Generate a scientific paper title, abstract, and keywords for a cancer epidemiology study with the following characteristics:

Cancer Type: ${data.cancerType}
Geographic Coverage: ${data.countries.join(", ")}
Time Period: ${data.timeRange.start}-${data.timeRange.end}
Total Cases: ${data.totalCases.toLocaleString()}
Key Risk Factors: ${data.riskFactors.slice(0, 5).map(f => f.name).join(", ")}

The abstract should be 250-300 words and follow Lancet style:
- Background (1-2 sentences)
- Methods (2-3 sentences)
- Findings (3-4 sentences with key statistics)
- Interpretation (1-2 sentences)

Provide 5-8 keywords relevant to the study.`;

  const response = await invokeLLM({
    messages: [
      {
        role: "system",
        content: "You are an expert medical researcher writing for The Lancet. Generate precise, academic content following journal standards.",
      },
      {
        role: "user",
        content: prompt,
      },
    ],
    response_format: {
      type: "json_schema",
      json_schema: {
        name: "paper_metadata",
        strict: true,
        schema: {
          type: "object",
          properties: {
            title: {
              type: "string",
              description: "Paper title (concise, informative, <150 characters)",
            },
            abstract: {
              type: "string",
              description: "Structured abstract (250-300 words)",
            },
            keywords: {
              type: "array",
              items: { type: "string" },
              description: "5-8 keywords",
            },
          },
          required: ["title", "abstract", "keywords"],
          additionalProperties: false,
        },
      },
    },
  });

  const content = response.choices[0]?.message?.content;
  if (!content || typeof content !== "string") {
    throw new Error("Failed to generate metadata");
  }

  const result = JSON.parse(content);
  const wordCount = result.abstract.split(/\s+/).length;

  return {
    title: result.title,
    abstract: result.abstract,
    keywords: result.keywords,
    wordCount,
  };
}

/**
 * Generate Introduction section
 */
async function generateIntroduction(data: AnalysisData): Promise<PaperSection> {
  const prompt = `Write the Introduction section for a cancer epidemiology paper about ${data.cancerType}.

Context:
- Geographic focus: ${data.countries.join(", ")}
- Time period: ${data.timeRange.start}-${data.timeRange.end}
- Key risk factors: ${data.riskFactors.slice(0, 5).map(f => f.name).join(", ")}

The introduction should:
1. Establish the burden and importance of ${data.cancerType} (2-3 paragraphs)
2. Review existing knowledge gaps (1-2 paragraphs)
3. State the study objectives clearly (1 paragraph)

Target length: 800-1000 words
Style: Academic, citing relevant literature (use [1], [2] format for citations)`;

  const response = await invokeLLM({
    messages: [
      {
        role: "system",
        content: "You are an expert medical researcher writing for The Lancet. Write clear, evidence-based academic prose.",
      },
      {
        role: "user",
        content: prompt,
      },
    ],
  });

  const content = response.choices[0]?.message?.content;
  if (!content || typeof content !== "string") {
    throw new Error("Failed to generate introduction");
  }

  return {
    title: "Introduction",
    content,
    wordCount: content.split(/\s+/).length,
  };
}

/**
 * Generate Methods section
 */
async function generateMethods(data: AnalysisData): Promise<PaperSection> {
  const prompt = `Write the Methods section for a cancer epidemiology study analyzing ${data.cancerType}.

Study Design:
- Data sources: GLOBOCAN 2022, GBD 2021, CI5 databases
- Geographic coverage: ${data.countries.join(", ")}
- Time period: ${data.timeRange.start}-${data.timeRange.end}
- Risk factors analyzed: ${data.riskFactors.map(f => f.name).join(", ")}

Include subsections:
1. Data Sources (describe each database)
2. Risk Factor Classification (categorize the ${data.riskFactors.length} risk factors)
3. Statistical Analysis (PAF calculation using CDPAF method, trend analysis using Joinpoint regression)
4. Ethical Considerations

Target length: 1000-1200 words
Style: Precise, methodological, reproducible`;

  const response = await invokeLLM({
    messages: [
      {
        role: "system",
        content: "You are an expert biostatistician writing methods for The Lancet. Be precise and comprehensive.",
      },
      {
        role: "user",
        content: prompt,
      },
    ],
  });

  const content = response.choices[0]?.message?.content;
  if (!content || typeof content !== "string") {
    throw new Error("Failed to generate methods");
  }

  return {
    title: "Methods",
    content,
    wordCount: content.split(/\s+/).length,
  };
}

/**
 * Generate Results section
 */
async function generateResults(
  data: AnalysisData,
  visualizations: { title: string; description: string }[]
): Promise<PaperSection> {
  const topRiskFactors = data.riskFactors.slice(0, 5);
  const significantTrends = data.trends.filter(t => t.significant);

  const prompt = `Write the Results section for a ${data.cancerType} epidemiology study.

Key Findings:
1. Global Burden:
   - Total cases: ${data.totalCases.toLocaleString()}
   - Total deaths: ${data.totalDeaths.toLocaleString()}
   
2. Risk Factor Contributions (top 5):
${topRiskFactors.map(f => `   - ${f.name}: PAF ${(f.paf * 100).toFixed(1)}%, ${f.cases.toLocaleString()} cases (${f.percentage.toFixed(1)}%)`).join("\n")}

3. Regional Patterns:
${data.regionalData.slice(0, 5).map(r => `   - ${r.region}: Incidence ${r.incidenceRate.toFixed(1)}/100,000, Mortality ${r.mortalityRate.toFixed(1)}/100,000`).join("\n")}

4. Temporal Trends:
${significantTrends.map(t => `   - ${t.metric}: APC ${t.apc.toFixed(2)}%/year (p<0.05)`).join("\n")}

Figures Available:
${visualizations.map((v, i) => `Figure ${i + 1}: ${v.title}`).join("\n")}

Structure the results with clear subsections, reference figures appropriately, and present statistics with 95% CIs where applicable.

Target length: 1500-1800 words`;

  const response = await invokeLLM({
    messages: [
      {
        role: "system",
        content: "You are an expert epidemiologist writing results for The Lancet. Present findings clearly with appropriate statistical detail.",
      },
      {
        role: "user",
        content: prompt,
      },
    ],
  });

  const content = response.choices[0]?.message?.content;
  if (!content || typeof content !== "string") {
    throw new Error("Failed to generate results");
  }

  return {
    title: "Results",
    content,
    wordCount: content.split(/\s+/).length,
  };
}

/**
 * Generate Discussion section
 */
async function generateDiscussion(data: AnalysisData): Promise<PaperSection> {
  const topRiskFactors = data.riskFactors.slice(0, 3);

  const prompt = `Write the Discussion section for a ${data.cancerType} epidemiology study.

Key Findings to Discuss:
- ${data.totalCases.toLocaleString()} cases globally
- Top risk factors: ${topRiskFactors.map(f => `${f.name} (${f.percentage.toFixed(1)}%)`).join(", ")}
- Geographic variations across ${data.countries.length} countries/regions
- Temporal trends from ${data.timeRange.start} to ${data.timeRange.end}

Structure:
1. Principal Findings (1-2 paragraphs)
2. Comparison with Previous Studies (2-3 paragraphs)
3. Implications for Policy and Prevention (2-3 paragraphs)
4. Strengths and Limitations (1-2 paragraphs)

Target length: 1200-1500 words
Style: Interpretive, balanced, forward-looking`;

  const response = await invokeLLM({
    messages: [
      {
        role: "system",
        content: "You are an expert public health researcher writing discussion for The Lancet. Provide balanced interpretation with policy implications.",
      },
      {
        role: "user",
        content: prompt,
      },
    ],
  });

  const content = response.choices[0]?.message?.content;
  if (!content || typeof content !== "string") {
    throw new Error("Failed to generate discussion");
  }

  return {
    title: "Discussion",
    content,
    wordCount: content.split(/\s+/).length,
  };
}

/**
 * Generate Conclusion section
 */
async function generateConclusion(data: AnalysisData): Promise<PaperSection> {
  const prompt = `Write a concise Conclusion for a ${data.cancerType} epidemiology study.

Key Messages:
- Substantial global burden (${data.totalCases.toLocaleString()} cases)
- Major risk factors identified: ${data.riskFactors.slice(0, 3).map(f => f.name).join(", ")}
- Geographic and temporal variations documented
- Need for targeted prevention strategies

Target length: 200-300 words
Style: Concise, impactful, actionable`;

  const response = await invokeLLM({
    messages: [
      {
        role: "system",
        content: "You are an expert medical researcher writing conclusions for The Lancet. Be concise and impactful.",
      },
      {
        role: "user",
        content: prompt,
      },
    ],
  });

  const content = response.choices[0]?.message?.content;
  if (!content || typeof content !== "string") {
    throw new Error("Failed to generate conclusion");
  }

  return {
    title: "Conclusion",
    content,
    wordCount: content.split(/\s+/).length,
  };
}

/**
 * Generate References
 */
async function generateReferences(data: AnalysisData): Promise<string[]> {
  // Standard references for cancer epidemiology papers
  return [
    "Sung H, Ferlay J, Siegel RL, et al. Global Cancer Statistics 2020: GLOBOCAN Estimates of Incidence and Mortality Worldwide for 36 Cancers in 185 Countries. CA Cancer J Clin 2021; 71: 209–49.",
    "GBD 2021 Cancer Collaborators. Global, regional, and national burden of cancer, 1990-2021: a systematic analysis for the Global Burden of Disease Study 2021. Lancet 2024; 403: 1989-2020.",
    "Bray F, Colombet M, Mery L, et al. Cancer Incidence in Five Continents, Vol. XI (electronic version). Lyon: International Agency for Research on Cancer, 2021.",
    "Islami F, Goding Sauer A, Miller KD, et al. Proportion and number of cancer cases and deaths attributable to potentially modifiable risk factors in the United States. CA Cancer J Clin 2018; 68: 31–54.",
    "Arnold M, Abnet CC, Neale RE, et al. Global Burden of 5 Major Types of Gastrointestinal Cancer. Gastroenterology 2020; 159: 335-349.e15.",
    "Fitzmaurice C, Abate D, Abbasi N, et al. Global, Regional, and National Cancer Incidence, Mortality, Years of Life Lost, Years Lived With Disability, and Disability-Adjusted Life-Years for 29 Cancer Groups, 1990 to 2017. JAMA Oncol 2019; 5: 1749–68.",
    "Collaborators GBDRF. Global burden of 87 risk factors in 204 countries and territories, 1990-2019: a systematic analysis for the Global Burden of Disease Study 2019. Lancet 2020; 396: 1223–49.",
    "Kim HJ, Fay MP, Feuer EJ, Midthune DN. Permutation tests for joinpoint regression with applications to cancer rates. Stat Med 2000; 19: 335–51.",
  ];
}
