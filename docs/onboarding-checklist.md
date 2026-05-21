# Customer onboarding checklist

Use this before accepting payment.

## 1. Scope validation

- [ ] Customer selected a plan.
- [ ] URL count is within plan limit.
- [ ] All URLs are public http/https pages.
- [ ] No URL contains tokens, credentials, personal data, private dashboards, or login-only pages.
- [ ] Customer described what changes matter.
- [ ] Delivery method is safe and clear.

## 2. Operator validation

Run:

```bash
python3 scripts/change_watch.py validate customers/<customer>.json
python3 scripts/change_watch.py run customers/<customer>.json
```

Confirm:

- [ ] Baseline report generated.
- [ ] No rejected/private URLs.
- [ ] No repeated fetch errors.
- [ ] Diff output is readable enough for manual review.

## 3. Scope confirmation message

```text
I can run this watch.

Plan: <plan>
URLs: <count>
Cadence: <daily / 48h>
Delivery: <GitHub issue comments / other agreed path>
What I’ll monitor for: <customer priorities>

Public-scope note: I will monitor only public pages and will stop/reject any URL that starts requiring login, credentials, captcha bypass, personal data, or unsafe scraping.

Price: <$amount>
Payment: <manual payment option after confirmation>

Once confirmed/paid, I’ll capture the baseline and send the first report after the next check window.
```

## 4. Payment status

- [ ] Unpaid / trial approved / paid.
- [ ] Payment evidence recorded privately, not in public repo if sensitive.
- [ ] Start date and renewal date recorded.

## 5. Delivery

- [ ] Send baseline note.
- [ ] Send daily report only after operator review.
- [ ] Record renewal/follow-up date.
