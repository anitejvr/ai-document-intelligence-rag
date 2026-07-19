variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "ai-document-intelligence-rag"
}

variable "document_bucket_name" {
  description = "S3 bucket for uploaded documents"
  type        = string
  default     = "ai-document-intelligence-rag-documents-207791567970"
}