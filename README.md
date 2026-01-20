## How to Run Tests

This framework supports local execution and CI-ready test runs for both UI and API automation. The steps below outline how to set up the environment and execute tests consistently.

### Prerequisites

- Python 3.10 or higher
- Git
- Playwright-supported browser dependencies

### Setup Instructions

1. Clone the repository:
   git clone https://github.com/wodud-khan/sdet-playwright-framework.git
   cd sdet-playwright-framework

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate

3. Install project dependencies:
   pip install -r requirements.txt

4. Install Playwright browsers:
   playwright install

### Running Tests Locally

- Run all tests:
  pytest

- Run UI tests only:
  pytest tests/ui

- Run API tests only:
  pytest tests/api

- Run tests in parallel:
  pytest -n auto

### Test Reporting

- Allure results are generated automatically during execution.
- To view the report locally:
  allure serve allure-results

### CI Execution

This repository includes CI configuration files (Dockerfile, Jenkinsfile, and Kubernetes job definitions) to enable automated execution in containerized and pipeline-based environments. These configurations demonstrate how the framework can be integrated into enterprise CI/CD workflows.

## Test Strategy & Coverage Overview

This framework is designed to demonstrate a balanced, risk-based testing strategy aligned with modern Quality Engineering principles. Test coverage is intentionally structured to validate critical system behavior across UI, API, and integration layers while maintaining execution efficiency and maintainability.

### Testing Philosophy

The test strategy prioritizes:
- Early validation at the API and contract level to reduce UI dependency
- Targeted UI automation focused on critical user workflows
- Clear separation between test intent, test data, and execution logic
- Deterministic, repeatable test execution suitable for CI environments

The goal is not exhaustive automation, but meaningful coverage that maximizes signal while minimizing maintenance overhead.

### UI Test Coverage

UI automation focuses on:
- Core user journeys and business-critical workflows
- High-risk functional paths where UI behavior impacts user outcomes
- Validation of navigation, form interactions, and end-to-end flows

UI tests are implemented using the Page Object Model (POM) to:
- Reduce duplication
- Improve readability
- Isolate selector changes from test logic

Visual styling, pixel-perfect validation, and non-critical UI elements are intentionally excluded to avoid brittle tests.

### API Test Coverage

API testing serves as the foundation of the framework and includes:
- Endpoint-level functional validation
- Request and response schema validation
- Negative-path and error-handling scenarios
- Data integrity and business rule enforcement

Reusable API clients and contract definitions are used to promote consistency and reduce duplication across tests.

### Integration & Contract Testing

Where applicable, integration-level tests validate:
- Interactions between dependent services
- Contract compatibility using JSON schema validation
- Controlled failure scenarios using mock services

This layer helps identify breaking changes early without requiring full end-to-end UI execution.

### Test Data Strategy

Test data is:
- Externalized from test logic
- Structured for clarity and reuse
- Designed to support positive, negative, and edge-case scenarios

This approach enables scalable test expansion without rewriting existing tests.

### Execution Scope & Non-Goals

The following are intentionally out of scope for this repository:
- Load and performance testing
- Cross-browser visual regression testing
- Accessibility audits beyond basic functional validation

These exclusions are deliberate to keep the framework focused on functional correctness, reliability, and maintainability.

### CI/CD Alignment

All tests are designed to be:
- Deterministic and environment-agnostic
- Executable in parallel
- Suitable for containerized and pipeline-based execution

This ensures the framework can scale from local development to enterprise CI/CD workflows.

## Folder Structure & Design Rationale

This repository follows a modular, scalable test automation architecture designed to support UI, API, and integration testing within a single framework. The structure emphasizes separation of concerns, maintainability, and ease of extension.

### Core Directories

- `pages/`  
  Implements the Page Object Model (POM) for UI automation using Playwright. Each page encapsulates selectors and behaviors to promote reuse and reduce test fragility.

- `tests/`  
  Contains all automated test cases, organized by test type:
  - `ui/` for end-to-end and functional UI tests
  - `api/` for API, contract, and schema validation tests
  - `data/` for structured test data inputs

- `api/`  
  Provides reusable API clients, endpoint definitions, request configurations, and response schemas to support robust backend testing and service-level validation.

- `utils/`  
  Shared utilities including logging, data factories, schema validation helpers, and failure intelligence to support consistent test behavior and diagnostics.

- `config/`  
  Centralized environment configuration and runtime settings, enabling clean separation between test logic and execution context.

- `contracts/`  
  JSON schema definitions used for contract and response validation to ensure backend compatibility and data integrity.

- `mock_services/`  
  Lightweight mock services used to simulate dependent systems during integration and negative-path testing.

- `observability/`  
  Metadata and hooks intended to support traceability, reporting enrichment, and future integration with monitoring or analytics systems.

- `ownership/`  
  Defines test ownership mappings to improve accountability and support triage workflows in team environments.

### Infrastructure & Execution

- `conftest.py`  
  Global Pytest fixtures and lifecycle hooks shared across UI and API tests.

- `pytest.ini`  
  Pytest configuration, markers, and execution defaults.

- `Dockerfile`  
  Enables containerized execution for local runs and CI pipelines.

- `Jenkinsfile`  
  Defines CI execution stages for automated test runs.

- `k8s/`  
  Kubernetes job configuration for running tests in containerized environments.

### Generated Artifacts

Execution artifacts such as logs, screenshots, videos, Allure results, virtual environments, and Python cache files are intentionally excluded from version control and generated dynamically during test execution.


## About the Author

I am a Quality Assurance Engineer with extensive experience spanning manual testing, test automation, and backend validation across business-critical software platforms. My professional background includes supporting web, mobile, API, and data-driven systems in healthcare, retail, and enterprise environments, with a consistent focus on reliability, scalability, and real-world usability.

My expertise covers the full software testing lifecycle, including test planning, functional and regression testing, API validation, database verification, defect lifecycle management, and release readiness support. I have hands-on experience designing and maintaining Python-based automation frameworks using tools such as Pytest, Selenium, and Playwright, as well as integrating automated tests into CI/CD pipelines using GitHub Actions and Jenkins.

In addition to traditional QA practices, I have worked extensively with backend systems, validating ETL workflows, business rules, and data integrity using SQL queries, log analysis, and API inspection. I am comfortable collaborating with developers, product owners, and business stakeholders in Agile and hybrid SDLC environments, and I place strong emphasis on clear documentation, reproducibility, and traceability.

I also bring experience in modern, AI-assisted and cloud-adjacent systems, including workflow automation, low-code platforms, and large-language-model–enabled solutions. This background has strengthened my ability to think beyond test execution and focus on system behavior, risk identification, and long-term maintainability.

This repository is maintained as a professional portfolio to demonstrate my approach to quality engineering, automation design, and practical problem-solving. It reflects how I structure test code, document assumptions, and apply industry best practices to deliver dependable, production-ready software.
