#!/usr/bin/env python3
"""Fetch a single brunch.co.kr article and emit it as markdown on stdout."""
from __future__ import annotations

import re
import sys

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def fetch(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")

    title_tag = soup.find("h1", class_="cover_title") or soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else url.rsplit("/", 1)[-1]

    body = soup.find("div", class_="wrap_body") or soup.body
    if body is None:
        raise RuntimeError(f"could not locate body for {url}")

    markdown = md(str(body), heading_style="ATX")
    markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()

    return f"# {title}\n\nSource: {url}\n\n{markdown}\n"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: fetch_one.py <brunch-url>", file=sys.stderr)
        return 2
    # Windows consoles default to cp1252; force utf-8 so Korean output works.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(fetch(argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
