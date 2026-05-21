# Micro Change Watch — Sample Report

Customer: `sample-founder`
Summary: 2 changed, 2 unchanged, 0 errors.

## Meaningful changes

### 1. Competitor pricing page
URL: `https://competitor.example/pricing`

**Change:** Pro plan price changed from `$19/mo` to `$29/mo`.

```diff
- Pro — $19/month
+ Pro — $29/month
```

**Why it may matter:** Review your pricing comparison and sales objection handling.

### 2. API changelog
URL: `https://api-vendor.example/changelog`

**Change:** New release note added for webhook retries.

```diff
+ May 21 — Webhook retry policy now supports exponential backoff up to 24h.
```

**Why it may matter:** Could reduce custom retry code or change integration behavior.

## No meaningful text change detected

- `https://competitor.example/docs`
- `https://status.vendor.example/`
