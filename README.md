# Metal Gear Solid: The Twin Snakes — Korean Patch Site

Private preview repository for the Korean localization release page.

## Structure

- `index.html` — single-page release site
- `assets/css/style.css` — MGS-inspired presentation layer
- `assets/js/site.js` — release metadata and external download provider settings

## Updating a release

Edit the `release` object at the top of `assets/js/site.js`.

```js
const release = {
  status: "RELEASED",
  title: "The Twin Snakes Korean Patch",
  version: "v1.0.0",
  date: "2026-08-10",
  size: "123 MB",
  provider: "MEGA",
  url: "https://example.invalid/download",
  patchSha256: "...",
  sourceSha256: "..."
};
```

The site intentionally keeps the download provider separate from the page layout so MEGA, GitHub Releases, Google Drive, or another mirror can be swapped without redesigning the page.

## Publishing later

Keep the repository private while the page is being prepared. When the project is ready for public release, either make the repository public and enable GitHub Pages or deploy the same static files through another static hosting provider.

## Asset policy

Do not commit original game data or copyrighted disc images. Screenshots and project artwork should be added only after reviewing their suitability for the public release page.
