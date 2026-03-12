---
name: airflow
description: Operate Apache Airflow through its stable REST API at https://airflow.windo.me/api/v1, including DAG discovery, pause/unpause, DAG run triggering, task instance inspection, logs, variables, connections, pools, and health/version checks. Use this skill when requests involve Airflow API calls, translating user intent to endpoints/methods/payloads, writing curl or Python API clients, or troubleshooting request/response errors against openapi.yaml/openapi.json.
---

# Airflow API

## Overview

Use this skill to map user goals to Airflow REST endpoints, build safe request plans, and produce working examples with correct URL, method, parameters, and payloads.
Default API base: `https://airflow.windo.me/api/v1`.

## Workflow

1. Confirm operation intent: read-only vs mutating action.
2. Resolve endpoint and method from [references/endpoint-playbook.md](references/endpoint-playbook.md).
3. Build URL using base `https://airflow.windo.me/api/v1`.
4. Add auth and headers:
   - `Authorization: Basic <base64(user:pass)>` when basic auth is used.
   - `Content-Type: application/json` for body requests.
5. Build minimal payload from [references/request-templates.md](references/request-templates.md), then adapt fields.
6. Execute safely:
   - Prefer GET checks before PATCH/POST/DELETE.
   - Surface deprecated endpoints and prefer newer alternatives.
7. Validate response and provide actionable next step.

## Authentication

- Prefer Basic auth when Airflow is configured with `airflow.api.auth.backend.basic_auth`.
- Keep secrets in environment variables; never hardcode credentials.
- If API returns `401` or `403`, verify auth backend, credentials, and role permissions.

## Safety Rules

- Always show full target URL before mutating calls.
- For pause/unpause and state changes, fetch current object first.
- For destructive actions (`DELETE`, clear task instances, state changes), require explicit user intent.
- Prefer non-deprecated endpoints; for role/user/permission APIs, use `/auth/fab/v1` instead of deprecated legacy endpoints.

## Quick Commands

- Health check:
  - `GET /health`
- Version check:
  - `GET /version`
- List DAGs:
  - `GET /dags?limit=100&offset=0`
- Pause/unpause DAG:
  - `PATCH /dags/{dag_id}?update_mask=is_paused` with `{"is_paused": true|false}`
- Trigger DAG run:
  - `POST /dags/{dag_id}/dagRuns`
- List task instances for a DAG run:
  - `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances`
- Variable CRUD:
  - `GET/POST /variables`, `GET/PATCH/DELETE /variables/{variable_key}`

## Python Usage (uv)

If Python is needed, run scripts with `uv`:

```bash
uv run python scripts/airflow_api.py --help
```

Use the helper script to avoid repeating auth/header/request plumbing.

## References

- Endpoint map: [references/endpoint-playbook.md](references/endpoint-playbook.md)
- Request body templates: [references/request-templates.md](references/request-templates.md)
- Python helper: [scripts/airflow_api.py](scripts/airflow_api.py)
