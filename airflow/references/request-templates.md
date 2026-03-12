# Request Templates

## Headers

```http
Authorization: Basic <base64(username:password)>
Content-Type: application/json
Accept: application/json
```

## Pause or unpause a DAG

Endpoint: `PATCH /dags/{dag_id}?update_mask=is_paused`

```json
{
  "is_paused": true
}
```

## Trigger DAG run

Endpoint: `POST /dags/{dag_id}/dagRuns`

```json
{
  "dag_run_id": "manual__2026-03-11T12:00:00Z",
  "logical_date": "2026-03-11T12:00:00Z",
  "conf": {
    "source": "api",
    "note": "manual trigger"
  },
  "note": "Triggered from API"
}
```

## Patch DAG run note

Endpoint: `PATCH /dags/{dag_id}/dagRuns/{dag_run_id}/setNote`

```json
{
  "note": "Re-run after upstream data fix"
}
```

## Update task instance state/note

Endpoint: `PATCH /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}`

```json
{
  "new_state": "success",
  "note": "State adjusted by operator"
}
```

## Create variable

Endpoint: `POST /variables`

```json
{
  "key": "example_key",
  "value": "example_value",
  "description": "Created by API"
}
```

## Patch variable

Endpoint: `PATCH /variables/{variable_key}`

```json
{
  "key": "example_key",
  "value": "new_value",
  "description": "Updated by API"
}
```

## Create connection

Endpoint: `POST /connections`

```json
{
  "connection_id": "my_postgres",
  "conn_type": "postgres",
  "host": "postgres.example.internal",
  "port": 5432,
  "login": "airflow",
  "password": "REDACTED",
  "schema": "analytics",
  "description": "Main warehouse connection"
}
```

## Create pool

Endpoint: `POST /pools`

```json
{
  "name": "etl_pool",
  "slots": 16,
  "description": "Shared ETL pool",
  "include_deferred": false
}
```
