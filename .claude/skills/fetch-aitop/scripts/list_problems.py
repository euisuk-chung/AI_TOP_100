#!/usr/bin/env python3
"""List all problems exposed by challenge.aitop100.org's public API.

Usage:
    list_problems.py [--season N] [--format json|table] [--save PATH]

Prints to stdout. The response is cached to `.cache/aitop_problems.json` (or
the path passed via `--save`) so downstream tools can read it without hitting
the network repeatedly.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

API_URL = "https://challenge.aitop100.org/api/problems"


def fetch() -> dict:
    resp = requests.get(API_URL, timeout=20)
    resp.raise_for_status()
    return resp.json()


def emit_table(data: dict) -> str:
    seasons = {s["id"]: s["title"] for s in data.get("seasons", [])}
    rows = ["| code | title | season |", "|------|-------|--------|"]
    for p in data["problems"]:
        rows.append(
            f"| {p['code']} | {p['title']} | {seasons.get(p['seasonId'], p['seasonId'])} |"
        )
    return "\n".join(rows)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--season", type=int, default=None)
    parser.add_argument("--format", choices=("json", "table"), default="json")
    parser.add_argument("--save", default=None, help="cache full response to this path")
    args = parser.parse_args(argv[1:])

    sys.stdout.reconfigure(encoding="utf-8")

    data = fetch()

    save_path = Path(args.save) if args.save else Path(".cache/aitop_problems.json")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.season is not None:
        data["problems"] = [p for p in data["problems"] if p["seasonId"] == args.season]

    if args.format == "table":
        sys.stdout.write(emit_table(data) + "\n")
    else:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
