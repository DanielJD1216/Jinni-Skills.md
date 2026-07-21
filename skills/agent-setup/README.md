# Agent Setup

## Plain English

Use this skill when coding agents need a clear operating manual for a repository. It tells them what to read, which commands are actually supported, which files or actions are protected, and what must be verified before work is considered complete.

It does not define the product. It turns accepted project context into practical working rules.

## When To Use It

- a repository that lacks `AGENTS.md` or `CLAUDE.md`;
- stale or incomplete agent operating instructions;
- verified install, dev, test, lint, typecheck, build, migration, or deploy commands;
- nested Codex instruction scope and `AGENTS.override.md` behavior;
- protected-file, verification, documentation-sync, tool, or risk rules.

## When Not To Use It

- inventing missing product or architecture context;
- implementing a feature;
- replacing mature instructions without evidence that they are stale;
- creating general documentation that does not control agent behavior.

## What It Produces

Depending on the coding assistant, it creates or refreshes:

- `AGENTS.md` for Codex;
- `CLAUDE.md` for Claude Code;
- another documented agent entrypoint when that assistant uses a different convention.

The entrypoint can include context read order, verified commands, protected files, nested instruction scope, verification gates, and unresolved decisions.

## Example

A repository already has accepted project context but no `AGENTS.md`. The skill inspects package scripts, tests, CI, deployment files, and existing rules. It creates a concise entrypoint linking to project context, records only evidence-backed commands, protects high-risk files, and requires concrete verification before completion.

## Pair It With Project Start

`project-start` owns what is true about the product and system. `agent-setup` owns how coding agents should operate in the repository.

When project memory is missing or stale, run `project-start` first. Agent Setup then links to the accepted context instead of duplicating it.

## Host Boundaries

- Codex uses `AGENTS.md` and supports nested `AGENTS.override.md` precedence.
- Claude Code uses `CLAUDE.md`.
- Other assistants may use different files. Preserve their existing conventions and verify current official documentation before claiming automatic discovery.

The bundled Codex guide is a dated snapshot. Refresh it from the official source when current behavior matters.

## Install

Place the `agent-setup` directory in the skill directory used by your coding assistant.

- Codex: `~/.codex/skills/agent-setup/`
- Claude Code: `~/.claude/skills/agent-setup/`
- Other Agent Skills compatible tools: use the documented user or project skill directory.

Keep the directory name and the `name` field in `SKILL.md` as `agent-setup`.

## Scaffold

Run from the installed skill directory:

```bash
python3 scripts/scaffold_agent_entrypoint.py /path/to/project --target agents
```

The script skips existing files by default. `--force` is required to overwrite, context paths must be project-relative, and symlink destinations are rejected.

## Package Contents

- `SKILL.md`: trigger boundary, workflow, and output contract
- `references/entrypoint-checklist.md`: complete entrypoint review checklist
- `references/openai-agents-md-guide.md`: dated Codex discovery snapshot and official source
- `assets/templates/AGENTS.md`: Codex entrypoint template
- `assets/templates/CLAUDE.md`: Claude Code entrypoint template
- `scripts/scaffold_agent_entrypoint.py`: safe scaffolder
- `tests/`: scaffolder regression tests
- `evals/`: behavioral and trigger-boundary cases
- `agents/openai.yaml`: optional Codex discovery metadata

## License

Released under the MIT License. See `LICENSE`.
