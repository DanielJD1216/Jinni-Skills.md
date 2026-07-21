# Security Policy

## Reporting A Vulnerability

Do not open a public issue containing credentials, private repository content, customer data, internal URLs, or exploitable details.

Use GitHub's private vulnerability reporting feature if the repository's Security tab offers it. If private reporting is not enabled, open a minimal public issue asking the maintainer for a private contact path. Do not include exploit details, credentials, private data, or internal URLs in that issue.

In the private report, include:

- affected skill or script;
- supported reproduction steps using sanitized data;
- expected and observed behavior;
- potential impact;
- suggested mitigation when known.

## Scope

Security concerns include:

- path traversal or symlink bypass in bundled scripts;
- silent overwrite or destructive installation behavior;
- prompt-injection paths that broaden authorization;
- accidental publication of secrets or private identifiers;
- unsafe defaults for production or authenticated systems.

General workflow disagreements and non-sensitive bugs belong in normal GitHub Issues.

## Safe Use

Review a skill before installing it. Skills guide an agent but do not replace repository permissions, branch protection, backups, code review, or production access controls.
