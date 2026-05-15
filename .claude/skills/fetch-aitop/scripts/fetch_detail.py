#!/usr/bin/env python3
"""Fetch a single problem's detail from challenge.aitop100.org.

The detail endpoint requires authentication. We try several candidate paths in
order, and fall back to the public summary if none succeed.

Usage:
    fetch_detail.py <code> [--cookies PATH]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from http.cookiejar import MozillaCookieJar
from pathlib import Path

import requests

BASE = "https://challenge.aitop100.org"
CANDIDATE_PATHS = [
    "/api/problems/{code}",
    "/api/problem/{code}",
    "/api/problems/{code}/detail",
    "/api/problems/{code}/description",
]
HEADERS = {
    "Accept": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
}


def load_cookies(path: Path) -> requests.cookies.RequestsCookieJar:
    jar = requests.cookies.RequestsCookieJar()
    raw = path.read_text(encoding="utf-8").strip()
    if raw.startswith("[") or raw.startswith("{"):
        items = json.loads(raw)
        if isinstance(items, dict):
            items = [items]
        for c in items:
            jar.set(
                c["name"],
                c.get("value", ""),
                domain=c.get("domain", "challenge.aitop100.org").lstrip("."),
                path=c.get("path", "/"),
            )
        return jar
    # Netscape format
    mj = MozillaCookieJar()
    mj.load(str(path), ignore_discard=True, ignore_expires=True)
    for c in mj:
        jar.set(c.name, c.value, domain=c.domain.lstrip("."), path=c.path)
    return jar


def try_detail(code: str, cookies) -> tuple[str, dict] | None:
    for tmpl in CANDIDATE_PATHS:
        url = BASE + tmpl.format(code=code)
        try:
            resp = requests.get(url, headers=HEADERS, cookies=cookies, timeout=20)
        except requests.RequestException:
            continue
        if resp.status_code == 200 and resp.text.strip().startswith(("{", "[")):
            try:
                return url, resp.json()
            except ValueError:
                continue
    return None


def public_summary(code: str) -> dict | None:
    resp = requests.get(f"{BASE}/api/problems", timeout=20)
    resp.raise_for_status()
    for p in resp.json().get("problems", []):
        if p["code"] == code:
            return p
    return None


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("code")
    parser.add_argument("--cookies", default=None)
    args = parser.parse_args(argv[1:])

    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    cookies = None
    if args.cookies:
        cookies_path = Path(os.path.expanduser(args.cookies))
        if not cookies_path.exists():
            print(f"warn: cookie file not found: {cookies_path}", file=sys.stderr)
        else:
            cookies = load_cookies(cookies_path)

    if cookies is not None:
        detail = try_detail(args.code, cookies)
        if detail:
            url, payload = detail
            print(f"# detail-source: {url}", file=sys.stderr)
            json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
            return 0

    print(
        "warn: detail unavailable (no/expired cookies); falling back to public summary",
        file=sys.stderr,
    )
    summary = public_summary(args.code)
    if summary is None:
        print(f"error: no such code '{args.code}'", file=sys.stderr)
        return 1
    json.dump({"source": "public-summary", "data": summary}, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
