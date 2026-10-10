"""Pure website publisher: validate, preview, render and safely commit/push.

Standard library only; interactive UI is in site_publisher.py.
Do not edit the user's existing dirty checkout. Publishing uses a temporary
detached Git worktree based on the latest origin/main.
"""
from __future__ import annotations

import base64
from datetime import date
from html import escape
import json
import mimetypes
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import urlsplit

from site_legal import html_notice, audit_page

FIELDS = {
    "slug": "페이지 주소 (영문/숫자/하이픈)",
    "title_ko": "게임명 (한국어)",
    "title_en": "게임명 (원어/영문)",
    "platform": "기종",
    "region": "대상 지역 / 버전",
    "genre": "장르",
    "original_release": "원작 발매일",
    "patch_version": "패치 버전",
    "patch_date": "패치 배포일",
    "status": "배포 상태",
    "intro": "게임 소개 / 패치 설명",
    "features": "한국어화 범위 (줄바꿈으로 항목 구분)",
    "notes": "수정 내역 (줄바꿈으로 항목 구분)",
    "known_issues": "미완료·검수 사항",
    "original_filename": "일본판 원본 파일명",
    "original_sha256": "원본 SHA-256",
    "patch_filename": "배포 ZIP 파일명",
    "patch_sha256": "배포 ZIP SHA-256",
    "download_url": "다운로드 URL (Google Drive 등)",
    "credits": "제작·검수",
    "cover_file": "표지 이미지 (로컬 파일)",
    "screenshot1": "화면 예시 1 (로컬 파일)",
    "screenshot2": "화면 예시 2 (로컬 파일)",
    "screenshot3": "화면 예시 3 (로컬 파일)",
}
PLATFORMS = {
    "Sony PlayStation": ("platform-ps1", "assets/images/platform-ps1.png"),
    "Sega Saturn": ("platform-saturn", ""),
    "Nintendo 64": ("platform-n64", "assets/images/platform-n64.png"),
    "Nintendo GameCube": ("platform-gc", "assets/images/platform-gamecube.png"),
    "Super Famicom": ("platform-n64", ""),
    "Other": ("platform-ps1", ""),
}
VALID_IMAGE_SUFFIX = {".png", ".jpg", ".jpeg", ".webp"}
IMAGE_MAX_BYTES = 16 * 1024 * 1024
HEX64 = re.compile(r"^[a-fA-F0-9]{64}$")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED = {"assets", "tools", "release", "site_publisher", "zelda-mm", "persona-2-innocent-sin",
            "getter-robo-daikessen", "slayers-royal"}
DEFAULT = {
    "slug": "", "title_ko": "", "title_en": "", "platform": "Sony PlayStation",
    "region": "Japan", "genre": "RPG", "original_release": "",
    "patch_version": "v1.0", "patch_date": date.today().strftime("%Y.%m.%d"),
    "status": "배포 준비 중", "intro": "", "features": "", "notes": "",
    "known_issues": "", "original_filename": "", "original_sha256": "",
    "patch_filename": "", "patch_sha256": "", "download_url": "",
    "credits": "한마루", "cover_file": "", "screenshot1": "", "screenshot2": "", "screenshot3": "",
}
STYLES = """
:root{--paper:#1d2231;--bg:#101520;--line:#465067;--text:#edf0f5;--sub:#c5ccda;--accent:#e6b9d2}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:linear-gradient(180deg,#302439,#101520 660px);color:var(--text);font:15px/1.75 "Malgun Gothic","Apple SD Gothic Neo",system-ui,sans-serif}
a{color:inherit}.nav{background:#191e2b;border-bottom:1px solid var(--line)}
.nav-inner{max-width:980px;margin:auto;padding:15px 24px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:18px}
.nav-inner a{text-decoration:none;font-weight:700;font-size:13px}
.shell{max-width:980px;margin:28px auto 56px;border:1px solid #4a4d65;border-radius:20px;overflow:hidden;background:var(--paper);box-shadow:0 18px 55px #0004}
.hero{display:grid;grid-template-columns:minmax(0,1.12fr) minmax(250px,.88fr);align-items:center;gap:clamp(22px,4vw,48px);min-height:390px;padding:clamp(26px,4.5vw,50px);border-bottom:1px solid #56506b;background:linear-gradient(125deg,#402841,#232438)}
.eyebrow{font-size:12px;letter-spacing:.12em;font-weight:800;color:var(--accent)}
h1{font-size:clamp(30px,4vw,42px);line-height:1.2;margin:12px 0 6px;letter-spacing:-.04em}
.subtitle{font-size:18px;color:#d2d6e1;margin:0 0 20px}
.pills{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px}
.pills span{padding:5px 12px;border:1px solid #665a77;border-radius:99px;background:#352f46;font-size:12px}
.lead{margin:0;color:#e2e5ef;line-height:1.9}
.hero-cover{margin:0;min-width:0;align-self:stretch;display:flex;align-items:center;justify-content:center;padding:16px;border:1px solid #665975;border-radius:15px;background:#171d2a;box-shadow:0 12px 30px #0004;min-height:280px}
.hero-cover img{display:block;width:100%;height:auto;max-height:350px;object-fit:contain}
.no-cover{font-size:16px;color:#bbc0d0;text-align:center}
.body{padding:36px clamp(20px,5.5vw,62px) 48px}
section{margin:0 0 30px}h2{font-size:21px;margin:0 0 14px;letter-spacing:-.02em}
.fact-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 20px}
.fact{display:grid;grid-template-columns:108px minmax(0,1fr);gap:10px;border-bottom:1px solid #384056;padding:12px 0;font-size:13px}
.fact b{color:#aeb9cf;font-weight:600}.fact span{overflow-wrap:anywhere}
hr{border:0;border-top:1px solid #40485e;margin:32px 0}
.muted{font-size:13px;color:var(--sub);overflow-wrap:anywhere}
.scope{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.scope article,.noticebox{padding:16px;background:#151d2e;border:1px solid #3b455e;border-radius:10px}
.scope article{font-size:13px}.screens{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.screens img{display:block;width:100%;height:150px;object-fit:contain;background:#0f1422;border-radius:8px}
.notes{padding-left:22px;font-size:13px;color:#d5dbe7}
.hash{font:12px/1.8 Consolas,ui-monospace,monospace;overflow-wrap:anywhere}
.download{border:1px solid #6a6179;border-radius:12px;padding:20px;background:#302e43}
.download .btn{display:inline-block;padding:10px 20px;border-radius:9px;background:#ead3ec;color:#1c1a28;font-weight:800;text-decoration:none;margin-top:13px}
.disabled{display:inline-block;background:#4a4e60;color:#d1d3db;padding:10px 18px;border-radius:9px;margin-top:13px}
.legal{border:1px solid #46536a;background:#151c2b;border-radius:12px;padding:21px}
.legal p{font-size:13px}.legal ol{padding-left:23px;font-size:13px;display:grid;gap:12px;line-height:1.85}
.legal li{padding-left:4px;overflow-wrap:anywhere}
footer{max-width:980px;margin:auto;padding:0 24px 40px;color:#9da6b9;font-size:12px}
@media(max-width:760px){.hero{grid-template-columns:1fr;gap:25px;padding:28px 22px;min-height:0}.hero-cover{width:min(100%,380px);margin:0 auto;align-self:auto;padding:14px}.hero-cover img{max-height:340px}.fact-grid,.scope,.screens{grid-template-columns:1fr}.body{padding:25px 22px 36px}.shell{border-radius:0;margin:0 auto 25px;border-left:0;border-right:0}}
"""

class PublishError(RuntimeError):
    pass

def h(s: object) -> str:
    return escape(str(s or ""), quote=True)

def merged(data: dict) -> dict:
    return {key: str(data.get(key, default) or "") for key, default in DEFAULT.items()}

def validate(data: dict, allow_existing: bool = True) -> dict:
    d = merged(data)
    slug = d["slug"]
    if not SLUG.fullmatch(slug):
        raise PublishError("페이지 주소는 영문 소문자·숫자·하이픈만 사용할 수 있습니다")
    if slug in RESERVED and not allow_existing:
        raise PublishError("기존 홈페이지 경로는 편집기 관리 데이터 없이 덮어쓸 수 없습니다")
    for key in ("title_ko", "title_en", "platform", "patch_version", "status"):
        if not d[key].strip():
            raise PublishError(f"필수 입력: {FIELDS[key]}")
    if d["platform"] not in PLATFORMS:
        raise PublishError("지원하지 않는 플랫폼입니다")
    if d["status"] not in {"배포 중", "배포 준비 중"}:
        raise PublishError("배포 상태를 선택해 주세요")
    for field in ("original_sha256", "patch_sha256"):
        if d[field] and not HEX64.fullmatch(d[field]):
            raise PublishError(f"{FIELDS[field]} 값은 64자리 SHA-256이어야 합니다")
    if d["download_url"]:
        link = urlsplit(d["download_url"])
        if link.scheme != "https" or not link.netloc or link.username or link.password:
            raise PublishError("다운로드 주소는 올바른 HTTPS 링크여야 합니다")
    if d["status"] == "배포 중":
        for field in ("patch_filename", "patch_sha256", "download_url"):
            if not d[field].strip():
                raise PublishError(f"배포 중에는 '{FIELDS[field]}'을 입력해야 합니다")
    for field in ("cover_file", "screenshot1", "screenshot2", "screenshot3"):
        if d[field]:
            src = Path(d[field]).expanduser()
            if not src.is_file():
                raise PublishError(f"이미지를 찾을 수 없습니다: {src}")
            if src.suffix.lower() not in VALID_IMAGE_SUFFIX or src.stat().st_size > IMAGE_MAX_BYTES:
                raise PublishError("이미지는 PNG/JPG/WEBP, 각각 16MB 이하만 지원합니다")
            sig = src.read_bytes()[:12]
            if not (sig[:3] == b"\xff\xd8\xff" or sig[:8] == b"\x89PNG\r\n\x1a\n" or
                    (sig[:4] == b"RIFF" and sig[8:12] == b"WEBP")):
                raise PublishError(f"지원하지 않는 이미지 형식입니다: {src}")
    return d

def render_page(data: dict, images: dict[str, str] | None = None) -> str:
    d = validate(data)
    images = images or {}
    cover = images.get("cover_file", "")
    hero = '<img src="' + h(cover) + '" alt="' + h(d["title_ko"]) + ' 표지 아트">' if cover else '<span class="no-cover">커버 아트 준비 중</span>'
    detail = [("게임명", d["title_ko"]), ("플랫폼", d["platform"]),
              ("지역 / 버전", d["region"]), ("장르", d["genre"]),
              ("원작 발매일", d["original_release"]), ("한국어 패치", d["patch_version"]),
              ("배포일", d["patch_date"]), ("제작 / 검수", d["credits"])]
    facts = "".join(f'<div class="fact"><b>{h(key)}</b><span>{h(value)}</span></div>' for key, value in detail if value)
    scope = "".join(f"<article>{h(line)}</article>" for line in d["features"].splitlines() if line.strip())
    notes = "".join(f"<li>{h(line)}</li>" for line in d["notes"].splitlines() if line.strip())
    shots = "".join('<img src="' + h(images[k]) + '" alt="게임 스크린샷 ' + str(i) + '">'
                    for i, k in enumerate(("screenshot1", "screenshot2", "screenshot3"), 1) if images.get(k))
    released = d["status"] == "배포 중"
    link = ('<a class="btn" href="' + h(d["download_url"]) +
            '" target="_blank" rel="noopener noreferrer">패치 다운로드 ↗</a>') if released else '<span class="disabled">배포 준비 중</span>'
    download = '<div class="download"><strong>' + h(d["patch_filename"] or "배포 준비 중") + '</strong>' + link
    if d["patch_sha256"]:
        download += '<p class="muted">ZIP SHA-256</p><div class="hash">' + h(d["patch_sha256"]) + '</div>'
    download += '</div>'
    original = ""
    if d["original_filename"]:
        original += "<p>" + h(d["original_filename"]) + "</p>"
    if d["original_sha256"]:
        original += '<p class="hash">' + h(d["original_sha256"]) + '</p>'
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{h(d['title_ko'])} 한국어 패치 {h(d['patch_version'])} 안내">
<title>{h(d['title_ko'])} — 한국어 패치 {h(d['patch_version'])}</title><style>{STYLES}</style><link rel="stylesheet" href="../assets/css/support-banner.css?v=20261010"></head>
<body><nav class="nav"><div class="nav-inner"><a href="../index.html">한마루 한글화 작업소</a><a href="#release">패치 다운로드</a><a class="support-coffee" href="https://litt.ly/hanmaru" target="_blank" rel="noopener noreferrer" aria-label="후원하기"><img src="https://www.owlstown.com/assets/icons/bmc-yellow-button-941f96a1.png" alt="후원하기" loading="eager"></a></div></nav>
<main class="shell"><section class="hero"><div><span class="eyebrow">{h(d['platform']).upper()} · KOREAN LOCALIZATION</span>
<h1>{h(d['title_ko'])}</h1><p class="subtitle">{h(d['title_en'])}</p>
<div class="pills"><span>{h(d['region'])}</span><span>{h(d['patch_version'])}</span><span>{h(d['status'])}</span></div>
<p class="lead">{h(d['intro'])}</p></div><figure class="hero-cover">{hero}</figure></section>
<div class="body"><section id="game"><h2>게임 정보</h2><div class="fact-grid">{facts}</div></section>
<hr><section id="features"><h2>한국어화 범위</h2><div class="scope">{scope or '<article>작업 범위 정리 중</article>'}</div></section>
{('<hr><section id="screens"><h2>스크린샷</h2><div class="screens">' + shots + '</div></section>') if shots else ''}
{('<hr><section id="updates"><h2>패치 내용</h2><ul class="notes">' + notes + '</ul></section>') if notes else ''}
{('<hr><section id="qa"><h2>검수·알려진 문제</h2><div class="noticebox">' + h(d['known_issues']) + '</div></section>') if d['known_issues'] else ''}
{('<hr><section id="original"><h2>지원 원본</h2>' + original + '</section>') if original else ''}
<hr><section id="release"><h2>패치 다운로드</h2>{download}</section>
<hr>{html_notice()}</div></main>
<footer>한마루 한글화 작업소 · {h(d['title_en'])} / {h(d['platform'])}</footer></body></html>
"""

def _image_data(file: str) -> str:
    p = Path(file)
    mime, _ = mimetypes.guess_type(p.name)
    return f"data:{mime or 'application/octet-stream'};base64," + base64.b64encode(p.read_bytes()).decode("ascii")

def preview(data: dict) -> Path:
    d = validate(data)
    paths = {key: _image_data(d[key]) for key in ("cover_file", "screenshot1", "screenshot2", "screenshot3") if d[key]}
    out = Path(tempfile.mkdtemp(prefix="site_publisher_preview_")) / "index.html"
    out.write_text(render_page(d, paths), encoding="utf-8")
    return out

def run_git(cwd: Path, args: list[str], *, timeout: int = 180) -> str:
    try:
        result = subprocess.run(["git", "-C", str(cwd), *args], text=True,
                                encoding="utf-8", errors="replace", capture_output=True,
                                timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PublishError(f"Git 실행 실패: {exc}") from exc
    if result.returncode:
        raise PublishError(f"Git {' '.join(args[:3])} 실패:\n{(result.stderr or result.stdout)[-1200:]}")
    return result.stdout.strip()

def _asset_uri(root: Path, data: dict, field: str) -> str:
    src = Path(data[field])
    target_dir = root / "assets" / "images" / data["slug"]
    target_dir.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower()
    filename = ("cover" if field == "cover_file" else field) + ext
    dst = target_dir / filename
    if src.resolve() != dst.resolve():
        shutil.copyfile(src, dst)
    return f"assets/images/{data['slug']}/{filename}"

def _card(d: dict, cover_uri: str) -> str:
    platform_class, logo_uri = PLATFORMS[d["platform"]]
    logo = f'<img src="{logo_uri}" alt="" aria-hidden="true">' if logo_uri else f'<span class="platform-wordmark">{h(d["platform"])}</span>'
    picture = f'<img src="{h(cover_uri)}" alt="{h(d["title_ko"])} 커버">' if cover_uri else f'<span class="thumb-placeholder"><strong>{h(d["title_en"])}</strong></span>'
    badge = '<span class="new-release-tag is-preview">PREVIEW</span>' if d["status"] != "배포 중" else '<span class="new-release-tag is-update">UPDATE</span>'
    return (f'        <a class="game-card" data-publisher-slug="{d["slug"]}" href="{d["slug"]}/">\n'
            f'          <div class="platform-strip {platform_class}">{logo}</div>\n'
            f'          <div class="thumb-frame">{badge}{picture}</div>\n'
            f'          <div class="card-meta"><time>{h(d["status"])} · {h(d["patch_version"])} · {h(d["patch_date"])}</time>'
            f'<h2>{h(d["title_ko"])}</h2></div>\n        </a>')

def _update_index(text: str, d: dict, cover: str) -> str:
    card = _card(d, cover)
    pattern = re.compile(r'\s*<a class="game-card" data-publisher-slug="' + re.escape(d["slug"]) + r'"[\s\S]*?</a>')
    if pattern.search(text):
        return pattern.sub("\n" + card, text, count=1)
    marker = '<div class="game-grid">'
    if text.count(marker) != 1:
        raise PublishError("메인 페이지의 게임 카드 영역을 찾을 수 없습니다")
    return text.replace(marker, marker + "\n" + card, 1)

def publish(repo: Path, data: dict, progress=lambda s: None) -> str:
    d = validate(data)
    repo = repo.expanduser().resolve()
    if not (repo / ".git").exists():
        raise PublishError("Git 저장소 경로가 아닙니다")
    top = Path(run_git(repo, ["rev-parse", "--show-toplevel"])).resolve()
    if repo != top:
        raise PublishError("저장소 최상위 경로를 선택해 주세요")
    if not (repo / "index.html").is_file():
        raise PublishError("홈페이지 index.html을 찾지 못했습니다")
    progress("GitHub 최신 main 확인 중...")
    run_git(repo, ["fetch", "origin", "main"], timeout=240)
    temp_root = Path(tempfile.mkdtemp(prefix="site_publisher_git_"))
    worktree = temp_root / "website"
    created = False
    success = False
    committed = False
    try:
        run_git(repo, ["worktree", "add", "--detach", str(worktree), "FETCH_HEAD"], timeout=240)
        created = True
        data_file = worktree / "site_publisher" / "entries" / (d["slug"] + ".json")
        page_file = worktree / d["slug"] / "index.html"
        if page_file.exists() and not data_file.exists():
            raise PublishError("기존 수동 제작 페이지를 자동으로 덮어쓰지 않습니다: " + d["slug"])
        # Confirm pages generated by an older app version use the same schema.
        image_uris = {}
        changed = [str(page_file.relative_to(worktree)), str(data_file.relative_to(worktree))]
        for field in ("cover_file", "screenshot1", "screenshot2", "screenshot3"):
            if d[field]:
                asset = _asset_uri(worktree, d, field)
                image_uris[field] = "../" + asset
                changed.append(asset)
            elif data_file.exists():
                # Keep previously published art if this edit leaves the field blank.
                try:
                    previous = json.loads(data_file.read_text(encoding="utf-8"))
                    old = previous.get("assets", {}).get(field, "")
                    if re.fullmatch(r"assets/images/[a-z0-9-]+/(?:cover|screenshot[123])\.(?:png|jpe?g|webp)", old):
                        image_uris[field] = "../" + old
                except (ValueError, OSError):
                    pass
        page_file.parent.mkdir(parents=True, exist_ok=True)
        page_html = render_page(d, image_uris)
        if audit_page(page_html):
            raise PublishError("공통 배포 고지 검증에 실패했습니다")
        page_file.write_text(page_html, encoding="utf-8")
        entry = {k: v for k, v in d.items() if k not in ("cover_file", "screenshot1", "screenshot2", "screenshot3")}
        entry["assets"] = {k: v[3:] for k, v in image_uris.items()}
        data_file.parent.mkdir(parents=True, exist_ok=True)
        data_file.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        home = worktree / "index.html"
        old_index = home.read_text(encoding="utf-8")
        cover_uri = image_uris.get("cover_file", "")[3:]
        if not cover_uri and "cover_file" in entry["assets"]:
            cover_uri = entry["assets"]["cover_file"]
        home.write_text(_update_index(old_index, d, cover_uri), encoding="utf-8")
        changed.append("index.html")
        progress("파일 생성·HTML 고지 검증 완료, 커밋 중...")
        run_git(worktree, ["add", "--", *sorted(set(changed))])
        if not run_git(worktree, ["diff", "--cached", "--name-only"]):
            raise PublishError("변경사항이 없습니다")
        run_git(worktree, ["diff", "--cached", "--check"])
        run_git(worktree, ["commit", "-m", f"Publish {d['title_en']} {d['patch_version']} site page"])
        committed = True
        commit = run_git(worktree, ["rev-parse", "--short", "HEAD"])
        progress(f"커밋 {commit} 생성, GitHub main으로 푸시 중...")
        run_git(worktree, ["push", "origin", "HEAD:refs/heads/main"], timeout=240)
        progress(f"완료: {commit} → origin/main")
        success = True
        return commit
    finally:
        if created and (success or not committed):
            try:
                run_git(repo, ["worktree", "remove", "--force", str(worktree)], timeout=60)
            except PublishError as exc:
                progress(f"임시 작업 공간 정리 경고: {exc}")
        elif created and committed:
            progress(f"푸시 실패: 커밋은 임시 작업 공간에 보존했습니다: {worktree}")
        if success or not committed:
            shutil.rmtree(temp_root, ignore_errors=True)

def load_published(repo: Path, slug: str) -> dict:
    """Load a page previously created by the publisher from remote main."""
    if not SLUG.fullmatch(slug):
        raise PublishError("올바른 게임 페이지 주소를 입력해 주세요")
    repo = repo.expanduser().resolve()
    run_git(repo, ["fetch", "origin", "main"], timeout=240)
    raw = run_git(repo, ["show", f"FETCH_HEAD:site_publisher/entries/{slug}.json"])
    try:
        data = json.loads(raw)
    except ValueError as exc:
        raise PublishError("게시된 페이지의 관리 데이터가 올바르지 않습니다") from exc
    if not isinstance(data, dict) or data.get("slug") != slug:
        raise PublishError("게시된 페이지의 게임 주소가 일치하지 않습니다")
    return data


def draft_directory() -> Path:
    folder = Path.home() / ".hanmaru_site_publisher" / "drafts"
    folder.mkdir(parents=True, exist_ok=True)
    return folder
