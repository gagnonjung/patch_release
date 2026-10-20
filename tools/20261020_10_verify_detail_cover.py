"""Verify consistent cover frames across all per-game detail pages.
No commits, pushes, game binaries, or existing screenshots are touched.
"""
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "patch.html",
    "persona-2-innocent-sin/index.html",
    "slam-dunk/index.html",
    "slayers-royal/index.html",
    "getter-robo-daikessen/index.html",
    "zelda-mm/index.html",
    "zelda-oot/index.html",
    "zelda-oot-ura/index.html",
]
CSS = ROOT / "assets/css/detail-cover.css"


class DetailParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.figure_count = 0
        self.art_count = 0
        self.links = []
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "link" and "stylesheet" in d.get("rel", ""):
            self.links.append(d.get("href", "").split("?")[0])
        if tag == "figure" and "detail-cover" in d.get("class", "").split():
            self.figure_count += 1
            self.depth += 1
        elif self.depth and tag == "img":
            self.art_count += 1

    def handle_endtag(self, tag):
        if tag == "figure" and self.depth:
            self.depth -= 1


def verify():
    rules = CSS.read_text(encoding="utf-8")
    assert rules.count("{") == rules.count("}"), "Unbalanced CSS braces"
    for rule in ("figure.detail-cover", "aspect-ratio: 1 / 1",
                 "padding: 16px !important", "object-fit: contain !important",
                 "max-height: 100% !important"):
        assert rule in rules, f"Missing CSS rule: {rule}"
    for page in PAGES:
        p = ROOT / page
        markup = p.read_text(encoding="utf-8")
        parser = DetailParser()
        parser.feed(markup)
        assert parser.figure_count == 1, f"{page}: expected one detail cover, got {parser.figure_count}"
        assert parser.art_count == 1, f"{page}: expected one cover image, got {parser.art_count}"
        style = "assets/css/detail-cover.css" if page == "patch.html" else "../assets/css/detail-cover.css"
        assert style in parser.links, f"{page}: missing stylesheet"
        assert (p.parent / style).resolve() == CSS.resolve(), f"{page}: wrong stylesheet path"
        assert "<main" in markup and "</main>" in markup, f"{page}: invalid main markup"
        print("PASS", page)
    print(f"PASS {len(PAGES)} cover frames; consistent 360px square / 16px inset / contain")


if __name__ == "__main__":
    verify()
