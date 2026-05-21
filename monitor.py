#!/usr/bin/env python3
"""Minimal public URL change watcher for Micro Change Watch.

Usage:
  python3 monitor.py config.json

Config shape:
{
  "customer": "demo",
  "urls": ["https://example.com/pricing"],
  "state_dir": "./state",
  "report_dir": "./reports"
}
"""
from __future__ import annotations

import difflib
import hashlib
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


def fetch_text(url: str, timeout: int = 25) -> tuple[str, str | None]:
    req = Request(url, headers={"User-Agent": "MicroChangeWatch/0.1 (+public page change monitor)"})
    try:
        with urlopen(req, timeout=timeout) as r:
            raw = r.read(1_500_000)
            ctype = r.headers.get("content-type", "")
    except Exception as e:
        return "", f"fetch error: {e}"

    text = raw.decode("utf-8", errors="replace")
    if "html" in ctype or "<html" in text[:5000].lower():
        text = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", text)
        text = re.sub(r"(?s)<[^>]+>", " ", text)
        text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines)[:250_000], None


def slug(url: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", url).strip("-")[:120] or "url"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: monitor.py config.json", file=sys.stderr)
        return 2
    cfg = json.loads(Path(sys.argv[1]).read_text())
    customer = cfg.get("customer", "customer")
    state_dir = Path(cfg.get("state_dir", "./state")) / customer
    report_dir = Path(cfg.get("report_dir", "./reports"))
    state_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    report = [f"# Micro Change Watch — {now}", "", f"Customer: `{customer}`", ""]
    changes = errors = nochange = baseline = 0

    for url in cfg.get("urls", []):
        name = slug(url)
        prev_path = state_dir / f"{name}.txt"
        meta_path = state_dir / f"{name}.json"
        current, err = fetch_text(url)
        report += [f"## {url}"]
        if err:
            errors += 1
            report += [f"Status: ERROR — {err}", ""]
            continue
        cur_hash = digest(current)
        old = prev_path.read_text(errors="replace") if prev_path.exists() else None
        old_hash = digest(old) if old is not None else None
        if old is None:
            baseline += 1
            report += ["Status: BASELINE CAPTURED — no prior snapshot.", ""]
        elif cur_hash == old_hash:
            nochange += 1
            report += ["Status: no meaningful text change detected.", ""]
        else:
            changes += 1
            diff = list(difflib.unified_diff(
                old.splitlines(), current.splitlines(),
                fromfile="before", tofile="after", lineterm="", n=2,
            ))
            # Keep only a concise evidence chunk.
            evidence = "\n".join(diff[:120])
            report += ["Status: CHANGED", "", "```diff", evidence[:8000], "```", ""]
        prev_path.write_text(current)
        meta_path.write_text(json.dumps({"url": url, "last_checked": now, "sha256": cur_hash}, indent=2))

    report.insert(3, f"Summary: {changes} changed, {nochange} unchanged, {baseline} baselined, {errors} errors.")
    out = report_dir / f"{customer}-{now[:10]}.md"
    out.write_text("\n".join(report) + "\n")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
