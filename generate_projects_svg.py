import os
import math
import html

OUTPUT_PROJECTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects.svg")

# User's REAL GitHub Projects — matching arifhaxn card style
projects = [
    {
        "repo": "UnnamedPeople-Chin/9router-go",
        "title": "9Router Go_",
        "desc": "32K RPS LLM proxy gateway & token saver",
        "tags": ["Go", "Svelte", "LLM Proxy"],
        "langs": [("Go", 84, "#22D3EE"), ("Svelte", 10, "#F59E0B"), ("TypeScript", 6, "#3B82F6")],
        "stars": 8,
        "updated": "updated 1d ago",
        "icon_color": "#22D3EE",
        "icon": '<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" fill="none" stroke="#22D3EE" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/discode",
        "title": "DisCode RPC_",
        "desc": "Next-gen Discord Rich Presence for VS Code",
        "tags": ["TypeScript", "VS Code", "RPC"],
        "langs": [("TypeScript", 83, "#3B82F6"), ("HTML", 17, "#EC4899")],
        "stars": 6,
        "updated": "updated 1w ago",
        "icon_color": "#A78BFA",
        "icon": '<rect x="2" y="4" width="20" height="16" rx="3" fill="none" stroke="#A78BFA" stroke-width="2.3"/><path d="M8 10l-2 2 2 2M16 10l2 2-2 2M13 9l-2 6" fill="none" stroke="#A78BFA" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/AetherCast",
        "title": "AetherCast_",
        "desc": "Real-time hand-tracking & particle engine",
        "tags": ["JavaScript", "MediaPipe", "Electron"],
        "langs": [("JavaScript", 70, "#F59E0B"), ("Python", 16, "#3B82F6"), ("CSS", 14, "#22D3EE")],
        "stars": 5,
        "updated": "updated 3w ago",
        "icon_color": "#F59E0B",
        "icon": '<circle cx="12" cy="12" r="4" fill="none" stroke="#F59E0B" stroke-width="2.3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1" fill="none" stroke="#F59E0B" stroke-width="2.2" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/aphelion-iot-hub",
        "title": "Aphelion IoT Hub_",
        "desc": "ESP32 landslide early warning & telemetry",
        "tags": ["ESP32", "Firebase", "Flutter"],
        "langs": [("HTML/JS", 74, "#10B981"), ("C++/ESP32", 16, "#22D3EE"), ("Dart", 10, "#3B82F6")],
        "stars": 4,
        "updated": "updated 2d ago",
        "icon_color": "#10B981",
        "icon": '<path d="M12 20h.01M8.5 16.5a5 5 0 017 0M5 13a10 10 0 0114 0M2 9.5a15 15 0 0120 0" fill="none" stroke="#10B981" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/chin-portfolio",
        "title": "Chin Portfolio_",
        "desc": "Interactive web portfolio & creative hub",
        "tags": ["HTML5", "TypeScript", "Vite"],
        "langs": [("HTML", 93, "#EC4899"), ("Python", 5, "#3B82F6"), ("JS/TS", 2, "#22D3EE")],
        "stars": 4,
        "updated": "updated 1w ago",
        "icon_color": "#EC4899",
        "icon": '<circle cx="12" cy="12" r="9" fill="none" stroke="#EC4899" stroke-width="2.3"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18" fill="none" stroke="#EC4899" stroke-width="2" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/Star-Wars-AR-Visualizer",
        "title": "Star Wars AR_",
        "desc": "Interactive 3D character AR visualizer",
        "tags": ["C#", "Unity 6", "Vuforia"],
        "langs": [("C#", 97, "#22D3EE"), ("HLSL", 2, "#10B981"), ("ShaderLab", 1, "#A78BFA")],
        "stars": 4,
        "updated": "updated 3w ago",
        "icon_color": "#3B82F6",
        "icon": '<path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" fill="none" stroke="#3B82F6" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/schedule-organizer",
        "title": "Schedule Organizer_",
        "desc": "Smart task & agenda app with Firebase sync",
        "tags": ["Python", "JavaScript", "Firebase"],
        "langs": [("Python", 38, "#A78BFA"), ("JavaScript", 31, "#F59E0B"), ("HTML/CSS", 31, "#22D3EE")],
        "stars": 3,
        "updated": "updated 3w ago",
        "icon_color": "#22D3EE",
        "icon": '<rect x="3" y="4" width="18" height="16" rx="2" fill="none" stroke="#22D3EE" stroke-width="2.3"/><path d="M16 2v4M8 2v4M3 10h18" fill="none" stroke="#22D3EE" stroke-width="2.3" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/Project-PBO-MoneyFlow",
        "title": "MoneyFlow Pro_",
        "desc": "Desktop personal finance & cashflow suite",
        "tags": ["Java", "Swing GUI", "OOP"],
        "langs": [("Java", 96, "#10B981"), ("Inno Setup", 2, "#A78BFA"), ("Batch", 2, "#F59E0B")],
        "stars": 2,
        "updated": "updated 3w ago",
        "icon_color": "#10B981",
        "icon": '<circle cx="12" cy="12" r="9" fill="none" stroke="#10B981" stroke-width="2.3"/><path d="M12 7v5l3 3" fill="none" stroke="#10B981" stroke-width="2.3" stroke-linecap="round"/>'
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
            f'{html.escape(name)} {pct}%</text>'
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
        (30, 728),
        (605, 728),
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
                f'fill="#22D3EE" text-anchor="middle">{html.escape(t)}</text>'
            )
            tx += tw + 8

        # --- Donut chart ---
        donut = build_donut(p["langs"], x + 480, y + 82, radius=32, stroke_w=7)

        # --- Language legend ---
        legend = build_lang_legend(p["langs"], x + 355, y + 62)

        cards_xml.append(f'''
    <!-- CARD {idx+1}: {html.escape(p["title"])} -->
    <g opacity="0">
      <!-- Card background -->
      <rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="14"
            fill="#0D1424" stroke="rgba(34,211,238,0.22)" stroke-width="1">
        <animate attributeName="stroke-opacity" values="0.18;0.40;0.18" dur="4s" repeatCount="indefinite"/>
      </rect>

      <!-- Repo path header -->
      <circle cx="{x + 14}" cy="{y + 18}" r="2.5" fill="#22D3EE" opacity="0.6"/>
      <text x="{x + 24}" y="{y + 22}" font-size="11" fill="#475569">{html.escape(p["repo"])}</text>

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
        {html.escape(p["title"])}</text>

      <!-- Description -->
      <text x="{x + 78}" y="{y + 82}" font-size="11" fill="#94A3B8">
        {html.escape(p["desc"])}</text>

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
        {html.escape(p["updated"])}</text>

      <!-- Entrance animation -->
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay:.2f}s" fill="freeze"/>
    </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="960" viewBox="0 0 1180 960"
     font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
     role="img" aria-label="Projects List">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#080D1A"/>
      <stop offset="1" stop-color="#0B1120"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1180" height="960" rx="16" fill="url(#bgGrad)"/>

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
