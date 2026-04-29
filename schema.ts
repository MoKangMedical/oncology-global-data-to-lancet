import { int, mysqlEnum, mysqlTable, text, timestamp, varchar, json, float } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 */
export const users = mysqlTable("users", {
  id: int("id").autoincrement().primaryKey(),
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

/**
 * Research projects table
 * Stores metadata for each cancer research project
 */
export const projects = mysqlTable("projects", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  title: varchar("title", { length: 500 }).notNull(),
  description: text("description"),
  
  // Research parameters extracted from proposal or manually entered
  cancerTypes: json("cancerTypes").$type<string[]>(), // e.g., ["Liver cancer", "HCC"]
  countries: json("countries").$type<string[]>(), // e.g., ["China", "USA", "Global"]
  regions: json("regions").$type<string[]>(), // e.g., ["East Asia", "North America"]
  timeRange: json("timeRange").$type<{ start: number; end: number }>(), // e.g., { start: 1990, end: 2022 }
  riskFactors: json("riskFactors").$type<string[]>(), // e.g., ["HBV", "HCV", "Obesity", "Smoking"]
  ageGroups: json("ageGroups").$type<string[]>(), // e.g., ["All ages", "0-14", "15-49"]
  sexGroups: json("sexGroups").$type<string[]>(), // e.g., ["Both", "Male", "Female"]
  
  // Research proposal document
  proposalFileUrl: text("proposalFileUrl"), // S3 URL
  proposalFileName: varchar("proposalFileName", { length: 255 }),
  
  // Project status
  status: mysqlEnum("status", ["draft", "data_collection", "analyzing", "completed", "failed"]).default("draft").notNull(),
  progress: int("progress").default(0), // 0-100
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Project = typeof projects.$inferSelect;
export type InsertProject = typeof projects.$inferInsert;

/**
 * Data files uploaded by users
 * Stores GLOBOCAN, GBD, CI5 data files
 */
export const dataFiles = mysqlTable("data_files", {
  id: int("id").autoincrement().primaryKey(),
  projectId: int("projectId").notNull(),
  
  // Data source type
  dataSource: mysqlEnum("dataSource", ["globocan", "gbd", "ci5", "other"]).notNull(),
  
  // File information
  fileName: varchar("fileName", { length: 255 }).notNull(),
  fileUrl: text("fileUrl").notNull(), // S3 URL
  fileSize: int("fileSize"), // bytes
  mimeType: varchar("mimeType", { length: 100 }),
  
  // Data metadata
  dataType: varchar("dataType", { length: 100 }), // e.g., "incidence", "mortality", "risk_factors"
  recordCount: int("recordCount"), // number of data records
  
  // Processing status
  status: mysqlEnum("status", ["uploaded", "processing", "processed", "failed"]).default("uploaded").notNull(),
  errorMessage: text("errorMessage"),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type DataFile = typeof dataFiles.$inferSelect;
export type InsertDataFile = typeof dataFiles.$inferInsert;

/**
 * Standardized cancer data
 * Stores processed and standardized data from all sources
 */
export const cancerData = mysqlTable("cancer_data", {
  id: int("id").autoincrement().primaryKey(),
  projectId: int("projectId").notNull(),
  dataFileId: int("dataFileId"), // reference to source file
  
  // Geographic information
  country: varchar("country", { length: 200 }),
  region: varchar("region", { length: 200 }),
  
  // Temporal information
  year: int("year"),
  
  // Cancer information
  cancerType: varchar("cancerType", { length: 200 }),
  cancerSite: varchar("cancerSite", { length: 200 }),
  icdCode: varchar("icdCode", { length: 50 }),
  
  // Demographic information
  ageGroup: varchar("ageGroup", { length: 50 }),
  sex: mysqlEnum("sex", ["male", "female", "both"]),
  
  // Incidence data
  incidenceCount: int("incidenceCount"),
  incidenceRate: float("incidenceRate"), // per 100,000
  incidenceASR: float("incidenceASR"), // age-standardized rate
  
  // Mortality data
  mortalityCount: int("mortalityCount"),
  mortalityRate: float("mortalityRate"),
  mortalityASR: float("mortalityASR"),
  
  // Prevalence data
  prevalence1Year: int("prevalence1Year"),
  prevalence3Year: int("prevalence3Year"),
  prevalence5Year: int("prevalence5Year"),
  
  // Risk factor data (stored as JSON for flexibility)
  riskFactorData: json("riskFactorData").$type<Record<string, number>>(),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type CancerData = typeof cancerData.$inferSelect;
export type InsertCancerData = typeof cancerData.$inferInsert;

/**
 * Analysis results
 * Stores statistical analysis results
 */
export const analysisResults = mysqlTable("analysis_results", {
  id: int("id").autoincrement().primaryKey(),
  projectId: int("projectId").notNull(),
  
  // Analysis type
  analysisType: varchar("analysisType", { length: 100 }).notNull(), // e.g., "PAF", "CDPAF", "RR", "trend"
  
  // Analysis parameters
  parameters: json("parameters").$type<Record<string, any>>(),
  
  // Results data
  results: json("results").$type<Record<string, any>>().notNull(),
  
  // Summary statistics
  summary: text("summary"),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type AnalysisResult = typeof analysisResults.$inferSelect;
export type InsertAnalysisResult = typeof analysisResults.$inferInsert;

/**
 * Generated visualizations
 * Stores metadata for generated charts and figures
 */
export const visualizations = mysqlTable("visualizations", {
  id: int("id").autoincrement().primaryKey(),
  projectId: int("projectId").notNull(),
  analysisResultId: int("analysisResultId"), // optional reference to analysis
  
  // Visualization metadata
  title: varchar("title", { length: 500 }).notNull(),
  description: text("description"),
  visualizationType: varchar("visualizationType", { length: 100 }).notNull(), // e.g., "heatmap", "bar", "line", "table"
  
  // File information
  imageUrl: text("imageUrl"), // S3 URL for PNG/SVG
  dataUrl: text("dataUrl"), // S3 URL for source data (CSV/JSON)
  
  // Chart configuration
  config: json("config").$type<Record<string, any>>(),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type Visualization = typeof visualizations.$inferSelect;
export type InsertVisualization = typeof visualizations.$inferInsert;

/**
 * Generated papers
 * Stores generated research papers
 */
export const papers = mysqlTable("papers", {
  id: int("id").autoincrement().primaryKey(),
  projectId: int("projectId").notNull(),
  
  // Paper metadata
  title: varchar("title", { length: 500 }).notNull(),
  abstract: text("abstract"),
  keywords: json("keywords").$type<string[]>(),
  
  // Paper sections
  introduction: text("introduction"),
  methods: text("methods"),
  results: text("results"),
  discussion: text("discussion"),
  conclusion: text("conclusion"),
  references: json("references").$type<string[]>(),
  
  // Full paper content
  fullContent: text("fullContent"), // Complete paper in markdown
  
  // Export files
  wordFileUrl: text("wordFileUrl"), // S3 URL for Word document
  pdfFileUrl: text("pdfFileUrl"), // S3 URL for PDF
  
  // Statistics
  wordCount: int("wordCount"),
  
  // Generation status
  status: mysqlEnum("status", ["generating", "completed", "failed"]).default("generating").notNull(),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Paper = typeof papers.$inferSelect;
export type InsertPaper = typeof papers.$inferInsert;
