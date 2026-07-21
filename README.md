# Jinni Skills

A curated collection of reusable agent skills maintained by Jinni. Each skill gives a coding agent a focused workflow, clear boundaries, and a defined output.

## Status

This is an open-source collection of sanitized, validated agent skills released under the MIT License.

Only sanitized distribution copies belong here. Installed skills under personal agent directories are working sources, not public release sources.

Repository-level original work is licensed under MIT. Adapted or third-party material must retain its upstream license and attribution, and may declare different terms inside its own directory.

## Start With The Router

When the correct workflow is unclear, start with [`project-flow-router`](skills/project-flow-router/). It checks the current request, target, prerequisites, live skill catalog, and accepted state, then chooses the narrowest valid owner or stops for one missing decision.

```mermaid
flowchart LR
    R["Current request"] --> P["project-flow-router"]
    P -->|project truth missing| S["project-start"]
    P -->|agent rules requested| A["agent-setup"]
    P -->|failure spans unknown layers| I["incident-triage"]
    P -->|consequential approval| U["understand-before-approve"]
    P -->|owner already clear| D["Direct specialist or action"]
    P -->|required context missing| X["Stop with one focused question"]
```

The router is optional. It should disappear when the owner is already clear, not add ceremony to every request.

## Choose Manually

```mermaid
flowchart TD
    A["What do you need right now?"] --> B{"Reliable project truth?"}
    B -->|Yes| P["project-start"]
    B -->|No| C{"Repository rules for coding agents?"}
    C -->|Yes| S["agent-setup"]
    C -->|No| D{"Diagnosis of an unclear multi-layer failure?"}
    D -->|Yes| I["incident-triage"]
    D -->|No| E{"Understanding before consequential approval?"}
    E -->|Yes| U["understand-before-approve"]
    E -->|No| N["Use a narrower task-specific workflow"]

    P -.->|after context is accepted, when needed| S
```

## Published Skills

| Skill | Plain-English purpose | What it produces |
|---|---|---|
| [`project-flow-router`](skills/project-flow-router/) | Chooses the right workflow owner or prerequisite order when the next move is unclear | Concise route decision, owner, reason, evidence boundary, and first stop gate |
| [`understand-before-approve`](skills/understand-before-approve/) | Makes sure the decision-maker understands a consequential change before approving it | Evidence brief, comprehension check, grading, and approval verdict |
| [`project-start`](skills/project-start/) | Builds reliable project memory from the repository and accepted decisions | Six focused context files and a first-debug runbook |
| [`agent-setup`](skills/agent-setup/) | Tells coding agents how to work safely and correctly inside a repository | `AGENTS.md`, `CLAUDE.md`, or another supported agent entrypoint |
| [`incident-triage`](skills/incident-triage/) | Finds the failed layer in a messy incident before anyone guesses at a fix | Read-only diagnostic packet, evidence gaps, safe checks, and the next decision |

## How They Fit Together

```mermaid
flowchart LR
    R["project-flow-router<br/>Which workflow owns this request?"] -.->|when ownership is unclear| P
    P["project-start<br/>What is true about this project?"] --> A["agent-setup<br/>How should agents work here?"]
    A --> B["Implementation<br/>Build within the accepted boundaries"]
    R -.->|clear owner| A
    R -.->|messy failure| I
    R -.->|material approval| U
    B -.->|unclear failure| I["incident-triage<br/>Prove the failed layer"]
    B -.->|consequential approval| U["understand-before-approve<br/>Confirm understanding first"]
    I -.->|high-risk fix approval| U
```

These skills are not a mandatory sequence. Use only the skill that matches the current situation. `project-flow-router` is the optional front door when that match is unclear. `project-start` and `agent-setup` are the main setup pair: one records project truth, and the other turns that truth into operating rules for agents.

## Release Order

1. `understand-before-approve`
2. `incident-triage`
3. `project-start` and `agent-setup`
4. `project-flow-router`
5. `loop-engineering`
6. `skill-forge`

Entries 1 through 4 are published. The remaining entries are planned and must pass the same release checklist before publication.

## Repository Rules

- Keep one installable folder per skill under `skills/`.
- Make each folder name match the `name` field in its `SKILL.md`.
- Never add client names, personal data, credentials, private URLs, local absolute paths, copied logs, or production identifiers.
- Keep private profiles, project-specific examples, and private evaluation transcripts outside this repository.
- Confirm authorship, upstream licenses, and required attribution before publishing.
- Validate an extracted release archive, not only the working directory.
- Treat approval to prepare a release as separate from approval to publish it.

## Structure

```text
skills/             Sanitized, installable skill folders
docs/               Release policy and portfolio documentation
README.md           Repository overview
```

Every skill must pass the release checklist before it is added to the public `main` branch.

## License

Original work in this repository is available under the [MIT License](LICENSE). Third-party or adapted material remains subject to any license and attribution included in its skill directory.
