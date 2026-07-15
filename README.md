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

## Things to fill in when you have them

A few slots are intentionally left for real assets (nothing is invented):

- **LinkedIn URL** — set `LINKEDIN_URL` in `build.py` to wire it into the footer
  and structured data.
- **Patent numbers** — the two U.S. patents are referenced by name; add numbers
  and USPTO links when documented.
- **Testimonials** — the About page has reserved slots; drop in real quotes
  (with permission) in `build.py`.
- **Real photos** — event, teaching, and project photos will strengthen the
  work and area pages.

See `DESIGN_AUDIT.md` for design notes.
