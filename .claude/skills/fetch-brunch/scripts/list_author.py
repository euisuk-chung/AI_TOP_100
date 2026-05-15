#!/usr/bin/env python3
"""List articles on a brunch.co.kr author page as JSON.

usage: list_author.py @username [--filter KEYWORD] [--max N]

Brunch's author page is a JS-heavy SPA, but the article URLs follow a stable
numeric scheme: `https://brunch.co.kr/@user/{id}`. We probe a contiguous range
of ids and capture (title, id) for the ones that exist.

This is intentionally pragmatic — brunch's article-list API is undocumented and
the public HTML uses lazy-rendered React. Probing by id is fast enough for our
purposes (a few dozen requests) and avoids fighting the SPA.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def probe(user: str, article_id: int) -> dict | None:
    url = f"https://brunch.co.kr/{user}/{article_id}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
    except requests.RequestException:
        return None
    if resp.status_code != 200:
        return None
    soup = BeautifulSoup(resp.content, "html.parser")
    h1 = soup.find("h1", class_="cover_title")
    title = h1.get_text(strip=True) if h1 else None
    if not title:
        meta = soup.find("meta", attrs={"property": "og:title"})
        title = meta["content"].strip() if meta and meta.get("content") else None
    if not title:
        return None
    return {"id": article_id, "title": title, "url": url}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("user", help="brunch username, with leading @")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=400)
    parser.add_argument("--filter", default=None, help="keyword to require in title")
    parser.add_argument("--max", type=int, default=None, help="limit number of results")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args(argv[1:])

    user = args.user if args.user.startswith("@") else f"@{args.user}"

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(probe, user, i): i for i in range(args.start, args.end + 1)}
        for fut in as_completed(futures):
            item = fut.result()
            if item is None:
                continue
            if args.filter and args.filter.lower() not in item["title"].lower():
                continue
            results.append(item)

    results.sort(key=lambda r: r["id"])
    if args.max:
        results = results[-args.max:]

    sys.stdout.reconfigure(encoding="utf-8")
    json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
