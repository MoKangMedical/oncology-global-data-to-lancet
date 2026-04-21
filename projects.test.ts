import { describe, expect, it } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

type AuthenticatedUser = NonNullable<TrpcContext["user"]>;

function createAuthContext(): { ctx: TrpcContext } {
  const user: AuthenticatedUser = {
    id: 1,
    openId: "test-user",
    email: "test@example.com",
    name: "Test User",
    loginMethod: "manus",
    role: "user",
    createdAt: new Date(),
    updatedAt: new Date(),
    lastSignedIn: new Date(),
  };

  const ctx: TrpcContext = {
    user,
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {
      clearCookie: () => {},
    } as TrpcContext["res"],
  };

  return { ctx };
}

describe("projects.create", () => {
  it("creates a new project with valid data", async () => {
    const { ctx } = createAuthContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.projects.create({
      title: "Test Cancer Research Project",
      description: "A test project for hepatocellular carcinoma research",
      cancerTypes: ["Liver cancer", "HCC"],
      countries: ["China", "USA"],
      timeRange: { start: 1990, end: 2022 },
      riskFactors: ["HBV", "HCV", "Obesity"],
    });

    expect(result).toHaveProperty("id");
    expect(typeof result.id).toBe("number");
    expect(result.id).toBeGreaterThan(0);
  });

  it("creates a project with minimal data", async () => {
    const { ctx } = createAuthContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.projects.create({
      title: "Minimal Project",
    });

    expect(result).toHaveProperty("id");
    expect(typeof result.id).toBe("number");
  });
});

describe("projects.list", () => {
  it("returns an array of projects", async () => {
    const { ctx } = createAuthContext();
    const caller = appRouter.createCaller(ctx);

    // Create a test project first
    await caller.projects.create({
      title: "Test Project for List",
      description: "Testing project listing",
    });

    const projects = await caller.projects.list();

    expect(Array.isArray(projects)).toBe(true);
    expect(projects.length).toBeGreaterThan(0);
    
    // Check structure of first project
    if (projects.length > 0) {
      const project = projects[0];
      expect(project).toHaveProperty("id");
      expect(project).toHaveProperty("title");
      expect(project).toHaveProperty("status");
      expect(project).toHaveProperty("userId");
    }
  });
});

describe("projects.get", () => {
  it("retrieves a specific project by id", async () => {
    const { ctx } = createAuthContext();
    const caller = appRouter.createCaller(ctx);

    // Create a test project
    const created = await caller.projects.create({
      title: "Test Project for Get",
      description: "Testing project retrieval",
      cancerTypes: ["Lung cancer"],
    });

    // Retrieve the project
    const project = await caller.projects.get({ id: created.id });

    expect(project).toBeDefined();
    expect(project.id).toBe(created.id);
    expect(project.title).toBe("Test Project for Get");
    expect(project.description).toBe("Testing project retrieval");
    expect(project.cancerTypes).toEqual(["Lung cancer"]);
  });

  it("throws error for non-existent project", async () => {
    const { ctx } = createAuthContext();
    const caller = appRouter.createCaller(ctx);

    await expect(
      caller.projects.get({ id: 999999 })
    ).rejects.toThrow("Project not found");
  });
});

describe("projects.update", () => {
  it("updates project fields", async () => {
    const { ctx } = createAuthContext();
    const caller = appRouter.createCaller(ctx);

    // Create a test project
    const created = await caller.projects.create({
      title: "Original Title",
      description: "Original description",
    });

    // Update the project
    await caller.projects.update({
      id: created.id,
      title: "Updated Title",
      description: "Updated description",
      status: "data_collection",
      progress: 50,
    });

    // Verify updates
    const updated = await caller.projects.get({ id: created.id });
    expect(updated.title).toBe("Updated Title");
    expect(updated.description).toBe("Updated description");
    expect(updated.status).toBe("data_collection");
    expect(updated.progress).toBe(50);
  });
});

describe("projects.delete", () => {
  it("deletes a project", async () => {
    const { ctx } = createAuthContext();
    const caller = appRouter.createCaller(ctx);

    // Create a test project
    const created = await caller.projects.create({
      title: "Project to Delete",
    });

    // Delete the project
    const result = await caller.projects.delete({ id: created.id });
    expect(result.success).toBe(true);

    // Verify deletion
    await expect(
      caller.projects.get({ id: created.id })
    ).rejects.toThrow("Project not found");
  });
});
