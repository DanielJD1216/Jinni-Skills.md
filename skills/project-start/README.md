# Project Start

`project-start` creates or refreshes durable project memory for AI-assisted software work. It captures product intent, architecture, UI rules, code standards, workflow rules, current progress, and first-debug procedures from repository evidence and explicit decisions.

## Use It For

- a new repository that needs durable project context;
- an inherited or messy codebase whose current state is unclear;
- missing or stale context files;
- a missing operational diagnostic runbook;
- resuming a build when decisions and current progress are scattered.

Do not use it for a narrow code fix, routine documentation synchronization, or a repository whose accepted context is already current.

## Pair It With Agent Setup

`project-start` owns what is true about the project. `agent-setup` owns how coding agents should operate in the repository.

Run `project-start` first when project memory is missing or stale. Run `agent-setup` after that context is accepted. The optional `--entry` flag creates only a minimal pointer entrypoint and defaults to `none`. Do not use it unless the current request explicitly asks for an entrypoint.

## Install

Place the `project-start` directory in the skill directory used by your coding assistant.

- Codex: `~/.codex/skills/project-start/`
- Claude Code: `~/.claude/skills/project-start/`
- Other Agent Skills compatible tools: use the documented user or project skill directory.

Keep the directory name and the `name` field in `SKILL.md` as `project-start`.

## Scaffold

Run from the installed skill directory:

```bash
python3 scripts/scaffold_six_file_context.py /path/to/project
```

The script skips existing files by default. `--force` is required to overwrite, and should be used only with explicit approval. Context destinations must stay inside the target project, and symlink destinations are rejected.

## Package Contents

- `SKILL.md`: trigger boundary, evidence rules, workflow, and output contract
- `references/methodology.md`: the context-file responsibility map
- `assets/templates/`: blank context, runbook, and minimal entrypoint templates
- `scripts/scaffold_six_file_context.py`: safe scaffolder
- `tests/`: scaffolder regression tests
- `evals/`: behavioral and trigger-boundary cases
- `agents/openai.yaml`: optional Codex discovery metadata

## License

Released under the MIT License. See `LICENSE`.
