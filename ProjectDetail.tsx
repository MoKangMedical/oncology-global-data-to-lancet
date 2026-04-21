import { useState } from "react";
import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { trpc } from "@/lib/trpc";
import { useLocation, useParams } from "wouter";
import { 
  ArrowLeft, 
  Upload, 
  Database, 
  BarChart3, 
  FileText,
  Settings,
  Loader2,
  CheckCircle2,
  AlertCircle,
  Download
} from "lucide-react";
import { Link } from "wouter";
import { toast } from "sonner";

export default function ProjectDetail() {
  const { id } = useParams<{ id: string }>();
  const projectId = parseInt(id || "0");
  const { isAuthenticated } = useAuth();
  const [, setLocation] = useLocation();
  const [uploadingFile, setUploadingFile] = useState(false);

  const { data: project, isLoading, refetch } = trpc.projects.get.useQuery(
    { id: projectId },
    { enabled: isAuthenticated && projectId > 0 }
  );

  const { data: dataFiles } = trpc.dataFiles.list.useQuery(
    { projectId },
    { enabled: isAuthenticated && projectId > 0 }
  );

  const { data: analysisResults } = trpc.analysis.getResults.useQuery(
    { projectId },
    { enabled: isAuthenticated && projectId > 0 }
  );

  const { data: visualizations } = trpc.visualizations.list.useQuery(
    { projectId },
    { enabled: isAuthenticated && projectId > 0 }
  );

  const { data: papers } = trpc.papers.list.useQuery(
    { projectId },
    { enabled: isAuthenticated && projectId > 0 }
  );

  const uploadFileMutation = trpc.dataFiles.upload.useMutation({
    onSuccess: () => {
      toast.success("Data file uploaded successfully!");
      refetch();
    },
    onError: (error) => {
      toast.error(error.message || "Failed to upload file");
    },
  });

  const runAnalysisMutation = trpc.analysis.runAnalysis.useMutation({
    onSuccess: () => {
      toast.success("Analysis completed successfully!");
      refetch();
    },
    onError: (error) => {
      toast.error(error.message || "Analysis failed");
    },
  });

  const handleFileUpload = async (
    e: React.ChangeEvent<HTMLInputElement>,
    dataSource: "globocan" | "gbd" | "ci5" | "other"
  ) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Check file type
    const allowedTypes = [
      "text/csv",
      "application/vnd.ms-excel",
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ];

    if (!allowedTypes.includes(file.type)) {
      toast.error("Please upload a CSV or Excel file");
      return;
    }

    // Check file size (max 50MB)
    if (file.size > 50 * 1024 * 1024) {
      toast.error("File size must be less than 50MB");
      return;
    }

    setUploadingFile(true);

    try {
      const reader = new FileReader();
      reader.onload = async (event) => {
        const content = event.target?.result as string;
        const base64Content = content.split(",")[1];

        await uploadFileMutation.mutateAsync({
          projectId,
          dataSource,
          fileName: file.name,
          fileContent: base64Content,
          mimeType: file.type,
        });
      };

      reader.readAsDataURL(file);
    } catch (error) {
      console.error("Error uploading file:", error);
      toast.error("Failed to upload file");
    } finally {
      setUploadingFile(false);
    }
  };

  const handleRunAnalysis = (analysisType: "paf" | "cdpaf" | "trend" | "summary") => {
    runAnalysisMutation.mutate({
      projectId,
      analysisType,
    });
  };

  if (!isAuthenticated) {
    return null;
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-primary mx-auto" />
          <p className="mt-4 text-muted-foreground">Loading project...</p>
        </div>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="py-12 text-center">
            <AlertCircle className="w-12 h-12 text-destructive mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Project Not Found</h3>
            <p className="text-muted-foreground mb-6">
              The project you're looking for doesn't exist or you don't have access to it.
            </p>
            <Link href="/projects">
              <Button>Back to Projects</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  const getStatusBadge = (status: string) => {
    const badges: Record<string, { label: string; className: string }> = {
      draft: { label: "Draft", className: "badge badge-info" },
      data_collection: { label: "Data Collection", className: "badge badge-warning" },
      analyzing: { label: "Analyzing", className: "badge badge-warning" },
      completed: { label: "Completed", className: "badge badge-success" },
      failed: { label: "Failed", className: "badge badge-error" },
    };
    const badge = badges[status] || badges.draft;
    return <span className={badge.className}>{badge.label}</span>;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      {/* Header */}
      <div className="bg-white border-b border-border">
        <div className="container py-6">
          <Link href="/projects">
            <Button variant="ghost" size="sm" className="gap-2 mb-4">
              <ArrowLeft className="w-4 h-4" />
              Back to Projects
            </Button>
          </Link>
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-3xl font-bold text-foreground">{project.title}</h1>
                {getStatusBadge(project.status)}
              </div>
              {project.description && (
                <p className="text-muted-foreground">{project.description}</p>
              )}
            </div>
          </div>

          {/* Progress bar */}
          {project.progress != null && project.progress > 0 && (
            <div className="mt-6 max-w-xl">
              <div className="flex items-center justify-between text-sm mb-2">
                <span className="text-muted-foreground">Overall Progress</span>
                <span className="font-medium">{project.progress}%</span>
              </div>
              <div className="w-full bg-muted rounded-full h-3">
                <div
                  className="bg-primary h-3 rounded-full transition-all"
                  style={{ width: `${project.progress}%` }}
                />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="container py-8">
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="bg-white">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="data">Data Files</TabsTrigger>
            <TabsTrigger value="analysis">Analysis</TabsTrigger>
            <TabsTrigger value="visualizations">Visualizations</TabsTrigger>
            <TabsTrigger value="papers">Papers</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="stat-card">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="stat-label">Data Files</p>
                      <p className="stat-value">{dataFiles?.length || 0}</p>
                    </div>
                    <Database className="w-8 h-8 text-primary opacity-20" />
                  </div>
                </CardContent>
              </Card>

              <Card className="stat-card">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="stat-label">Analyses</p>
                      <p className="stat-value">{analysisResults?.length || 0}</p>
                    </div>
                    <BarChart3 className="w-8 h-8 text-primary opacity-20" />
                  </div>
                </CardContent>
              </Card>

              <Card className="stat-card">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="stat-label">Papers</p>
                      <p className="stat-value">{papers?.length || 0}</p>
                    </div>
                    <FileText className="w-8 h-8 text-primary opacity-20" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Research Parameters */}
            <Card>
              <CardHeader>
                <CardTitle>Research Parameters</CardTitle>
                <CardDescription>Key parameters for this research project</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {project.cancerTypes && project.cancerTypes.length > 0 && (
                  <div>
                    <p className="text-sm font-medium mb-1">Cancer Types</p>
                    <div className="flex flex-wrap gap-2">
                      {project.cancerTypes.map((type, i) => (
                        <span key={i} className="badge badge-info">
                          {type}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {project.countries && project.countries.length > 0 && (
                  <div>
                    <p className="text-sm font-medium mb-1">Countries/Regions</p>
                    <div className="flex flex-wrap gap-2">
                      {project.countries.map((country, i) => (
                        <span key={i} className="badge badge-info">
                          {country}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {project.timeRange && (
                  <div>
                    <p className="text-sm font-medium mb-1">Time Range</p>
                    <p className="text-muted-foreground">
                      {project.timeRange.start} - {project.timeRange.end}
                    </p>
                  </div>
                )}

                {project.riskFactors && project.riskFactors.length > 0 && (
                  <div>
                    <p className="text-sm font-medium mb-1">Risk Factors</p>
                    <div className="flex flex-wrap gap-2">
                      {project.riskFactors.map((factor, i) => (
                        <span key={i} className="badge badge-warning">
                          {factor}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Data Files Tab */}
          <TabsContent value="data" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Upload Data Files</CardTitle>
                <CardDescription>
                  Upload cancer data from GLOBOCAN, GBD, or CI5 databases
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {["globocan", "gbd", "ci5"].map((source) => (
                  <div key={source} className="border border-border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium capitalize">{source.toUpperCase()}</h4>
                      <label htmlFor={`upload-${source}`}>
                        <Button variant="outline" size="sm" disabled={uploadingFile} asChild>
                          <span className="gap-2 cursor-pointer">
                            <Upload className="w-4 h-4" />
                            Upload
                          </span>
                        </Button>
                      </label>
                      <input
                        id={`upload-${source}`}
                        type="file"
                        accept=".csv,.xls,.xlsx"
                        onChange={(e) =>
                          handleFileUpload(e, source as "globocan" | "gbd" | "ci5")
                        }
                        className="hidden"
                      />
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Upload CSV or Excel files from {source.toUpperCase()} database
                    </p>
                  </div>
                ))}
              </CardContent>
            </Card>

            {dataFiles && dataFiles.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Uploaded Files</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {dataFiles.map((file) => (
                      <div
                        key={file.id}
                        className="flex items-center justify-between p-3 border border-border rounded-lg"
                      >
                        <div className="flex items-center gap-3">
                          <Database className="w-5 h-5 text-muted-foreground" />
                          <div>
                            <p className="font-medium">{file.fileName}</p>
                            <p className="text-xs text-muted-foreground">
                              {file.dataSource.toUpperCase()} • {file.status}
                            </p>
                          </div>
                        </div>
                        {file.status === "processed" && (
                          <CheckCircle2 className="w-5 h-5 text-green-500" />
                        )}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Analysis Tab */}
          <TabsContent value="analysis" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Run Statistical Analysis</CardTitle>
                <CardDescription>
                  Perform various statistical analyses on your cancer data
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button
                  onClick={() => handleRunAnalysis("summary")}
                  disabled={runAnalysisMutation.isPending}
                  className="w-full justify-start"
                  variant="outline"
                >
                  Summary Statistics
                </Button>
                <Button
                  onClick={() => handleRunAnalysis("paf")}
                  disabled={runAnalysisMutation.isPending}
                  className="w-full justify-start"
                  variant="outline"
                >
                  Population Attributable Fraction (PAF)
                </Button>
                <Button
                  onClick={() => handleRunAnalysis("trend")}
                  disabled={runAnalysisMutation.isPending}
                  className="w-full justify-start"
                  variant="outline"
                >
                  Trend Analysis (Joinpoint)
                </Button>
              </CardContent>
            </Card>

            {analysisResults && analysisResults.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Analysis Results</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {analysisResults.map((result) => (
                      <div
                        key={result.id}
                        className="p-4 border border-border rounded-lg"
                      >
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-medium capitalize">
                            {result.analysisType} Analysis
                          </h4>
                          <CheckCircle2 className="w-5 h-5 text-green-500" />
                        </div>
                        <pre className="text-xs bg-muted p-3 rounded overflow-auto">
                          {JSON.stringify(result.results, null, 2)}
                        </pre>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Visualizations Tab */}
          <TabsContent value="visualizations">
            <Card>
              <CardContent className="py-12 text-center">
                <BarChart3 className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">
                  Visualizations will be generated after running analyses
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Papers Tab */}
          <TabsContent value="papers">
            <Card>
              <CardContent className="py-12 text-center">
                <FileText className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground mb-4">
                  Generate research papers after completing data analysis
                </p>
                <Button disabled>Generate Paper (Coming Soon)</Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
