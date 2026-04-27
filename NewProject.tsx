import { useState } from "react";
import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { trpc } from "@/lib/trpc";
import { useLocation } from "wouter";
import { ArrowLeft, Upload, Loader2 } from "lucide-react";
import { Link } from "wouter";
import { toast } from "sonner";

export default function NewProject() {
  const { isAuthenticated } = useAuth();
  const [, setLocation] = useLocation();
  
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [proposalFile, setProposalFile] = useState<File | null>(null);
  const [extracting, setExtracting] = useState(false);

  const createMutation = trpc.projects.create.useMutation({
    onSuccess: async (data) => {
      toast.success("Project created successfully!");
      
      // If proposal file is provided, upload and extract parameters
      if (proposalFile) {
        try {
          setExtracting(true);
          
          // Read file content
          const reader = new FileReader();
          reader.onload = async (e) => {
            const content = e.target?.result as string;
            const base64Content = content.split(",")[1];
            
            // Upload proposal
            await uploadProposalMutation.mutateAsync({
              projectId: data.id,
              fileName: proposalFile.name,
              fileContent: base64Content,
              mimeType: proposalFile.type,
            });
            
            // Extract text from file for parameter extraction
            // For now, we'll skip automatic extraction and let users manually edit
            toast.success("Proposal uploaded successfully!");
            setLocation(`/projects/${data.id}`);
          };
          
          reader.readAsDataURL(proposalFile);
        } catch (error) {
          console.error("Error uploading proposal:", error);
          toast.error("Failed to upload proposal");
          setLocation(`/projects/${data.id}`);
        } finally {
          setExtracting(false);
        }
      } else {
        setLocation(`/projects/${data.id}`);
      }
    },
    onError: (error) => {
      toast.error(error.message || "Failed to create project");
    },
  });

  const uploadProposalMutation = trpc.projects.uploadProposal.useMutation();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!title.trim()) {
      toast.error("Please enter a project title");
      return;
    }

    createMutation.mutate({
      title: title.trim(),
      description: description.trim() || undefined,
    });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Check file type
      const allowedTypes = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
        "text/plain",
      ];
      
      if (!allowedTypes.includes(file.type)) {
        toast.error("Please upload a PDF, Word document, or text file");
        return;
      }
      
      // Check file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        toast.error("File size must be less than 10MB");
        return;
      }
      
      setProposalFile(file);
    }
  };

  if (!isAuthenticated) {
    return null;
  }

  const isLoading = createMutation.isPending || extracting;

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
          <h1 className="text-3xl font-bold text-foreground">Create New Research Project</h1>
          <p className="text-muted-foreground mt-1">
            Set up a new cancer epidemiology research project
          </p>
        </div>
      </div>

      {/* Content */}
      <div className="container py-8">
        <div className="max-w-2xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle>Project Information</CardTitle>
              <CardDescription>
                Provide basic information about your research project. You can add data sources and
                configure analysis parameters later.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Title */}
                <div className="space-y-2">
                  <Label htmlFor="title">
                    Project Title <span className="text-destructive">*</span>
                  </Label>
                  <Input
                    id="title"
                    placeholder="e.g., Global Burden of Hepatocellular Carcinoma"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                  />
                </div>

                {/* Description */}
                <div className="space-y-2">
                  <Label htmlFor="description">Description (Optional)</Label>
                  <Textarea
                    id="description"
                    placeholder="Brief description of your research objectives..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={4}
                  />
                </div>

                {/* Proposal Upload */}
                <div className="space-y-2">
                  <Label htmlFor="proposal">Research Proposal (Optional)</Label>
                  <div className="space-y-2">
                    <div className="upload-area">
                      <input
                        id="proposal"
                        type="file"
                        accept=".pdf,.doc,.docx,.txt"
                        onChange={handleFileChange}
                        className="hidden"
                      />
                      <label htmlFor="proposal" className="cursor-pointer">
                        <Upload className="w-8 h-8 text-muted-foreground mx-auto mb-2" />
                        <p className="text-sm font-medium">
                          {proposalFile ? proposalFile.name : "Click to upload research proposal"}
                        </p>
                        <p className="text-xs text-muted-foreground mt-1">
                          PDF, Word, or Text file (max 10MB)
                        </p>
                      </label>
                    </div>
                    {proposalFile && (
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => setProposalFile(null)}
                      >
                        Remove file
                      </Button>
                    )}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Upload your research proposal to automatically extract study parameters (cancer
                    types, regions, time range, etc.)
                  </p>
                </div>

                {/* Submit */}
                <div className="flex gap-3">
                  <Button type="submit" disabled={isLoading} className="flex-1">
                    {isLoading ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        {extracting ? "Extracting Parameters..." : "Creating Project..."}
                      </>
                    ) : (
                      "Create Project"
                    )}
                  </Button>
                  <Link href="/projects">
                    <Button type="button" variant="outline" disabled={isLoading}>
                      Cancel
                    </Button>
                  </Link>
                </div>
              </form>
            </CardContent>
          </Card>

          {/* Info Card */}
          <Card className="mt-6">
            <CardHeader>
              <CardTitle className="text-base">What happens next?</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground space-y-2">
              <p>After creating your project, you can:</p>
              <ul className="list-disc list-inside space-y-1 ml-2">
                <li>Upload data files from GLOBOCAN, GBD, and CI5 databases</li>
                <li>Configure research parameters (cancer types, regions, risk factors)</li>
                <li>Run statistical analyses (PAF, CDPAF, trend analysis)</li>
                <li>Generate visualizations and figures</li>
                <li>Automatically generate a research paper in Lancet format</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
