# Skills

Each child directory must be a self-contained, installable skill package.

Do not symlink personal installed skills into this directory. Copy only a reviewed and sanitized distribution candidate.

Expected shape:

```text
skills/
  skill-name/
    SKILL.md
    README.md
    agents/
    references/
    scripts/
    tests/
```

Only include directories that the skill actually uses.
