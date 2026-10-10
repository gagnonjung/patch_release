"""Canonical A–F distribution notice shared by every patch page.

The wording follows the existing Zelda / Metal Gear Solid release pages.
Do not shorten or paraphrase it in individual projects.
"""
from __future__ import annotations
from html import escape
import re

INTRO = "파일 다운로드 전에 아래 사항을 반드시 확인 바랍니다."
LEGAL_ITEMS = (
    "원칙적으로, 해당 기종의 원본 디스크 또는 카트리지를 보유한 분이 개인적으로만 이용한다는 전제 하에 본 한글패치 파일을 다운로드할 수 있습니다.",
    "상기 A항 조건에 해당하지 않는 분이 본 한글패치 파일을 다운로드하여 이용할 경우에 발생하는 모든 책임은 이용 당사자에게 있으며, 패치 제작자는 어떠한 책임도 지지 않습니다.",
    "본 한글패치 파일 자체를 제작자의 허가 없이 타 사이트에 재배포하지 말아 주시고, 재배포를 원하실 경우 패치원본 게시물의 링크를 공유해 주시기 바랍니다.(아카이빙 포함)",
    "본 게시물의 본문 글 일부 또는 전체를 무단으로 옮겨 작성하지 말아 주시기 바랍니다. 단, 타 사이트에서 발췌하거나 인용한 문구에 대해서는 예외로 합니다.",
    "본 한글패치 파일을 이용하여 금전적 이득을 취하는 모든 행위를 일절 금합니다. 해당 행위로 발생하는 모든 책임은 이용 당사자에게 있으며, 패치 제작자는 어떠한 책임도 지지 않습니다.(패치 파일 자체 및 패치 롬 파일 판매, 패치 롬 카트리지 제작 및 판매, 웹하드 등 상업적 사이트 업로드, 토렌트 사이트 공유 등)",
    "상기 C·D·E항의 금지 행위가 적발된 경우, 또는 본 한글패치 파일 공유로 인해 원저작자 및 유통사, 기관의 요청이 있을 경우 예고 없이 게시물이 비공개 처리될 수 있으며, 향후 작업 예정인 작품의 한글패치 파일도 공유하지 않을 수 있습니다.",
)

def html_notice() -> str:
    lis = "\n".join(f"<li>{escape(item)}</li>" for item in LEGAL_ITEMS)
    return ('<section id="notice" class="section"><h2>파일 이용에 관한 권리 및 책임 고지</h2>'
            '<div class="legal"><p><strong>' + escape(INTRO) +
            '</strong></p><ol type="A">\n' + lis + '\n</ol></div></section>')

def audit_page(html: str) -> list[str]:
    """Check all six full, canonical items and the canonical intro."""
    missing = []
    if INTRO not in html:
        missing.append("intro")
    for index, text in enumerate(LEGAL_ITEMS):
        if text not in html:
            missing.append(chr(65 + index))
    return missing

if __name__ == "__main__":
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    paths = ["getter-robo-daikessen/index.html", "slayers-royal/index.html",
             "persona-2-innocent-sin/index.html", "zelda-mm/index.html", "patch.html"]
    bad = {p: audit_page((root / p).read_text(encoding="utf-8")) for p in paths}
    bad = {p: issues for p, issues in bad.items() if issues}
    if bad:
        print("NOTICE FAIL:", bad)
        raise SystemExit(1)
    print("NOTICE PASS: 5 pages × 6 canonical clauses")
