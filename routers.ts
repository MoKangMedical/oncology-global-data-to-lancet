import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, protectedProcedure, router } from "./_core/trpc";
import { z } from "zod";
import * as db from "./db";
import { storagePut } from "./storage";
import { nanoid } from "nanoid";
import { invokeLLM } from "./_core/llm";

export const appRouter = router({
  system: systemRouter,
  
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return {
        success: true,
      } as const;
    }),
  }),

  // Project management
  projects: router({
    // List all projects for current user
    list: protectedProcedure.query(async ({ ctx }) => {
      return db.getProjectsByUserId(ctx.user.id);
    }),

    // Get single project details
    get: protectedProcedure
      .input(z.object({ id: z.number() }))
      .query(async ({ input, ctx }) => {
        const project = await db.getProjectById(input.id);
        if (!project) {
          throw new Error("Project not found");
        }
        if (project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }
        return project;
      }),

    // Create new project
    create: protectedProcedure
      .input(z.object({
        title: z.string().min(1),
        description: z.string().optional(),
        cancerTypes: z.array(z.string()).optional(),
        countries: z.array(z.string()).optional(),
        regions: z.array(z.string()).optional(),
        timeRange: z.object({ start: z.number(), end: z.number() }).optional(),
        riskFactors: z.array(z.string()).optional(),
        ageGroups: z.array(z.string()).optional(),
        sexGroups: z.array(z.string()).optional(),
      }))
      .mutation(async ({ input, ctx }) => {
        const projectId = await db.createProject({
          userId: ctx.user.id,
          title: input.title,
          description: input.description,
          cancerTypes: input.cancerTypes,
          countries: input.countries,
          regions: input.regions,
          timeRange: input.timeRange,
          riskFactors: input.riskFactors,
          ageGroups: input.ageGroups,
          sexGroups: input.sexGroups,
          status: "draft",
          progress: 0,
        });
        return { id: projectId };
      }),

    // Update project
    update: protectedProcedure
      .input(z.object({
        id: z.number(),
        title: z.string().optional(),
        description: z.string().optional(),
        cancerTypes: z.array(z.string()).optional(),
        countries: z.array(z.string()).optional(),
        regions: z.array(z.string()).optional(),
        timeRange: z.object({ start: z.number(), end: z.number() }).optional(),
        riskFactors: z.array(z.string()).optional(),
        ageGroups: z.array(z.string()).optional(),
        sexGroups: z.array(z.string()).optional(),
        status: z.enum(["draft", "data_collection", "analyzing", "completed", "failed"]).optional(),
        progress: z.number().optional(),
      }))
      .mutation(async ({ input, ctx }) => {
        const { id, ...updates } = input;
        const project = await db.getProjectById(id);
        if (!project || project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }
        await db.updateProject(id, updates);
        return { success: true };
      }),

    // Delete project
    delete: protectedProcedure
      .input(z.object({ id: z.number() }))
      .mutation(async ({ input, ctx }) => {
        const project = await db.getProjectById(input.id);
        if (!project || project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }
        await db.deleteProject(input.id);
        return { success: true };
      }),

    // Upload research proposal and extract parameters
    uploadProposal: protectedProcedure
      .input(z.object({
        projectId: z.number(),
        fileName: z.string(),
        fileContent: z.string(), // base64 encoded
        mimeType: z.string(),
      }))
      .mutation(async ({ input, ctx }) => {
        const project = await db.getProjectById(input.projectId);
        if (!project || project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }

        // Upload file to S3
        const fileBuffer = Buffer.from(input.fileContent, 'base64');
        const fileKey = `projects/${input.projectId}/proposal/${nanoid()}-${input.fileName}`;
        const { url } = await storagePut(fileKey, fileBuffer, input.mimeType);

        // Update project with proposal file URL
        await db.updateProject(input.projectId, {
          proposalFileUrl: url,
          proposalFileName: input.fileName,
        });

        return { 
          success: true, 
          fileUrl: url,
        };
      }),

    // Extract parameters from proposal using LLM
    extractParameters: protectedProcedure
      .input(z.object({
        projectId: z.number(),
        proposalText: z.string(),
      }))
      .mutation(async ({ input, ctx }) => {
        const project = await db.getProjectById(input.projectId);
        if (!project || project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }

        // Use LLM to extract research parameters
        const response = await invokeLLM({
          messages: [
            {
              role: "system",
              content: `You are an expert in cancer epidemiology research. Extract key research parameters from the provided research proposal.
              
Return a JSON object with the following structure:
{
  "cancerTypes": ["list of cancer types mentioned"],
  "countries": ["list of countries/regions"],
  "regions": ["list of geographic regions"],
  "timeRange": { "start": year, "end": year },
  "riskFactors": ["list of risk factors to study"],
  "ageGroups": ["list of age groups"],
  "sexGroups": ["list of sex groups: Male, Female, Both"]
}

If any field is not mentioned in the proposal, use reasonable defaults based on standard cancer epidemiology research.`
            },
            {
              role: "user",
              content: `Extract research parameters from this proposal:\n\n${input.proposalText}`
            }
          ],
          response_format: {
            type: "json_schema",
            json_schema: {
              name: "research_parameters",
              strict: true,
              schema: {
                type: "object",
                properties: {
                  cancerTypes: {
                    type: "array",
                    items: { type: "string" },
                    description: "List of cancer types to study"
                  },
                  countries: {
                    type: "array",
                    items: { type: "string" },
                    description: "List of countries or regions"
                  },
                  regions: {
                    type: "array",
                    items: { type: "string" },
                    description: "List of geographic regions"
                  },
                  timeRange: {
                    type: "object",
                    properties: {
                      start: { type: "integer", description: "Start year" },
                      end: { type: "integer", description: "End year" }
                    },
                    required: ["start", "end"],
                    additionalProperties: false
                  },
                  riskFactors: {
                    type: "array",
                    items: { type: "string" },
                    description: "List of risk factors"
                  },
                  ageGroups: {
                    type: "array",
                    items: { type: "string" },
                    description: "List of age groups"
                  },
                  sexGroups: {
                    type: "array",
                    items: { type: "string" },
                    description: "List of sex groups"
                  }
                },
                required: ["cancerTypes", "countries", "regions", "timeRange", "riskFactors", "ageGroups", "sexGroups"],
                additionalProperties: false
              }
            }
          }
        });

        const content = response.choices[0]?.message?.content;
        if (!content || typeof content !== 'string') {
          throw new Error("Failed to extract parameters");
        }

        const parameters = JSON.parse(content);

        // Update project with extracted parameters
        await db.updateProject(input.projectId, {
          cancerTypes: parameters.cancerTypes,
          countries: parameters.countries,
          regions: parameters.regions,
          timeRange: parameters.timeRange,
          riskFactors: parameters.riskFactors,
          ageGroups: parameters.ageGroups,
          sexGroups: parameters.sexGroups,
        });

        return parameters;
      }),
  }),

  // Analysis and visualization
  analysis: router({
    // Run statistical analysis
    runAnalysis: protectedProcedure
      .input(z.object({
        projectId: z.number(),
        analysisType: z.enum(["paf", "cdpaf", "trend", "summary"]),
      }))
      .mutation(async ({ input, ctx }) => {
        const project = await db.getProjectById(input.projectId);
        if (!project || project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }

        // Get cancer data for the project
        const cancerData = await db.getCancerDataByProjectId(input.projectId);
        
        if (cancerData.length === 0) {
          throw new Error("No data available for analysis");
        }

        // Perform analysis based on type
        let results: any = {};
        
        if (input.analysisType === "summary") {
          // Calculate summary statistics
          const totalCases = cancerData.reduce((sum, d) => sum + (d.incidenceCount || 0), 0);
          const totalDeaths = cancerData.reduce((sum, d) => sum + (d.mortalityCount || 0), 0);
          
          const uniqueCountries = new Set(cancerData.map(d => d.country).filter(Boolean));
          const uniqueYears = new Set(cancerData.map(d => d.year).filter(Boolean));
          
          results = {
            totalCases,
            totalDeaths,
            dataPoints: cancerData.length,
            countries: uniqueCountries.size,
            years: uniqueYears.size,
          };
        }

        // Save analysis result
        const analysisId = await db.createAnalysisResult({
          projectId: input.projectId,
          analysisType: input.analysisType,
          parameters: {},
          results,
        });

        return { id: analysisId, results };
      }),

    // Get analysis results
    getResults: protectedProcedure
      .input(z.object({ projectId: z.number() }))
      .query(async ({ input, ctx }) => {
        const project = await db.getProjectById(input.projectId);
        if (!project || project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }
        return db.getAnalysisResultsByProjectId(input.projectId);
      }),
  }),

  // Visualization generation
  visualizations: router({
    // List visualizations
    list: protectedProcedure
      .input(z.object({ projectId: z.number() }))
      .query(async ({ input, ctx }) => {
        const project = await db.getProjectById(input.projectId);
        if (!project || project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }
        return db.getVisualizationsByProjectId(input.projectId);
      }),

    // Generate visualization
    generate: protectedProcedure
      .input(z.object({
        projectId: z.number(),
        visualizationType: z.string(),
        title: z.string(),
        config: z.any(),
      }))
      .mutation(async ({ input, ctx }) => {
        const project = await db.getProjectById(input.projectId);
        if (!project || project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }

        const vizId = await db.createVisualization({
          projectId: input.projectId,
          title: input.title,
          visualizationType: input.visualizationType,
          config: input.config,
        });

        return { id: vizId };
      }),
  }),

  // Paper generation
  papers: router({
    // List papers
    list: protectedProcedure
      .input(z.object({ projectId: z.number() }))
      .query(async ({ input, ctx }) => {
        const project = await db.getProjectById(input.projectId);
        if (!project || project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }
        return db.getPapersByProjectId(input.projectId);
      }),

    // Generate paper
    generate: protectedProcedure
      .input(z.object({ projectId: z.number() }))
      .mutation(async ({ input, ctx }) => {
        const project = await db.getProjectById(input.projectId);
        if (!project || project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }

        // Create paper record
        const paperId = await db.createPaper({
          projectId: input.projectId,
          title: `Research on ${project.cancerTypes?.join(", ") || "Cancer"} Epidemiology`,
          status: "generating",
        });

        // Paper generation will be done asynchronously
        // For now, just return the paper ID
        return { id: paperId };
      }),

    // Get paper details
    get: protectedProcedure
      .input(z.object({ paperId: z.number() }))
      .query(async ({ input, ctx }) => {
        const papers = await db.getPapersByProjectId(0); // Get all papers
        const paper = papers.find(p => p.id === input.paperId);
        
        if (!paper) {
          throw new Error("Paper not found");
        }

        // Verify access through project
        const project = await db.getProjectById(paper.projectId);
        if (!project || project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }

        return paper;
      }),
  }),

  // Data file management
  dataFiles: router({
    // List data files for a project
    list: protectedProcedure
      .input(z.object({ projectId: z.number() }))
      .query(async ({ input, ctx }) => {
        const project = await db.getProjectById(input.projectId);
        if (!project || project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }
        return db.getDataFilesByProjectId(input.projectId);
      }),

    // Upload data file
    upload: protectedProcedure
      .input(z.object({
        projectId: z.number(),
        dataSource: z.enum(["globocan", "gbd", "ci5", "other"]),
        fileName: z.string(),
        fileContent: z.string(), // base64 encoded
        mimeType: z.string(),
        dataType: z.string().optional(),
      }))
      .mutation(async ({ input, ctx }) => {
        const project = await db.getProjectById(input.projectId);
        if (!project || project.userId !== ctx.user.id) {
          throw new Error("Access denied");
        }

        // Upload file to S3
        const fileBuffer = Buffer.from(input.fileContent, 'base64');
        const fileKey = `projects/${input.projectId}/data/${input.dataSource}/${nanoid()}-${input.fileName}`;
        const { url } = await storagePut(fileKey, fileBuffer, input.mimeType);

        // Create data file record
        const fileId = await db.createDataFile({
          projectId: input.projectId,
          dataSource: input.dataSource,
          fileName: input.fileName,
          fileUrl: url,
          fileSize: fileBuffer.length,
          mimeType: input.mimeType,
          dataType: input.dataType,
          status: "uploaded",
        });

        return { 
          id: fileId,
          fileUrl: url,
        };
      }),
  }),
});

export type AppRouter = typeof appRouter;
