# Published Skills

Every child directory is a complete, independently installable skill package.

| Skill | Best first use |
|---|---|
| `project-flow-router` | the next useful workflow is unclear |
| `project-start` | project context is missing or stale |
| `agent-setup` | coding-agent repository rules are missing or stale |
| `incident-triage` | an important failure spans unknown layers |
| `understand-before-approve` | a consequential decision needs a comprehension gate |

Install all skills:

```bash
python3 scripts/install_skills.py --target codex --all
```

Run that command from the repository root. See [Getting Started](../docs/getting-started.md) for other hosts and selective installation.

Do not symlink personal installed skills into this directory. Public packages must be sanitized, validated distribution copies.
