# Morning queue — 2026-05-17

Last commit shipped: `e499846` (credibility sweep #1 — Est. 1894 wording + crimson Demo Preview banner).

Two passes to run when you fire up Code Agent:

---

## Pass A — Amber fixes (Bob's catch + Murdoch's catch from the sweep)

Three "club has been at Castle Hall since 1894" claims that Bob's first prompt didn't catch. Same factual issue as the wider sweep:

### A1. `index.html` hero lede

**Find:**
> The ACA Business Club has anchored the Northland since 1894 — today operating out of Castle Hall on Liberty Square and a growing presence at Vivion. Members host events, share work, and back each other up.

**Replace with:** *(rewrite needed — see Pass B too; the "anchored at Castle Hall" framing also needs flipping per Tim's Vivion-is-original catch)*

### A2. `liberty/index.html` hero lede

**Find:**
> A grand second-floor event hall on Liberty Square — built in 1894 and the home of the ACA Business Club ever since. Available for member bookings at preferred rates.

**Replace with:**
> A grand second-floor event hall on Liberty Square — built in 1894 and the modern home of the ACA Business Club. Available for member bookings at preferred rates.

### A3. Footer brand paragraph (all 5 pages)

**Find:**
> Operating Castle Hall on Liberty Square since 1894

**Replace with:**
> Headquartered at Castle Hall on Liberty Square — built 1894

---

## Pass B — Vivion/Liberty positioning flip (Tim caught 2026-05-16 night)

**THE TRUTH:** Vivion is the ORIGINAL ACA Business Club location. Castle Hall on Liberty Square is the NEW / recently activated chapter — leveraging the historic 1894 Pythian building as the club's expanded home.

Current site has this BACKWARDS:
- Home hub puts "NEW" badge on Vivion → should be on Liberty
- `/vivion` reads "Coming Soon, skeleton page" → should read as the established original home
- `/liberty` reads as the long-standing anchor → should read as the new chapter at a historic building
- Footer brand paragraphs say "operating Castle Hall since 1894" → false in two ways

### Fix list (Pass B)

1. **`index.html` Home — Pick a Location section:**
   - Vivion card: remove "· NEW" badge, change badge to "ORIGINAL" or "EST. ____" (need real year from Tim), reposition as the established home
   - Liberty card: add "NEW" or "RECENTLY OPENED" badge, reframe as the new chapter at the historic 1894 building
   - Swap any "second Northland location" language: Castle Hall is the SECOND location, Vivion is the FIRST

2. **`vivion/index.html`:**
   - Drop the "Opening Soon" + "Coming Soon" framing entirely
   - Reframe as the established original ACA home
   - Real photos / hours / address needed from Tim
   - This page becomes the FOUNDATIONAL location, not a placeholder

3. **`liberty/index.html`:**
   - Reframe: "The ACA Business Club's new chapter at Castle Hall — a grand 1894 Pythian building on Liberty Square, recently activated as the club's second home."
   - Keep heritage credibility (building IS 1894 Pythian) but separate building age from club's presence there

4. **`index.html` hero lede (replaces Pass A1):**
   - Rewrite to reflect: ACA Business Club original = Vivion, new chapter = Castle Hall on Liberty Square
   - Heritage + restart frame: "An established Northland business club expanding into a historic 1894 building" — something like that

5. **Footer brand paragraph across 5 pages:**
   - Drop "Operating Castle Hall on Liberty Square since 1894"
   - New version separates building heritage from club presence
   - Suggested: "ACA Business Club of the Northland · home at Vivion, new chapter at Castle Hall (built 1894)"

### Blockers Tim needs to provide

- Real year the ACA Business Club was founded at Vivion (or "founded YYYY at Vivion")
- Real Vivion address + photos when ready
- Date of the Castle Hall activation (when did the club start at Castle Hall?)

---

## Pass C — Side items (when you have bandwidth)

- `.org` redirects via Cloudflare playbook (waiting on the two domain names from registrar)
- Flip Cloudflare DNS records to **proxied/orange cloud** for CDN — wait 24-48h after cert provisioning, then set SSL/TLS mode to Full (strict) first
- 1894.tours HTTPS — flip "Enforce HTTPS" in Pages settings once cert provisions
- Phase B Vivion content depends on Pass B completing first
- Monday: 1894.tours/book form + calendar + GHL pipeline

---

## Don't forget

- Bob's prompt closed with "stop after the three credibility fixes" — Pass A1 + Pass B are NEW work that came up AFTER. Confirm scope expansion is approved before going wide.
- All current copy on the live site is from `e499846`. The Vivion/Liberty narrative is currently wrong AS PUSHED.
- No customer-facing emergency. Garrett-level credibility issue, not a five-alarm fire.
