# Support And Compatibility

## Supported Distribution Shape

Each folder under `skills/` follows the Agent Skills pattern: `SKILL.md` is the entrypoint, and optional references, assets, scripts, tests, evaluations, and host metadata live beside it.

The repository provides installation shortcuts for current documented personal-skill locations:

- Codex: `~/.agents/skills/`
- Claude Code: `~/.claude/skills/`
- generic Agent Skills directories: `~/.agents/skills/`
- older Codex installs: `~/.codex/skills/` through `--target codex-legacy`
- custom destinations through `--dest`

Host discovery rules can change. Check the current [Codex skills documentation](https://developers.openai.com/codex/skills) or [Claude Code skills documentation](https://docs.anthropic.com/en/docs/claude-code/skills) when a skill is not discovered.

## Runtime Support

- Installer and repository validation: Python 3.9 or newer
- Skill Markdown: no runtime dependency
- Bundled skill scripts: requirements are documented in each skill README

## Support Expectations

This is currently a single-maintainer open-source project with no uptime or response-time guarantee.

Use GitHub Issues for:

- reproducible installer problems;
- broken links or validation failures;
- unclear skill boundaries;
- portability defects;
- proposed skills or examples.

Include the host, operating system, Python version, command, observed error, and whether the destination already contained a skill. Remove credentials and private project information before posting.

Security-sensitive reports follow [SECURITY.md](SECURITY.md), not public issues.
