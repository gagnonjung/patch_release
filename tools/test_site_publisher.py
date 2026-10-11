"""Offline QA for the publisher; never pushes to the real website."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_legal import INTRO, LEGAL_ITEMS, audit_page
from site_publisher_core import PublishError, preview, publish, load_published, render_page, validate


def git(path: Path, *args):
    proc = subprocess.run(["git", "-C", str(path), *args], text=True,
                          encoding="utf-8", capture_output=True)
    if proc.returncode:
        raise AssertionError(f"Git {' '.join(args)} failed: {proc.stderr}")
    return proc.stdout.strip()


class SitePublisherTest(unittest.TestCase):
    def setUp(self):
        self.data = {
            "slug": "test-game-release",
            "title_ko": "테스트 <게임>",
            "title_en": "Test Game",
            "platform": "Sega Saturn",
            "status": "배포 준비 중",
            "patch_version": "v0.1",
            "intro": "한국어화 & 이미지",
            "features": "대사\n그래픽",
            "notes": "텍스트 검수",
        }

    def test_legal_same_on_all_five_projects(self):
        root = Path(__file__).resolve().parent.parent
        for name in ("getter-robo-daikessen/index.html", "slayers-royal/index.html",
                     "persona-2-innocent-sin/index.html", "zelda-mm/index.html", "patch.html"):
            with self.subTest(name=name):
                html = (root / name).read_text(encoding="utf-8")
                self.assertEqual([], audit_page(html))
                self.assertTrue(all(html.count(c) == 1 for c in LEGAL_ITEMS))
                self.assertEqual(1, html.count(INTRO))

    def test_preview_and_xss(self):
        d = validate(self.data)
        html = render_page(d)
        self.assertEqual([], audit_page(html))
        self.assertIn("테스트 &lt;게임&gt;", html)
        self.assertIn("한국어화 &amp; 이미지", html)
        self.assertIn('class="hero-cover"', html)
        self.assertNotIn("<h1>테스트 <게임>", html)
        file = preview(d)
        self.assertTrue(file.is_file())
        self.assertEqual([], audit_page(file.read_text(encoding="utf-8")))

    def test_coffee_banner_on_all_pages_and_generated_template(self):
        root = Path(__file__).resolve().parent.parent
        expected_url = 'href="https://litt.ly/hanmaru"'
        expected_icon = 'bmc-yellow-button-941f96a1.png'
        for name in ("getter-robo-daikessen/index.html", "slayers-royal/index.html",
                     "persona-2-innocent-sin/index.html", "zelda-mm/index.html", "patch.html"):
            with self.subTest(name=name):
                text = (root / name).read_text(encoding="utf-8")
                self.assertEqual(1, text.count(expected_url))
                self.assertEqual(1, text.count(expected_icon))
                self.assertEqual(1, text.count("support-banner.css?v=20261010"))
        sample = render_page(validate(self.data))
        self.assertEqual(1, sample.count(expected_url))
        self.assertEqual(1, sample.count(expected_icon))
        self.assertEqual(1, sample.count("support-banner.css?v=20261010"))

    def test_patch_history_on_all_other_projects(self):
        root = Path(__file__).resolve().parent.parent
        for path in ("getter-robo-daikessen/index.html",
                     "persona-2-innocent-sin/index.html",
                     "zelda-mm/index.html", "zelda-oot/index.html",
                     "zelda-oot-ura/index.html", "patch.html"):
            with self.subTest(page=path):
                source = (root / path).read_text("utf-8")
                self.assertEqual(1, source.count('<details class="history">'))
                self.assertEqual(1, source.count('id="changelog"'))
                self.assertEqual(1, source.count("assets/css/patch-history.css?v=20261011"))
                self.assertIn("버전별 상세 변경 내역 펼치기", source)
                self.assertTrue('id="download"' in source or 'id="release"' in source)
        data = {**self.data, "notes": "맞춤법 정리\nUI 보완"}
        generated = render_page(data)
        self.assertEqual(1, generated.count('<details class="history">'))
        self.assertEqual(1, generated.count('assets/css/patch-history.css?v=20261011'))
        self.assertIn("맞춤법 정리", generated)

    def test_red_warning_below_production_qa_in_all_projects(self):
        root = Path(__file__).resolve().parent.parent
        warning = "본 한국어 패치의 임의 변조나 타기종으로의 포팅, 동의 없는 재배포는 허가하지 않습니다. 판매 또한 금지됩니다."
        stylesheet = (root / "assets/css/patch-warning.css").read_text("utf-8")
        self.assertIn("color:#ff9ca3", stylesheet)
        for rel in ("slayers-royal/index.html", "getter-robo-daikessen/index.html",
                    "persona-2-innocent-sin/index.html", "zelda-mm/index.html",
                    "zelda-oot/index.html", "zelda-oot-ura/index.html", "patch.html"):
            with self.subTest(page=rel):
                page = (root / rel).read_text("utf-8")
                self.assertEqual(1, page.count('id="patch-warning"'))
                self.assertEqual(1, page.count(warning))
                self.assertIn("assets/css/patch-warning.css?v=20261012", page)
                credit_heads = ("제작 및 검수", "패치 제작 및 테스트",
                                "제작 및 테스트 정보", "패치 정보 및 테스트")
                self.assertTrue(any(heading in page[:page.index('id="patch-warning"')]
                                    for heading in credit_heads))
                self.assertIn("파일 이용에 관한 권리 및 책임 고지", page)
        generated = render_page(self.data)
        self.assertEqual(1, generated.count('id="patch-warning"'))
        self.assertEqual(1, generated.count(warning))
        self.assertIn('color:#ff9ca3', generated)
        self.assertLess(generated.index('id="credits"'), generated.index('id="patch-warning"'))

    def test_invalid_fields(self):
        for val in ("../danger", "a/b", "UPPER", "", "a..b"):
            with self.subTest(val=val):
                with self.assertRaises(PublishError):
                    validate({**self.data, "slug": val})
        with self.assertRaises(PublishError):
            validate({**self.data, "status": "배포 중"})
        with self.assertRaises(PublishError):
            validate({**self.data, "original_sha256": "invalid"})
        with self.assertRaises(PublishError):
            validate({**self.data, "download_url": "javascript:alert(1)"})

    def test_publish_and_update_with_local_remote(self):
        with tempfile.TemporaryDirectory(prefix="publisher_test_") as tmp:
            base = Path(tmp)
            remote, local = base / "remote.git", base / "local"
            remote.mkdir()
            git(remote, "init", "--bare", "--initial-branch=main")
            local.mkdir()
            git(local, "init", "--initial-branch=main")
            git(local, "config", "user.name", "QA Test")
            git(local, "config", "user.email", "qa@example.invalid")
            (local / "index.html").write_text('<html><div class="game-grid">\n</div></html>', encoding="utf-8")
            (local / "sample.txt").write_text("original", encoding="utf-8")
            git(local, "add", "index.html", "sample.txt")
            git(local, "commit", "-m", "Init")
            git(local, "remote", "add", "origin", str(remote))
            git(local, "push", "-u", "origin", "main")
            # Keep unrelated changes in the main local workspace; publisher must preserve them.
            (local / "sample.txt").write_text("uncommitted modification", encoding="utf-8")
            d = {**self.data, "title_ko": "테스트게임"}
            published = publish(local, d)
            self.assertTrue(published)
            self.assertEqual("uncommitted modification", (local / "sample.txt").read_text(encoding="utf-8"))
            self.assertFalse((local / d["slug"]).exists())
            home = git(local, "show", "origin/main:index.html")
            self.assertEqual(1, home.count('data-publisher-slug="test-game-release"'))
            html = git(local, "show", f"origin/main:{d['slug']}/index.html")
            self.assertEqual([], audit_page(html))
            self.assertIn("테스트게임", html)
            obj = json.loads(git(local, "show", f"origin/main:site_publisher/entries/{d['slug']}.json"))
            self.assertEqual("테스트게임", obj["title_ko"])
            self.assertEqual("테스트게임", load_published(local, d["slug"])["title_ko"])
            updated = publish(local, {**d, "patch_version": "v0.2"})
            self.assertTrue(updated)
            updated_html = git(local, "show", f"origin/main:{d['slug']}/index.html")
            self.assertIn("v0.2", updated_html)
            home = git(local, "show", "origin/main:index.html")
            self.assertEqual(1, home.count('data-publisher-slug="test-game-release"'))

    def test_legacy_page_protection(self):
        # A pre-existing manually edited page must never be automatically replaced.
        with tempfile.TemporaryDirectory(prefix="publisher_legacy_") as tmp:
            base = Path(tmp)
            remote, local = base / "remote.git", base / "local"
            remote.mkdir()
            git(remote, "init", "--bare", "--initial-branch=main")
            local.mkdir()
            git(local, "init", "--initial-branch=main")
            git(local, "config", "user.name", "QA Test")
            git(local, "config", "user.email", "qa@example.invalid")
            (local / "index.html").write_text('<div class="game-grid"></div>', encoding="utf-8")
            target = local / "test-game-release"
            target.mkdir()
            (target / "index.html").write_text("manual page DO NOT EDIT", encoding="utf-8")
            git(local, "add", "index.html", "test-game-release/index.html")
            git(local, "commit", "-m", "Init")
            git(local, "remote", "add", "origin", str(remote))
            git(local, "push", "-u", "origin", "main")
            with self.assertRaisesRegex(PublishError, "수동 제작"):
                publish(local, self.data)
            self.assertEqual("manual page DO NOT EDIT",
                             git(local, "show", "origin/main:test-game-release/index.html"))


if __name__ == "__main__":
    unittest.main()
