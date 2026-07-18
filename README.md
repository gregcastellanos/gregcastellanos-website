# Gregory Castellanos Website

Static GitHub Pages site for gregcastellanos.com.

## Contact form

The contact form submits to **Web3Forms** (`https://api.web3forms.com/submit`).
The `access_key` hidden field in `contact.html` is a public, email-scoped key
(safe to commit); Web3Forms handles delivery to gregcastellanoswork@gmail.com and
server-side spam filtering. To change the destination, replace the key with one
from a new Web3Forms form.

The form also keeps a client-side honeypot, a timing check, and validation, and
posts via `fetch` for inline success/error messages (native POST works without
JS too).

Note: Web3Forms only accepts submissions from a real browser (it blocks
server/datacenter requests), so verify actual delivery by submitting once from
the deployed site or a browser — not from a script.

## Notes

- The fixed backdrop is a pure CSS gradient (no video download).
- Images ship as WebP with JPEG/PNG fallbacks.

## Pages

- Core: `/`, `/ventures`, `/about`, `/contact`, `/privacy`
- Services: `/av-event-production`, `/sound-system-dj-booth-rentals`, `/ai-consulting-evaluation`, `/learning-design-steam`, `/creative-strategy`, `/project-development`
- Case studies: `/recreation-sound-systems`, `/local-maker-mart`, `/techshop-steam`, `/enterprise-event-production`
- `/resume`

URLs are extensionless. The underlying `.html` source files remain, and Cloudflare
serves the extensionless path (the `.html` form 308-redirects to it).

New photos: several pages contain `IMAGE PLACEHOLDER` HTML comments describing the
type, orientation, dimensions, filename, and alt-text pattern for future original
photographs. Add real images as responsive `<picture>` (WebP + JPG), with width and
height set and `loading="lazy"` below the fold. Do not use stock imagery.

## Google Search Console Launch Checklist

Greg completes these manually:

1. Add `gregcastellanos.com` as a **Domain property** in Google Search Console.
2. **Verify through Cloudflare DNS** (add the TXT record Search Console provides).
3. Submit the sitemap: `https://gregcastellanos.com/sitemap.xml`.
4. Use **URL Inspection** to inspect and **Request indexing** for the homepage and
   primary service pages (`/av-event-production`, `/ai-consulting-evaluation`,
   `/learning-design-steam`, `/creative-strategy`).
5. Monitor **indexing, queries, clicks, and Core Web Vitals** over the following weeks.
6. **Re-submit or update the sitemap** as new pages are added.

No verification token is stored in the repo. If Search Console offers an HTML-file or
meta-tag verification method and you prefer it over DNS, provide the token and it can
be added.
