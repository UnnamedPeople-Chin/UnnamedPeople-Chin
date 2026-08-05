import os
import math

OUTPUT_PROJECTS = r"d:\Git setup\projects.svg"

# User's REAL GitHub Projects
projects = [
    {
        "repo": "UnnamedPeople-Chin/Star-Wars-AR-Interactive-Character-Visualizer",
        "title": "Star Wars AR Visualizer_",
        "desc": "Immersive Star Wars character 3D &amp; AR visualizer",
        "tags": ["C#", "Unity", "Augmented Reality"],
        "lang_name": "C#",
        "lang_pct": 63,
        "stars": 4,
        "updated": "updated 2w ago",
        "icon_color": "#22D3EE",
        "donut_color": "#22D3EE",
        "icon": '<path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" fill="none" stroke="#22D3EE" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/Project-PBO-MoneyFlow",
        "title": "MoneyFlow PBO_",
        "desc": "Finance &amp; Money Flow Manager (OOP Java)",
        "tags": ["Java", "OOP", "Finance"],
        "lang_name": "Java",
        "lang_pct": 78,
        "stars": 2,
        "updated": "updated 1mo ago",
        "icon_color": "#10B981",
        "donut_color": "#10B981",
        "icon": '<circle cx="12" cy="12" r="9" fill="none" stroke="#10B981" stroke-width="2.5"/><path d="M12 7v5l3 3" fill="none" stroke="#10B981" stroke-width="2.5" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/schedule-organizer",
        "title": "Schedule Organizer_",
        "desc": "Smart Schedule &amp; Task Routine Organizer App",
        "tags": ["JavaScript", "HTML5", "CSS3"],
        "lang_name": "JavaScript",
        "lang_pct": 85,
        "stars": 3,
        "updated": "updated 1mo ago",
        "icon_color": "#A78BFA",
        "donut_color": "#A78BFA",
        "icon": '<rect x="3" y="4" width="18" height="16" rx="2" fill="none" stroke="#A78BFA" stroke-width="2.5"/><path d="M16 2v4M8 2v4M3 10h18" fill="none" stroke="#A78BFA" stroke-width="2.5" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/Wand-Enhancer",
        "title": "Wand Enhancer_",
        "desc": "Advanced UX &amp; Interoperability Suite",
        "tags": ["C++", "System", "UX Extension"],
        "lang_name": "C++",
        "lang_pct": 72,
        "stars": 5,
        "updated": "updated 1mo ago",
        "icon_color": "#F59E0B",
        "donut_color": "#F59E0B",
        "icon": '<path d="M7 21h10M12 3v14M8 7h8M9 11h6" fill="none" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/github-readme-stats",
        "title": "GitHub Readme Stats_",
        "desc": "Dynamically generated stats cards for GitHub",
        "tags": ["Node.js", "Vercel", "Express"],
        "lang_name": "JavaScript",
        "lang_pct": 91,
        "stars": 7,
        "updated": "updated 3d ago",
        "icon_color": "#EC4899",
        "donut_color": "#EC4899",
        "icon": '<polygon points="23 7 16 12 23 17 23 7" fill="none" stroke="#EC4899" stroke-width="2.5" stroke-linejoin="round"/><rect x="1" y="5" width="15" height="14" rx="2" fill="none" stroke="#EC4899" stroke-width="2.5"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/Alexios-AI-Portfolio",
        "title": "AI Full-Stack Portfolio_",
        "desc": "Personal AI Engineer Showcase Terminal",
        "tags": ["React", "Python", "TailwindCSS"],
        "lang_name": "Python",
        "lang_pct": 88,
        "stars": 10,
        "updated": "updated 1d ago",
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

        # Animated Donut Calculations
        pct = p["lang_pct"]
        radius = 28
        circumference = 2 * math.pi * radius
        final_dashoffset = circumference * (1 - pct / 100.0)

        # Entrance delay
        intro_delay = 0.2 + idx * 0.15

        # Truncate long repo text cleanly
        repo_display = p["repo"]
        if len(repo_display) > 42:
            repo_display = repo_display[:39] + "..."

        # Tags pills with neat spacing
        tag_pills = []
        tag_x = x_pos + 80
        tag_y = y_pos + 128
        
        for t in p["tags"]:
            w_tag = len(t) * 7.2 + 16
            tag_pills.append(f'''
        <rect x="{tag_x}" y="{tag_y}" width="{w_tag:.1f}" height="22" rx="11" fill="rgba(124,58,237,0.18)" stroke="rgba(167,139,250,0.35)"/>
        <text x="{tag_x + w_tag/2:.1f}" y="{tag_y + 15}" font-size="10" font-weight="bold" fill="#A78BFA" text-anchor="middle">{t}</text>
            ''')
            tag_x += w_tag + 8

        cards_xml.append(f'''
    <!-- CARD {idx+1}: {p["title"]} -->
    <g opacity="0">
      <!-- Card Outer Border & Subtle Pulse Glow -->
      <rect x="{x_pos}" y="{y_pos}" width="{card_w}" height="{card_h}" rx="12" fill="#0A101F" stroke="rgba(34,211,238,0.35)" stroke-width="1.5" filter="url(#glow3)">
        <animate attributeName="stroke-opacity" values="0.25;0.55;0.25" dur="4s" repeatCount="indefinite"/>
      </rect>
      <rect x="{x_pos}" y="{y_pos}" width="{card_w}" height="{card_h}" rx="12" fill="#0A101F" stroke="rgba(34,211,238,0.25)"/>

      <!-- Repo Path Header with Pulsing Dot -->
      <circle cx="{x_pos + 20}" cy="{y_pos + 22}" r="3" fill="#22D3EE">
        <animate attributeName="opacity" values="0.4;1;0.4" dur="2s" repeatCount="indefinite"/>
      </circle>
      <text x="{x_pos + 30}" y="{y_pos + 26}" font-size="11" font-weight="500" fill="#64748B">{repo_display}</text>

      <!-- Vector Icon Box -->
      <rect x="{x_pos + 20}" y="{y_pos + 48}" width="46" height="46" rx="10" fill="rgba(15,23,42,0.85)" stroke="{p["icon_color"]}" stroke-width="1.5"/>
      <g transform="translate({x_pos + 31}, {y_pos + 59}) scale(0.9)">
        {p["icon"]}
      </g>

      <!-- Title & Description -->
      <text x="{x_pos + 80}" y="{y_pos + 68}" font-size="15" font-weight="bold" fill="#F8FAFC">{p["title"]}</text>
      <text x="{x_pos + 80}" y="{y_pos + 92}" font-size="11" fill="#94A3B8">{p["desc"]}</text>

      <!-- Tag Pills -->
      {"".join(tag_pills)}

      <!-- Stars & Last Updated Footer -->
      <g transform="translate({x_pos + 80}, {y_pos + 168})">
        <path d="M0 0l1.2 2.5 2.8.4-2 2 .5 2.8-2.5-1.3-2.5 1.3.5-2.8-2-2 2.8-.4z" fill="#F59E0B"/>
        <text x="14" y="4" font-size="10" font-weight="bold" fill="#94A3B8">{p["stars"]}</text>
        <text x="36" y="4" font-size="10" fill="#64748B">{p["updated"]}</text>
      </g>

      <!-- Animated Donut Progress Circle -->
      <g transform="translate({x_pos + 465}, {y_pos + 105})">
        <circle cx="0" cy="0" r="{radius}" fill="none" stroke="#1E293B" stroke-width="5.5"/>
        <circle cx="0" cy="0" r="{radius}" fill="none" stroke="{p["donut_color"]}" stroke-width="5.5"
                stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{circumference:.1f}" transform="rotate(-90)">
          <animate attributeName="stroke-dashoffset" from="{circumference:.1f}" to="{final_dashoffset:.1f}" dur="1.4s" begin="{intro_delay + 0.3:.2f}s" fill="freeze"/>
        </circle>
        <text x="0" y="4" font-size="11" font-weight="bold" fill="#F8FAFC" text-anchor="middle">{pct}%</text>
      </g>

      <!-- Language Legend Indicator -->
      <g transform="translate({x_pos + 360}, {y_pos + 85})">
        <circle cx="0" cy="0" r="3" fill="{p["donut_color"]}"/>
        <text x="8" y="3" font-size="10" font-weight="600" fill="#94A3B8">{p["lang_name"]} {pct}%</text>
      </g>

      <!-- Sequential Card Entrance Animation -->
      <animate attributeName="opacity" values="0;1" dur="0.6s" begin="{intro_delay:.2f}s" fill="freeze"/>
    </g>
        ''')

    svg_code = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="765" viewBox="0 0 1180 765" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace" role="img" aria-label="Projects List">
  <defs>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#22D3EE"/>
      <stop offset="0.5" stop-color="#A78BFA"/>
      <stop offset="1" stop-color="#10B981"/>
    </linearGradient>
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
    
    <!-- Top Header Bar with Shimmer Animation -->
    <g opacity="0">
      <text x="38" y="38" font-size="11" font-weight="bold" letter-spacing="3" fill="#22D3EE">PROJECTS.LIST <tspan fill="#475569">./projects.sh --all</tspan></text>
      <line x1="38" y1="46" x2="1142" y2="46" stroke="rgba(34,211,238,0.25)"/>
      <animate attributeName="opacity" values="0;1" dur="0.5s" begin="0.1s" fill="freeze"/>
    </g>

    <!-- ANIMATED PROJECT CARDS GRID -->
{"".join(cards_xml)}
  </g>
</svg>'''

    with open(OUTPUT_PROJECTS, "w", encoding="utf-8") as f:
        f.write(svg_code)
    print(f"Saved {OUTPUT_PROJECTS}")

if __name__ == "__main__":
    build_projects_svg()
