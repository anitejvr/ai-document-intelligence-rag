# AI Document Intelligence Platform

> A cloud-native AI document analysis platform built with Python, Flask, Docker, AWS, Terraform, and GitHub Actions.

## Overview

AI Document Intelligence Platform enables users to upload PDF documents and automatically generate AI-powered insights using OpenAI language models.

The application extracts text from uploaded PDFs, analyzes document content, and generates:

- Executive Summaries
- Key Findings
- Risks & Concerns
- Recommended Actions

The platform is fully containerized with Docker, deployed on AWS ECS Fargate behind an Application Load Balancer, managed with Terraform, and automatically deployed through GitHub Actions.

This project demonstrates practical experience building and operating a production-style AI application using modern cloud engineering and DevOps practices.

---

# Current Features

## Document Processing

- Upload PDF documents
- Multi-page PDF support
- Automatic text extraction using PyPDF2

## AI Analysis

Generate AI-powered:

- Executive Summary
- Key Findings
- Risks & Concerns
- Recommended Actions

## Cloud Deployment

- Docker containerization
- AWS ECS Fargate deployment
- Amazon ECR image repository
- Application Load Balancer
- AWS Secrets Manager
- CloudWatch logging
- IAM roles and least-privilege permissions

## Infrastructure as Code

Infrastructure is managed using Terraform.

Current infrastructure includes:

- Amazon ECS Cluster
- Amazon ECR Repository
- IAM Roles
- Security Groups
- CloudWatch Log Groups
- Application Load Balancer
- Target Groups
- Listeners

## CI/CD

Every push to the `main` branch automatically:

1. Builds a Docker image
2. Tags the image with the Git commit SHA
3. Pushes the image to Amazon ECR
4. Registers a new ECS Task Definition revision
5. Deploys the new task definition to Amazon ECS
6. Waits for service stabilization

No manual deployments are required.

---

# Architecture

```
                    GitHub
                       │
               GitHub Actions
                       │
        Build & Push Docker Image
                       │
                       ▼
                 Amazon ECR
                       │
                       ▼
                  Amazon ECS
                 (AWS Fargate)
                       │
                       ▼
        Application Load Balancer
                       │
                       ▼
              Flask Web Application
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
   OpenAI API                 CloudWatch Logs
                       │
                       ▼
                Secrets Manager
```

---

# Technology Stack

## Backend

- Python
- Flask
- Gunicorn

## AI

- OpenAI API
- Prompt Engineering

## Document Processing

- PyPDF2

## Cloud

- Amazon ECS
- AWS Fargate
- Amazon ECR
- Application Load Balancer
- IAM
- Secrets Manager
- CloudWatch
- VPC
- Security Groups

## Infrastructure

- Terraform

## DevOps

- Docker
- GitHub Actions
- Git
- GitHub

---

# Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── deploy.yaml
│
├── terraform/
│   ├── alb.tf
│   ├── ecs.tf
│   ├── ecr.tf
│   ├── iam.tf
│   ├── logs.tf
│   ├── provider.tf
│   ├── security.tf
│   ├── variables.tf
│   └── data.tf
│
├── static/
├── templates/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Running Locally

Clone the repository:

```bash
git clone https://github.com/anitejvr/ai-document-intelligence-rag.git
cd ai-document-intelligence-rag
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file containing:

```text
OPENAI_API_KEY=your_api_key
FLASK_SECRET_KEY=your_secret_key
```

Run the application:

```bash
python app.py
```

---

# Running with Docker

Build the image:

```bash
docker build -t ai-document-intelligence-rag .
```

Run the container:

```bash
docker run -p 5000:5000 --env-file .env ai-document-intelligence-rag
```

---

# Infrastructure

Infrastructure is provisioned and managed using Terraform.

Typical workflow:

```bash
cd terraform

terraform init

terraform plan

terraform apply
```

---

# Engineering Concepts Demonstrated

This project demonstrates experience with:

- Cloud-native application deployment
- Containerization
- Infrastructure as Code
- CI/CD pipelines
- Secure secret management
- AI application development
- AWS networking
- Docker image lifecycle
- Cloud logging and monitoring
- Production deployment workflows

---

# Roadmap

## Completed

- AI-powered PDF document analysis
- Docker containerization
- AWS ECS Fargate deployment
- Application Load Balancer
- Terraform Infrastructure as Code
- GitHub Actions CI/CD
- Immutable Docker image deployments
- CloudWatch logging
- IAM security
- Secrets Manager integration

## Next

- Amazon S3 document storage
- Document chunking
- OpenAI embeddings
- Vector database (pgvector)
- Retrieval-Augmented Generation (RAG)
- Semantic search
- Source citations
- Multi-document querying

## Future

- User authentication
- Conversation history
- Multi-user workspaces
- Streaming responses
- CloudWatch dashboards
- ECS Auto Scaling
- HTTPS with AWS Certificate Manager
- Custom domain
- Cost monitoring

---

# Lessons Learned

This project provided hands-on experience with building, deploying, and operating a production-style AI application on AWS.

Key areas of learning included:

- Designing cloud-native architectures
- Managing infrastructure using Terraform
- Building automated deployment pipelines with GitHub Actions
- Deploying containerized applications on ECS Fargate
- Securely managing secrets with AWS Secrets Manager
- Troubleshooting IAM permissions, networking, Docker, and ECS deployments

---

# Author

**Anitej Ramesh**

- Economics, University of Chicago
- AWS Certified Solutions Architect – Associate
- Solutions Architect | Cloud Engineer | AI Engineer

---

## License

This project is licensed under the MIT License.