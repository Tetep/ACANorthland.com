"""Generate directory/index.html from multiple chamber CSVs.

Sources (add new sources by adding to SOURCES list):
- Liberty Chamber  — schema: Letter, Name, Phone, Address, Website, Category, DetailURL, Tags
- Gladstone Chamber — schema: Letter, Name, Address, Phone, Fax, Category, Contacts, MemberSince, Description, Tags

Each row is normalized to a common Member record. Cards show ONLY the fields
the source actually provides — no fabrication. Gladstone has richer data
(descriptions + member-since), Liberty has links to its Chamber detail page.

Idempotent. Re-run any time the CSV(s) update:  python build_directory.py
"""
import csv
import os
import re
import html
from collections import Counter

OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "directory", "index.html")

SOURCES = [
    {
        "key":   "liberty",
        "label": "Liberty Chamber",
        "path":  r"C:\Users\tpete\liberty-chamber-directory.csv",
    },
    {
        "key":   "gladstone",
        "label": "Gladstone Chamber",
        "path":  r"C:\Users\tpete\gladstone-chamber-directory.csv",
    },
]

INDUSTRY_BUCKETS = [
    ("food",          "Food & Beverage",
     ["restaurant", "bakery", "cafe", "coffee", "brewery", "catering", "food", "ice cream", "deli", "winery", "bar & grill", "pub", "tavern", "dining"]),
    ("finance",       "Finance & Insurance",
     ["financial", "insurance", "bank", "credit union", "mortgage", "accountant", "tax", "investment", "wealth", "cpa"]),
    ("health",        "Health & Wellness",
     ["chiropract", "health", "medical", "dental", "dentist", "vision", "optomet", "pharmac", "fitness", "wellness", "counseling", "therapy", "spa", "aesthetic", "salon", "hair", "nail", "barber", "massage", "yoga", "veterinar"]),
    ("pro",           "Professional Services",
     ["attorney", "lawyer", "consultant", "marketing", "advertising", "design", "agency", "real estate", "realtor", "appraisal", "title company", "business services", "engineering", "architect", "printing", "photography"]),
    ("retail",        "Retail & Shopping",
     ["retail", "boutique", "store", "shop", "jewelry", "gift", "antique", "clothing", "books", "florist", "furniture", "automotive sales"]),
    ("trades",        "Trades & Construction",
     ["construct", "roof", "hvac", "plumb", "heating", "cooling", "electric", "carpentry", "remodel", "home improvement", "landscape", "lawn", "tree", "pest", "pressure wash", "trash", "cleaning", "fire & water", "restoration", "moving", "storage", "manufactur", "machine", "auto repair", "auto body", "auto service", "car wash"]),
    ("entertainment", "Entertainment & Hospitality",
     ["entertainment", "hotel", "motel", "lodg", "event", "wedding", "venue", "music", "theatr", "recreation", "fitness center", "country club", "golf", "martial arts"]),
    ("community",     "Community & Non-Profit",
     ["non-profit", "nonprofit", "church", "ministry", "community", "education", "school", "library", "museum", "chamber", "foundation", "association", "senior living", "child care", "preschool", "civic"]),
]


def industry_bucket(category):
    cat = (category or "").lower()
    for slug, _, keywords in INDUSTRY_BUCKETS:
        if any(k in cat for k in keywords):
            return slug
    return "other"


def industry_label(slug):
    if slug == "other":
        return "Other"
    for s, label, _ in INDUSTRY_BUCKETS:
        if s == slug:
            return label
    return "Other"


CITY_RE = re.compile(r",\s*([A-Za-z .'\-]+?),\s*[A-Z]{2}\s*\d{5}")


def extract_city(addr):
    if not addr:
        return ""
    m = CITY_RE.search(addr)
    return m.group(1).strip() if m else ""


def city_slug(city):
    return re.sub(r"[^a-z0-9]+", "-", city.lower()).strip("-") if city else ""


def normalize_url(url):
    if not url:
        return ""
    u = url.strip()
    if not u:
        return ""
    if not u.startswith(("http://", "https://")):
        u = "https://" + u
    return u


def first_letter(name):
    n = re.sub(r"^(the|a|an)\s+", "", name.strip(), flags=re.IGNORECASE)
    return (n[:1] or "?").upper()


def truncate(text, max_chars=180):
    if not text:
        return ""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    # cut at word boundary
    cut = text[:max_chars].rsplit(" ", 1)[0]
    return cut.rstrip(",.;:") + "…"


def first_contact(contacts):
    """Gladstone 'Contacts' field is 'Name, Title; Name, Title' — return first name only, no title."""
    if not contacts:
        return ""
    first = contacts.split(";")[0].strip()
    name = first.split(",")[0].strip()
    return name


def load_source(src):
    """Read CSV and normalize to common Member records."""
    members = []
    with open(src["path"], "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            name = (row.get("Name") or "").strip()
            if not name:
                continue
            members.append({
                "source_key":   src["key"],
                "source_label": src["label"],
                "name":         name,
                "category":     (row.get("Category") or "").strip(),
                "address":      (row.get("Address") or "").strip(),
                "phone":        (row.get("Phone") or "").strip(),
                "website":      normalize_url(row.get("Website")),
                "detail_url":   normalize_url(row.get("DetailURL")),
                "contact":      first_contact(row.get("Contacts") or ""),
                "member_since": (row.get("MemberSince") or "").strip(),
                "description":  (row.get("Description") or "").strip(),
            })
    return members


def render_card(m):
    letter = first_letter(m["name"])
    ind = industry_bucket(m["category"])
    ind_label = industry_label(ind)
    city = extract_city(m["address"])
    city_s = city_slug(city)

    # Contact row: phone + website (skip empty)
    contact_bits = []
    if m["phone"]:
        contact_bits.append(f'<a href="tel:{m["phone"]}">{html.escape(m["phone"])}</a>')
    if m["website"]:
        domain = re.sub(r"^https?://(www\.)?", "", m["website"]).rstrip("/")
        contact_bits.append(f'<a href="{html.escape(m["website"])}" target="_blank" rel="noopener">{html.escape(domain)}</a>')
    contact_row = " &middot; ".join(contact_bits) if contact_bits else "<em>No contact listed</em>"

    addr_html = (
        f'<p class="dir-card-addr">{html.escape(m["address"])}</p>' if m["address"]
        else '<p class="dir-card-addr"><em>No address listed</em></p>'
    )

    # Description block (Gladstone has it; Liberty doesn't)
    desc_html = (
        f'<p class="dir-card-bio">{html.escape(truncate(m["description"], 220))}</p>'
        if m["description"] else ""
    )

    # Contact person line (Gladstone)
    person_html = (
        f'<p class="dir-card-person">{html.escape(m["contact"])}</p>'
        if m["contact"] else ""
    )

    # Member since (Gladstone)
    since_text = (
        f'Member since {html.escape(m["member_since"])} &middot; {html.escape(m["source_label"])}'
        if m["member_since"]
        else html.escape(m["source_label"])
    )

    # CTA: detail URL if available (Liberty), otherwise just source label
    cta = (
        f'<a class="dir-card-cta" href="{html.escape(m["detail_url"])}" target="_blank" rel="noopener">View Chamber listing &rarr;</a>'
        if m["detail_url"] else
        '<span class="dir-card-cta" style="opacity:0.5;border-bottom-color:transparent;">—</span>'
    )

    tags = []
    if ind != "other":
        tags.append(f'<span class="dir-tag circle">{html.escape(ind_label)}</span>')
    if m["category"]:
        tags.append(f'<span class="dir-tag">{html.escape(m["category"])}</span>')
    if city:
        tags.append(f'<span class="dir-tag">{html.escape(city)}</span>')
    tags_html = "\n            ".join(tags)

    return f'''        <article class="dir-card" data-name="{html.escape(m["name"])}" data-letter="{letter}" data-industry="{ind}" data-city="{city_s}" data-source="{m["source_key"]}">
          <div class="dir-card-head">
            <div class="dir-card-logo">{letter}</div>
            <div class="dir-card-headline">
              <h3>{html.escape(m["name"])}</h3>
              <p class="dir-card-position">{html.escape(m["category"]) if m["category"] else "<em>Uncategorized</em>"}</p>
              {person_html}
            </div>
          </div>
          {desc_html}
          <div class="dir-card-meta">
            {addr_html}
            <p class="dir-card-contact">{contact_row}</p>
          </div>
          <div class="dir-card-tags">
            {tags_html}
          </div>
          <div class="dir-card-foot">
            <span class="dir-card-since">{since_text}</span>
            {cta}
          </div>
        </article>'''


def render_chips(group_label, attr, options, include_all=True, all_label="All"):
    """options is list of (slug, label, count_or_None) tuples."""
    chips = []
    if include_all:
        chips.append(f'<button class="dir-chip active" data-{attr}="all">{html.escape(all_label)}</button>')
    for slug, label, count in options:
        cnt = f' <span style="opacity:0.6;">({count})</span>' if count is not None else ""
        chips.append(f'<button class="dir-chip" data-{attr}="{html.escape(slug)}">{html.escape(label)}{cnt}</button>')
    return "\n            ".join(chips)


def build():
    all_members = []
    counts_by_source = {}
    for src in SOURCES:
        ms = load_source(src)
        counts_by_source[src["label"]] = len(ms)
        all_members.extend(ms)

    total = len(all_members)
    # Sort by name for stable A-Z (strip leading "The/A/An")
    all_members.sort(key=lambda m: re.sub(r"^(the|a|an)\s+", "", m["name"].strip().lower()))

    # Distributions
    industries = Counter(industry_bucket(m["category"]) for m in all_members)
    cities = Counter(extract_city(m["address"]) for m in all_members if extract_city(m["address"]))

    # Chip option lists
    industry_options = []
    for slug, label, _ in INDUSTRY_BUCKETS:
        c = industries.get(slug, 0)
        if c > 0:
            industry_options.append((slug, label, c))
    if industries.get("other", 0) > 0:
        industry_options.append(("other", "Other", industries["other"]))

    top_cities = cities.most_common(10)
    city_options = [(city_slug(c), c, n) for c, n in top_cities]

    source_options = [(src["key"], src["label"], counts_by_source[src["label"]]) for src in SOURCES]

    cards_html = "\n\n".join(render_card(m) for m in all_members)
    industry_chips = render_chips("Industry", "industry", industry_options, all_label="All Industries")
    city_chips = render_chips("City", "city", city_options, all_label="All Cities")
    source_chips = render_chips("Source", "source", source_options, all_label="All Sources")

    # Demo banner: which sources, total count
    source_breakdown = " + ".join(f"{src['label']} ({counts_by_source[src['label']]})" for src in SOURCES)

    page = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Member Directory | ACA Northland</title>
    <meta name="description" content="Find and connect with members of the ACA Northland business club. A trust device for members — not a phonebook.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">
    <style>
      .demo-banner {{
        background: #8a2828;
        color: #f5ede1;
        padding: 10px clamp(18px, 5vw, 48px);
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        text-align: center;
        border-bottom: 1px solid rgba(245,237,225,0.18);
      }}
      .demo-banner strong {{ color: #e8c670; font-weight: 700; }}
      @media (max-width: 480px) {{
        .demo-banner {{ font-size: 11px; padding: 8px 14px; letter-spacing: 0.12em; line-height: 1.5; }}
      }}
      .dir-card-meta {{ margin: 0 0 12px; }}
      .dir-card-addr {{
        font-size: 12px; color: var(--muted);
        margin: 0 0 4px; line-height: 1.4;
      }}
      .dir-card-contact {{
        font-size: 12px; margin: 0; line-height: 1.5;
      }}
      .dir-card-contact a {{
        color: var(--ink-soft); text-decoration: none;
        border-bottom: 1px dotted var(--border);
      }}
      .dir-card-contact a:hover {{ color: var(--gold); border-bottom-color: var(--gold); }}
      .dir-card-person {{
        font-size: 11px; color: var(--gold); margin: 4px 0 0;
        font-weight: 600; letter-spacing: 0.02em;
      }}
      .dir-card-bio {{
        font-size: 12.5px; line-height: 1.5;
        color: var(--ink-soft);
        margin: 0 0 12px;
        font-family: "Playfair Display", Georgia, serif;
        font-style: italic;
      }}
      .dir-count {{
        font-size: 13px; color: var(--muted);
        padding: 12px clamp(18px, 5vw, 48px) 0;
        max-width: 1280px; margin: 0 auto;
      }}
      .dir-count strong {{ color: var(--ink); }}
    </style>
  </head>
  <body>
    <header class="aca-header">
      <div class="aca-header-inner">
        <a class="aca-brand" href="../"><img class="aca-brand-logo" src="../assets/logos/aca-white.png" alt="ACA Business Club"><span>
            <strong>ACA Northland</strong>
            <small>Business Club &middot; Liberty &amp; Vivion</small>
          </span>
        </a>
        <nav class="aca-nav">
          <a href="../">Home</a>
          <a href="../liberty/">Liberty</a>
          <a href="../vivion/">Vivion</a>
          <a href="./" class="active">Directory</a>
          <a href="../contact.html">Contact</a>
        </nav>
      </div>
    </header>

    <main>
      <div class="demo-banner">
        <strong>Demo Preview</strong> &middot; Directory populated with Liberty + Gladstone Chamber businesses ({total} listings) &middot; Real ACA member listings coming soon
      </div>

      <section class="aca-hero aca-hero-directory">
        <div class="aca-hero-inner">
          <span class="aca-eyebrow">Member Directory</span>
          <h1>Members of the ACA Business Club</h1>
          <p class="aca-lede">
            A roster of small businesses, makers, and stewards across the Northland. Built so members
            can find each other &mdash; not for the public phonebook.
          </p>
        </div>
        <div class="dir-hero-addresses">
          <div class="dir-hero-address"><strong>Northland</strong>1400 NW Vivion Rd, Kansas City, MO 64118</div>
          <div class="dir-hero-address"><strong>Liberty</strong>1 East Kansas Street, Liberty, MO 64068</div>
        </div>
      </section>

      <div class="dir-toolbar">
        <div class="dir-toolbar-inner">
          <div class="dir-search-row">
            <input class="dir-search" id="dirSearch" type="search" placeholder="Search by name, category, contact, or keyword&hellip;" autocomplete="off">
          </div>

          <div class="dir-chips" data-filter-group="source">
            <span class="dir-chip-group-label">Source</span>
            {source_chips}
          </div>

          <div class="dir-chips" data-filter-group="industry">
            <span class="dir-chip-group-label">Industry</span>
            {industry_chips}
          </div>

          <div class="dir-chips" data-filter-group="city">
            <span class="dir-chip-group-label">City</span>
            {city_chips}
          </div>

          <div class="dir-az-bar" id="dirAzBar"></div>
        </div>
      </div>

      <p class="dir-count"><strong id="dirCount">{total}</strong> of <strong>{total}</strong> businesses</p>

      <div class="dir-grid" id="dirGrid">
{cards_html}
      </div>

      <section class="aca-info-strip">
        <h2>This is what the pattern looks like at scale.</h2>
        <p>The real ACA Business Club directory will run on the same UX but with curated club members &mdash; trust device first, lookup tool second.</p>
        <p style="margin-top:24px;"><a class="aca-btn aca-btn-gold" href="../contact.html">Inquire About Membership</a></p>
      </section>
    </main>

    <footer class="aca-footer">
      <div class="aca-footer-inner">
        <div class="aca-footer-brand"><img class="aca-footer-logo" src="../assets/logos/aca-white.png" alt="ACA Business Club"><strong>ACA Northland</strong>
          <p>The regional business club for the Northland. With locations at Vivion and the historic 1894 Restoration Building on Liberty Square.</p>
        </div>
        <div>
          <h3>Locations</h3>
          <a href="../liberty/">Liberty &mdash; 1894 Restoration Building</a>
          <a href="../vivion/">Vivion</a>
        </div>
        <div>
          <h3>The Club</h3>
          <a href="./">Member Directory</a>
          <a href="../contact.html">Contact &amp; Membership</a>
          <a href="https://1894.tours" rel="noopener">1894.tours &mdash; Book the Space</a>
        </div>
      </div>
      <div class="aca-footer-bottom">
        <div class="footer-copyright">
          <p class="copyright-line">
            © 2026 ACA Northland Business Club · Liberty Square ·
            Operating at the 1894 Restoration Building
          </p>
          <p class="site-credit">
            Site by
            <a href="https://ninja-360.com" target="_blank" rel="noopener">
              Ninja 360 Digital Media
            </a>
            · © Ninja360.net
          </p>
        </div>
      </div>
    </footer>

    <script>
      (function() {{
        var grid = document.getElementById('dirGrid');
        var cards = Array.from(grid.querySelectorAll('.dir-card'));
        var searchInput = document.getElementById('dirSearch');
        var azBar = document.getElementById('dirAzBar');
        var countEl = document.getElementById('dirCount');
        var state = {{ search: '', industry: 'all', city: 'all', source: 'all' }};

        var letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
        var present = new Set();
        cards.forEach(function(c) {{ if (c.dataset.letter) present.add(c.dataset.letter); }});
        letters.forEach(function(L) {{
          var a = document.createElement('a');
          a.textContent = L;
          a.href = '#letter-' + L;
          a.dataset.letter = L;
          if (!present.has(L)) a.classList.add('disabled');
          a.addEventListener('click', function(e) {{
            e.preventDefault();
            var match = cards.find(function(c) {{
              return c.dataset.letter === L && c.style.display !== 'none';
            }});
            if (match) match.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
          }});
          azBar.appendChild(a);
        }});

        function bindGroup(groupName, attr, key) {{
          var chips = document.querySelectorAll('[data-filter-group="' + groupName + '"] .dir-chip');
          chips.forEach(function(chip) {{
            chip.addEventListener('click', function() {{
              chips.forEach(function(c) {{ c.classList.remove('active'); }});
              chip.classList.add('active');
              state[key] = chip.dataset[attr];
              applyFilters();
            }});
          }});
        }}
        bindGroup('industry', 'industry', 'industry');
        bindGroup('city', 'city', 'city');
        bindGroup('source', 'source', 'source');

        searchInput.addEventListener('input', function(e) {{
          state.search = e.target.value.toLowerCase().trim();
          applyFilters();
        }});

        function applyFilters() {{
          var visible = 0;
          cards.forEach(function(c) {{
            var matchIndustry = state.industry === 'all' || c.dataset.industry === state.industry;
            var matchCity = state.city === 'all' || c.dataset.city === state.city;
            var matchSource = state.source === 'all' || c.dataset.source === state.source;
            var matchSearch = !state.search || c.textContent.toLowerCase().indexOf(state.search) !== -1;
            var show = matchIndustry && matchCity && matchSource && matchSearch;
            c.style.display = show ? '' : 'none';
            if (show) visible++;
          }});
          countEl.textContent = visible;

          var existing = grid.querySelector('.dir-empty');
          if (existing) existing.remove();
          if (visible === 0) {{
            var empty = document.createElement('p');
            empty.className = 'dir-empty';
            empty.textContent = 'No businesses match those filters. Try clearing one.';
            grid.appendChild(empty);
          }}
        }}
      }})();
    </script>
  </body>
</html>
'''
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(page)

    print(f"Wrote {OUT_PATH}")
    print(f"  Total members: {total}")
    for src in SOURCES:
        print(f"    {src['label']:<22} {counts_by_source[src['label']]:>4}")
    print(f"  Industry distribution:")
    for slug, label, _ in INDUSTRY_BUCKETS:
        if industries.get(slug):
            print(f"    {slug:<14} {industries[slug]:>4}  ({label})")
    if industries.get("other"):
        print(f"    {'other':<14} {industries['other']:>4}")
    print(f"  Top cities: {top_cities}")


if __name__ == "__main__":
    build()
