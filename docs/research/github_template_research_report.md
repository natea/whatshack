# GitHub Template Research Report: Township Connect

**Version:** 1.1
**Date:** May 17, 2025
**Author:** AI Assistant (Orchestrator GitHub Template Scout)

## 1. Introduction

This report details the research conducted to find suitable GitHub cookiecutter project templates to accelerate the development of the "Township Connect" project. The research was guided by the project's Master Project Plan ([`docs/project_plan.md`](docs/project_plan.md)), Master Acceptance Test Plan ([`tests/acceptance/master_acceptance_test_plan.md`](tests/acceptance/master_acceptance_test_plan.md)), Product Requirements Document ([`docs/prd.md`](docs/prd.md)), and associated strategic research documents.

The primary goal is to identify a template that aligns with the project's technical stack (Python core, Supabase/PostgreSQL, Redis, n8n, WhatsApp integration) and can provide a solid foundation for building the required features. This version of the report updates previous findings, leveraging the now-operational Firecrawl MCP server for comprehensive research.

## 2. Project Requirements Summary for Template Selection

Based on the project documentation, a suitable template should ideally offer:

*   **Primary Language:** Python.
*   **Framework:** A modern Python web framework (e.g., FastAPI, Flask) is suitable. The core logic will likely be invoked by n8n or run as background tasks.
*   **Database Integration:** Support for PostgreSQL (compatible with Supabase), including an ORM (e.g., SQLAlchemy, SQLModel) and migration tools (e.g., Alembic).
*   **Message Queue Integration:** Support for Redis (for caching and potentially Celery tasks).
*   **Task Queue (Optional but good):** Support for Celery (though n8n is primary orchestrator, Celery can be used for Python-specific async tasks).
*   **Modularity & Structure:** A clean, well-organized project structure that facilitates feature development, testing, and maintenance.
*   **Configuration Management:** Robust handling of environment variables and configurations.
*   **Testing:** Integrated testing framework (e.g., `pytest`).
*   **Containerization:** Docker and Docker Compose support.
*   **Dependency Management:** Modern tool like Poetry.

## 3. Search Strategy & Keywords

The Firecrawl MCP server was used for web searching and scraping of GitHub templates. The following refined search queries were used:

1.  `site:github.com python cookiecutter template fastapi postgresql redis`
2.  `site:github.com python cookiecutter template flask postgresql redis sqlalchemy`
3.  `site:github.com python project template fastapi sqlalchemy redis async`
4.  `site:github.com cookiecutter python backend supabase redis`
5.  `site:github.com python cookiecutter "project-template" fastapi postgresql redis`

The initial query `site:github.com python cookiecutter template fastapi postgresql redis` provided the most relevant starting points.

## 4. Considered Templates

Based on the research, the following templates were identified and evaluated:

1.  **`nickatnight/cookiecutter-fastapi-backend`**
    *   **URL:** [`https://github.com/nickatnight/cookiecutter-fastapi-backend`](https://github.com/nickatnight/cookiecutter-fastapi-backend)
    *   **Description:** Cookiecutter template for FastAPI backends. Includes Docker, SQLModel, Alembic, PostgreSQL, Redis, Celery, NGINX, Let's Encrypt, GitHub Actions for CI/CD, and pre-commit hooks.
    *   **Stars:** ~150
    *   **Activity:** Actively maintained, last relevant commit Dec 2024.

2.  **`s3rius/FastAPI-template`**
    *   **URL:** [`https://github.com/s3rius/FastAPI-template`](https://github.com/s3rius/FastAPI-template)
    *   **Description:** A highly configurable *generator* (installed via pip) for FastAPI projects. Supports various ORMs (SQLAlchemy 2.0, TortoiseORM, etc.), databases (PostgreSQL, MongoDB, etc.), Redis, RabbitMQ, GraphQL/REST, migrations, CI/CD, Kubernetes, Prometheus, Sentry.
    *   **Stars:** ~2.3k
    *   **Activity:** Very actively maintained, last commit Jan 2025.

3.  **`jonra1993/fastapi-alembic-sqlmodel-async`**
    *   **URL:** [`https://github.com/jonra1993/fastapi-alembic-sqlmodel-async`](https://github.com/jonra1993/fastapi-alembic-sqlmodel-async)
    *   **Description:** Project template (clonable base) using FastAPI, Pydantic 2.0, Alembic, and async SQLModel. Includes Celery (Redis broker, Postgres backend), JWT auth, RBAC, Docker, Caddy, Minio.
    *   **Stars:** ~1.1k
    *   **Activity:** Actively maintained, last commit Mar 2024.

4.  `tiangolo/full-stack-fastapi-postgresql`
    *   **URL:** [`https://github.com/tiangolo/full-stack-fastapi-postgresql`](https://github.com/tiangolo/full-stack-fastapi-postgresql)
    *   **Description:** Official FastAPI project generator. Very comprehensive, includes frontend options (Vue, React), OAuth2, Celery, etc.
    *   **Stars:** ~15.5k
    *   **Activity:** Actively maintained.
    *   *Note: While excellent, this might be overly complex for our primarily backend Python needs, as n8n and Node.js (Baileys) handle other aspects.*

Other templates were briefly reviewed but deemed less suitable due to lower feature alignment, fewer stars, or less recent activity.

## 5. Comparative Analysis

| Feature                 | `nickatnight/cookiecutter-fastapi-backend` | `s3rius/FastAPI-template` (Generator) | `jonra1993/fastapi-alembic-sqlmodel-async` | Township Connect Needs Met? |
| :---------------------- | :----------------------------------------- | :------------------------------------ | :----------------------------------------- | :-------------------------- |
| **Type**                | Cookiecutter Template                      | Project Generator (pip installable)   | Clonable Project Template                | Both approaches acceptable  |
| **FastAPI**             | Yes                                        | Yes                                   | Yes                                        | ✅                          |
| **PostgreSQL**          | Yes                                        | Yes (configurable)                    | Yes                                        | ✅                          |
| **ORM**                 | SQLModel                                   | SQLAlchemy 2.0, Tortoise, etc.        | Async SQLModel                             | ✅ (SQLModel/SQLAlchemy)    |
| **Migrations**          | Alembic                                    | Yes (ORM dependent, e.g. Alembic)     | Alembic                                    | ✅                          |
| **Redis**               | Yes                                        | Yes (optional)                        | Yes (for Celery broker)                    | ✅                          |
| **Celery**              | Yes (optional)                             | Yes (via RabbitMQ/Redis, Taskiq)      | Yes                                        | ✅ (Good to have)           |
| **Docker/Compose**      | Yes                                        | Yes                                   | Yes                                        | ✅                          |
| **Poetry**              | Yes                                        | Yes                                   | Yes                                        | ✅                          |
| **Testing (`pytest`)**  | Yes (implied, common for such templates)   | Yes (generated tests)                 | Yes (pytest, pytest-asyncio)               | ✅                          |
| **CI/CD**               | GitHub Actions                             | Yes (configurable)                    | GitHub Actions                             | ✅                          |
| **Async Focus**         | SQLModel supports async                    | Yes (configurable, ORM dependent)     | Strong (async SQLModel)                    | ✅                          |
| **Popularity (Stars)**  | ~150                                       | ~2.3k                                 | ~1.1k                                      | Higher is generally better  |
| **Maintenance**         | Good                                       | Excellent                             | Excellent                                  | ✅                          |
| **Ease of Use**         | Standard Cookiecutter                      | Run CLI tool, answer questions        | Clone and adapt                            | All manageable            |
| **Supabase Specifics**  | No direct Supabase utils                   | No direct Supabase utils              | No direct Supabase utils                   | (To be added)             |

**Key Considerations:**

*   **`nickatnight/cookiecutter-fastapi-backend`**: A solid, batteries-included cookiecutter. Good balance of features and direct usability. SQLModel is a good fit.
*   **`s3rius/FastAPI-template`**: Extremely flexible due to its generator nature. Can precisely tailor the project to include only what's needed (e.g., SQLAlchemy 2.0 for ORM, PostgreSQL, Redis). High popularity and excellent maintenance are big pluses. The TUI/CLI for generation is user-friendly.
*   **`jonra1993/fastapi-alembic-sqlmodel-async`**: Very strong async focus with SQLModel. Also includes Minio which isn't a primary requirement but could be useful later. It's a direct template to clone and modify.

## 6. Rationale for Final Decision

After reviewing the features and considering the project's needs, the **`s3rius/FastAPI-template` generator** emerges as the most promising option.

**Rationale:**

1.  **High Configurability:** The generator approach allows us to select precisely the components we need (FastAPI, SQLAlchemy 2.0 for ORM, PostgreSQL, Redis, Alembic, Poetry, Docker, `pytest`) and omit what we don't, leading to a cleaner starting point. This aligns well with the PRD and Project Plan which call for specific technologies.
2.  **Modern Stack:** Support for SQLAlchemy 2.0 and Pydantic V2 ensures we are using up-to-date libraries.
3.  **Excellent Maintenance & Popularity:** High star count and frequent updates indicate a reliable and well-supported tool.
4.  **Comprehensive Features:** It covers all core technical requirements identified for the Python backend.
5.  **Structured Output:** The generator is designed to produce a well-structured project, which is a key requirement.

While `nickatnight/cookiecutter-fastapi-backend` and `jonra1993/fastapi-alembic-sqlmodel-async` are excellent templates, the generator nature of `s3rius/FastAPI-template` offers a slight edge in tailoring the initial setup perfectly to our needs, potentially reducing the amount of initial modification required.

**Decision:** Proceed with evaluating the integration of a project generated by **`s3rius/FastAPI-template`**.

The confidence level is high (around 80-85%) that a project generated by this tool will significantly accelerate development and align well with the project's core needs.

## 7. Required Modifications (If Template Selected)

Assuming we generate a project using `s3rius/FastAPI-template` with selections for FastAPI, SQLAlchemy 2.0, PostgreSQL, Redis, Alembic, Poetry, Docker, and `pytest`:

1.  **Supabase Integration:**
    *   Modify database connection settings to use Supabase connection strings and service keys (from environment variables).
    *   Ensure the generated SQLAlchemy models and Alembic migrations are compatible with Supabase's PostgreSQL.
    *   Add Supabase Python client (`supabase-py`) if direct interaction beyond ORM is needed (e.g., for auth helpers or specific Supabase features not covered by standard PostgreSQL).
    *   Implement RLS (Row-Level Security) policies in Supabase and ensure the application code respects/utilizes them. The template might provide basic user models, which will need to be adapted or extended to match `users` table schema in `docs/project_plan.md` (MT1.2).
2.  **Project Structure Alignment:**
    *   Review the generated project structure and adjust if necessary to fit any overarching project conventions (though good templates usually follow best practices).
    *   Organize API routers and service logic according to the features outlined in the Township Connect project plan.
3.  **n8n Interaction Points:**
    *   Define clear API endpoints or callable Python functions/modules that n8n workflows will trigger for core business logic.
4.  **Specific Business Logic Implementation:**
    *   The template provides the *framework*. All specific business logic for Township Connect (user management, POPIA flows, service bundle selection, payment link generation via n8n, sales/expense logging, Q&A, etc.) will need to be implemented within this framework.
5.  **Content Management:**
    *   Integrate the planned `content/` directory structure for multilingual messages and static Q&A/guides.
6.  **Testing:**
    *   Adapt and expand generated `pytest` tests to cover all specific Township Connect features and acceptance criteria.
7.  **Configuration:**
    *   Ensure all sensitive configurations (API keys, Supabase details, Redis URL) are handled via environment variables as per best practices.
8.  **WhatsApp Specifics:**
    *   Since the Python core is likely invoked by n8n (which connects to the WhatsApp gateway), the Python template itself won't directly handle WhatsApp protocol specifics. However, data models for messages and users will need to align with WhatsApp data structures.

The `s3rius/FastAPI-template` generator itself is not a "cookiecutter" in the traditional sense (it's a pip-installable tool that generates a project), but its output will be the "template" we integrate.