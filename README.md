# Metal Gear Solid: The Twin Snakes — Korean Patch Site

Public release site for the Korean localization patch of **Metal Gear Solid: The Twin Snakes** (Nintendo GameCube / Japan).

- GitHub: `https://github.com/gagnonjung/patch_release`
- GitHub Pages: `https://gagnonjung.github.io/patch_release/`
- Current release: **v1.1**

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

### Metal Gear Solid: The Twin Snakes Korean Patch v1.1 Final

Release archive:

`MGS_TTS_KO_v1.1_xdelta_windows.zip`

- Size: `140,131,259 bytes / 133.64 MiB`
- SHA-256: `5585366354ed0ba6244c4e9e290fed4b7136f0c8d7850c72d8d6f34472d2e127`
- ZIP integrity: `13 entries / ISO 0 / SHA256SUMS.txt 12/12 PASS`
- Primary download: `https://mega.nz/file/Av0GHCYQ#c4F86nb_R14bPMNbpjz1Pn89MgYEJUjfOExeUsiZOe4`
- Mirror: `https://drive.google.com/file/d/1Ejo5skEyC9QniIZbN8xEFpcM4C3nIt0S/view?usp=sharing`

v1.1 is the final release. It integrates Mission Log `80/80` and Demo Theater `48/48` into the canonical source, reflows all Demo Theater descriptions to a maximum of `24.0 cells`, revalidates the Otacon-route ending and Campbell/Meryl speaker register, preserves two runtime-sensitive Ninja/Otacon cutscene record boundaries, and keeps the v1.02 fixed-span stage stability policy. The v1.1 core regression suite passes `23/23`.

**v1.1 is not an incremental patch for v1.03 or any earlier version.** Apply it directly to supported Japanese retail Disc 1 / Disc 2 images.

## Supported originals

### Disc 1

- MD5: `796319a44e67e9d34e90482d36b26e18`
- SHA-256: `c514c3a672cf3587be87af9874629dfe31b21f92a46e760a9d7ba317f0399591`

### Disc 2

- MD5: `4b0bc9bfe1c4098725bef272f5e03f4d`
- SHA-256: `e1fac2270a95eb40781af29db67d2c741931bc96e884931e42371c036e94a4e4`

## Expected patched ISO hashes

### Disc 1

- SHA-256: `1865619d814f791544ed6e9aa79e23312fa97663ac1c561d78ac3964888c73ae`

### Disc 2

- SHA-256: `1652bd924d7f07c04a6b11fc98d0ce54f06b46788c9c3301faf54ae3080b88fd`

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
