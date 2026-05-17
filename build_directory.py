"""Generate directory/index.html from liberty-chamber-directory.csv.

Each run rebuilds the directory page from the CSV. Idempotent. Re-run any
time the CSV updates.

Mapping:
- 187 raw categories -> 8 broad industry chips (food, finance, health, pro,
  retail, trades, entertainment, community)
- City extracted from Address column for a CITY filter (replaces ACA-specific
  Circle chips since Chamber data has no circles)
- Availability dot OMITTED (no real data for it; not fabricating)
- "Member since" OMITTED (not in CSV; not fabricating)
- Per-card content: address, phone, website, category chip, industry chip,
  and a 'View Chamber listing' link to the DetailURL
"""
import csv
import os
import re
import html

CSV_PATH = r"C:\Users\tpete\liberty-chamber-directory.csv"
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "directory", "index.html")

# Industry buckets — substring match, case-insensitive, first match wins
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
     ["non-profit", "nonprofit", "church", "ministry", "community", "education", "school", "library", "museum", "chamber", "foundation", "association", "senior living", "child care", "preschool"]),
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
    if m:
        return m.group(1).strip()
    return ""


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


def render_card(row):
    name = row["Name"].strip()
    cat = row["Category"].strip()
    phone = row["Phone"].strip()
    addr = row["Address"].strip()
    web = normalize_url(row["Website"])
    detail = normalize_url(row["DetailURL"])
    letter = first_letter(name)
    ind = industry_bucket(cat)
    ind_label = industry_label(ind)
    city = extract_city(addr)
    city_s = city_slug(city)

    # Build address-row HTML (skip empty bits, never invent)
    contact_bits = []
    if phone:
        contact_bits.append(f'<a href="tel:{phone}">{html.escape(phone)}</a>')
    if web:
        domain = re.sub(r"^https?://(www\.)?", "", web).rstrip("/")
        contact_bits.append(f'<a href="{html.escape(web)}" target="_blank" rel="noopener">{html.escape(domain)}</a>')
    contact_row = " &middot; ".join(contact_bits) if contact_bits else "<em>No contact listed</em>"

    addr_html = (
        f'<p class="dir-card-addr">{html.escape(addr)}</p>' if addr
        else '<p class="dir-card-addr"><em>No address listed</em></p>'
    )

    cta = (
        f'<a class="dir-card-cta" href="{html.escape(detail)}" target="_blank" rel="noopener">View Chamber listing &rarr;</a>'
        if detail else
        '<span class="dir-card-cta" style="opacity:0.5;border-bottom-color:transparent;">No listing URL</span>'
    )

    return f'''        <article class="dir-card" data-name="{html.escape(name)}" data-letter="{letter}" data-industry="{ind}" data-city="{city_s}">
          <div class="dir-card-head">
            <div class="dir-card-logo">{letter}</div>
            <div class="dir-card-headline">
              <h3>{html.escape(name)}</h3>
              <p class="dir-card-position">{html.escape(cat) if cat else "<em>Uncategorized</em>"}</p>
            </div>
          </div>
          <div class="dir-card-meta">
            {addr_html}
            <p class="dir-card-contact">{contact_row}</p>
          </div>
          <div class="dir-card-tags">
            {f'<span class="dir-tag circle">{html.escape(ind_label)}</span>' if ind != "other" else ''}
            {f'<span class="dir-tag">{html.escape(cat)}</span>' if cat else ''}
            {f'<span class="dir-tag">{html.escape(city)}</span>' if city else ''}
          </div>
          <div class="dir-card-foot">
            <span class="dir-card-since">Liberty Chamber listing</span>
            {cta}
          </div>
        </article>'''


def render_industry_chips():
    chips = ['<button class="dir-chip active" data-industry="all">All Industries</button>']
    for slug, label, _ in INDUSTRY_BUCKETS:
        chips.append(f'<button class="dir-chip" data-industry="{slug}">{html.escape(label)}</button>')
    chips.append('<button class="dir-chip" data-industry="other">Other</button>')
    return "\n            ".join(chips)


def render_city_chips(cities):
    chips = ['<button class="dir-chip active" data-city="all">All Cities</button>']
    # cities is a list of (city, count) sorted desc by count, top N
    for city, count in cities:
        slug = city_slug(city)
        chips.append(f'<button class="dir-chip" data-city="{html.escape(slug)}">{html.escape(city)} <span style="opacity:0.6;">({count})</span></button>')
    return "\n            ".join(chips)


def build():
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    # Sort by name for stable A-Z
    rows.sort(key=lambda r: r["Name"].strip().lower())

    # Compute city distribution -> top 8 chips
    from collections import Counter
    city_counts = Counter(extract_city(r["Address"]) for r in rows)
    city_counts.pop("", None)
    top_cities = city_counts.most_common(8)

    cards_html = "\n\n".join(render_card(r) for r in rows)
    industry_chips = render_industry_chips()
    city_chips = render_city_chips(top_cities)

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
        background: #fff7e0;
        border-bottom: 2px solid #c48c37;
        color: #4a3c2c;
        padding: 14px clamp(18px, 5vw, 48px);
        font-size: 14px;
        text-align: center;
        font-weight: 500;
      }}
      .demo-banner strong {{ color: #8a2828; }}
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
        <a class="aca-brand" href="../">
          <span>
            <strong>ACA Northland</strong>
            <small>Business Club &middot; est. 1894</small>
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
        <strong>Demo data:</strong> populated with {len(rows)} businesses scraped from the Liberty Chamber of Commerce directory for design review. <strong>These are NOT ACA Business Club members.</strong> Real ACA member data replaces this for launch.
      </div>

      <section class="aca-hero sepia">
        <div class="aca-hero-inner">
          <span class="aca-eyebrow">Member Directory</span>
          <h1>Members of the ACA Business Club</h1>
          <p class="aca-lede">
            A roster of small businesses, makers, and stewards across the Northland. Built so members
            can find each other &mdash; not for the public phonebook.
          </p>
        </div>
      </section>

      <div class="dir-toolbar">
        <div class="dir-toolbar-inner">
          <div class="dir-search-row">
            <input class="dir-search" id="dirSearch" type="search" placeholder="Search by name, category, or keyword&hellip;" autocomplete="off">
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

      <p class="dir-count"><strong id="dirCount">{len(rows)}</strong> of <strong>{len(rows)}</strong> businesses</p>

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
        <div class="aca-footer-brand">
          <strong>ACA Northland</strong>
          <p>The regional business club for the Northland &mdash; Liberty, Gladstone, and the Kansas City Northland. Operating Castle Hall on Liberty Square since 1894.</p>
        </div>
        <div>
          <h3>Locations</h3>
          <a href="../liberty/">Liberty &mdash; Castle Hall</a>
          <a href="../vivion/">Vivion</a>
        </div>
        <div>
          <h3>The Club</h3>
          <a href="./">Member Directory</a>
          <a href="../contact.html">Contact &amp; Membership</a>
          <a href="https://1894.tours" rel="noopener">1894.tours &mdash; Castle Hall</a>
        </div>
      </div>
      <div class="aca-footer-bottom">
        &copy; ACA Northland Business Club &middot; Liberty Square &middot; Est. 1894
      </div>
    </footer>

    <script>
      (function() {{
        var grid = document.getElementById('dirGrid');
        var cards = Array.from(grid.querySelectorAll('.dir-card'));
        var searchInput = document.getElementById('dirSearch');
        var azBar = document.getElementById('dirAzBar');
        var countEl = document.getElementById('dirCount');
        var state = {{ search: '', industry: 'all', city: 'all' }};

        // Build A-Z bar from member letters
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

        searchInput.addEventListener('input', function(e) {{
          state.search = e.target.value.toLowerCase().trim();
          applyFilters();
        }});

        function applyFilters() {{
          var visible = 0;
          cards.forEach(function(c) {{
            var matchIndustry = state.industry === 'all' || c.dataset.industry === state.industry;
            var matchCity = state.city === 'all' || c.dataset.city === state.city;
            var matchSearch = !state.search || c.textContent.toLowerCase().indexOf(state.search) !== -1;
            var show = matchIndustry && matchCity && matchSearch;
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

    # Stats
    from collections import Counter
    industries = Counter(industry_bucket(r["Category"]) for r in rows)
    cities = Counter(extract_city(r["Address"]) for r in rows if extract_city(r["Address"]))
    print(f"Wrote {OUT_PATH}")
    print(f"  {len(rows)} cards rendered")
    print(f"  Industry distribution:")
    for slug, _, _ in INDUSTRY_BUCKETS:
        print(f"    {slug:<14} {industries.get(slug,0):>4}")
    print(f"    {'other':<14} {industries.get('other',0):>4}")
    print(f"  Top cities: {cities.most_common(8)}")


if __name__ == "__main__":
    build()
