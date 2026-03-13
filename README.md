# skill-airflow

Codex skill project for operating Apache Airflow through the Stable REST API.

## Scope

- Airflow skill name: `airflow`
- API base: `https://airflow.windo.me/api/v1`
- Source specs: `openapi.yaml`, `openapi.json`

## Authentication

The OpenAPI spec defines these security schemes:

- `Basic` (`type: http`, `scheme: basic`)
- `GoogleOpenId` (`type: openIdConnect`)
- `Kerberos` (`type: http`, `scheme: negotiate`)

Important: Airflow authentication is backend-dependent at runtime. The spec lists available schemes, but the active auth method on your server (`https://airflow.windo.me`) depends on Airflow configuration.

Current helper script support:

- `.agents/skills/airflow/scripts/airflow_api.py` supports **Basic Auth**.
- Provide credentials using:
  - `AIRFLOW_USERNAME` and `AIRFLOW_PASSWORD` environment variables, or
  - `--username` with one of:
    - `--prompt-password`
    - `--password-stdin`
- `.env` file support is built in (default path: `.env`).
- Avoid `--password` on CLI because it can leak via shell history/process list.

Example:

```bash
$env:AIRFLOW_USERNAME="your_user"
$env:AIRFLOW_PASSWORD="your_pass"
uv run python .agents/skills/airflow/scripts/airflow_api.py health
```

Interactive prompt example:

```bash
uv run python .agents/skills/airflow/scripts/airflow_api.py --username your_user --prompt-password health
```

Stdin example:

```bash
"your_pass" | uv run python .agents/skills/airflow/scripts/airflow_api.py --username your_user --password-stdin health
```

`.env` example (project root):

```env
AIRFLOW_BASE_URL=https://airflow.windo.me/api/v1
AIRFLOW_USERNAME=your_user
AIRFLOW_PASSWORD=your_pass
```

Then run:

```bash
uv run python .agents/skills/airflow/scripts/airflow_api.py health
```

Optional overrides:

- `--env-file path/to/file.env` to use another file
- `--env-file ""` to disable `.env` loading
- CLI flags still take precedence over `.env`

## Repository Layout

- `.agents/skills/airflow/SKILL.md`: Skill instructions and workflow
- `.agents/skills/airflow/agents/openai.yaml`: UI metadata and default prompt
- `.agents/skills/airflow/references/`: Endpoint and request templates
- `.agents/skills/airflow/scripts/airflow_api.py`: Python helper CLI

## Python / uv

Use `uv` for Python execution and dependency resolution.

```bash
uv run python .agents/skills/airflow/scripts/airflow_api.py --help
```

Example validation:

```bash
uv run --with pyyaml python C:/Users/antonio/.codex/skills/.system/skill-creator/scripts/quick_validate.py airflow
```

## Pre-commit Secret Scan

Install and enable pre-commit hooks:

```bash
uvx pre-commit install
```

Run hooks on all files:

```bash
uvx pre-commit run --all-files
```

## Quick Start

1. Review API docs in `openapi.yaml` and `openapi.json`.
2. Update skill content under `.agents/skills/airflow/` if the API changes.
3. Validate the skill using `quick_validate.py`.

## DAG Run Commands

- List DAG runs:
  - `uv run python .agents/skills/airflow/scripts/airflow_api.py list-dag-runs <dag_id> --limit 20 --offset 0`
- Get one DAG run:
  - `uv run python .agents/skills/airflow/scripts/airflow_api.py get-dag-run <dag_id> <dag_run_id>`
- Trigger a new DAG run (POST):
  - `uv run python .agents/skills/airflow/scripts/airflow_api.py post-dag-run <dag_id> --run-id manual__2026-03-11T10:00:00Z --conf '{"source":"cli"}'`

Backward-compatible alias:

- `trigger-dag` is still supported and maps to `post-dag-run`.
