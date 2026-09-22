# FastestImageConvert — HEIC to JPG page update

Upload these files to your live site (paths match your current structure):

## Tool page
Copy everything in `tools/convert-heic-to-jpg/` to:
`/tools/convert-heic-to-jpg/` on the server

- `convert-heic-to-jpg-index.php` — SEO content + modern FAQ (tool UI IDs unchanged)
- `heic_to_jpg_style.css` — page styles + FAQ accordion
- `heic_to_jpg_script.js` — converter + FAQ behavior
- `index.php` — unchanged loader

## Shared assets
Copy `global/` files to your existing `/global/` folder if you want the updated settings list. `global.css` / `global.js` / `config.php` are unchanged functionally from your upload.

## What changed (SEO)
- Title/H1 focused on **HEIC to JPG Converter**
- Stronger CTR meta description (free, private, no upload)
- Honest content (EXIF claim corrected)
- 10 FAQ items with matching FAQPage schema
- Fixed broken duplicate HowTo JSON-LD from the old file
- Internal links to HEIC blog, Windows guide, and related tools

After upload, CSS/JS cache bust is already `?v=6`. Request indexing for `/convert-heic-to-jpg` in Google Search Console.
