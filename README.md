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
