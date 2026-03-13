#!/usr/bin/env python3
"""Small Airflow API helper for common operations.

Run with uv:
    uv run python scripts/airflow_api.py --help
"""

from __future__ import annotations

import argparse
import base64
import getpass
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_BASE_URL = "https://airflow.windo.me/api/v1"


def build_auth_header(username: str | None, password: str | None) -> str | None:
    if not username:
        return None
    if password is None:
        password = ""
    token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def load_env_file(path: str) -> None:
    """Load KEY=VALUE pairs from .env-style files into process environment.

    Existing environment variables are preserved.
    """
    if not path or not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export ") :].strip()
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if not key:
                continue

            if len(value) >= 2 and (
                (value[0] == '"' and value[-1] == '"')
                or (value[0] == "'" and value[-1] == "'")
            ):
                value = value[1:-1]

            os.environ.setdefault(key, value)


def read_password_from_stdin() -> str:
    """Read password from stdin without trimming spaces."""
    data = sys.stdin.read()
    return data.rstrip("\r\n")


def request_json(
    method: str,
    base_url: str,
    path: str,
    auth_header: str | None,
    payload: dict[str, Any] | None = None,
    query: dict[str, str] | None = None,
) -> Any:
    url = base_url.rstrip("/") + path
    if query:
        url += "?" + urllib.parse.urlencode(query)

    headers = {"Accept": "application/json"}
    data: bytes | None = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if auth_header:
        headers["Authorization"] = auth_header

    req = urllib.request.Request(url=url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            if not body:
                return {}
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        msg = f"HTTP {exc.code} {exc.reason}: {body}"
        raise SystemExit(msg) from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Network error: {exc}") from exc


def cmd_health(args: argparse.Namespace, auth: str | None) -> int:
    result = request_json("GET", args.base_url, "/health", auth)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_version(args: argparse.Namespace, auth: str | None) -> int:
    result = request_json("GET", args.base_url, "/version", auth)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_list_dags(args: argparse.Namespace, auth: str | None) -> int:
    result = request_json(
        "GET",
        args.base_url,
        "/dags",
        auth,
        query={"limit": str(args.limit), "offset": str(args.offset)},
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_pause_dag(args: argparse.Namespace, auth: str | None) -> int:
    payload = {"is_paused": args.pause}
    result = request_json(
        "PATCH",
        args.base_url,
        f"/dags/{urllib.parse.quote(args.dag_id, safe='')}",
        auth,
        payload=payload,
        query={"update_mask": "is_paused"},
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def build_dag_run_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.run_id:
        payload["dag_run_id"] = args.run_id
    if args.logical_date:
        payload["logical_date"] = args.logical_date
    if args.note:
        payload["note"] = args.note
    if args.conf:
        try:
            payload["conf"] = json.loads(args.conf)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid --conf JSON: {exc}") from exc
    return payload


def cmd_list_dag_runs(args: argparse.Namespace, auth: str | None) -> int:
    query: dict[str, str] = {"limit": str(args.limit), "offset": str(args.offset)}
    if args.order_by:
        query["order_by"] = args.order_by

    result = request_json(
        "GET",
        args.base_url,
        f"/dags/{urllib.parse.quote(args.dag_id, safe='')}/dagRuns",
        auth,
        query=query,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_get_dag_run(args: argparse.Namespace, auth: str | None) -> int:
    path = (
        f"/dags/{urllib.parse.quote(args.dag_id, safe='')}"
        f"/dagRuns/{urllib.parse.quote(args.dag_run_id, safe='')}"
    )
    result = request_json("GET", args.base_url, path, auth)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_post_dag_run(args: argparse.Namespace, auth: str | None) -> int:
    payload = build_dag_run_payload(args)

    result = request_json(
        "POST",
        args.base_url,
        f"/dags/{urllib.parse.quote(args.dag_id, safe='')}/dagRuns",
        auth,
        payload=payload if payload else {},
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_trigger_dag(args: argparse.Namespace, auth: str | None) -> int:
    # Backward-compatible alias for post-dag-run.
    return cmd_post_dag_run(args, auth)


def cmd_list_task_instances(args: argparse.Namespace, auth: str | None) -> int:
    path = (
        f"/dags/{urllib.parse.quote(args.dag_id, safe='')}"
        f"/dagRuns/{urllib.parse.quote(args.dag_run_id, safe='')}/taskInstances"
    )
    result = request_json("GET", args.base_url, path, auth)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_get_variable(args: argparse.Namespace, auth: str | None) -> int:
    path = f"/variables/{urllib.parse.quote(args.key, safe='')}"
    result = request_json("GET", args.base_url, path, auth)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_set_variable(args: argparse.Namespace, auth: str | None) -> int:
    payload = {"key": args.key, "value": args.value}
    if args.description:
        payload["description"] = args.description
    if args.create:
        result = request_json("POST", args.base_url, "/variables", auth, payload=payload)
    else:
        path = f"/variables/{urllib.parse.quote(args.key, safe='')}"
        result = request_json("PATCH", args.base_url, path, auth, payload=payload)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Airflow API helper")
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to .env file (default: %(default)s). Use --env-file \"\" to disable.",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Airflow API base URL (overrides AIRFLOW_BASE_URL/.env)",
    )
    parser.add_argument(
        "--username",
        default=None,
        help="Airflow username (overrides AIRFLOW_USERNAME/.env)",
    )
    parser.add_argument(
        "--password",
        default=None,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--password-stdin",
        action="store_true",
        help="Read Airflow password from stdin (safer than passing via CLI argument)",
    )
    parser.add_argument(
        "--prompt-password",
        action="store_true",
        help="Prompt for Airflow password interactively",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    p_health = subparsers.add_parser("health", help="Get /health")
    p_health.set_defaults(func=cmd_health)

    p_version = subparsers.add_parser("version", help="Get /version")
    p_version.set_defaults(func=cmd_version)

    p_list_dags = subparsers.add_parser("list-dags", help="List DAGs")
    p_list_dags.add_argument("--limit", type=int, default=100)
    p_list_dags.add_argument("--offset", type=int, default=0)
    p_list_dags.set_defaults(func=cmd_list_dags)

    p_pause = subparsers.add_parser("pause-dag", help="Pause or unpause a DAG")
    p_pause.add_argument("dag_id")
    p_pause.add_argument(
        "--pause",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Set paused state (use --no-pause to unpause)",
    )
    p_pause.set_defaults(func=cmd_pause_dag)

    p_list_dag_runs = subparsers.add_parser("list-dag-runs", help="List DAG runs for a DAG")
    p_list_dag_runs.add_argument("dag_id")
    p_list_dag_runs.add_argument("--limit", type=int, default=100)
    p_list_dag_runs.add_argument("--offset", type=int, default=0)
    p_list_dag_runs.add_argument(
        "--order-by",
        help="Order by field, e.g. start_date or -start_date",
    )
    p_list_dag_runs.set_defaults(func=cmd_list_dag_runs)

    p_get_dag_run = subparsers.add_parser("get-dag-run", help="Get one DAG run")
    p_get_dag_run.add_argument("dag_id")
    p_get_dag_run.add_argument("dag_run_id")
    p_get_dag_run.set_defaults(func=cmd_get_dag_run)

    p_post = subparsers.add_parser("post-dag-run", help="Trigger a new DAG run")
    p_post.add_argument("dag_id")
    p_post.add_argument("--run-id")
    p_post.add_argument("--logical-date")
    p_post.add_argument("--note")
    p_post.add_argument(
        "--conf",
        help='JSON object string, e.g. \'{"k":"v"}\'',
    )
    p_post.set_defaults(func=cmd_post_dag_run)

    p_trigger = subparsers.add_parser("trigger-dag", help="Alias of post-dag-run")
    p_trigger.add_argument("dag_id")
    p_trigger.add_argument("--run-id")
    p_trigger.add_argument("--logical-date")
    p_trigger.add_argument("--note")
    p_trigger.add_argument(
        "--conf",
        help='JSON object string, e.g. \'{"k":"v"}\'',
    )
    p_trigger.set_defaults(func=cmd_trigger_dag)

    p_ti = subparsers.add_parser("list-task-instances", help="List task instances in DAG run")
    p_ti.add_argument("dag_id")
    p_ti.add_argument("dag_run_id")
    p_ti.set_defaults(func=cmd_list_task_instances)

    p_get_var = subparsers.add_parser("get-variable", help="Get a variable by key")
    p_get_var.add_argument("key")
    p_get_var.set_defaults(func=cmd_get_variable)

    p_set_var = subparsers.add_parser("set-variable", help="Create or patch a variable")
    p_set_var.add_argument("key")
    p_set_var.add_argument("value")
    p_set_var.add_argument("--description")
    p_set_var.add_argument(
        "--create",
        action="store_true",
        help="Use POST /variables (default is PATCH existing variable)",
    )
    p_set_var.set_defaults(func=cmd_set_variable)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.env_file:
        load_env_file(args.env_file)

    base_url = args.base_url or os.environ.get("AIRFLOW_BASE_URL") or DEFAULT_BASE_URL
    username = args.username or os.environ.get("AIRFLOW_USERNAME")
    password = os.environ.get("AIRFLOW_PASSWORD")
    if args.password:
        print(
            "Warning: --password is deprecated and insecure (leaks in history/process list). "
            "Use AIRFLOW_PASSWORD, --password-stdin, or --prompt-password.",
            file=sys.stderr,
        )
        password = args.password
    if args.password_stdin:
        if args.prompt_password:
            raise SystemExit("Use either --password-stdin or --prompt-password, not both.")
        password = read_password_from_stdin()
    elif args.prompt_password:
        password = getpass.getpass("Airflow password: ")

    args.base_url = base_url
    auth = build_auth_header(username, password)
    if not auth:
        print(
            "Warning: no username provided; requests may fail with 401 depending on server config.",
            file=sys.stderr,
        )
    return args.func(args, auth)


if __name__ == "__main__":
    raise SystemExit(main())
