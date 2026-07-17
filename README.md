# Gregory Castellanos Website

Static GitHub Pages site for gregcastellanos.com.

## Contact form

The contact form is ready for Formspree. Set one value — the form's endpoint —
in `contact.html`:

```html
<form class="contact-form" id="contact-form" method="post"
      action="" data-endpoint="https://formspree.io/f/XXXXXXXX" novalidate>
```

Put the endpoint in `data-endpoint` (and mirror it in `assets/site-data.json`
`formspreeEndpoint` for tooling). While it is empty, the form keeps the honeypot,
timing check, and client-side validation, and falls back to a mailto draft.

After setting the endpoint, test: successful submission, error state, spam trap,
keyboard flow, mobile layout, the confirmation message, and delivery to
gregcastellanoswork@gmail.com.

## Notes

- Pages: `index`, `ventures`, `about`, `contact`, `privacy`, `404`.
- The background video is gated so mobile and reduced-motion visitors get the
  static poster instead of a video download.
- Images ship as WebP with JPEG/PNG fallbacks.
