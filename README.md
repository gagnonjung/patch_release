# Metal Gear Solid: The Twin Snakes — Korean Patch Site

Public release site for the Korean localization patch of **Metal Gear Solid: The Twin Snakes** (Nintendo GameCube / Japan).

- GitHub: `https://github.com/gagnonjung/patch_release`
- GitHub Pages: `https://gagnonjung.github.io/patch_release/`
- Current release: **v1.03**

## Structure

- `index.html` — CODEC-style CALL landing page
- `patch.html` — main patch introduction, patch notes, install guide, license, downloads, and credits
- `assets/css/intro.css` — landing page presentation
- `assets/css/style.css` — main release page presentation
- `assets/js/intro.js` — landing page CALL interaction/audio
- `assets/js/site.js` — release metadata, download links, CODEC presentation, and BGM controls
- `assets/images/` — logo, CODEC portraits, package artwork, and feature screenshots
- `assets/audio/` — landing page CALL/answer audio

## Current release

### Metal Gear Solid: The Twin Snakes Korean Patch v1.03

Release archive:

`MGS_TTS_KO_v1.03_xdelta_windows.zip`

- Size: `140,134,834 bytes / 133.64 MiB`
- SHA-256: `4096ea62dbb1f55cdd7ef830a56c5a7e658c541031eccc84bc2804bac35eead8`
- ZIP integrity: `13 entries / ISO 0 / SHA256SUMS.txt 12/12 PASS`
- Primary download: https://mega.nz/file/JzdDQQwR#qDYFh2cmF5PWdouFDQuiG7Yay5HP_W5d2GtEzW6VXug
- Mirror: https://drive.google.com/file/d/1E-MtgvnhPWZFnklfRHpu8uxFdsdNNpsM/view?usp=sharing

v1.03 keeps the v1.02 fixed-span stage stability fix and adds user-feedback QA for untranslated system text, Meryl/Psycho Mantis dialogue, semantic line breaks, and Korean run-on sentence boundaries. The final sentence-boundary audit corrected 24 cutscene cases and 10 VOX cases, for 34 fixes total.

**v1.03 is not an incremental patch for v1.02.** Apply it directly to supported Japanese retail Disc 1 / Disc 2 images.

## Supported originals

### Disc 1

- MD5: `796319a44e67e9d34e90482d36b26e18`
- SHA-256: `c514c3a672cf3587be87af9874629dfe31b21f92a46e760a9d7ba317f0399591`

### Disc 2

- MD5: `4b0bc9bfe1c4098725bef272f5e03f4d`
- SHA-256: `e1fac2270a95eb40781af29db67d2c741931bc96e884931e42371c036e94a4e4`

## Expected patched ISO hashes

### Disc 1

- SHA-256: `472a22767df0d9efa3a5f027909a104f38f652213a1c4833df5accb5a29a591f`

### Disc 2

- SHA-256: `e493addb95dd9e88b600b3839621c7929cdd08a19efba6921d0cab29513bb94d`

Expected output filenames:

- `Metal Gear Solid - The Twin Snakes (Korea) (Disc 1).iso`
- `Metal Gear Solid - The Twin Snakes (Korea) (Disc 2).iso`

## Updating a release

Release metadata and external download links are defined at the top of `assets/js/site.js`. Keep the corresponding fallback values in `patch.html` synchronized so the page remains correct even before JavaScript runs.

When changing the page, preserve the existing CODEC-inspired visual language and the current download section order:

1. `04-A / PATCH NOTES`
2. `04-B / INSTALL GUIDE`
3. `04-C / DISTRIBUTION LICENSE`
4. `04-D / RELEASE`
5. `04-E / CREDITS`

Do not add empty or `PENDING` game pages unless they are explicitly requested.

## Verification

At minimum, run static checks after changes:

```text
node --check assets/js/site.js
git diff --check
```

Before publishing, verify the changed files, commit them, push `main`, fetch the remote, and confirm the local branch is synchronized with `origin/main`.

## Asset policy

Do not commit original game data, disc images, or reconstructed game binaries. Public-facing screenshots and artwork should be limited to assets appropriate for the patch release page.
