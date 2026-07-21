# Getting Started

This guide gets one useful skill running without requiring you to understand the full methodology first.

## Requirements

- Git
- Python 3.9 or newer
- Codex, Claude Code, or another tool that supports Agent Skills style directories

The skills themselves are Markdown packages. Python is used only by the installer, validators, and the few skills that bundle deterministic helpers.

## Install In Two Minutes

```bash
git clone https://github.com/DanielJD1216/Jinni-Skills.md.git
cd Jinni-Skills.md
python3 scripts/install_skills.py --target codex --all
```

Replace `codex` with `claude` for Claude Code. For another host, pass its skill directory with `--dest`.

If the skills do not appear, restart the coding assistant once so it refreshes its skill catalog.

## First Prompt

Open a repository and use:

```text
Use project-flow-router. Inspect the current repository state and run only the workflow worth running now. Do not create lifecycle artifacts that are not needed.
```

The router should return one of four useful outcomes:

1. **Direct owner:** one installed skill clearly owns the task.
2. **Prerequisite order:** one workflow must establish evidence before the requested workflow can run.
3. **Direct action:** no specialist is needed.
4. **Focused stop:** a missing target, pointer, permission, or decision prevents safe routing.

## Skip The Router When The Skill Is Obvious

```text
Use project-start to build durable project context for this inherited repository.
```

```text
Use agent-setup to create repository instructions from the accepted project context.
```

```text
Use incident-triage on this staging outage. Diagnose only. Do not mutate production.
```

```text
Use understand-before-approve before I approve this production migration.
```

## Install Only What You Need

List the collection:

```bash
python3 scripts/install_skills.py --list
```

Install selected skills:

```bash
python3 scripts/install_skills.py --target codex project-start agent-setup
```

Preview without writing:

```bash
python3 scripts/install_skills.py --target codex --all --dry-run
```

## Update Safely

```bash
git pull
python3 scripts/install_skills.py --target codex --all --force
```

Existing skill directories are never silently overwritten. `--force` renames each old copy to a timestamped backup before installing the new copy.

Review or remove those backups only after the new version works in your environment.

## Manual Installation

Copy one complete directory from `skills/` into the skill directory used by your assistant. Keep the directory name unchanged.

Examples:

```text
~/.agents/skills/project-start/
~/.claude/skills/project-start/
```

Older Codex installations that still use `~/.codex/skills/` can use `--target codex-legacy`. Prefer the current documented `--target codex` location for new installations.

Do not copy only `SKILL.md` when the package also contains references, assets, scripts, or tests.

## Verify The Repository

Contributors and cautious installers can run:

```bash
python3 scripts/validate_repository.py
```

This validates all five skill packages, runs focused tests, checks links and JSON, validates the router profile, scans for local paths and generated files, and rejects em dash characters used against the repository style rule.

## Troubleshooting

### The Skill Is Not Discovered

- Confirm the complete skill directory is under the correct host directory.
- Confirm the directory name matches `name:` in `SKILL.md`.
- Restart the coding assistant.
- Check the current [Codex skills documentation](https://developers.openai.com/codex/skills) or [Claude Code skills documentation](https://docs.anthropic.com/en/docs/claude-code/skills) for that host's discovery locations.

### Installation Says The Skill Already Exists

Run with `--dry-run` first. Use `--force` only when you intend to replace the installed copy. The old copy will be retained as a backup.

### The Router Selects An Unavailable Skill

The public router profile is a Codex-oriented starter, not proof that every listed owner is installed. Adapt `references/routing-profile.yaml` to your live skill catalog and run its validator after any change.

### I Only Want Speed

Invoke the fitting specialist directly. The router and setup skills are optional. A known bug with a clear failing component usually needs ordinary implementation or diagnosis, not the full project sequence.
