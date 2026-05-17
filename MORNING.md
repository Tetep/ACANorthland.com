# Morning queue — UPDATED 2026-05-16/17 night

## ✅ Resolved by commit `4c8612c` (homepage strategic rewrite)

**Pass A (amber 1894 continuity fixes) and Pass B (Vivion/Liberty positioning flip) — both OBSOLETE.**

The new strategic narrative resolves the false continuity claim cleanly:

| 1882 | Kansas City Club founded (ACA's roots — Eisenhower, Truman, Bradley) |
| 1894 | Castle Hall built on Liberty Square (Pythian Castle building) |
| 2026 | ACA Northland chapter reignites Castle Hall as Northland home |

Two American traditions converging in one Northland room. Both verifiable, neither conflated. Pythian heritage of the building stays separate from ACA's parent-club lineage.

## ⏳ Still on the queue

### Pass C — Side items

- **`.org` redirects** (waiting on the two domain names from registrar). Cloudflare playbook saved in memory.
- **Cloudflare orange cloud** for acanorthland.com — wait 24-48h after cert provisioning, then set SSL/TLS to **Full (strict)**, then flip DNS records to proxied.
- ~~1894.tours Enforce HTTPS~~ ✅ DONE (Let's Encrypt cert valid for `1894.tours` + `www.1894.tours`)

### Phase B (when content is ready)

- Real ACA member data → replace 579 Chamber-demo cards on `/directory`
- Real Vivion content (address, photos, hours) — currently still "Opening Soon" skeleton
- Real photos across the site (currently placeholder gradient cards on hub + Liberty)
- Calendar embed on `/contact`

### Inputs Tim still needs to provide

- Vivion: real address, photos, opening date/hours
- Castle Hall: activation date for the ACA Northland chapter (year they took over the hall)
- Real ACA Business Club member list to replace Chamber demo data
- Two `.org` redirect domain names

## Sites currently live

- 🏥 https://koblerchiro.com — Kobler Chiropractic (WordPress)
- 🏛️ https://1894.tours — Castle Hall venue site (HTTPS now clean)
- 🏢 https://acanorthland.com — Regional parent brand + Directory + Liberty + Vivion + Contact (HTTPS clean)

## Commits this session

```
4c8612c  Homepage strategic rewrite: ACA 1882 + Castle Hall 1894 convergence
1e07164  Vivion: add 4 FB Reels + promote reel CSS to styles.css
43bfeba  Liberty: add 3rd FB reel
61b4019  Liberty: add Facebook Reels embed section
e499846  Credibility sweep #1: Est. 1894 wording + crimson DEMO banner
3cfd4b6  Re-add CNAME after DNS pointed
34131d6  Remove CNAME for testing
bc4b7ab  Compact mobile filter toolbar (horizontal scroll)
d9738e2  Directory: add Gladstone Chamber (579 total) + multi-source generator
8368433  Directory: populate with 380 Liberty Chamber + generator
e3ef693  Initial scaffold — ACA Northland Phase A
```
