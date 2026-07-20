# Jinni Skills

A curated collection of reusable agent skills maintained by Jinni.

## Status

This repository is private while the first public release candidates are sanitized, licensed, and validated.

Only sanitized distribution copies belong here. Installed skills under personal agent directories are working sources, not public release sources.

## Initial Release Order

1. `understand-before-approve`
2. `incident-triage`
3. `project-start` and `agent-setup`
4. `loop-engineering`
5. `skill-forge`
6. A generalized `project-flow-router`

## Repository Rules

- Keep one installable folder per skill under `skills/`.
- Make each folder name match the `name` field in its `SKILL.md`.
- Never add client names, personal data, credentials, private URLs, local absolute paths, copied logs, or production identifiers.
- Keep private profiles, project-specific examples, and internal evaluations outside this repository.
- Confirm authorship, upstream licenses, and required attribution before publishing.
- Validate an extracted release archive, not only the working directory.
- Treat approval to prepare a release as separate from approval to publish it.

## Structure

```text
skills/             Sanitized, installable skill folders
docs/               Release policy and portfolio documentation
README.md           Repository overview
```

The first skill will be added only from its sanitized distribution package.
