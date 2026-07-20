# Skill Release Checklist

## Ownership

- [ ] Authorship or redistribution rights are confirmed.
- [ ] Upstream projects and licenses are identified.
- [ ] Required license and attribution files are included.
- [ ] The skill is not presented as original work when it is a fork or adaptation.

## Privacy

- [ ] Client and project names are removed.
- [ ] Personal names and contact details are removed.
- [ ] Local absolute paths are removed.
- [ ] Credentials, tokens, cookies, and private keys are absent.
- [ ] Private URLs, repository names, task IDs, and production identifiers are absent.
- [ ] Examples and evaluations use clearly fictional data.
- [ ] OS metadata and copied logs are absent.

## Portability

- [ ] The directory name matches the skill frontmatter name.
- [ ] Commands use relative paths or documented environment variables.
- [ ] Host-specific metadata is optional and clearly labeled.
- [ ] Required runtimes and third-party dependencies are documented.
- [ ] Unsupported hosts fail clearly instead of silently degrading.

## Verification

- [ ] Frontmatter and package structure validate.
- [ ] JSON and YAML resources parse.
- [ ] Bundled scripts pass focused tests.
- [ ] Trigger and near-miss behavior is evaluated.
- [ ] The packaged archive extracts cleanly.
- [ ] The extracted archive passes validation and privacy scanning.
- [ ] Human release acceptance is recorded separately from technical validation.
