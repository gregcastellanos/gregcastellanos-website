# Gregory Castellanos Website

Static GitHub Pages site for gregcastellanos.com.

## Contact form

The contact form is prepared for Formspree. Configure the single value `site.formspreeEndpoint` in `work/site-builder/build-site.mjs` with the real Formspree endpoint, then rebuild and test a real submission.

Until that value is set, the public form keeps the honeypot and timing check and offers a mailto fallback.
