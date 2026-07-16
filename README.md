# Gregory Castellanos Website

Static site for [gregcastellanos.com](https://gregcastellanos.com) — the umbrella
site for Greg Castellanos, organized around six connected areas: People, Ideas,
Brands, Technology, Experiences, and Places.

## How it's built

The HTML pages are **generated** from a single source of truth so the header,
footer, meta tags, structured data, and shared components stay consistent.

- `build.py` — the generator (Python 3 standard library only). Holds the
  content model, page templates, inline SVG artwork, and per-page JSON-LD.
- `assets/styles.css` — the design system (light + dark themes, all components).
- `assets/site.js` — behavior: theme toggle, mobile nav, scroll reveal, work
  filter, and the contact form.
- The generated `*.html` files and `sitemap.xml` live at the repo root for
  GitHub Pages.

### To make a content change

1. Edit the relevant data in `build.py` (e.g. the `AREAS`, `CASES`, `STATS`,
   `TIMELINE`, or `FAQ` lists).
2. Run the generator:

   ```sh
   python3 build.py
   ```

3. Commit the changed `build.py` **and** the regenerated HTML.

Editing the generated `.html` directly works too, but changes will be
overwritten the next time `build.py` runs — prefer editing `build.py`.

## Optional future additions

The core content is in place (LinkedIn, patents with USPTO links, real client
testimonials, and real photos of Greg). Nice-to-haves when available:

- **More photos** — teaching/classroom, coaching context, and real place/property
  photos would let People, Technology, and Places carry images too. Drop web-ready
  files in `assets/images/` and reference them in `build.py`.
- **Additional testimonials** — production leads or education partners, added to
  `TESTIMONIALS` in `build.py` (only with permission).

Photos are processed with Pillow — auto-oriented, resized, and compressed. See the
one-off script pattern used in the project history if adding more.

See `DESIGN_AUDIT.md` for design notes.
