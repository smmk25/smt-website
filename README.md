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

The quote form POSTs JSON to an n8n webhook, which persists every legitimate
enquiry to a Postgres database (Neon) *before* notifying anyone — the DB row
is the source of truth, the email is just a notification about it:

```
Webhook → Validate & Normalise → IF (spam?) ─┬→ Save Lead to Neon → Email (SMTP) → Respond to browser
                                             └→ Respond to browser (spam silently dropped)
```

**Setup:**

1. Import `n8n-quote-workflow.json` into n8n
2. Copy the *Production* webhook URL into `N8N_WEBHOOK_URL` in `index-scroll.html`
3. Create a free [Neon](https://neon.tech) Postgres project, then run this once
   in its SQL editor to create the leads table:
   ```sql
   CREATE TABLE quote_requests (
     id            BIGSERIAL PRIMARY KEY,
     dedupe_key    TEXT UNIQUE NOT NULL,
     service       TEXT NOT NULL,
     frequency     TEXT,
     is_contract   BOOLEAN,
     priority      TEXT,
     company       TEXT NOT NULL,
     contact_name  TEXT NOT NULL,
     phone         TEXT NOT NULL,
     email         TEXT NOT NULL,
     description   TEXT,
     source        TEXT,
     submitted_at  TIMESTAMPTZ,
     received_at   TIMESTAMPTZ NOT NULL DEFAULT now()
   );
   ```
4. In n8n, add a Postgres credential (Neon's connection string, from the Neon
   dashboard) and select it on the "Save Lead to Neon" node
5. Add an SMTP credential to the email node
6. Set Allowed Origins (CORS) on the webhook node to your domain
7. Activate the workflow

**Notes on the design:**

- Validation is repeated server-side in the Code node — browser validation is
  trivially bypassed by POSTing directly to a public webhook
- A honeypot field catches bots without a CAPTCHA
- Spam receives a `200` rather than an error, so bots don't retry
- `dedupe_key` (email + company + submitted_at) is unique in Postgres, and the
  insert uses `ON CONFLICT ... DO NOTHING` — a retried webhook POST (e.g. a
  flaky network on the visitor's end) can't create a duplicate lead
- The Neon node is set to continue-on-error, so a transient DB hiccup
  doesn't swallow the sales email entirely — check the n8n execution log
  if that ever fires, since it means a lead didn't get persisted
- Neon free tier scales to zero and auto-resumes on the next query, so it
  stays reachable even between quiet weeks — no manual reactivation step

## Weekly report

No dashboard, no login — every Monday at 8am Dubai time the workflow emails
`info@salmanmohammadtransport.ae` a CSV of the last 7 days of leads:

```
Every Monday 8am Dubai → Fetch Last 7 Days (Postgres) → Build CSV → Email Weekly Report
```

This is a second, independent trigger branch in the same workflow — it doesn't
touch the webhook path above.

**On the timezone:** your n8n workflow's default timezone is already set to
UTC+4, so the cron is just the plain local time you want — `0 8 * * 1`, 8:00
AM every Monday, no manual UTC conversion needed. (The UAE has no daylight
saving time, so this offset never changes and there's nothing to revisit
later.)

**Extra setup (on top of the steps above):**

1. On the "Fetch Last 7 Days" node, select the same Neon Postgres credential
   used on "Save Lead to Neon"
2. On the "Email Weekly Report" node, select the same SMTP credential used on
   "Email Sales Team"
3. Double-check the "Build CSV" node's `this.helpers.prepareBinaryData` call
   and the "Email Weekly Report" node's attachment option still match your
   n8n version's exact API — both were hand-written outside the n8n editor,
   so open each node once after import to confirm it validates cleanly
4. Send yourself a manual test run (the node's "Execute step" button) before
   relying on the Monday schedule, and confirm the email actually lands at
   8am Dubai time on the first real Monday run — that's the real proof the
   timezone assumption above was correct

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
