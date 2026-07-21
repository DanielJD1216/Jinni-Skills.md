# OpenAI AGENTS.md Guide Notes

Official source: `https://learn.chatgpt.com/docs/agent-configuration/agents-md`

Snapshot checked against the official Codex manual on 2026-07-20. Use these notes as a baseline, but re-check the official source when current accuracy matters. If `$openai-docs` is available, use it for that refresh.

## Discovery Model

- Codex reads `AGENTS.md` files before doing work.
- Global scope lives in `CODEX_HOME`, defaulting to `~/.codex`.
- At global scope, Codex reads `AGENTS.override.md` if it exists; otherwise it reads `AGENTS.md`.
- At project scope, Codex starts at the project root, usually the Git root, and walks down to the current working directory.
- In each directory, Codex checks `AGENTS.override.md`, then `AGENTS.md`, then configured fallback filenames.
- Codex includes at most one instruction file per directory.
- Files closer to the current working directory appear later in the combined prompt and can override broader guidance.
- Empty files are skipped.
- The default combined instruction size limit is controlled by `project_doc_max_bytes`; the OpenAI guide currently states 32 KiB by default.

## Practical Use

- Put stable personal defaults in global `~/.codex/AGENTS.md`.
- Put repo-wide expectations in the repository root `AGENTS.md`.
- Put narrow service, package, or team rules close to the relevant directory.
- Use `AGENTS.override.md` when narrower guidance should replace the regular guidance at that same level.
- Keep root guidance compact. Split large or specialized rules into nested instruction files.

## Verification Patterns

- From a repo root, run `codex --ask-for-approval never "Summarize the current instructions."`.
- From a subdirectory, run `codex --cd subdir --ask-for-approval never "Show which instruction files are active."`.
- If instructions look stale, restart Codex in the target directory. The OpenAI guide says the instruction chain is rebuilt on every run and at the start of each TUI session.

## Fallback Filenames

- Codex can be configured to treat alternate filenames as instruction files with `project_doc_fallback_filenames`.
- Restart Codex or run a new command after changing this configuration.
- Prefer standard `AGENTS.md` unless the repo already has a strong alternate convention.
