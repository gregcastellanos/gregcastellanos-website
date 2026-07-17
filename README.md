# Gregory Castellanos Website

Static GitHub Pages site for gregcastellanos.com.

## Contact form

The contact form uses Web3Forms and posts directly from the static GitHub Pages
site to:

```html
https://api.web3forms.com/submit
```

The public Web3Forms access key is included in `contact.html`, as intended for
client-side Web3Forms integrations. Delivery is associated with:
`gregcastellanoswork@gmail.com`.

Before launch, test: successful submission, error state, spam trap, keyboard
flow, mobile layout, the confirmation message, and delivery to
`gregcastellanoswork@gmail.com`.

## Notes

- Pages: `index`, `ventures`, `about`, `contact`, `privacy`, `404`.
- The background video is gated so mobile and reduced-motion visitors get the
  static poster instead of a video download.
- Images ship as WebP with JPEG/PNG fallbacks.
