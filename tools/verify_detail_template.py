#!/usr/bin/env python3
"""Reject deviations from Hanmaru's approved Persona 2 patch detail layout.

Usage: python tools/verify_detail_template.py slam-dunk
No network, third-party dependencies, or game file access required.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "persona-2-innocent-sin" / "index.html"
STYLES = (
    "assets/css/detail-cover.css",
    "assets/css/support-banner.css",
    "assets/css/patch-warning.css",
    "assets/css/patch-history.css",
)
EXPECTED_SECTIONS = (
    "game", "overview", "features", "progress", "changelog",
    "source", "release", "install", "credits", "patch-warning", "notice",
)
REQUIRED_CLASSES = (
    "nav-inner", "shell", "hero-banner", "hero-copy", "hero-preview",
    "detail-cover", "body", "section", "sep", "grid", "fact", "scope",
    "qa", "test-env", "hash", "download", "download-link", "steps",
    "patch-warning", "legal",
)


class Markup(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.classes: set[str] = set()
        self.hrefs: list[str] = []
        self.sections: list[str] = []
        self.images: list[dict[str, str]] = []
        self.li_count = 0

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.append(str(attrs["id"]))
        self.classes.update((attrs.get("class") or "").split())
        if tag == "section":
            self.sections.append(attrs.get("id") or "")
        if tag == "a" and attrs.get("href"):
            self.hrefs.append(str(attrs["href"]))
        if tag == "img":
            self.images.append({k: str(v) for k, v in attrs.items() if v is not None})
        if tag == "li":
            self.li_count += 1


def region(data: str, start: str, end: str) -> str:
    s = data.find(start)
    if s < 0:
        raise AssertionError(f"section missing: {start}")
    e = data.find(end, s)
    if e < 0:
        raise AssertionError(f"section end missing: {end}")
    return data[s:e + len(end)]


def audit(slug: str) -> None:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        raise AssertionError("slug must be a repository directory name")
    ref = REFERENCE.read_text(encoding="utf-8")
    candidate = (ROOT / slug / "index.html").read_text(encoding="utf-8")
    r, c = Markup(), Markup()
    r.feed(ref)
    c.feed(candidate)
    assert len(c.ids) == len(set(c.ids)), "duplicate ID"
    assert tuple(c.sections) == EXPECTED_SECTIONS, f"section ordering drift: {c.sections}"
    missing = set(REQUIRED_CLASSES) - c.classes
    assert not missing, f"missing shared layout classes: {sorted(missing)}"
    assert len(re.findall(r"<style>", candidate)) == 1
    assert region(candidate, "<style>", "</style>") == region(ref, "<style>", "</style>"), "CSS differs from approved Persona 2 template"
    assert region(candidate, '<section class="section patch-warning"', "</ol></div></section>") == region(ref, '<section class="section patch-warning"', "</ol></div></section>"), "approved warning / A-F rights notice differs"
    assert '<figure class="hero-preview detail-cover">' in candidate, "shared square cover layout missing"
    assert "class=\"test-env\"" in candidate, "red bold test status missing"
    assert "미검증" in candidate, "must distinguish runtime from static verification"
    assert "<ol class=\"steps\">" in candidate, "install guide missing"
    assert candidate.count("https://drive.google.com/file/d/") <= 1, "unexpected duplicate Drive URL"
    assert re.search(r"[a-fA-F0-9]{64}", candidate), "verified SHA-256 metadata absent"
    for style in STYLES:
        css_path = ROOT / style
        assert css_path.is_file(), f"missing shared stylesheet: {style}"
        assert f'../{style}' in candidate, f"not linked: {style}"
    cover = (ROOT / "assets/css/detail-cover.css").read_text(encoding="utf-8")
    assert "360px" in cover and "16px" in cover and "object-fit: contain" in cover, "cover sizing drift"
    assert all(src.get("alt") for src in c.images if "support" not in src.get("class", "")), "missing image alt"
    assert all(href[1:] in c.ids for href in c.hrefs if href.startswith("#")), "broken in-page navigation"
    assert ".hero-banner" in candidate and "@media(max-width:760px)" in candidate, "mobile layout missing"
    assert "../assets/css/slam-dunk.css" not in candidate, "legacy dedicated layout returned"
    print(f"PASS: {slug}/index.html — CSS / 11 sections / cover / warning A-F / links / mobile")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python tools/verify_detail_template.py <slug>")
    audit(sys.argv[1])
