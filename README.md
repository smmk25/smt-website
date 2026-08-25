# Salman Mohammad Transport LLC — Website

A single-page, scroll-driven marketing site for a Dubai-based tanker and freight company, built as static HTML/CSS/JS with an automated lead-capture pipeline.

Live site: [salmanmohammadtransport.ae](https://salmanmohammadtransport.ae)

---

## What this is

A rebuild of an existing brochure site, with the goal of turning it from a static
listing into something that actually generates leads. The original had no contact
form at all — just a phone number — so every visitor who didn't feel like calling
simply left.

**Key changes:**

- Full-height scroll-snapping sections with entry/exit animations
- Two-level services mega-menu (Environmental / Freight)
- Two-step quote form in a modal panel, wired to an automation backend
- Client logo wall, service categories, real brand assets
- No framework, no build step — plain HTML/CSS/JS

---

## Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | Vanilla HTML/CSS/JS | Static host (cPanel), no build tooling needed |
| Typography | Montserrat (self-hosted WOFF2 variable font) | No Google Fonts dependency; one file covers every weight |
| Logo/icons | SVG extracted from the original Illustrator PDF | Sharp at any size; 2.4KB vs 58KB for the PNG |
| Form backend | n8n (webhook → validate → email + Teams) | Static sites can't process forms; keeps lead data self-owned |
| Scroll behaviour | CSS scroll-snap + IntersectionObserver | No scroll-jacking library; respects `prefers-reduced-motion` |

---

## Structure

```
index-scroll.html          # the whole site — one page, five sections
splash.html                # logo animation, forwards to the main page
footer-block.html          # footer as a standalone reusable snippet
build_preview.py           # inlines every asset into one self-contained file
n8n-quote-workflow.json    # importable automation workflow

assets/
  logo.svg                 # for light backgrounds
  logo-white.svg           # for dark backgrounds (the "T" is white)
  favicon/                 # .ico, .svg, PNGs, apple-touch, manifest
  services/                # service card photography
  about/                   # About carousel images
  clients/                 # client logos, background-trimmed
fonts/
  Montserrat-*.woff2       # + .ttf fallbacks
```

---

## Running locally

No build step. Serve the folder over HTTP — don't open the file directly,
or `file://` origin will block the form submission:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000/splash.html
```

To generate a single self-contained file with every asset inlined
(useful for sharing a preview without the folder structure):

```bash
python3 build_preview.py     # writes preview-full.html
```

---

## Form pipeline

The quote form POSTs JSON to an n8n webhook:

```
Webhook → Validate & Normalise → IF (spam?) ─┬→ Email (SMTP)
                                             ├→ Teams notification
                                             └→ Respond to browser
```

**Setup:**

1. Import `n8n-quote-workflow.json` into n8n
2. Copy the *Production* webhook URL into `N8N_WEBHOOK_URL` in `index-scroll.html`
3. Add an SMTP credential to the email node
4. Set Allowed Origins (CORS) on the webhook node to your domain
5. Activate the workflow

**Notes on the design:**

- Validation is repeated server-side in the Code node — browser validation is
  trivially bypassed by POSTing directly to a public webhook
- A honeypot field catches bots without a CAPTCHA
- Spam receives a `200` rather than an error, so bots don't retry
- The Teams node is set to continue-on-error, so a Teams outage
  never blocks the email

---

## Things worth knowing

**Scroll snapping is `proximity`, not `mandatory`.** Mandatory fights trackpad
momentum and feels like the page is grabbing at you. Proximity settles naturally.

**Logo trimming samples corner pixels** rather than assuming a white background —
client logos arrived on white, grey, and transparent backgrounds.

**The favicon uses only the road glyph** from the left of the wordmark. The full
"SMT" lockup is illegible below about 48px.

---

## Credits

Design and build: [your name]
Brand assets: Salman Mohammad Transport LLC

Client logos are the property of their respective owners and are shown
with permission.
