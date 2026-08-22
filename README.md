# Metal Gear Solid: The Twin Snakes — Korean Patch Site

Public release site for the Korean localization patch of **Metal Gear Solid: The Twin Snakes** (Nintendo GameCube / Japan).

- GitHub: `https://github.com/gagnonjung/patch_release`
- GitHub Pages: `https://gagnonjung.github.io/patch_release/`
- Current release: **v1.11**

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

### Metal Gear Solid: The Twin Snakes Korean Patch v1.11

Release archive:

`MGS_TTS_KO_v1.11_xdelta_windows.zip`

- Size: `139,977,986 bytes / 133.49 MiB`
- SHA-256: `36dba5eb935a7a8f6f5b9f5a95a5af3af6760bb0ec940e780e273b589c10a7da`
- Download: `https://drive.google.com/file/d/1dI9TfL_eiRmlsL2ldWLu5zeGzXoQHkyO/view?usp=sharing`

v1.11 is a maintenance release that incorporates user-reported bug fixes after v1.1. It corrects text/display issues, speaker/register mismatches, and the ending message display issue while preserving the earlier Mission Log, Demo Theater, and stage stability work.

**v1.11 is not an incremental patch for v1.1 or any earlier version.** Apply it directly to supported Japanese retail Disc 1 / Disc 2 images.

## Supported originals

### Disc 1

- MD5: `796319a44e67e9d34e90482d36b26e18`
- SHA-256: `c514c3a672cf3587be87af9874629dfe31b21f92a46e760a9d7ba317f0399591`

### Disc 2

- MD5: `4b0bc9bfe1c4098725bef272f5e03f4d`
- SHA-256: `e1fac2270a95eb40781af29db67d2c741931bc96e884931e42371c036e94a4e4`

## Expected patched ISO hashes

### Disc 1

- SHA-256: `8a29ec8617bb48ec8b98aca86ccac81af4410df4de4a77c280965717b8c6c18f`

### Disc 2

- SHA-256: `82a7dda78f4c4d4d6d55ca634ded63e93d80582848cd430cd0c5d28eaa83e96f`

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
