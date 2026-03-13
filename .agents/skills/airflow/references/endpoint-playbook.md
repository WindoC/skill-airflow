# Endpoint Playbook

## Base URL and auth

- Base URL: `https://airflow.windo.me/api/v1`
- OpenAPI source: repository `openapi.yaml` and `openapi.json`
- Security schemes in spec: `Basic`, `GoogleOpenId`, `Kerberos`
- Most operational examples in the spec use Basic auth.

## Monitoring

- `GET /health` -> instance health
- `GET /version` -> Airflow version metadata

## DAGs

- `GET /dags` -> list DAGs (supports pagination and filters)
- `PATCH /dags` -> patch multiple DAGs
- `GET /dags/{dag_id}` -> basic DAG info
- `GET /dags/{dag_id}/details` -> full DAG details
- `PATCH /dags/{dag_id}` -> patch DAG fields (for example, `is_paused`)
- `GET /dags/{dag_id}/tasks` -> list tasks in DAG
- `GET /dags/{dag_id}/tasks/{task_id}` -> task details

## DAG runs

- `GET /dags/{dag_id}/dagRuns` -> list DAG runs
- `POST /dags/{dag_id}/dagRuns` -> trigger DAG run
- `GET /dags/{dag_id}/dagRuns/{dag_run_id}` -> get one DAG run
- `PATCH /dags/{dag_id}/dagRuns/{dag_run_id}` -> update DAG run
- `POST /dags/{dag_id}/dagRuns/{dag_run_id}/clear` -> clear in a DAG run
- `PATCH /dags/{dag_id}/dagRuns/{dag_run_id}/setNote` -> set DAG run note
- Batch:
  - `POST /dags/~/dagRuns/list` -> batch list DAG runs

## Task instances

- `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances`
- `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}`
- `PATCH /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}`
- `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/{task_try_number}`
- `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries`
- Batch:
  - `POST /dags/~/dagRuns/~/taskInstances/list`

## Variables

- `GET /variables`
- `POST /variables`
- `GET /variables/{variable_key}`
- `PATCH /variables/{variable_key}`
- `DELETE /variables/{variable_key}`

## Connections and pools

- Connections:
  - `GET/POST /connections`
  - `GET/PATCH/DELETE /connections/{connection_id}`
  - `POST /connections/test`
- Pools:
  - `GET/POST /pools`
  - `GET/PATCH/DELETE /pools/{pool_name}`

## Datasets and events

- `GET /datasets`
- `GET /datasets/events`
- `GET /datasets/queuedEvent/{uri}`
- `GET /dags/{dag_id}/upstreamDatasetEvents`

## Deprecated groups

Prefer `/auth/fab/v1` equivalents instead of deprecated legacy endpoints:

- `/permissions`
- `/roles` and `/roles/{role_name}`
- `/users` and `/users/{username}`
