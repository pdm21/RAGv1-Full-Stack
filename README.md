# Docu-Dive
Docu-Dive is a full-stack multi-document-search web-app by utilizing Retrieval Augmented Generation techniques to get the most out of Generative AI LLMs. I used React.js for the frontend, and Python, Langchain, AWS Bedrock, ChromaDB, and FastAPI for the backend. I used Docker to containerize the frontend and backend, AWS ECR to store the Docker images, and AWS EC2 to run the containers, with Nginx configured on EC2 to manage traffic and SSL/TLS certificates for secure access. 

For a demonstration video, process document, and more information on the tech stack behind this application, visit: https://about-docu-dive.netlify.app/.

For more information on deploying this code, or similar code, one could follow these steps:

# Overview
This document outlines the step-by-step process for deploying a full-stack application using Docker and AWS services. The process includes building Docker images, pushing them to AWS ECR, and deploying the application using AWS ECS and EC2.

# Prerequisites
- AWS CLI configured with appropriate IAM permissions
- Docker installed on your local machine
- An AWS account with access to ECR, ECS, and EC2 services
- Domain configured in Route 53

## Step-by-Step Deployment Process
### Prepare Python Files:
- Organize all your Python backend files, including main.py and any supporting scripts like query.py.
### Create Dockerfiles:
- Create Dockerfiles for both the frontend and backend applications.
- The Dockerfiles specify the environment and dependencies needed for each component.
```docker
# Example Dockerfile for frontend
FROM node:14
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "start"]
```
```docker
# Example Dockerfile for backend
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build Docker Images:
- Use the Dockerfiles to build images for the frontend and backend.
- Ensure the correct platform is specified during the build process.
```bash
docker build --platform linux/amd64 -t frontend-image .
docker build --platform linux/amd64 -t backend-image .
```
### Push Docker Images to AWS ECR:
- Create ECR repositories for the frontend and backend if they don't exist.
- Tag and push the Docker images to the respective ECR repositories.
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account_id>.dkr.ecr.us-east-1.amazonaws.com
docker tag frontend-image:latest <account_id>.dkr.ecr.us-east-1.amazonaws.com/frontend-repo:latest
docker push <account_id>.dkr.ecr.us-east-1.amazonaws.com/frontend-repo:latest
docker tag backend-image:latest <account_id>.dkr.ecr.us-east-1.amazonaws.com/backend-repo:latest
docker push <account_id>.dkr.ecr.us-east-1.amazonaws.com/backend-repo:latest
```
### Set Up ECS Cluster:
- Create an ECS cluster to manage the Docker containers.
### Register ECS Task Definitions:
- Create task definitions for the frontend and backend services using JSON configuration files.
- These definitions specify how the containers should be run within ECS.
```bash
aws ecs register-task-definition --cli-input-json file://frontend-task-definition.json
aws ecs register-task-definition --cli-input-json file://backend-task-definition.json
```
### Create ECS Services:
- Create ECS services for the frontend and backend tasks.
- Ensure the services are configured to run the correct number of tasks and are properly networked.
```bash
aws ecs create-service --cluster docu-dive-cluster --service-name frontend-service --task-definition frontend-task --desired-count 1 --launch-type FARGATE
aws ecs create-service --cluster docu-dive-cluster --service-name backend-service --task-definition backend-task --desired-count 1 --launch-type FARGATE
```
### Set Up EC2 Instance:
- Launch an EC2 instance to host the Nginx server.
- Configure security groups to allow necessary traffic.
### Deploy Nginx Configuration:
- Configure Nginx as a reverse proxy to route traffic to the frontend and backend services.
```nginx
server {
    listen 80;
    server_name docu-dive.com www.docu-dive.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name docu-dive.com www.docu-dive.com;

    ssl_certificate /etc/letsencrypt/live/docu-dive.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/docu-dive.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;  # Frontend
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://localhost:8000;  # Backend
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
### Run Docker Containers on EC2:
- Run the Docker containers on the EC2 instance
- Do this for both the frontend and backend applications.
```bash
docker run -d -p 3000:3000 --name frontend-container <account_id>.dkr.ecr.us-east-1.amazonaws.com/frontend-repo:latest
docker run -d -p 8000:8000 --name backend-container <account_id>.dkr.ecr.us-east-1.amazonaws.com/backend-repo:latest
```
