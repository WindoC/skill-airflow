# AGENTS Memory

## Project Identity

- Project: `skill-airflow`
- Skill folder: `.agents/skills/airflow/`
- Skill name in frontmatter: `airflow`
- Target API base: `https://airflow.windo.me/api/v1`

## Working Rules

- Prefer deriving API behavior from `openapi.yaml` and `openapi.json`.
- Keep `.agents/skills/airflow/SKILL.md` concise and operational.
- Keep endpoint specifics in `.agents/skills/airflow/references/`.
- If Python is required, use `uv` to run scripts and tools.

## Common Commands

```bash
uv run python .agents/skills/airflow/scripts/airflow_api.py --help
uv run --with pyyaml python C:/Users/antonio/.codex/skills/.system/skill-creator/scripts/quick_validate.py airflow
```

## Update Checklist

1. Update references and templates when API endpoints or schemas change.
2. Keep `.agents/skills/airflow/agents/openai.yaml` aligned with `.agents/skills/airflow/SKILL.md`.
3. Re-run skill validation after edits.
