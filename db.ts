import { eq, and, desc } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import { 
  InsertUser, 
  users, 
  projects, 
  InsertProject,
  Project,
  dataFiles,
  InsertDataFile,
  DataFile,
  cancerData,
  InsertCancerData,
  CancerData,
  analysisResults,
  InsertAnalysisResult,
  AnalysisResult,
  visualizations,
  InsertVisualization,
  Visualization,
  papers,
  InsertPaper,
  Paper
} from "../drizzle/schema";
import { ENV } from './_core/env';

let _db: ReturnType<typeof drizzle> | null = null;

export async function getDb() {
  if (!_db && process.env.DATABASE_URL) {
    try {
      _db = drizzle(process.env.DATABASE_URL);
    } catch (error) {
      console.warn("[Database] Failed to connect:", error);
      _db = null;
    }
  }
  return _db;
}

// ============ User Operations ============

export async function upsertUser(user: InsertUser): Promise<void> {
  if (!user.openId) {
    throw new Error("User openId is required for upsert");
  }

  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot upsert user: database not available");
    return;
  }

  try {
    const values: InsertUser = {
      openId: user.openId,
    };
    const updateSet: Record<string, unknown> = {};

    const textFields = ["name", "email", "loginMethod"] as const;
    type TextField = (typeof textFields)[number];

    const assignNullable = (field: TextField) => {
      const value = user[field];
      if (value === undefined) return;
      const normalized = value ?? null;
      values[field] = normalized;
      updateSet[field] = normalized;
    };

    textFields.forEach(assignNullable);

    if (user.lastSignedIn !== undefined) {
      values.lastSignedIn = user.lastSignedIn;
      updateSet.lastSignedIn = user.lastSignedIn;
    }
    if (user.role !== undefined) {
      values.role = user.role;
      updateSet.role = user.role;
    } else if (user.openId === ENV.ownerOpenId) {
      values.role = 'admin';
      updateSet.role = 'admin';
    }

    if (!values.lastSignedIn) {
      values.lastSignedIn = new Date();
    }

    if (Object.keys(updateSet).length === 0) {
      updateSet.lastSignedIn = new Date();
    }

    await db.insert(users).values(values).onDuplicateKeyUpdate({
      set: updateSet,
    });
  } catch (error) {
    console.error("[Database] Failed to upsert user:", error);
    throw error;
  }
}

export async function getUserByOpenId(openId: string) {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot get user: database not available");
    return undefined;
  }

  const result = await db.select().from(users).where(eq(users.openId, openId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

// ============ Project Operations ============

export async function createProject(project: InsertProject): Promise<number> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(projects).values(project);
  return Number(result[0].insertId);
}

export async function getProjectById(projectId: number): Promise<Project | undefined> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.select().from(projects).where(eq(projects.id, projectId)).limit(1);
  return result[0];
}

export async function getProjectsByUserId(userId: number): Promise<Project[]> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  return db.select().from(projects).where(eq(projects.userId, userId)).orderBy(desc(projects.createdAt));
}

export async function updateProject(projectId: number, updates: Partial<InsertProject>): Promise<void> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.update(projects).set(updates).where(eq(projects.id, projectId));
}

export async function deleteProject(projectId: number): Promise<void> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.delete(projects).where(eq(projects.id, projectId));
}

// ============ Data File Operations ============

export async function createDataFile(dataFile: InsertDataFile): Promise<number> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(dataFiles).values(dataFile);
  return Number(result[0].insertId);
}

export async function getDataFilesByProjectId(projectId: number): Promise<DataFile[]> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  return db.select().from(dataFiles).where(eq(dataFiles.projectId, projectId)).orderBy(desc(dataFiles.createdAt));
}

export async function updateDataFile(fileId: number, updates: Partial<InsertDataFile>): Promise<void> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.update(dataFiles).set(updates).where(eq(dataFiles.id, fileId));
}

// ============ Cancer Data Operations ============

export async function insertCancerData(data: InsertCancerData[]): Promise<void> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  if (data.length === 0) return;
  
  // Insert in batches to avoid query size limits
  const batchSize = 1000;
  for (let i = 0; i < data.length; i += batchSize) {
    const batch = data.slice(i, i + batchSize);
    await db.insert(cancerData).values(batch);
  }
}

export async function getCancerDataByProjectId(projectId: number): Promise<CancerData[]> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  return db.select().from(cancerData).where(eq(cancerData.projectId, projectId));
}

// ============ Analysis Result Operations ============

export async function createAnalysisResult(result: InsertAnalysisResult): Promise<number> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const insertResult = await db.insert(analysisResults).values(result);
  return Number(insertResult[0].insertId);
}

export async function getAnalysisResultsByProjectId(projectId: number): Promise<AnalysisResult[]> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  return db.select().from(analysisResults).where(eq(analysisResults.projectId, projectId)).orderBy(desc(analysisResults.createdAt));
}

// ============ Visualization Operations ============

export async function createVisualization(viz: InsertVisualization): Promise<number> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(visualizations).values(viz);
  return Number(result[0].insertId);
}

export async function getVisualizationsByProjectId(projectId: number): Promise<Visualization[]> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  return db.select().from(visualizations).where(eq(visualizations.projectId, projectId)).orderBy(desc(visualizations.createdAt));
}

// ============ Paper Operations ============

export async function createPaper(paper: InsertPaper): Promise<number> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(papers).values(paper);
  return Number(result[0].insertId);
}

export async function getPapersByProjectId(projectId: number): Promise<Paper[]> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  return db.select().from(papers).where(eq(papers.projectId, projectId)).orderBy(desc(papers.createdAt));
}

export async function updatePaper(paperId: number, updates: Partial<InsertPaper>): Promise<void> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.update(papers).set(updates).where(eq(papers.id, paperId));
}
