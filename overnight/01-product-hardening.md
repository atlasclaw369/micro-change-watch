# Overnight product hardening report — Micro Change Watch

Generated: 2026-05-21 19:49:00 UTC

## Repo

- Public repo: https://github.com/atlasclaw369/micro-change-watch
- Local workspace: `/home/atlas/money-lab/change-watch-microservice`

## Status checked

- Verified Git remote: `origin https://github.com/atlasclaw369/micro-change-watch.git`
- Starting status had only untracked `overnight/` notes.
- Ran the existing test/demo path before changes: `make test` passed.

## Product hardening completed

Commit pushed:

- `97adb4c` — `Harden watch validation for launch`

Changes:

- Added plan-limit validation in `scripts/change_watch.py`:
  - Starter: max 3 URLs.
  - Standard: max 10 URLs.
  - 48-hour/one-off watch: max 5 URLs.
- Made `validate` fail closed on bad config instead of only validating individual URLs.
- Expanded URL safety checks for secret-looking query keys: `token`, `api_key`, `apikey`, `access_token`, `password`, `secret`, `signature`, `sig`, `auth`, `code`, `key`.
- Added operator-review/customer-priority lines to generated reports so reports are safer to forward after human review.
- Added unit tests in `tests/test_validation.py` for plan limits, pricing plan names, secret query rejection, localhost rejection, and embedded credentials.
- Updated `Makefile` so `make test` runs unit tests.
- Updated public README and onboarding checklist to explain the safety validation.

## Verification

Ran after changes:

```bash
make test
```

Result:

- Python compile: OK.
- Unit tests: `Ran 4 tests ... OK`.
- Example customer validation: OK for all 3 demo URLs.
- Demo report generated: `/home/atlas/money-lab/change-watch-microservice/reports/demo/2026-05-21.md`.

Ran:

```bash
git diff --check
```

Result: OK / no whitespace errors.

Push result:

- `4090a69..97adb4c main -> main`

## Current commits

- `97adb4c` — Harden watch validation for launch
- `4090a69` — Harden public monitoring MVP for launch
- `8f97f9a` — Exclude generated monitor artifacts
- `4db5500` — Launch Micro Change Watch MVP

## Blockers / risks

- No credential/payment setup performed.
- No external posting/outreach performed.
- `overnight/` remains local/untracked as operating notes; product code/docs are pushed.
- Public product is more launch-ready, but acquisition still needs a manual buyer channel/login/posting path from JLO before real demand can arrive.
