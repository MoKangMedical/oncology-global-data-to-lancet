import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { trpc } from "@/lib/trpc";
import { Plus, FileText, Database, BarChart3, FileCheck, Trash2 } from "lucide-react";
import { Link } from "wouter";
import { getLoginUrl } from "@/const";

export default function Projects() {
  const { user, loading: authLoading, isAuthenticated } = useAuth();
  const { data: projects, isLoading, refetch } = trpc.projects.list.useQuery(undefined, {
    enabled: isAuthenticated,
  });

  const deleteMutation = trpc.projects.delete.useMutation({
    onSuccess: () => {
      refetch();
    },
  });

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-50">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Authentication Required</CardTitle>
            <CardDescription>Please sign in to access your research projects</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full">
              <a href={getLoginUrl()}>Sign In</a>
            </Button>
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
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-foreground">My Research Projects</h1>
              <p className="text-muted-foreground mt-1">
                Manage your cancer epidemiology research projects
              </p>
            </div>
            <Link href="/projects/new">
              <Button size="lg" className="gap-2">
                <Plus className="w-5 h-5" />
                New Project
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container py-8">
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-muted-foreground">Loading projects...</p>
          </div>
        ) : projects && projects.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <Card key={project.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg line-clamp-2">{project.title}</CardTitle>
                      <CardDescription className="mt-1 line-clamp-2">
                        {project.description || "No description"}
                      </CardDescription>
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => {
                        if (confirm("Are you sure you want to delete this project?")) {
                          deleteMutation.mutate({ id: project.id });
                        }
                      }}
                      className="text-destructive hover:text-destructive"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                  <div className="mt-2">{getStatusBadge(project.status)}</div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {/* Project metadata */}
                    <div className="text-sm space-y-1">
                      {project.cancerTypes && project.cancerTypes.length > 0 && (
                        <div className="flex items-start gap-2">
                          <FileText className="w-4 h-4 text-muted-foreground mt-0.5" />
                          <span className="text-muted-foreground">
                            {project.cancerTypes.join(", ")}
                          </span>
                        </div>
                      )}
                      {project.countries && project.countries.length > 0 && (
                        <div className="flex items-start gap-2">
                          <Database className="w-4 h-4 text-muted-foreground mt-0.5" />
                          <span className="text-muted-foreground">
                            {project.countries.length} countries/regions
                          </span>
                        </div>
                      )}
                      {project.timeRange && (
                        <div className="flex items-start gap-2">
                          <BarChart3 className="w-4 h-4 text-muted-foreground mt-0.5" />
                          <span className="text-muted-foreground">
                            {project.timeRange.start} - {project.timeRange.end}
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Progress bar */}
                    {project.progress != null && project.progress > 0 && (
                      <div className="space-y-1">
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-muted-foreground">Progress</span>
                          <span className="font-medium">{project.progress}%</span>
                        </div>
                        <div className="w-full bg-muted rounded-full h-2">
                          <div
                            className="bg-primary h-2 rounded-full transition-all"
                            style={{ width: `${project.progress}%` }}
                          />
                        </div>
                      </div>
                    )}

                    {/* Actions */}
                    <div className="pt-2 flex gap-2">
                      <Link href={`/projects/${project.id}`} className="flex-1">
                        <Button variant="outline" size="sm" className="w-full gap-2">
                          <FileCheck className="w-4 h-4" />
                          View Details
                        </Button>
                      </Link>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="max-w-2xl mx-auto">
            <CardContent className="py-12 text-center">
              <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
                <FileText className="w-8 h-8 text-muted-foreground" />
              </div>
              <h3 className="text-lg font-semibold mb-2">No Projects Yet</h3>
              <p className="text-muted-foreground mb-6">
                Create your first cancer research project to get started with automated data analysis
                and paper generation.
              </p>
              <Link href="/projects/new">
                <Button size="lg" className="gap-2">
                  <Plus className="w-5 h-5" />
                  Create Your First Project
                </Button>
              </Link>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
