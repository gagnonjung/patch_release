"""Headless Edge render checks for shared detail-cover layout. Saves review captures only."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
edge = next((p for p in (
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
) if p.is_file()), None)
if not edge:
    raise RuntimeError("Microsoft Edge not found")
outdir = root / "tools" / "20261020_05_site_preview"
outdir.mkdir(exist_ok=True)
items = [
    ("patch.html", "mgs-desktop", "1440,1000"),
    ("persona-2-innocent-sin/index.html", "persona-desktop", "1440,1000"),
    ("slayers-royal/index.html", "slayers-desktop", "1440,1000"),
    ("slam-dunk/index.html", "slam-desktop", "1440,1000"),
    ("slam-dunk/index.html", "slam-mobile", "520,900"),
    ("zelda-mm/index.html", "zelda-mobile", "520,900"),
]
for page, label, viewport in items:
    target = outdir / f"20261020_detail_cover_{label}.png"
    with tempfile.TemporaryDirectory(prefix="hanmaru-cover-") as profile:
        cmd = [str(edge), "--headless=new", "--disable-gpu", "--no-first-run",
               "--no-default-browser-check", "--hide-scrollbars",
               f"--user-data-dir={profile}", f"--window-size={viewport}",
               "--virtual-time-budget=2200", f"--screenshot={target}",
               (root / page).as_uri()]
        result = subprocess.run(cmd, capture_output=True, timeout=45)
    assert result.returncode == 0 and target.is_file() and target.stat().st_size > 16000, (
        page, result.returncode, result.stderr[-500:])
    print("RENDER PASS", label, target.stat().st_size)
