import os
import math

OUTPUT_PROJECTS = r"d:\Git setup\projects.svg"

# User's REAL GitHub Projects — matching arifhaxn card style
projects = [
    {
        "repo": "UnnamedPeople-Chin/Star-Wars-AR",
        "title": "Star Wars AR_",
        "desc": "Immersive Star Wars character AR visualizer",
        "tags": ["C#", "Unity"],
        "langs": [("C#", 63, "#22D3EE"), ("ShaderLab", 24, "#A78BFA"), ("HLSL", 13, "#10B981")],
        "stars": 4,
        "updated": "updated 2w ago",
        "icon_color": "#22D3EE",
        "icon": '<path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" fill="none" stroke="#22D3EE" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/MoneyFlow",
        "title": "MoneyFlow_",
        "desc": "Finance money flow manager for PBO project",
        "tags": ["Java", "OOP"],
        "langs": [("Java", 78, "#10B981"), ("XML", 15, "#F59E0B"), ("Gradle", 7, "#A78BFA")],
        "stars": 2,
        "updated": "updated 1mo ago",
        "icon_color": "#10B981",
        "icon": '<circle cx="12" cy="12" r="9" fill="none" stroke="#10B981" stroke-width="2.5"/><path d="M12 8v4l3 3" fill="none" stroke="#10B981" stroke-width="2.5" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/schedule-organizer",
        "title": "Schedule Organizer_",
        "desc": "Smart schedule and task routine organizer",
        "tags": ["JavaScript", "CSS"],
        "langs": [("JavaScript", 55, "#A78BFA"), ("HTML", 28, "#EC4899"), ("CSS", 17, "#22D3EE")],
        "stars": 3,
        "updated": "updated 1mo ago",
        "icon_color": "#A78BFA",
        "icon": '<rect x="3" y="4" width="18" height="16" rx="2" fill="none" stroke="#A78BFA" stroke-width="2.5"/><path d="M16 2v4M8 2v4M3 10h18" fill="none" stroke="#A78BFA" stroke-width="2.5" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/Wand-Enhancer",
        "title": "Wand Enhancer_",
        "desc": "Advanced UX and interoperability extension",
        "tags": ["C++", "System"],
        "langs": [("C++", 72, "#F59E0B"), ("CMake", 18, "#10B981"), ("Shell", 10, "#A78BFA")],
        "stars": 5,
        "updated": "updated 1mo ago",
        "icon_color": "#F59E0B",
        "icon": '<path d="M13 2L3 14h9l-1 6 10-12h-9l1-6z" fill="none" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/github-readme-stats",
        "title": "Readme Stats_",
        "desc": "Dynamically generated stats for github",
        "tags": ["Node.js", "Vercel"],
        "langs": [("JavaScript", 65, "#EC4899"), ("CSS", 22, "#22D3EE"), ("EJS", 13, "#F59E0B")],
        "stars": 7,
        "updated": "updated 3d ago",
        "icon_color": "#EC4899",
        "icon": '<rect x="3" y="3" width="18" height="18" rx="2" fill="none" stroke="#EC4899" stroke-width="2.5"/><path d="M8 17V11M12 17V7M16 17V13" fill="none" stroke="#EC4899" stroke-width="2.5" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/AI-Portfolio",
        "title": "Career Logic AI_",
        "desc": "AI powered CV management and career builder",
        "tags": ["Python", "React", "Groq"],
        "langs": [("Python", 80, "#3B82F6"), ("TypeScript", 12, "#22D3EE"), ("CSS", 8, "#EC4899")],
        "stars": 10,
        "updated": "updated 1d ago",
        "icon_color": "#3B82F6",
        "icon": '<circle cx="12" cy="12" r="10" fill="none" stroke="#3B82F6" stroke-width="2.5"/><path d="M12 8v4l2.5 2.5" fill="none" stroke="#3B82F6" stroke-width="2.5" stroke-linecap="round"/><circle cx="12" cy="12" r="2" fill="#3B82F6"/>'
    }
]


def build_donut(langs, cx, cy, radius=32, stroke_w=7):
    """Build a multi-segment donut chart exactly like arifhaxn."""
    total = sum(l[1] for l in langs)
    circ = 2 * math.pi * radius
    segments = []
    offset = 0
    for name, pct, color in langs:
        dash_len = (pct / total) * circ
        gap = circ - dash_len
        segments.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_w}" '
            f'stroke-dasharray="{dash_len:.1f} {gap:.1f}" '
            f'stroke-dashoffset="{-offset:.1f}" '
            f'transform="rotate(-90 {cx} {cy})"/>'
        )
        offset += dash_len
    # Center percentage text
    primary_pct = langs[0][1]
    segments.append(
        f'<text x="{cx}" y="{cy + 5}" font-size="13" font-weight="bold" '
        f'fill="#F8FAFC" text-anchor="middle">{primary_pct}%</text>'
    )
    return "\n        ".join(segments)


def build_lang_legend(langs, x, y):
    """Build stacked language legend dots like arifhaxn."""
    items = []
    for i, (name, pct, color) in enumerate(langs):
        ly = y + i * 18
        items.append(
            f'<circle cx="{x}" cy="{ly}" r="3.5" fill="{color}"/>'
            f'<text x="{x + 10}" y="{ly + 4}" font-size="10" fill="#94A3B8">'
            f'{name} {pct}%</text>'
        )
    return "\n        ".join(items)


def build_projects_svg():
    cards_xml = []

    positions = [
        (30, 56),
        (605, 56),
        (30, 280),
        (605, 280),
        (30, 504),
        (605, 504),
    ]
    card_w, card_h = 545, 200

    for idx, p in enumerate(projects):
        x, y = positions[idx]
        delay = 0.15 + idx * 0.12

        # --- Tag pills ---
        tag_pills = []
        tx = x + 18
        ty = y + 142
        for t in p["tags"]:
            tw = len(t) * 7.0 + 18
            tag_pills.append(
                f'<rect x="{tx}" y="{ty}" width="{tw:.0f}" height="24" rx="12" '
                f'fill="rgba(34,211,238,0.08)" stroke="rgba(34,211,238,0.35)" stroke-width="1"/>'
                f'<text x="{tx + tw/2:.0f}" y="{ty + 16}" font-size="10" '
                f'fill="#22D3EE" text-anchor="middle">{t}</text>'
            )
            tx += tw + 8

        # --- Donut chart ---
        donut = build_donut(p["langs"], x + 480, y + 82, radius=32, stroke_w=7)

        # --- Language legend ---
        legend = build_lang_legend(p["langs"], x + 355, y + 62)

        cards_xml.append(f'''
    <!-- CARD {idx+1}: {p["title"]} -->
    <g opacity="0">
      <!-- Card background -->
      <rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="14"
            fill="#0D1424" stroke="rgba(34,211,238,0.22)" stroke-width="1">
        <animate attributeName="stroke-opacity" values="0.18;0.40;0.18" dur="4s" repeatCount="indefinite"/>
      </rect>

      <!-- Repo path header -->
      <circle cx="{x + 14}" cy="{y + 18}" r="2.5" fill="#22D3EE" opacity="0.6"/>
      <text x="{x + 24}" y="{y + 22}" font-size="11" fill="#475569">{p["repo"]}</text>

      <!-- Status dot (top-right) -->
      <circle cx="{x + card_w - 16}" cy="{y + 18}" r="3.5" fill="#10B981" opacity="0.7">
        <animate attributeName="opacity" values="0.4;0.9;0.4" dur="3s" repeatCount="indefinite"/>
      </circle>

      <!-- Icon box -->
      <rect x="{x + 14}" y="{y + 38}" width="52" height="52" rx="14"
            fill="rgba(15,23,42,0.9)" stroke="{p["icon_color"]}" stroke-width="1.2"/>
      <g transform="translate({x + 28},{y + 52}) scale(1.05)">
        {p["icon"]}
      </g>

      <!-- Title -->
      <text x="{x + 78}" y="{y + 60}" font-size="18" font-weight="bold" fill="#F8FAFC">
        {p["title"]}</text>

      <!-- Description -->
      <text x="{x + 78}" y="{y + 82}" font-size="11" fill="#94A3B8">
        {p["desc"]}</text>

      <!-- Language legend (stacked dots) -->
      {legend}

      <!-- Donut chart (multi-segment) -->
      {donut}

      <!-- Tag pills -->
      {"".join(tag_pills)}

      <!-- Stars + updated -->
      <text x="{x + 18}" y="{y + 188}" font-size="11" fill="#F59E0B">★</text>
      <text x="{x + 32}" y="{y + 188}" font-size="11" font-weight="bold" fill="#94A3B8">
        {p["stars"]}</text>
      <text x="{x + 56}" y="{y + 188}" font-size="11" fill="#475569">
        {p["updated"]}</text>

      <!-- Entrance animation -->
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay:.2f}s" fill="freeze"/>
    </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="760" viewBox="0 0 1180 760"
     font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
     role="img" aria-label="Projects List">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#080D1A"/>
      <stop offset="1" stop-color="#0B1120"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1180" height="760" rx="16" fill="url(#bgGrad)"/>

  <!-- Header -->
  <g opacity="0">
    <text x="32" y="34" font-size="12" font-weight="bold" letter-spacing="2.5" fill="#22D3EE">
      PROJECTS.LIST
      <tspan fill="#475569" letter-spacing="1"> ./projects.sh --all</tspan>
    </text>
    <line x1="32" y1="44" x2="1148" y2="44" stroke="rgba(34,211,238,0.15)"/>
    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.05s" fill="freeze"/>
  </g>

  <!-- Cards -->
{"".join(cards_xml)}
</svg>'''

    with open(OUTPUT_PROJECTS, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Saved {OUTPUT_PROJECTS}")


if __name__ == "__main__":
    build_projects_svg()
