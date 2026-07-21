# Contributing

Contributions are welcome when they make a skill clearer, safer, more portable, or easier to use.

## Before Opening A Pull Request

1. Open an issue for a new skill or a meaningful scope change.
2. Keep one coherent workflow per skill.
3. Use fictional examples and evaluation data.
4. Keep private profiles, customer information, credentials, internal URLs, task IDs, copied logs, and local absolute paths out of the repository.
5. Run the repository validator.

```bash
python3 scripts/validate_repository.py
```

## Skill Package Requirements

- The directory name must match the `name` field in `SKILL.md`.
- `SKILL.md` must state when the skill should and should not trigger.
- Supporting references, scripts, templates, examples, and tests must be included when the workflow depends on them.
- Host-specific metadata must remain optional.
- Scripts must refuse unsafe overwrites and path escapes.
- Unknown facts must remain unknown instead of being invented.
- The package must include or inherit a compatible license.

Use [docs/release-checklist.md](docs/release-checklist.md) before requesting release.

## Pull Request Shape

Include:

- the problem being solved;
- why a new skill or change is warranted;
- positive and negative trigger examples;
- verification performed;
- privacy and licensing notes;
- any compatibility limits.

Keep unrelated cleanup out of the same pull request.

## Style

- Use plain English before specialist terminology.
- Explain important restrictions and their reason.
- Prefer short sections and concrete examples.
- Never use em dash characters.
- Do not claim a test, deployment, or review passed without evidence.
