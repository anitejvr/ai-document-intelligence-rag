resource "aws_ecs_cluster" "app" {
  name = "ai-document-intelligence-cluster"

  tags = {
    Project = var.project_name
  }
}