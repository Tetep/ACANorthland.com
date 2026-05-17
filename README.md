# ACA Northland

The regional business club for the Kansas City Northland — Liberty, Gladstone, and surrounding. Static site, GitHub Pages hosting (when wired up).

## Sites in the family
- **acanorthland.com** (this repo) — parent brand, location hub, member directory
- **1894.tours** — Castle Hall, Liberty (venue-specific narrative + booking)

## Structure
```
ACANorthland.com/
├── index.html          # Hub home + location picker (Liberty / Vivion)
├── liberty/index.html  # Castle Hall summary + booking CTA -> 1894.tours
├── vivion/index.html   # Vivion location skeleton (Coming Soon)
├── directory/          # Member directory (showpiece)
│   └── index.html      # Card grid, search, filter chips, A-Z bar, availability dots
├── contact.html        # Shared contact + calendar placeholder
├── assets/             # Logos, photos
├── styles.css          # Heritage palette, mobile-first, 480/768 breakpoints
├── CNAME               # acanorthland.com (placeholder — confirm domain choice)
├── robots.txt
└── README.md           # this file
```

## Directory page
The directory is the showpiece per the May 2026 research. Each member card has:
- Logo placeholder + name + one-line positioning + green availability dot
- Two-line bio (member since YYYY — what they do)
- Tag chips: circle (Castle Hall Hosts / Retail on the Square / Services & Pros / Makers) + industry
- "View profile" CTA

Filters: keyword search, availability toggle, circle (single-select), industry (single-select), persistent A-Z bar. Vanilla JS, no dependencies.

**Sample data:** 8 placeholder members. Replace with real ACA Northland member data when ready.

## Brand
- Palette: cream paper, ink/dark brown, gold (#c48c37), crimson, forest green availability dot
- Fonts: Playfair Display (headings) + Inter (body) — slightly cleaner pairing than 1894.tours' Brown Sugar / Caveat Brush
- Mobile-first; breakpoints at 480px and 768px

## Domain
CNAME currently set to `acanorthland.com`. Three options were on the table:
- `acanorthland.com` (current default)
- `NorthlandBusinessClub.com`
- `KCBusinessClub.com`

Confirm choice and update CNAME + GitHub Pages settings before launch.

## Roadmap (V2+)
- Real member data
- Member profile pages (each card -> own URL)
- Calendar integration (Google Cal or GHL)
- Vivion full content
- Mobile 480px QA on real iPhone
