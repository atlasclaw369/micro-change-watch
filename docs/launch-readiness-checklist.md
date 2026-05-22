# Micro Change Watch — launch readiness checklist

Use this before public launch or first paid watch.

## 1. Public intake

- [ ] Public repo renders: `https://github.com/atlasclaw369/micro-change-watch`
- [ ] README explains the $10 / $9 / $19 offers clearly.
- [ ] Intake issue template exists: `.github/ISSUE_TEMPLATE/watch-request.yml`
- [ ] Intake CTA works for logged-in GitHub users: `https://github.com/atlasclaw369/micro-change-watch/issues/new?template=watch-request.yml`
- [ ] Payment wording stays manual: no public wallet/payment identifiers in repo issues.

## 2. Safety gate

- [ ] Request contains only public `http`/`https` URLs.
- [ ] No localhost/private-network URLs.
- [ ] No embedded credentials.
- [ ] No secret-looking query params: token, API key, password, signature, access token, etc.
- [ ] No private dashboards, cookies, login pages, captcha-heavy pages, personal data, or access-control bypassing.

## 3. First-customer scope

- [ ] Plan selected and URL count fits the plan.
- [ ] Buyer states what changes matter.
- [ ] Delivery preference is safe and practical.
- [ ] Operator confirms price/scope before payment.
- [ ] JLO handles any payment/wallet/payment-link details manually and privately.

## 4. Fulfillment proof

- [ ] Customer config created from `customers/example.customer.json` or `customers/sample-saas-founder-48h.json`.
- [ ] Config validates: `python3 scripts/change_watch.py validate customers/<customer>.json`
- [ ] Baseline/report runs: `python3 scripts/change_watch.py run customers/<customer>.json`
- [ ] Report appears under `reports/<customer>/`.
- [ ] Operator reviews changed/error sections before forwarding.
- [ ] Customer receives concise summary, evidence snippets, errors if any, and no-change list.

## 5. Launch-day success criteria

Minimum credible launch state:

- [ ] README + intake form public.
- [ ] One sample customer config exists.
- [ ] One sample report exists.
- [ ] At least one real demo run completed successfully.
- [ ] Tests pass.
- [ ] One public/manual acquisition post is ready to send.

First revenue target:

- [ ] 1 paid `$10` 48-hour watch, or
- [ ] 1 inbound request with URLs ready for validation.
