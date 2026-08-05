import os
import math

OUTPUT_PROJECTS = r"d:\Git setup\projects.svg"

projects = [
    {
        "repo": "UnnamedPeople-Chin/LeadUnity",
        "title": "LeadUnity_",
        "desc": "AI Powered Lead Management &amp; Analytics Platform",
        "tags": ["Next.js", "Node.js", "TailwindCSS"],
        "lang_name": "TypeScript",
        "lang_pct": 82,
        "stars": 12,
        "updated": "updated 2d ago",
        "icon_color": "#7C3AED",
        "donut_color": "#A78BFA",
        "icon": '<path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" fill="none" stroke="#22D3EE" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/OnePick",
        "title": "OnePick_",
        "desc": "Smart Decision &amp; Character Matcher Engine",
        "tags": ["React", "Express", "MongoDB"],
        "lang_name": "Python",
        "lang_pct": 65,
        "stars": 8,
        "updated": "updated 5d ago",
        "icon_color": "#10B981",
        "donut_color": "#10B981",
        "icon": '<circle cx="12" cy="12" r="9" fill="none" stroke="#10B981" stroke-width="2.5"/><path d="M12 7v5l3 3" fill="none" stroke="#10B981" stroke-width="2.5" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/Chessy",
        "title": "Chessy_",
        "desc": "Real-time Multiplayer Chess Engine &amp; AI Bot",
        "tags": ["C++", "React", "WebSockets"],
        "lang_name": "C++",
        "lang_pct": 74,
        "stars": 15,
        "updated": "updated 1w ago",
        "icon_color": "#F59E0B",
        "donut_color": "#F59E0B",
        "icon": '<path d="M7 21h10M12 3v14M8 7h8M9 11h6" fill="none" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/Claster",
        "title": "Claster_",
        "desc": "Class Scheduling &amp; Routine Tracking App",
        "tags": ["Next.js", "PostgreSQL", "Prisma"],
        "lang_name": "TypeScript",
        "lang_pct": 58,
        "stars": 6,
        "updated": "updated 2w ago",
        "icon_color": "#EC4899",
        "donut_color": "#EC4899",
        "icon": '<rect x="3" y="4" width="18" height="16" rx="2" fill="none" stroke="#EC4899" stroke-width="2.5"/><path d="M16 2v4M8 2v4M3 10h18" fill="none" stroke="#EC4899" stroke-width="2.5" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/OneTELE",
        "title": "OneTELE_",
        "desc": "Custom Teleprompter &amp; Recording Studio Suite",
        "tags": ["React", "WebRTC", "TailwindCSS"],
        "lang_name": "JavaScript",
        "lang_pct": 79,
        "stars": 10,
        "updated": "updated 3w ago",
        "icon_color": "#6366F1",
        "donut_color": "#6366F1",
        "icon": '<polygon points="23 7 16 12 23 17 23 7" fill="none" stroke="#6366F1" stroke-width="2.5" stroke-linejoin="round"/><rect x="1" y="5" width="15" height="14" rx="2" fill="none" stroke="#6366F1" stroke-width="2.5"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/CareerLogicAI",
        "title": "Career Logic AI_",
        "desc": "AI Powered Resume Analyzer &amp; Career Builder",
        "tags": ["Python", "FastAPI", "OpenAI"],
        "lang_name": "Python",
        "lang_pct": 88,
        "stars": 22,
        "updated": "updated 1mo ago",
        "icon_color": "#3B82F6",
        "donut_color": "#3B82F6",
        "icon": '<path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 14a4 4 0 1 1 4-4 4 4 0 0 1-4 4z" fill="none" stroke="#3B82F6" stroke-width="2.5"/>'
    }
]

def build_projects_svg():
    cards_xml = []
    
    positions = [
        (36, 60),    # Card 0: Col 1, Row 1
        (608, 60),   # Card 1: Col 2, Row 1
        (36, 290),   # Card 2: Col 1, Row 2
        (608, 290),  # Card 3: Col 2, Row 2
        (36, 520),   # Card 4: Col 1, Row 3
        (608, 520),  # Card 5: Col 2, Row 3
    ]

    for idx, p in enumerate(projects):
        x_pos, y_pos = positions[idx]
        card_w, card_h = 536, 205

        # Donut progress math
        pct = p["lang_pct"]
        radius = 28
        circumference = 2 * math.pi * radius
        stroke_dasharray = f"{(pct / 100.0) * circumference:.1f} {circumference:.1f}"

        # Tags pills
        tag_pills = []
        tag_x = x_pos + 80
        tag_y = y_pos + 130
        
        for t in p["tags"]:
            w_tag = len(t) * 7.5 + 16
            tag_pills.append(f'''
        <rect x="{tag_x}" y="{tag_y}" width="{w_tag}" height="22" rx="11" fill="rgba(124,58,237,0.20)" stroke="rgba(167,139,250,0.4)"/>
        <text x="{tag_x + w_tag/2}" y="{tag_y + 15}" font-size="10" font-weight="bold" fill="#A78BFA" text-anchor="middle">{t}</text>
            ''')
            tag_x += w_tag + 8

        cards_xml.append(f'''
    <!-- CARD {idx+1}: {p["title"]} -->
    <g>
      <!-- Card Outer Border & Glow -->
      <rect x="{x_pos}" y="{y_pos}" width="{card_w}" height="{card_h}" rx="12" fill="#0A101F" stroke="rgba(34,211,238,0.30)" stroke-width="1.5" filter="url(#glow3)"/>
      <rect x="{x_pos}" y="{y_pos}" width="{card_w}" height="{card_h}" rx="12" fill="#0A101F" stroke="rgba(34,211,238,0.25)"/>

      <!-- Repo Path Header -->
      <circle cx="{x_pos + 20}" cy="{y_pos + 22}" r="3" fill="#22D3EE"/>
      <text x="{x_pos + 30}" y="{y_pos + 26}" font-size="11" fill="#64748B">{p["repo"]}</text>

      <!-- Icon Box -->
      <rect x="{x_pos + 20}" y="{y_pos + 48}" width="48" height="48" rx="10" fill="rgba(15,23,42,0.8)" stroke="{p["icon_color"]}" stroke-width="1.5"/>
      <g transform="translate({x_pos + 32}, {y_pos + 60}) scale(0.9)">
        {p["icon"]}
      </g>

      <!-- Title & Description -->
      <text x="{x_pos + 80}" y="{y_pos + 68}" font-size="16" font-weight="bold" fill="#F8FAFC">{p["title"]}</text>
      <text x="{x_pos + 80}" y="{y_pos + 92}" font-size="11" fill="#94A3B8">{p["desc"]}</text>

      <!-- Tag Pills -->
      {"".join(tag_pills)}

      <!-- Stars & Updated -->
      <path d="M{x_pos + 80} {y_pos + 172}l1.2 2.5 2.8.4-2 2 .5 2.8-2.5-1.3-2.5 1.3.5-2.8-2-2 2.8-.4z" fill="#F59E0B"/>
      <text x="{x_pos + 95}" y="{y_pos + 176}" font-size="10" font-weight="bold" fill="#94A3B8">{p["stars"]}</text>
      <text x="{x_pos + 120}" y="{y_pos + 176}" font-size="10" fill="#64748B">{p["updated"]}</text>

      <!-- Donut Circle Chart -->
      <g transform="translate({x_pos + 460}, {y_pos + 105})">
        <circle cx="0" cy="0" r="{radius}" fill="none" stroke="#1E293B" stroke-width="6"/>
        <circle cx="0" cy="0" r="{radius}" fill="none" stroke="{p["donut_color"]}" stroke-width="6" stroke-dasharray="{stroke_dasharray}" transform="rotate(-90)"/>
        <text x="0" y="4" font-size="12" font-weight="bold" fill="#F8FAFC" text-anchor="middle">{pct}%</text>
      </g>

      <!-- Language Legend -->
      <circle cx="{x_pos + 365}" cy="{y_pos + 90}" r="3" fill="{p["donut_color"]}"/>
      <text x="{x_pos + 375}" y="{y_pos + 93}" font-size="10" fill="#94A3B8">{p["lang_name"]} {pct}%</text>
    </g>
        ''')

    svg_code = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="765" viewBox="0 0 1180 765" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace" role="img" aria-label="Projects List">
  <defs>
    <linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0A101F"/>
      <stop offset="1" stop-color="#0C1426"/>
    </linearGradient>
    <filter id="glow3" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
    <clipPath id="winClip">
      <rect x="2" y="2" width="1176" height="761" rx="18"/>
    </clipPath>
  </defs>

  <rect x="2" y="2" width="1176" height="761" rx="18" fill="#070B16"/>
  <g clip-path="url(#winClip)">
    <rect x="2" y="2" width="1176" height="761" fill="url(#panelGrad)"/>
    
    <!-- Top Header -->
    <text x="38" y="38" font-size="12" font-weight="bold" letter-spacing="3" fill="#22D3EE">PROJECTS.LIST <tspan fill="#475569">./projects.sh --all</tspan></text>
    <line x1="38" y1="46" x2="1142" y2="46" stroke="rgba(34,211,238,0.20)"/>

    <!-- PROJECT CARDS GRID -->
{"".join(cards_xml)}
  </g>
</svg>'''

    with open(OUTPUT_PROJECTS, "w", encoding="utf-8") as f:
        f.write(svg_code)
    print(f"Saved {OUTPUT_PROJECTS}")

if __name__ == "__main__":
    build_projects_svg()
