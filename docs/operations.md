# Operator workflow

## New customer

1. Validate request URLs are public and acceptable.
2. Confirm plan, price, cadence, delivery, and payment state.
3. Create `customers/<customer>.json` from `customers/example.customer.json`.
4. Run baseline:

```bash
python3 scripts/change_watch.py run customers/<customer>.json
```

5. Schedule daily run with cron/Hermes after payment/approval.

## Daily fulfillment

```bash
python3 scripts/change_watch.py run customers/<customer>.json
```

Reports appear under `reports/<customer>/`.

Before sending a report, manually review changed diffs, remove boilerplate/noise, and add a 1–2 sentence customer-facing summary for each meaningful change. The script creates evidence; the operator owns the concise business-readable digest.

If delivery is GitHub issue comments, paste the concise reviewed report into the intake issue. If delivery is Telegram/email, forward the Markdown report.

## Stop conditions

Stop or reject if URL starts requiring login/captcha, customer asks for private data, target blocks normal public access, or monitoring creates ToS/security/privacy risk.
