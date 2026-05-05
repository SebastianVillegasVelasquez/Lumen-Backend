# Lumen Learning Management System (LMS) & AI Service

## Introduction
This project is a specialized educational platform developed for **Fontur** (Fondo Nacional de Turismo de Colombia). The system is designed to manage and deliver tourism-related training through a modern, scalable architecture. It features a bilingual learning environment (English and Spanish) and integrates Local Large Language Models (LLM) to provide intelligent feedback and automated content processing.

The core mission of this platform is to professionalize the Colombian tourism sector by providing structured learning paths, SCORM-compliant content tracking, and AI-driven pedagogical support.

## Getting Started: Installation & Setup

This project uses **Poetry** for dependency management and virtual environment handling. Follow these steps to set up your local development environment.

### 1. Prerequisites
Ensure you have the following installed:
* **Python 3.13+**
* **PostgreSQL** (Active service and a database named `fontur` created)
* **Poetry** (If not installed: `pip install poetry`)

### 2. Environment Setup
Clone the repository and navigate to the project root. Then, install the dependencies:

```bash
# Install all required packages and create a virtual environment
poetry install
```

### 3.Activating the Virtual Environment
To run commands within the project's isolated environment, you can either prefix commands with poetry run or activate the shell:

```bash
# Option A: Enter the virtual environment shell
poetry shell

# Option B: Run a command without entering the shell
poetry run uvicorn src.main:src --reload
```

### 4. Configuration
Create a `.env` file in the root directory based on the `.env.example` provided. Ensure your DATABASE_URL is correctly configured to allow Alembic and FastAPI to connect to your local PostgreSQL instance.

## Core Technologies
The project leverages a high-performance Python-based stack:

* **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous, high-performance web framework).
* **Database:** [PostgreSQL](https://www.postgresql.org/) (Advanced relational database).
* **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Modern Pythonic SQL toolkit with static typing support).
* **Database Migrations:** [Alembic](https://alembic.sqlalchemy.org/) (Lightweight database migration tool).
* **AI Inference:** [vLLM](https://github.com/vllm-project/vllm) (High-throughput serving for LLMs, optimized for NVIDIA RTX 5080).
* **Dependency Management:** [Poetry](https://python-poetry.org/) (Python packaging and dependency management made easy).

## Project Methodology
We follow **Clean Architecture** principles and a **Schema-First** database design. All database changes are version-controlled via migrations to ensure consistency across development, staging, and production environments.

---

## Database Migration Guide

The database schema and initial data are managed through Alembic. All history is stored in the `migrations/versions/` directory and version-controlled via Git.

### 1. Synchronizing Your Local Database
If you are setting up the project for the first time or after a git pull, you must synchronize your local PostgreSQL instance with the current project state:

```bash
# Apply all existing migrations to reach the latest version (HEAD)
alembic upgrade head
```
_This command will build the entire schema and populate initial seed data (Levels and Components) automatically._

## 2. Making New Structural Changes (Schema)
If you modify the models in app/models/, you need to generate a new structural migration:
## Alembic Workflow

### 1. Detection
Alembic compares your Python classes with the database.

```bash
alembic revision --autogenerate -m "describe_your_changes"
```

### 2. Review
Always check the generated file in `migrations/versions/` to ensure the changes are correct.

### 3. Execution
Apply the changes to your local database.

```bash
alembic upgrade head
```

---

# 3. Manual Data Seeding (Initial Content)

For inserting or updating static data (like new course categories or levels) without changing the table structure:

## Create an empty migration

```bash
alembic revision -m "seed_new_manual_data"
```

## Implement the seed

Open the new file in `migrations/versions/` and use `op.bulk_insert()`.

### Example

```bash
def upgrade():
    # Define table reference
    my_table = table('my_table_name', column('id', Integer), column('name', String))
    
    # Insert data
    op.bulk_insert(my_table, [{'id': 1, 'name': 'New Category'}])
```

## Apply
Run the following command to apply the data:

```bash
alembic upgrade head
```

---

# 4. Versioning Workflow

To maintain consistency across all environments (Development, Staging, Production), follow this Git workflow:

- **Commit Migration Files**: Always include the new files generated in `migrations/versions/` in your commits.  
- **Avoid Deletions**: Never delete migration files that have already been pushed to the main repository; use a new migration to "undo" changes if necessary.  
- **Shared History**: By versioning these files, any developer can replicate the exact database state by simply running the upgrade command.