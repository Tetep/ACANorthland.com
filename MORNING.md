# Morning queue — UPDATED 2026-05-17 (late night)

## ⏳ Pass D — ACA Palette Swap (NEW — queued by Bob)

Bob extracted the full ACA brand palette from the parent corporate site via ColorZilla. Saved to memory at `reference_aca_corporate_brand.md`. Apply across the site.

### Step 1 — Replace `:root` block in `styles.css`

```css
:root {
  /* ============ ACA CORPORATE LAYER ============ */
  --aca-deep: #1D2F2C;           /* primary dark teal — hero, header */
  --aca-deeper: #0F1A17;         /* deepest — footer bottom strip */
  --aca-deep-lighter: #2C4A45;   /* quote boxes, hover, card bg on dark */
  --aca-navy: #1A2332;           /* secondary dark — nav alt, dark sections */
  --aca-pale-blue: #C8DEE8;      /* soft accent — info callouts, highlights */

  /* ============ HERITAGE BODY LAYER (keep) ============ */
  --paper: #F4ECD8;
  --paper-deep: #E8DCC0;
  --paper-shadow: #D8C9A8;

  /* ============ SHARED ACCENTS ============ */
  --gold: #B89A4B;
  --gold-bright: #D4B36A;
  --gold-deep: #8F7637;
  --crimson: #8B2635;

  /* ============ TEXT ============ */
  --ink: #1F1A17;
  --ink-soft: #3D332B;
  --paper-on-dark: #F8F6F2;
}
```

(Currently `styles.css` has different var names — `--paper-soft`, `--green-dot`, etc. Map old → new where needed. The existing palette is close but not exact to ACA corporate.)

### Step 2 — Section mapping (apply across all 5 pages)

| Element | New value |
|---|---|
| Header bg | `--aca-deep` |
| Header text | `--paper-on-dark` |
| Header active link underline | `--gold` |
| Hero bg gradient | `--aca-deep` → `--aca-deeper` |
| Hero primary CTA | `--gold` bg, `--aca-deep` text |
| Hero outline CTA | `--paper-on-dark` border + text |
| Pull-quote/testimonial | `--aca-deep-lighter` bg |
| Info callout banners | `--aca-pale-blue` bg, `--aca-navy` text |
| "Two Northland Locations" section | `--paper` (heritage — keep) |
| Hub cards | `--paper-deep` (heritage — keep) |
| Directory bg | `--paper` (keep) |
| BETA banner on directory | `--crimson` (keep — preserves contrast) |
| Footer top | `--aca-deep` |
| Footer bottom strip | `--aca-deeper` |
| Three Pillars section | `--aca-navy` bg, `--paper-on-dark` text, `--gold` icons |

### Step 3 — Mobile contrast check
The dark-light hybrid (paper sections + dark hero/footer/pillars) needs to read well at 480px. Verify contrast on hub cards, pillar cards, directory cards.

### Step 4 — Caveat from Bob
Hex estimates were eye-read from ColorZilla swatch row, ±3-5 hex points. For perfect precision, run ColorZilla eyedropper on individual elements. Good enough for V1 alignment with parent brand.

---

## ⏳ Pass C — still queued

- `.org` redirects (waiting on the two domain names from registrar). Cloudflare playbook saved in memory.
- Cloudflare orange cloud for acanorthland.com — wait 24-48h after cert provisioning, then SSL/TLS = Full (strict), then flip records.

## ⏳ Phase B — when content's ready

- Real ACA member data → replace 579 Chamber-demo cards on `/directory`
- Vivion real content (address, photos, hours) — currently "Opening Soon" skeleton
- Real photos across the site (placeholder gradient cards on hub + Liberty)
- Calendar embed on `/contact`
- Hero image: ACA reception photo Tim mentioned but hasn't saved yet — when it's in `assets/hero/`, wire it into homepage hero with dark overlay

## ⏳ Liberty/Vivion narrative cleanup (deferred from morning queue)

The hub cards on index.html now reflect Vivion=established, Liberty=new chapter. BUT:
- `liberty/index.html` hero lede still says "home of the ACA Business Club ever since" — implies club continuity from 1894 (false)
- `vivion/index.html` still reads as "Opening Soon / Coming Soon" — should reflect established home status
- Footer brand paragraph on liberty + vivion still says "Operating Castle Hall on Liberty Square since 1894" (continuity claim)

When Pass D palette swap happens, also fix these narrative inconsistencies on the two location pages.

## Sites currently live

- 🏥 https://koblerchiro.com — Kobler Chiropractic (WordPress)
- 🏛️ https://1894.tours — Castle Hall venue site (HTTPS clean)
- 🏢 https://acanorthland.com — Regional parent brand + Directory + Liberty + Vivion + Contact (HTTPS clean, ACA logo sitewide)

## Recent commits

```
2c935f7  Brand: add ACA logo to header + footer across all pages
4175928  Hub H2: 'Two Northland Homes' -> 'Two Northland Locations'
53bc854  Hero eyebrow tweak: 'Northland Chapter' -> 'Northland Chapter of the ACA'
bda7084  Hero: cut to 30 words, align to corporate ACA brand voice
aa7d8aa  Flip hub cards: Vivion is established, Liberty is the new chapter
7888ee5  Homepage meta description: align with new narrative
c8ea01c  Update MORNING.md
4c8612c  Homepage strategic rewrite: ACA 1882 + Castle Hall 1894 convergence
1e07164  Vivion: add 4 FB Reels + promote reel CSS to styles.css
43bfeba  Liberty: add 3rd FB reel
61b4019  Liberty: add Facebook Reels embed section
e499846  Credibility sweep #1: Est. 1894 wording + crimson DEMO banner
bc4b7ab  Compact mobile filter toolbar (horizontal scroll)
d9738e2  Directory: add Gladstone Chamber (199) + multi-source generator
8368433  Directory: populate with 380 Liberty Chamber + generator
e3ef693  Initial scaffold — ACA Northland Phase A
```
