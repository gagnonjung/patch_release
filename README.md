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

- Size: `140,136,058 bytes / 133.64 MiB`
- SHA-256: `2879e80fe169a00645433a69d8ad1f0c184f2c0adf0c7016217be0b500c60e1d`
- ZIP integrity: `13 entries / ISO 0 / SHA256SUMS.txt 12/12 PASS`
- Primary download: `https://mega.nz/file/djlmRRAC#DmqlNevDLrqSsEsHN5oCAxJ01XsrbK9H6JrtEV0wj_Y`
- Mirror: `https://drive.google.com/file/d/1E-MtgvnhPWZFnklfRHpu8uxFdsdNNpsM/view?usp=sharing`

v1.03 keeps the v1.02 fixed-span stage stability fix and includes the latest user-feedback QA: the remaining dog-tag load completion message, Meryl/Naomi/Psycho Mantis dialogue, PSG1/PSG1-T description layout, 34 run-on sentence boundaries, and 5 missing spaces after `!`/`!!`. The final project test suite passes `310/310`.

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

- SHA-256: `4d32884defc8fd550bdf9dadba340f114912ee253c5ba2ebcb4d3b2f1fa78d91`

### Disc 2

- SHA-256: `7ceca2b04b4c5ffaec423c939de8fd083d5ed4cc83877634e3625b63085b83c9`

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
