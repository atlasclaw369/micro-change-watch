#!/usr/bin/env python3
"""Micro Change Watch operator CLI.

Commands:
  run CUSTOMER_JSON      Fetch public URLs, update snapshots, write report.
  validate CUSTOMER_JSON Validate URL config and scope shape.

No credentials, no browser automation, no login/cookie bypass. Public URLs only.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import html
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE = ROOT / "state"
DEFAULT_REPORTS = ROOT / "reports"

BLOCKED_HOST_PATTERNS = [
    "localhost", "127.0.0.1", "0.0.0.0", "169.254.", "10.", "192.168.",
]

@dataclass
class UrlItem:
    url: str
    name: str
    why: str = ""


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")[:120] or "url"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_customer(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not data.get("customer"):
        raise ValueError("customer is required")
    if not isinstance(data.get("urls"), list) or not data["urls"]:
        raise ValueError("urls must be a non-empty list")
    return data


def parse_url_item(raw: Any) -> UrlItem:
    if isinstance(raw, str):
        return UrlItem(url=raw, name=raw)
    if isinstance(raw, dict):
        return UrlItem(url=raw["url"], name=raw.get("name") or raw["url"], why=raw.get("why", ""))
    raise ValueError(f"unsupported url item: {raw!r}")


def validate_public_url(url: str) -> list[str]:
    problems: list[str] = []
    p = urlparse(url)
    if p.scheme not in {"http", "https"}:
        problems.append("URL must use http/https")
    if not p.netloc:
        problems.append("URL missing host")
    host = p.hostname or ""
    if any(host == pat or host.startswith(pat) for pat in BLOCKED_HOST_PATTERNS):
        problems.append("local/private network URL is not allowed")
    if any(token in url.lower() for token in ["token=", "api_key=", "apikey=", "password=", "secret="]):
        problems.append("URL appears to contain a secret/token")
    return problems


def html_to_text(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript|svg|canvas).*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<!--.*?-->", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n\s*\n+", "\n", raw)
    lines = []
    seen_blank = False
    for ln in raw.splitlines():
        ln = ln.strip()
        if not ln:
            if not seen_blank:
                seen_blank = True
            continue
        seen_blank = False
        # Drop very noisy short nav crumbs while keeping evidence text.
        if len(ln) == 1 and not ln.isalnum():
            continue
        lines.append(ln)
    return "\n".join(lines)


def fetch_public_text(url: str, timeout: int = 25) -> tuple[str, str | None, dict[str, str]]:
    req = Request(url, headers={
        "User-Agent": "MicroChangeWatch/0.1 public-page-monitor (+https://github.com/atlasclaw369/micro-change-watch)",
        "Accept": "text/html,text/plain,application/json;q=0.9,*/*;q=0.2",
    })
    try:
        with urlopen(req, timeout=timeout) as r:
            raw_bytes = r.read(1_500_000)
            headers = {k.lower(): v for k, v in r.headers.items()}
            status = getattr(r, "status", 200)
    except Exception as e:
        return "", f"fetch error: {type(e).__name__}: {e}", {}
    ctype = headers.get("content-type", "")
    text = raw_bytes.decode("utf-8", errors="replace")
    if "html" in ctype.lower() or "<html" in text[:2000].lower():
        text = html_to_text(text)
    else:
        text = html.unescape(text)
    text = text[:250_000]
    return text, None if 200 <= status < 400 else f"HTTP status {status}", headers


def concise_diff(old: str, new: str, max_lines: int = 160, max_chars: int = 10_000) -> str:
    diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(), fromfile="before", tofile="after", lineterm="", n=2))
    # Prefer hunks with actual additions/removals, but keep headers for context.
    selected = []
    for ln in diff:
        selected.append(ln)
        if len(selected) >= max_lines:
            break
    out = "\n".join(selected)
    return out[:max_chars]


def run(config_path: Path) -> Path:
    cfg = load_customer(config_path)
    customer = slug(cfg["customer"])
    state_dir = Path(cfg.get("state_dir") or DEFAULT_STATE) / customer
    report_dir = Path(cfg.get("report_dir") or DEFAULT_REPORTS) / customer
    state_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    checked = now_utc()

    changed = unchanged = baselined = errors = 0
    sections: list[str] = []
    machine_events: list[dict[str, Any]] = []

    for raw in cfg["urls"]:
        item = parse_url_item(raw)
        problems = validate_public_url(item.url)
        safe_name = slug(item.name or item.url)
        prev_path = state_dir / f"{safe_name}.txt"
        meta_path = state_dir / f"{safe_name}.json"
        header = f"## {item.name}\nURL: `{item.url}`"
        if item.why:
            header += f"\nWatch reason: {item.why}"
        if problems:
            errors += 1
            msg = "; ".join(problems)
            sections.append(f"{header}\n\nStatus: REJECTED / CONFIG ERROR — {msg}\n")
            machine_events.append({"url": item.url, "status": "config_error", "error": msg})
            continue

        text, err, headers = fetch_public_text(item.url)
        if err:
            errors += 1
            sections.append(f"{header}\n\nStatus: ERROR — {err}\n")
            machine_events.append({"url": item.url, "status": "fetch_error", "error": err})
            continue

        current_hash = sha256(text)
        old = prev_path.read_text(errors="replace") if prev_path.exists() else None
        if old is None:
            baselined += 1
            sections.append(f"{header}\n\nStatus: BASELINE CAPTURED — no previous snapshot yet.\n")
            status = "baseline"
        elif sha256(old) == current_hash:
            unchanged += 1
            sections.append(f"{header}\n\nStatus: no meaningful text change detected.\n")
            status = "unchanged"
        else:
            changed += 1
            evidence = concise_diff(old, text)
            sections.append(f"{header}\n\nStatus: CHANGED\n\n```diff\n{evidence}\n```\n")
            status = "changed"
        prev_path.write_text(text)
        meta_path.write_text(json.dumps({
            "url": item.url,
            "name": item.name,
            "why": item.why,
            "last_checked": checked,
            "sha256": current_hash,
            "content_type": headers.get("content-type", ""),
            "status": status,
        }, indent=2))
        machine_events.append({"url": item.url, "name": item.name, "status": status, "sha256": current_hash})

    title = f"# Micro Change Watch — {checked}"
    summary = f"Summary: {changed} changed, {unchanged} unchanged, {baselined} baselined, {errors} errors."
    report = "\n\n".join([
        title,
        f"Customer: `{cfg['customer']}`",
        summary,
        f"Plan: `{cfg.get('plan','unknown')}` | Cadence: `{cfg.get('cadence','daily')}` | Delivery: `{cfg.get('delivery','unspecified')}`",
        *sections,
    ]) + "\n"
    out = report_dir / f"{checked[:10]}.md"
    out.write_text(report)
    event_path = report_dir / f"{checked[:10]}.json"
    event_path.write_text(json.dumps({
        "checked_at": checked,
        "customer": cfg["customer"],
        "summary": {"changed": changed, "unchanged": unchanged, "baselined": baselined, "errors": errors},
        "events": machine_events,
        "report": str(out),
    }, indent=2))
    print(out)
    return out


def validate(config_path: Path) -> int:
    cfg = load_customer(config_path)
    failures = 0
    for raw in cfg["urls"]:
        item = parse_url_item(raw)
        problems = validate_public_url(item.url)
        if problems:
            failures += 1
            print(f"ERROR {item.url}: {'; '.join(problems)}")
        else:
            print(f"OK {item.url}")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    runp = sub.add_parser("run")
    runp.add_argument("config", type=Path)
    valp = sub.add_parser("validate")
    valp.add_argument("config", type=Path)
    args = ap.parse_args(argv)
    if args.cmd == "run":
        run(args.config)
        return 0
    if args.cmd == "validate":
        return validate(args.config)
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
