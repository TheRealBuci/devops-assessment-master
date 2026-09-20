# DevOps Engineer Homework

## Overview

The goal of this assignment is to evaluate how you approach a typical DevOps engineering task involving:

- Application development / scripting
- Containerization
- Kubernetes
- Helm
- Terraform
- CI/CD
- Code review

The repository contains intentionally incomplete and imperfect components.
Your task is to complete, improve and document the solution.

You are not expected to produce a perfect production-ready system. We are more interested in your engineering approach, decision-making and ability to balance quality with the time constraints.

Time limit: approximately **3 hours**

## Repository Contents

The repository contains:

- An incomplete application skeleton
- Terraform configuration requiring review and improvement
- An incomplete Helm chart
- An incomplete CI/CD pipeline

Your task is to complete and improve these components. Our goal is to understand your engineering approach, and we will build the upcoming technical interview on this project.

## Goal 1

Complete and improve the provided project.

The repository contains the following files:

- Incomplete application code
- Broken/incomplete terraform configuration
- Incomplete Helm Chart
- Incomplete Gitlab CI pipeline

### Requirements

#### Application

Implement a simple application in either:

- Go
- Python

The application must expose the following endpoints:

##### `GET /health`

**Response:**

```json
{
    "status": "ok"
}
```

##### `GET /version`

**Response:**

```json
{
    "version": "1.0.0"
}
```

##### `GET /env`

**Response:**

```json
{
    "environment": "<value from ENVIRONMENT variable>"
}
```

##### `POST /config`

**Request:**

```json
{
    "name": "database_url",
    "value": "postgres://example"
}
```

**Response:**

```json
{
    "name": "database_url",
    "value": "postgres://example"
}
```

##### `GET /config/{name}`

**Example:**

```bash
GET /config/database_url
```

**Response:**

```json
{
    "name": "database_url",
    "value": "postgres://example"
}
```

##### `DELETE /config/{name}`

**Response:**

```json
{
    "deleted": true
}
```

#### Containerization

- Create the necessary Dockerfile with minimal setup
- The image should:
  - build successfully
  - run locally
  - expose the application endpoint

#### Terraform

- Review and fix/complete the Terraform code
- The Terraform code contains several issues and areas for improvement
- In case you don't get time to implement changes describe what would you still improve and why
- Document any changes you make

#### Helm

- Review and fix/complete the Helm Chart
- The chart should deploy the application to Kubernetes
- Document any change you make

#### Gitlab CI

- Complete the pipeline so it becomes capable of building and deploying the application
- The pipeline should support the workflow required to build and deploy the application
- The pipeline should be logically complete and demonstrate how you would automate the process
- Add any other necessary jobs to the pipeline

#### Documentation

Update the project README with following information.

##### What You Changed

Describe the changes and the rationale behind it.

##### Assumptions

Describe the assumptions made while completing the assignment.

##### Known Limitations

Describe anything you intentionally omitted.

##### Production Improvements

Describe how you would evolve this solution for production use.

### Deliverables

- Source Code of the Go/Python application
- Dockerfile
- Terraform changes
- Helm changes
- CI pipeline changes
- README describing decisions, assumptions and user guide for the project.

### Notes

You are not expected to deploy to a cloud provider.
The solution should work with a local Kubernetes cluster such as:

- Kind
- Minikube
- K3d

### Timing

Timebox yourself to approximately **3 hours**. If you can't finish the work within the timebox, describe in the README.md what is left and how you would approach it.

## Goal 2

You get this half-baked project from one of your colleagues who is a Junior and asking for your guidance.

Provide a short code review in `REVIEW.md` where you address the **top 5 most important things** to fix so the colleague can move forward.

### Review Timing

Spend no more than **30 minutes** on review and feedback.

### Evaluation Criteria

We will evaluate:

- Code quality
- Terraform quality
- Kubernetes and Helm knowledge
- CI/CD design and implementation
- Documentation quality
- Code review quality
- Maintainability and operational thinking

### Use of AI

The use of AI-assisted tools is permitted. However, we encourage you to complete the assignment primarily based on your own knowledge, experience and reasoning. During the interview, we will discuss your implementation choices, trade-offs and decision-making process, so it is important that you fully understand and can explain every part of your solution.

## What You Changed

### Application

I completed the FastAPI service in `app/main.py` so it matches the requested behavior:

- `GET /health` returns `{ "status": "ok" }`
- `GET /version` returns `{ "version": "1.0.0" }`
- `GET /env` reads the `ENVIRONMENT` variable and returns its value
- `POST /config` stores a config entry and returns it
- `GET /config/{name}` retrieves a stored config item
- `DELETE /config/{name}` deletes the item and returns `{ "deleted": true }`

I added some error handling for non-existent config cases, so the response is clear.

I also added requirements.txt for installing the dependencies.

### Docker

I added a minimal Dockerfile that:

- uses a slim Python 3.12 base image
- installs the app dependencies from `app/requirements.txt`
- copies the application source into the container
- exposes port 8080
- runs the app with Uvicorn

This was necessary so the service could be built and run locally as a container, satisfying the requirements.

Added docker ignore file so helm and terraform files aren't packaged up (although they aren't big in size now, they can slow things down).

### Helm chart

The chart in `helm/` was corrected so that it can deploy the app in a Kubernetes cluster.

The fixes were:
- deployment.yaml:
  - use the replicaCount value from values.yaml isntead of hardcoding
  - use IfNotPresent imagePullPolicy (so image doesn't get pulled each time)
  - use consistent container port
- ingress.yaml:
  - fix the service name (using "myapp")
- service.yaml:
  - align service selector (using "myapp")

### Terraform

The Terraform configuration in `terraform/` was improved to create a namespace and install the Helm release in a predictable way.

The changes were:

- main.tf:
  - replace kubernetes_namespace with kubernetes_namespace_v1 to remove deprication warning
  - fix chart path
  - set image.tag and environment values to the values contained in values.yaml
- outputs.tf:
  - added outputs (namespaces, vars)
- providers.tf:
  - add required providers (without fixed providers I had inconsistencies, e.g had to use set = [{...}, {...}] instead of set {...} )
- variables.tf:
  - added description and default values (not necessary, but helpful)
- terraform.tfvars:
  - added the file so terraform deployment uses the vars

For a minimal local setup, the current files are enough, but further improvements could include:
- adding extra settings such as `depends_on`, `wait`, and `timeout`
- separate environment files such as `dev.tfvars` and `prod.tfvars`
- splitting the namespace and Helm release into reusable modules
- keeping provider versions pinned more tightly in a shared environment
- using a `values` block in the Helm release for more complex configuration (instead of sets)
- adding validation checks to catch config issues early

### GitLab CI

The pipeline in `.gitlab-ci.yml` was completed to include a logical flow for:

- test execution
- image build and push
- Helm deployment to a target cluster

The pipeline currently demonstrates the expected CI/CD pattern for a small service while remaining lightweight enough for a local homework project.

A more complete pipeline could include linting, security checks, and separate environment jobs.

Added testing to see if app in itself is working before building and deploying it.

## Assumptions

- The project is intended as a local demo service rather than a full production platform.
- Configuration is stored in memory only, which is acceptable for the assignment and keeps the application simple.
- Before running Helm or Terraform, a local Kubernetes cluster such as Kind, Minikube, or k3d must already exist and the kube context must point to it.
- Docker registry credentials and cluster access are assumed to exist in a real CI environment for image push and deployment.
- The app is expected to be run in a minimal environment without external services such as a database or secret manager.

## Known Limitations

- Config data is not persistent and will be lost when the app restarts.
- The project does not include a database, external secret management, or persistent storage.
- The Kubernetes chart is intentionally lightweight and does not include advanced production features like autoscaling, TLS, or security policies.
- The deployment pipeline requires valid registry credentials and a reachable Kubernetes API server.
- Terraform is suitable for a local demo use case, not for a large multi-environment production deployment model.

## Production Improvements

If this solution were to evolve for production, the next improvements would be:

- persist configuration in a real backing store such as PostgreSQL or Redis
- add structured logging and request tracing
- add readiness/liveness probes in Kubernetes
- manage secrets via Kubernetes Secrets or an external secret manager
- split configuration for dev, test, and prod environments
- use immutable image tags and promotion between deployment stages
- add automated API tests and deployment smoke checks
- add rollback procedures and operational monitoring

## Local Usage

### Run the app locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
export ENVIRONMENT=dev
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Test the endpoints

```bash
curl http://localhost:8080/health
curl http://localhost:8080/version
curl http://localhost:8080/env
```

### Build and run with Docker

```bash
docker build -t myapp:latest .
docker run --rm -p 8080:8080 -e ENVIRONMENT=dev myapp:latest
```

### Deploy with Helm

```bash
helm upgrade --install myapp ./helm \
  --namespace homework \
  --create-namespace \
  --set image.repository=myapp \
  --set image.tag=latest \
  --set environment=dev
```

### Deploy with Terraform

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## Summary

This repository was intentionally incomplete at the start, but it has now been completed into a functional local demo covering the required Python app, Docker packaging, Kubernetes deployment, Terraform provisioning, and GitLab CI workflow. The implementation is intentionally lightweight, easy to follow, and suitable for a local cluster environment while still demonstrating the core DevOps practices expected by the assignment.

## Use of AI

AI was used during the project for debugging support, generating improvement ideas, and helping draft the documentation. The final version was then reviewed and adjusted manually to keep it accurate, realistic, and aligned with the actual repository state.
