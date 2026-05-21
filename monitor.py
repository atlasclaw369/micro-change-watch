#!/usr/bin/env python3
"""Backward-compatible shim for the Micro Change Watch operator CLI."""
from scripts.change_watch import main

if __name__ == "__main__":
    raise SystemExit(main())
