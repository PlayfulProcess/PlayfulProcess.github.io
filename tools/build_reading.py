"""Build reading.json (the "Reading with" section) and feed.xml (this home's own feed).

Run by .github/workflows/reading.yml once a day; run it by hand with `python tools/build_reading.py`.
Standard library only. A source that fails keeps its items from the last run.

Add or remove a person by editing SOURCES below.
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_JSON = ROOT / "reading.json"
OUT_FEED = ROOT / "feed.xml"
HOME = "https://playfulprocess.github.io/"
PER_SOURCE = 3

# The open repositories behind recursive.eco's study sites: their commits are recursive.eco being built in the open.
OPEN_REPOS = ["recursive-tarot", "recursive-iching", "recursive-astrology", "recursive-repatterning", "PlayfulProcess.github.io"]

SOURCES = [
    {
        "id": "playfulprocess",
        "name": "PlayfulProcess",
        "kind": "Writing",
        "site": "https://www.playfulprocess.com/",
        "icon": "icons/playfulprocess-logo.svg",
        "feeds": ["https://www.playfulprocess.com/feed"],
    },
    {
        "id": "recursive-eco",
        "name": "recursive.eco",
        "kind": "Built in the open",
        "site": "https://recursive.eco/",
        "icon": "icons/recursive-logo.svg",
        "feeds": [f"https://github.com/PlayfulProcess/{r}/commits/main.atom" for r in OPEN_REPOS],
        "commits": True,
        "follow": "feed.xml",
    },
    {
        "id": "martin-fowler",
        "name": "Martin Fowler",
        "kind": "Software design",
        "site": "https://martinfowler.com/",
        "icon": "https://martinfowler.com/favicon.ico",
        "feeds": ["https://martinfowler.com/feed.atom"],
    },
    {
        "id": "john-onolan",
        "name": "John O'Nolan",
        "kind": "Ghost, open source",
        "site": "https://john.onolan.org/",
        "icon": "https://john.onolan.org/favicon.ico",
        "feeds": ["https://john.onolan.org/rss/"],
    },
]

ATOM = "{http://www.w3.org/2005/Atom}"
UA = "PlayfulProcess-home-reading/1.0 (+https://playfulprocess.github.io/)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/atom+xml, application/rss+xml, application/xml;q=0.9, */*;q=0.5"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def parse_date(text):
    text = (text or "").strip()
    if not text:
        return None
    try:
        d = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        try:
            d = parsedate_to_datetime(text)
        except (TypeError, ValueError):
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)


def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def entries(xml_bytes):
    """Yield (title, url, date, author) from an Atom or RSS 2.0 document."""
    root = ET.fromstring(xml_bytes)
    if root.tag == ATOM + "feed":
        for e in root.findall(ATOM + "entry"):
            link = next((l.get("href") for l in e.findall(ATOM + "link") if l.get("rel", "alternate") == "alternate"), None)
            date = parse_date(e.findtext(ATOM + "published") or e.findtext(ATOM + "updated"))
            yield clean(e.findtext(ATOM + "title")), link, date, clean(e.findtext(ATOM + "author/" + ATOM + "name"))
    else:
        for i in root.iter("item"):
            yield clean(i.findtext("title")), clean(i.findtext("link")), parse_date(i.findtext("pubDate")), ""


def commit_title(title, author):
    """Keep commits a person wrote; drop bots and housekeeping."""
    if not title or "[bot]" in author or author.lower() in ("github-actions", "dependabot"):
        return None
    if re.match(r"(?i)^(chore|ci|build)(\(|:)", title) or "[skip ci]" in title or title.lower().startswith("merge branch"):
        return None
    return re.sub(r"^Merge (PR|pull request) #\d+[:\s]*(from \S+\s*)?", "", title).strip() or None


def collect(source):
    items = []
    for url in source["feeds"]:
        repo = re.search(r"PlayfulProcess/([^/]+)/commits", url)
        for title, link, date, author in entries(fetch(url)):
            if source.get("commits"):
                title = commit_title(title, author)
                if title and repo:
                    title = f"{title} ({repo.group(1).replace('recursive-', '').replace('PlayfulProcess.github.io', 'home')})"
            if not title or not link or not link.startswith("https://") or not date:
                continue
            items.append({"title": title, "url": link, "date": date.isoformat().replace("+00:00", "Z")})
    items.sort(key=lambda x: x["date"], reverse=True)
    seen, out = set(), []
    for it in items:
        key = re.sub(r"[^a-z0-9]+", "", it["title"].lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out


def write_feed(sources):
    """This home's own Atom feed: PlayfulProcess's writing and recursive.eco's open work."""
    mine = [dict(it, by=s["name"]) for s in sources if s["id"] in ("playfulprocess", "recursive-eco") for it in s.get("all", s["items"])]
    mine.sort(key=lambda x: x["date"], reverse=True)
    mine = mine[:30]
    updated = mine[0]["date"] if mine else datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        "  <title>PlayfulProcess</title>",
        "  <subtitle>Writing, and recursive.eco built in the open</subtitle>",
        f'  <link rel="alternate" type="text/html" href="{HOME}"/>',
        f'  <link rel="self" type="application/atom+xml" href="{HOME}feed.xml"/>',
        f"  <id>{HOME}</id>",
        f"  <updated>{updated}</updated>",
        "  <author><name>PlayfulProcess</name></author>",
    ]
    for it in mine:
        lines += [
            "  <entry>",
            f"    <title>{escape(it['title'])}</title>",
            f'    <link rel="alternate" href="{escape(it["url"])}"/>',
            f"    <id>{escape(it['url'])}</id>",
            f"    <updated>{it['date']}</updated>",
            f"    <category term=\"{escape(it['by'])}\"/>",
            "  </entry>",
        ]
    lines.append("</feed>")
    OUT_FEED.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main():
    previous = {}
    if OUT_JSON.exists():
        previous = {s["id"]: s for s in json.loads(OUT_JSON.read_text(encoding="utf-8")).get("sources", [])}
    out, failed = [], []
    for src in SOURCES:
        entry = {k: src[k] for k in ("id", "name", "kind", "site", "icon")}
        entry["feed"] = src.get("follow") or src["feeds"][0]
        try:
            got = collect(src)
            entry["items"], entry["all"] = got[:PER_SOURCE], got
        except Exception as exc:  # keep last run's items; report and carry on
            failed.append(f"{src['id']}: {exc}")
            entry["items"] = previous.get(src["id"], {}).get("items", [])
        out.append(entry)
    newest = max((s["items"][0]["date"] for s in out if s["items"]), default=None)
    write_feed(out)
    for s in out:
        s.pop("all", None)
    # "updated" is the newest item, not the run time, so a quiet day makes no commit.
    OUT_JSON.write_text(json.dumps({"newest": newest, "sources": out}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    for f in failed:
        print("WARN", f, file=sys.stderr)
    print(f"reading.json: {sum(len(s['items']) for s in out)} items from {len(out)} sources; feed.xml written")


if __name__ == "__main__":
    main()
