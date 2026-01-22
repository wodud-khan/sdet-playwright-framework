# 🎭 SDET Playwright Framework

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Automation-green?style=for-the-badge&logo=playwright&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Framework-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)

A modular, scalable test automation architecture designed to support **UI, API, and Integration testing** within a single framework. This repository demonstrates a production-style quality engineering system reflecting real-world enterprise constraints, including scalability, maintainability, and CI/CD readiness.

---

## ⚡ Quick Start (5 Minutes)

This section provides the fastest path to clone the repository, install dependencies, and execute a sample test suite.

```bash
# 1. Clone the repository
git clone [https://github.com/wodud-khan/sdet-playwright-framework.git](https://github.com/wodud-khan/sdet-playwright-framework.git)
cd sdet-playwright-framework

# 2. Set up Virtual Environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install Dependencies
pip install -r requirements.txt
playwright install

**Start the Mock Service (Terminal 1)**
uvicorn mock_services.auth_service.main:app --port 8001

**Run API Tests (Terminal 2)**
pytest tests/api
```

## Project Structure

```bash
sdet-playwright-framework/
│
├── api/                    # API client, endpoints, schemas, and configurations
│   ├── client/
│   ├── config/
│   ├── endpoints/
│   └── schemas/
│
├── pages/                 # Playwright Page Object Model (POM) implementation
│
├── tests/
│   ├── api/               # API test suites (auth, users, orders, integration)
│   ├── ui/                # UI end-to-end and regression tests
│   └── data/              # Test data management
│
├── utils/                 # Shared utilities, helpers, logging, schema validation
│
├── mock_services/         # Local mock API services for test isolation
│
├── config/                # Environment & framework configuration
│
├── contracts/             # API contract validation schemas
│
├── observability/         # Logging, metrics, and failure intelligence
│
├── artifacts/             # Screenshots and video recordings from test execution
│
├── k8s/                   # Kubernetes test job manifests
│
├── ownership/             # Test ownership and responsibility mapping
│
├── Dockerfile             # Containerized execution support
├── Jenkinsfile            # CI pipeline automation
├── pytest.ini             # Pytest execution configuration
├── requirements.txt       # Python dependency definitions
└── README.md              # Project documentation
```

## How to Run Tests

This framework supports local execution and CI-ready test runs for both UI and API automation. The steps below outline how to set up the environment and execute tests consistently.

### Prerequisites

To run this framework locally, ensure the following prerequisites are installed and available on your system:

- Python 3.10 or higher  
  Required for running Pytest, Playwright automation, and supporting utilities.

- Git  
  Used to clone the repository and manage version control.

- Playwright-supported browser dependencies  
  Required for executing UI tests across Chromium, Firefox, and WebKit. These dependencies are installed automatically during Playwright setup.

- Virtual environment support (recommended)  
  Using `venv` or a similar tool is recommended to isolate project dependencies and avoid conflicts.

- Uvicorn  
  Required to run the local mock API service used by API test suites.

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

### Start Local Mock API Service (Required for API Tests)

Some API test suites in this framework rely on a locally running mock authentication service to simulate backend dependencies. This service is implemented using FastAPI and served via Uvicorn.

Before running API tests, start the mock service in a separate terminal session:

uvicorn mock_services.auth_service.main:app --port 8001

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

## Framework Capabilities & Key Design Decisions

This framework is intentionally designed as a production-style quality engineering system rather than a simple test automation project. Architectural and tooling decisions reflect real-world enterprise constraints, including scalability, maintainability, and CI/CD readiness.

### Core Capabilities

The framework supports:

- **Multi-layer testing**
  - UI automation with Playwright
  - API automation with Pytest
  - Integration and contract validation
  - Data-driven testing patterns

- **Modular architecture**
  - Clear separation between test logic, test data, and execution layers
  - Reusable components for API clients, page objects, and utilities
  - Centralized configuration management

- **CI/CD readiness**
  - Headless execution support
  - Parallel test execution
  - Containerized execution capability
  - Pipeline-compatible reporting and logging

- **Observability and diagnostics**
  - Centralized logging
  - Failure traceability
  - Artifact generation (screenshots, logs, reports)
  - Structured test outputs for debugging and triage

### Key Design Decisions

#### Pytest as the Core Test Runner

Pytest was selected due to:
- Mature fixture model
- Plugin ecosystem
- Native parallel execution support
- Strong CI/CD compatibility
- Readable test structure

This enables scalable test growth without increasing framework complexity.

#### Playwright for UI Automation

Playwright is used for UI testing because of:
- Modern browser automation architecture
- Reliable synchronization and waiting mechanisms
- Native headless execution
- Strong CI stability
- Cross-browser support readiness

This ensures UI automation is stable, fast, and pipeline-friendly.

#### Page Object Model (POM)

The Page Object Model is implemented to:
- Encapsulate UI behavior
- Reduce selector duplication
- Improve test readability
- Isolate UI changes from test logic

This design significantly reduces maintenance costs as the application evolves.

#### API-First Validation Strategy

The framework emphasizes API testing before UI testing to:
- Detect defects earlier in the lifecycle
- Reduce test execution time
- Improve failure isolation
- Increase test reliability

This mirrors enterprise testing pyramids used in production systems.

#### Externalized Configuration

Environment-specific values are:
- Centralized
- Externalized from test logic
- Configurable per environment
- CI/CD injectable

This enables seamless execution across local, staging, and pipeline environments.

#### Contract and Schema Validation

JSON schema validation is used to:
- Enforce backend compatibility
- Detect breaking API changes
- Protect dependent systems
- Support backward compatibility testing

This supports long-term system stability and integration confidence.

#### Logging and Diagnostics Strategy

The logging architecture is designed to:
- Capture both UI and API execution flows
- Support parallel test execution
- Enable failure root-cause analysis
- Integrate with CI/CD artifacts

This ensures failures are diagnosable without rerunning tests.

#### Scalability Considerations

The framework is structured to support:
- Test suite growth
- Team collaboration
- Service expansion
- Multi-project reuse
- Enterprise governance models

This makes the framework suitable not only for portfolio demonstration, but also for real organizational adoption.

### Design Philosophy

All design choices follow three guiding principles:

1. **Maintainability over cleverness**  
2. **Reliability over speed**  
3. **Clarity over abstraction**

This ensures the framework remains understandable, extensible, and sustainable as complexity increases.

## Reporting, Logging & Observability

This framework incorporates a structured observability strategy to ensure that test execution results are transparent, diagnosable, and actionable in both local and CI/CD environments. The design emphasizes reproducibility, failure traceability, and minimal reliance on manual reruns.

### Reporting Strategy

The framework is designed to support rich, pipeline-friendly test reporting with the following objectives:

- Clear visibility into test outcomes
- Actionable failure insights
- Easy consumption by engineers and reviewers
- Compatibility with CI/CD artifact storage

Key reporting characteristics include:

- Structured test execution summaries
- Separation of passed, failed, and skipped tests
- Support for historical trend analysis when integrated with CI tools
- Artifact linkage for failures (logs, screenshots, traces)

The reporting approach is intentionally decoupled from test logic, allowing reporting tools to be swapped or extended without impacting test code.

### Logging Architecture

Logging is treated as a first-class component of the framework rather than an afterthought. The logging design supports both UI and API test execution flows.

Logging capabilities include:

- Centralized logging utilities shared across test layers
- Consistent log formatting for readability and parsing
- Timestamped entries for execution traceability
- Log-level separation (INFO, DEBUG, ERROR)
- Context-rich messages tied to test execution steps

Logs are designed to answer the following questions during failure analysis:
- What action was performed?
- Against which system or endpoint?
- With what input data?
- What response or behavior was observed?

This approach significantly reduces investigation time and supports asynchronous debugging in CI pipelines.

### UI Observability

For UI test execution, the framework supports automatic artifact generation to aid visual diagnosis:

- Screenshots captured on failure
- Browser traces (when enabled)
- Execution metadata associated with test cases

These artifacts provide immediate insight into application state at the time of failure and reduce reliance on manual reproduction.

### API Observability

For API test execution, observability focuses on request and response transparency:

- Request method, endpoint, and payload logging
- Response status codes and body validation summaries
- Schema validation results
- Error response diagnostics

This enables precise identification of backend failures and contract violations.

### CI/CD Artifact Management

The framework is designed so that all relevant execution artifacts can be:

- Generated dynamically during test runs
- Persisted as CI/CD pipeline artifacts
- Reviewed post-execution without rerunning tests

Typical artifacts include:
- Test execution reports
- Logs
- Screenshots
- Trace files
- Failure metadata

This design aligns with enterprise pipeline standards and supports remote review by distributed teams.

### Observability Extensibility

The observability layer is intentionally extensible to support future enhancements such as:

- Advanced reporting tools (e.g., Allure)
- Centralized log aggregation platforms
- Metrics dashboards
- Test execution analytics
- Failure pattern analysis

This ensures the framework can evolve alongside organizational maturity without requiring architectural rework.

### Design Rationale

The reporting and logging strategy follows three guiding principles:

1. **Failures should be diagnosable without reruns**
2. **Artifacts should explain behavior, not just outcomes**
3. **Observability should scale with test execution**

These principles ensure that automated tests provide meaningful feedback rather than opaque pass/fail signals.

## Roadmap & Extensibility

This framework is intentionally designed as a living system rather than a static automation project. The architecture supports incremental evolution as application complexity, team size, and testing maturity increase.

The roadmap outlined below reflects realistic, enterprise-aligned enhancements that can be introduced without disrupting existing test suites or execution pipelines.

### Planned Enhancements

The following capabilities are natural extensions of the current framework design:

- Advanced reporting integration to provide richer visualization, historical trends, and failure analytics
- Parallelized test execution strategies to reduce feedback cycle time at scale
- Expanded contract testing coverage for service-to-service validation
- Enhanced test data management strategies to support complex scenarios and stateful workflows
- Improved test environment orchestration for multi-service and cloud-based systems

These enhancements are intentionally staged to ensure stability and maintainability remain primary concerns.

### Scalability Considerations

The framework is built to scale along multiple dimensions:

- **Test volume:** Modular structure supports growth in test coverage without code duplication
- **Execution environments:** Local, containerized, and CI-based execution paths are first-class citizens
- **Team collaboration:** Clear ownership, documentation, and conventions support multi-contributor workflows
- **Technology evolution:** Tooling and integrations can be replaced or upgraded with minimal refactoring

This scalability focus ensures the framework remains viable as organizational needs evolve.

### Extensibility by Design

Key architectural decisions were made to support extensibility:

- Decoupling test logic from configuration and execution context
- Centralized utilities to avoid cross-cutting concerns leaking into test cases
- Clear separation between UI, API, and integration testing layers
- Explicit contracts and schemas to reduce brittle test dependencies

As a result, new test types, tools, or execution strategies can be introduced without rewriting existing tests.

### Quality Engineering Maturity

Beyond automation, the framework is designed to support broader quality engineering practices, including:

- Risk-based testing strategies
- Incremental automation coverage aligned with business impact
- Feedback-driven improvements based on failure analysis
- Alignment with release readiness and deployment confidence

This positions the framework not just as a test suite, but as a quality enablement platform.

### Long-Term Vision

The long-term vision for this framework is to serve as:

- A reusable foundation for multiple projects
- A reference implementation for enterprise-grade test automation
- A demonstration of pragmatic, maintainable quality engineering practices

The emphasis remains on delivering meaningful feedback, reducing operational friction, and enabling confident software delivery at scale.

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
