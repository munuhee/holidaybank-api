# Holidaybank Expeditions: API

The Django 6 + Django REST Framework API behind the Holidaybank Expeditions website and admin
dashboard. It serves content, bookings/enquiries, users and roles, and the media library.

The website and `/admin` dashboard are in a separate repo, **holidaybank-web** (Next.js).

The API was ported to Django from the Lekker Tours Express/Prisma API. It keeps the same endpoints
and response shapes, so the dashboard works unchanged.

---

## Run it locally

Requirements: Python 3.12+. SQLite is used by default; PostgreSQL via `DATABASE_URL`.

```bash
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env              # set DJANGO_DEBUG=true, and ADMIN_PASSWORD (12+ chars)
python manage.py migrate
python manage.py seed             # catalogue, content, demo enquiries, and the admin account
python manage.py runserver 8000
```

Then start the web app (see its README). `REVALIDATE_SECRET` must match in both repos.

| | URL |
|---|---|
| API health | http://localhost:8000/api/health |
| Django admin (superusers) | http://localhost:8000/django-admin/ |
| Dashboard (web app) | http://localhost:3000/admin, signing in with `ADMIN_EMAIL` / `ADMIN_PASSWORD` from `.env` |

### With Docker

`docker-compose.yml` runs PostgreSQL 16, this API under gunicorn and the built Next.js site. It
expects the web repo checked out next to this one as `../holidaybank-web`.

```bash
cp .env.docker.example .env.docker    # fill in the secrets
docker compose --env-file .env.docker up --build
docker compose --env-file .env.docker exec api python manage.py seed
```

### On Railway

`railway.json` builds the `Dockerfile` and waits for `/api/health` before switching traffic.

1. New project from this GitHub repo, then add a PostgreSQL database to the project.
2. Add a volume to the API service mounted at `/app/uploads`, so dashboard uploads survive deploys.
3. Set the service variables:

   ```
   DJANGO_DEBUG=false
   DJANGO_SECRET_KEY=<random>
   JWT_SECRET=<random>
   REVALIDATE_SECRET=<random, same value on Netlify>
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   DJANGO_ALLOWED_HOSTS=<service>.up.railway.app,healthcheck.railway.app
   PUBLIC_API_URL=https://<service>.up.railway.app
   WEB_ORIGIN=https://holidaybank.netlify.app
   REVALIDATE_URL=https://holidaybank.netlify.app/api/revalidate
   ADMIN_EMAIL=<email>
   ADMIN_PASSWORD=<12+ characters>
   RAILWAY_RUN_UID=0
   WEB_CONCURRENCY=2
   ```

   `RAILWAY_RUN_UID=0` lets the container write to the volume, which Railway mounts as root.
   `healthcheck.railway.app` is the host Railway's health check sends.
4. Generate a domain under Settings → Networking, then seed once: `railway ssh` and
   `python manage.py seed`. Migrations run on every start.

### Tests

```bash
python manage.py test tests      # 40 API tests, SQLite or PostgreSQL
```

CI (`.github/workflows/ci.yml`) runs them against PostgreSQL.

### Endpoints

Public endpoints (no auth): `/api/tours`, `/api/tours/<slug>`, `/api/tours/<slug>/related`,
`/api/destinations`, `/api/categories`, `/api/countries`, `/api/blog`, `/api/testimonials`,
`/api/faqs`, `/api/services`, `/api/settings`, `/api/media`, `POST /api/enquiries`,
`/api/enquiries/options`, `/api/health`.

Dashboard endpoints live under `/api/admin/*` and `/api/auth/*`. Each is gated by a permission from
`apps/accounts/permissions_catalog.py`.

---

## Content: what is real and what is demo

The original prototype website was treated as the authoritative source. The footer shows a site notice,
**"Prices are per person and subject to availability at the time of booking."**, which an
administrator can edit or switch off (Site settings → Site notice).

**Taken from the original site**

- Brand name, the "Travel in Style" tagline, the logo, the colour palette (charcoal, gold, green,
  cream) and the fonts (Fraunces and Jost).
- Hero copy and buttons: "Feel The Experience", "Discover East Africa's Wild Beauty".
- The navigation and product lines: Kenyan Packages › Locals, International › Europe,
  Safaris › Kenyan Safaris / Kenya · Tanzania · Uganda · Rwanda, with each section's intro text.
- All **17 packages**: title, place line, card description and "from" price (KSh for local
  packages, USD for the rest), and durations wherever the description states them.
- Contact details: Nairobi, Kenya; hello@holidaybankexpeditions.com; +254 700 000 000. The phone
  number is the original's placeholder.
- The nine hero photographs and eight card photographs embedded in the page.

**Generated for this build** (flagged in the database and dashboard)

- Each record has `is_sample` and a `source_note`. The dashboard shows a "Sample" badge, and so do
  the public cards and pages for demo packages, reviews and articles.
- For the 17 original packages, the **itineraries, inclusions, exclusions and group sizes** were
  drafted from the card text. Their `source_note` says to confirm them before launch.
- **7 demo packages**, for example Lake Nakuru Day Safari and Madrid & Toledo City Break.
- **Destination pages** (9 countries, 26 places): overviews and best-time notes written around the
  packages sold.
- **8 testimonials**: shown publicly with a "Sample review" label. Replace them with real reviews.
- **5 blog posts**, **10 FAQs** (answers kept general; confirm they match policy) and **4
  services** (these restate what the original site says the company does).
- **3 demo staff accounts** (they cannot sign in) and **10 demo enquiries** across every pipeline
  stage, with timelines and audit entries.
- **Ratings and review counts are zero.** The site hides them until real reviews exist, rather
  than inventing scores.
- **No licence numbers, founding dates, team sizes or accreditations** are claimed anywhere.

`python manage.py seed --no-demo` loads only the original-site content.
`python manage.py seed --reset` wipes content and restores the defaults.

Images are registered in the media library (`ImageAsset`, seeded from `apps/seed/data/images.py`).
The files themselves are in the web repo's `public/images/`.

---

## Architecture notes

**API shape.** Every response is `{success, data, meta?}` or `{success: false, error: {message,
code, details?}}`. Validation errors come back as a flat `{field: message}` map that the forms
highlight.

**Data model** (`apps/`)

| App | Models |
|---|---|
| `catalog` | `Country`, `TourCategory` (tree), `Destination`, `Place`, `Tour`, `TourImage` |
| `content` | `BlogPost`, `Tag`, `Testimonial`, `Faq`, `Service`, `SiteSettings` (singleton) |
| `media` | `ImageAsset`: every image with its credit and origin |
| `enquiries` | `Enquiry`, `EnquiryEvent` (timeline), `EnquiryReferenceCounter` |
| `accounts` | `AdminUser` (email login), `Role` (permission sets), `AuditLog` |

Countries, categories and tags are relational rather than Postgres arrays, so filtering behaves
identically on SQLite and PostgreSQL. The menu, footer and tour filters are built from
`/api/categories` and `/api/countries`, so new product lines need no deploy.

**Auth.** The dashboard signs in with a JWT in an httpOnly cookie (`hb_admin_token`), re-checked
against the database on every request. Cookie-authenticated writes must carry the web app's
`Origin` (see `common/middleware.py`). Failed logins are rate-limited per IP; public enquiries are
throttled at 20 an hour.

**Permissions.** Roles hold `resource.verb` permissions (`tours.publish`, `enquiries.assign`...).
They are seeded as Administrator (locked), Editor, Author and Travel Consultant, and editable under
Roles. Changing a record's status counts as publishing.

**Enquiries.** Each gets an `ENQ-YYMM-NNNN` reference, allocated under a row lock. They move through
new → assigned → in progress → quoted → booked / closed, with claim/assign, follow-up dates, and an
append-only timeline.

**Cache.** After an admin save the API POSTs the affected cache tags to Next.js
(`/api/revalidate`), so public pages update within moments. Otherwise they revalidate every five
minutes.

### Production checklist

- Set `DJANGO_DEBUG=false`, real `DJANGO_SECRET_KEY` / `JWT_SECRET` / `REVALIDATE_SECRET`,
  `DATABASE_URL` (PostgreSQL), `DJANGO_ALLOWED_HOSTS`, `WEB_ORIGIN`, `PUBLIC_API_URL`, and
  `COOKIE_DOMAIN` (the shared parent domain).
- Set `CACHE_URL` (Redis) when running more than one worker, so rate limits are shared.
- Replace the placeholder phone number, add a WhatsApp number and street address in Site settings,
  and switch off the prototype notice once prices are confirmed.
- Confirm the itineraries marked in each package's source note, and the licence of the nine
  original-site photographs.
- Replace demo testimonials, blog posts and FAQs, or unpublish them: filter by the Sample badge.
- Optional: set `NEXT_PUBLIC_TAWK_SRC` to the company's own Tawk.to widget for live chat.
