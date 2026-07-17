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

- Pages: `index`, `ventures`, `about`, `contact`, `privacy`, `404`.
- The background video is gated so mobile and reduced-motion visitors get the
  static poster instead of a video download.
- Images ship as WebP with JPEG/PNG fallbacks.
