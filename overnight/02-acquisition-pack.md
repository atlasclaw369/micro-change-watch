# Overnight acquisition pack — Micro Change Watch

Generated: 2026-05-21 21:46:03 UTC

## Goal

Prepare launch/acquisition assets JLO can use tomorrow without requiring Hermes to be logged into social accounts.

## Assets created / improved

1. `launch-copy.md`
   - Expanded Hacker News freelancer thread copy.
   - Added Show HN style draft.
   - Added Reddit post draft for r/SaaS / r/startups style communities.
   - Added Reddit reply format for contextual, non-spammy replies.
   - Added LinkedIn post draft.
   - Added X short post and X thread.
   - Added invited-only DM/reply copy.
   - Added one-line profile/bio text.

2. `docs/buyer-personas-and-queries.md`
   - Tightened the 10 best first buyer personas.
   - Preserved exactly 25 prospect-search queries.
   - Added “who to approach first tomorrow” filters.
   - Added manual outreach guardrails.

3. `docs/onboarding-checklist.md`
   - Expanded into a first-customer checklist.
   - Added intake, scope validation, operator validation, payment status, fulfillment, and delivery sections.
   - Added a payment/scope confirmation template.
   - Explicitly keeps wallet/payment/identity/private financial steps manual for JLO.

## Verification

Ran:

```bash
python3 - <<'PY'
from pathlib import Path
p=Path('docs/buyer-personas-and-queries.md').read_text()
persona=[l for l in p.splitlines() if l[:2].strip('.').isdigit() and '**' in l]
queries=[l for l in p.splitlines() if l.startswith(tuple(f'{i}. `' for i in range(1,26)))]
print('personas',len(persona))
print('queries',len(queries))
PY
```

Result:

- Personas: 10.
- Queries: 25.

Ran:

```bash
git diff --check
make test
```

Result:

- `git diff --check`: OK.
- `make test`: OK.
- Unit tests: `Ran 4 tests ... OK`.
- Demo validation/run path still works.

## Exact next manual actions for JLO tomorrow

### 1. Post one public launch message first

Recommended first post: Hacker News monthly freelancer / seeking-work thread if the current thread is active.

Use: `launch-copy.md` → `Hacker News — monthly freelancer / seeking work thread`.

If no suitable HN thread is active, use LinkedIn first:

Use: `launch-copy.md` → `LinkedIn — founder/operator post`.

Do not post all channels at once. Start with 1–2 channels and watch for replies.

### 2. Put the repo link in one profile/bio

Use: `launch-copy.md` → `One-line bio / profile text`.

Best options:

- X bio / pinned post.
- LinkedIn featured item/post.
- Indie Hackers profile if available.

### 3. Run 10 targeted searches, not broad spam

Start with these 10 from `docs/buyer-personas-and-queries.md`:

1. `"monitor competitor pricing" SaaS founder`
2. `"competitor changed pricing" startup`
3. `"API docs changed" "broke"`
4. `"vendor changelog" "API docs" startup`
5. `"manual competitor research" SaaS`
6. `site:news.ycombinator.com "competitor pricing" SaaS`
7. `site:news.ycombinator.com "API docs changed"`
8. `site:reddit.com/r/SaaS "competitor pricing"`
9. `site:reddit.com/r/startups "competitor pricing"`
10. `"launch week" "competitor" "pricing" founder`

For each result, only reply if:

- the person is clearly asking about monitoring/research pain;
- self-promotion or tool suggestions are allowed;
- the reply can be specific to their context;
- no private/sensitive monitoring is involved.

Use: `launch-copy.md` → `Manual DM/reply only when invited` or `Reddit — reply format when someone describes the pain`.

### 4. Offer the smallest paid ask

Default CTA:

> Want me to sanity-check 3–5 public URLs for a $10 48-hour watch?

Avoid pushing monthly plans until someone has used or clearly wants the service.

### 5. On first inbound interest, use the checklist before payment

Use: `docs/onboarding-checklist.md`.

Order:

1. Confirm URLs are public and within plan limit.
2. Create customer config.
3. Run validation.
4. Send the payment/scope confirmation template.
5. Only then collect payment or approve a trial/demo.

### 6. Payment handling

Keep payment manual. Do not expose wallet/payment details publicly in repo issues unless JLO explicitly chooses that.

Safe phrasing:

> Payment is manual after scope confirmation. I can send the payment option privately once we confirm the URLs are a fit.

### 7. Success target for tomorrow

Primary target:

- 1 paid $10 48-hour watch, or
- 1 concrete inbound request with URLs ready for validation.

Secondary target:

- 3–5 qualified conversations where the pain is real and the person may buy later.

## Blockers / risks

- No external posting was performed.
- No social/login/payment actions were performed.
- Public acquisition still needs JLO to manually post from accounts/channels where posting is allowed.
- Avoid monitoring private/login-only/customer-data pages even if a buyer asks.
