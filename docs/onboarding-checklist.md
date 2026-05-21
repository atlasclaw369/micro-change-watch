# Customer onboarding checklist

Use this before accepting payment. Goal: confirm scope fast, avoid unsafe monitoring, and give the first customer a clean start.

## 1. Intake received

- [ ] Customer name/handle recorded.
- [ ] Contact/delivery path recorded.
- [ ] Plan requested: Starter / Standard / 48-hour one-off / trial-demo.
- [ ] URLs provided.
- [ ] Customer described what changes matter.
- [ ] Customer understands this is public-page monitoring only.

## 2. Scope validation

- [ ] URL count is within plan limit:
  - Starter: up to 3 URLs.
  - Standard: up to 10 URLs.
  - 48-hour one-off: up to 5 URLs.
- [ ] All URLs are public `http`/`https` pages.
- [ ] No URL contains tokens, credentials, private dashboard paths, personal data, or login-only pages.
- [ ] No localhost/private-network target.
- [ ] No secret-looking query parameters.
- [ ] Customer priorities are objective enough to review manually.
- [ ] Delivery method is safe and clear.
- [ ] No ToS/scraping/captcha-sensitive target.

## 3. Operator validation

Create the customer config from `customers/example.customer.json`, then run:

```bash
python3 scripts/change_watch.py validate customers/<customer>.json
python3 scripts/change_watch.py run customers/<customer>.json
```

Confirm:

- [ ] Config validates cleanly.
- [ ] Baseline report generated.
- [ ] No rejected/private URLs.
- [ ] URL count is accepted by the selected plan limit.
- [ ] No embedded credentials, localhost/private-network targets, unsafe redirects, or secret-looking query parameters.
- [ ] No repeated fetch errors.
- [ ] Diff output is readable enough for manual review.
- [ ] Baseline report does not expose sensitive customer data before sharing.

## 4. Payment + scope confirmation template

Send this after validation and before starting paid fulfillment.

```text
I can run this Micro Change Watch.

Plan: <Starter / Standard / 48-hour one-off>
Price: <$9/mo / $19/mo / $10 one-off / trial-demo approved>
URLs: <count> public URLs
Cadence/window: <daily / 48 hours>
Delivery: <GitHub issue comment / email / DM / other agreed path>
What I’ll monitor for: <customer priorities>
First report timing: <baseline now + next check time/window>

Public-scope note: I monitor only public pages. I will stop/reject any URL that requires login, credentials, cookies, captcha bypass, personal data, private dashboards, or unsafe scraping.

Payment: <manual payment option after confirmation>
Payment status: <unpaid / paid / trial approved>

Please reply “confirmed” if this scope and price are correct. Once confirmed/paid, I’ll capture the baseline and send the first report after the next check window.
```

## 5. Payment status

- [ ] Unpaid / trial approved / paid.
- [ ] Payment evidence recorded privately, not in the public repo if sensitive.
- [ ] Start date recorded.
- [ ] Renewal/follow-up date recorded.
- [ ] Any wallet/payment/identity/private financial step handled manually by JLO only.

## 6. Start fulfillment

- [ ] Save customer config.
- [ ] Run baseline.
- [ ] Review baseline manually.
- [ ] Send baseline note.
- [ ] Set next check date/time.
- [ ] Store report under the correct customer/report path.

## 7. Delivery checklist

Before sending each report:

- [ ] Confirm report belongs to the right customer.
- [ ] Check no sensitive URL/query/customer data is exposed.
- [ ] Summarize meaningful changes in plain English.
- [ ] Include no-change list so customer knows the watch ran.
- [ ] Mention fetch errors honestly.
- [ ] Record renewal/follow-up date if applicable.
