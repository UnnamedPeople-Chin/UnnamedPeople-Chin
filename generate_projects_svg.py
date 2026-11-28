import os
import math
import html
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DARK = os.path.join(BASE_DIR, "projects.svg")
OUTPUT_LIGHT = os.path.join(BASE_DIR, "projects-light.svg")

# User's REAL GitHub Projects — matching arifhaxn card style
projects = [
    {
        "repo": "UnnamedPeople-Chin/discode",
        "title": "DisCode RPC_",
        "desc": "Discord Rich Presence & 24+ AI agent presets",
        "tags": ["TypeScript", "VS Code", "RPC"],
        "langs": [("TypeScript", 83, "#3B82F6"), ("HTML", 17, "#EC4899")],
        "stars": 6,
        "updated": "updated today",
        "icon_color": "#A78BFA",
        "icon": '<rect x="2" y="4" width="20" height="16" rx="3" fill="none" stroke="#A78BFA" stroke-width="2.3"/><path d="M8 10l-2 2 2 2M16 10l2 2-2 2M13 9l-2 6" fill="none" stroke="#A78BFA" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/AetherCast",
        "title": "AetherCast_",
        "desc": "144 FPS hand-tracking & particle physics sandbox",
        "tags": ["JavaScript", "MediaPipe", "Electron"],
        "langs": [("JavaScript", 70, "#F59E0B"), ("Python", 16, "#3B82F6"), ("CSS", 14, "#22D3EE")],
        "stars": 5,
        "updated": "updated today",
        "icon_color": "#F59E0B",
        "icon": '<circle cx="12" cy="12" r="4" fill="none" stroke="#F59E0B" stroke-width="2.3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1" fill="none" stroke="#F59E0B" stroke-width="2.2" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/qris-track",
        "title": "QRIS-Track_",
        "desc": "ISO-18004 dynamic QRIS & zero-dep Node 22 ledger",
        "tags": ["Node 22", "SQLite", "QRIS"],
        "langs": [("JavaScript", 54, "#F59E0B"), ("HTML/CSS", 46, "#EC4899")],
        "stars": 2,
        "updated": "updated today",
        "icon_color": "#22D3EE",
        "icon": '<rect x="3" y="3" width="7" height="7" rx="1" fill="none" stroke="#22D3EE" stroke-width="2.2"/><rect x="14" y="3" width="7" height="7" rx="1" fill="none" stroke="#22D3EE" stroke-width="2.2"/><rect x="3" y="14" width="7" height="7" rx="1" fill="none" stroke="#22D3EE" stroke-width="2.2"/><path d="M14 14h3v3h-3zM18 18h3v3h-3zM14 20h2" fill="none" stroke="#22D3EE" stroke-width="2.2" stroke-linecap="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/SignFlow",
        "title": "SignFlow_",
        "desc": "Gamified sign language & MediaPipe hand coach",
        "tags": ["MediaPipe", "Canvas 2D", "EdTech"],
        "langs": [("JavaScript", 64, "#F59E0B"), ("CSS", 24, "#22D3EE"), ("HTML", 12, "#EC4899")],
        "stars": 1,
        "updated": "updated today",
        "icon_color": "#10B981",
        "icon": '<path d="M18 11V6a2 2 0 00-4 0v5M14 10V4a2 2 0 00-4 0v6M10 10.5V6a2 2 0 00-4 0v8l-1.5-1.5a2 2 0 00-2.8 2.8l4.3 4.7a6 6 0 004.5 2h2.5a6 6 0 006-6v-5a2 2 0 00-2-2z" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/qris-dinamis",
        "title": "qris-dinamis_",
        "desc": "Zero-dep npm CLI & SDK for dynamic QRIS",
        "tags": ["npm", "EMVCo", "CRC16"],
        "langs": [("JavaScript", 88, "#F59E0B"), ("TypeScript", 12, "#3B82F6")],
        "stars": 1,
        "updated": "updated today",
        "icon_color": "#EC4899",
        "icon": '<path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" fill="none" stroke="#EC4899" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/>'
    },
    {
        "repo": "UnnamedPeople-Chin/9router-go",
        "title": "9Router Go_",
        "desc": "Fork & Go/Svelte AI proxy gateway + RTK saver",
        "tags": ["Go", "Svelte", "LLM Proxy"],
        "langs": [("Go", 84, "#22D3EE"), ("Svelte", 10, "#F59E0B"), ("TypeScript", 6, "#3B82F6")],
        "stars": 8,
        "updated": "updated 1d ago",
        "icon_color": "#22D3EE",
        "icon": '<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" fill="none" stroke="#22D3EE" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/>'
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
        "icon_color": "#3B82F6",
        "icon": '<circle cx="12" cy="12" r="9" fill="none" stroke="#3B82F6" stroke-width="2.3"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round"/>'
    }
]


def format_relative_time(iso_ts):
    """Format an ISO-8601 UTC timestamp into a compact relative 'updated ...' label."""
    dt = datetime.strptime(iso_ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    days = max(0, (datetime.now(timezone.utc) - dt).days)
    if days == 0:
        return "updated today"
    if days < 7:
        return f"updated {days}d ago"
    if days < 30:
        return f"updated {days // 7}w ago"
    if days < 365:
        return f"updated {days // 30}mo ago"
    return f"updated {days // 365}y ago"


def sync_from_github_api(project_list):
    """Fetch live stars and pushed_at timestamps from GitHub REST API with graceful fallback."""
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    headers = {
        "User-Agent": "UnnamedPeople-Chin-Profile-Sync",
        "Accept": "application/vnd.github+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    for p in project_list:
        api_repo = p.get("api_repo", p["repo"])
        url = f"https://api.github.com/repos/{api_repo}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            api_stars = int(data.get("stargazers_count") or 0)
            p["stars"] = max(p["stars"], api_stars)
            if data.get("pushed_at"):
                p["updated"] = format_relative_time(data["pushed_at"])
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError, TimeoutError) as exc:
            print(f"[sync] skipped {api_repo}: {exc}")


def build_donut(langs, cx, cy, title_color, radius=32, stroke_w=7):
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
    primary_pct = langs[0][1]
    segments.append(
        f'<text x="{cx}" y="{cy + 5}" font-size="13" font-weight="bold" '
        f'fill="{title_color}" text-anchor="middle">{primary_pct}%</text>'
    )
    return "\n        ".join(segments)


def build_lang_legend(langs, x, y, body_color):
    """Build stacked language legend dots like arifhaxn."""
    items = []
    for i, (name, pct, color) in enumerate(langs):
        ly = y + i * 18
        items.append(
            f'<circle cx="{x}" cy="{ly}" r="3.5" fill="{color}"/>'
            f'<text x="{x + 10}" y="{ly + 4}" font-size="10" fill="{body_color}">'
            f'{html.escape(name)} {pct}%</text>'
        )
    return "\n        ".join(items)


def build_projects_svg(output_path, mode="dark"):
    """Render the 8-card PROJECTS.LIST SVG for dark or light mode."""
    if mode == "light":
        theme = {
            "bg_start": "#F8FAFC",
            "bg_end": "#F1F5F9",
            "card_fill": "#FFFFFF",
            "card_border": "rgba(8,145,178,0.28)",
            "header_color": "#0891B2",
            "muted_color": "#64748B",
            "line_stroke": "rgba(8,145,178,0.20)",
            "title_color": "#0F172A",
            "body_color": "#475569",
            "icon_bg": "#F1F5F9",
            "pill_bg": "rgba(8,145,178,0.10)",
            "pill_stroke": "rgba(8,145,178,0.35)",
            "pill_text": "#0891B2",
            "dot_accent": "#0891B2",
        }
    else:
        theme = {
            "bg_start": "#080D1A",
            "bg_end": "#0B1120",
            "card_fill": "#0D1424",
            "card_border": "rgba(34,211,238,0.22)",
            "header_color": "#22D3EE",
            "muted_color": "#475569",
            "line_stroke": "rgba(34,211,238,0.15)",
            "title_color": "#F8FAFC",
            "body_color": "#94A3B8",
            "icon_bg": "rgba(15,23,42,0.9)",
            "pill_bg": "rgba(34,211,238,0.08)",
            "pill_stroke": "rgba(34,211,238,0.35)",
            "pill_text": "#22D3EE",
            "dot_accent": "#22D3EE",
        }

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

        tag_pills = []
        tx = x + 18
        ty = y + 142
        for t in p["tags"]:
            tw = len(t) * 7.0 + 18
            tag_pills.append(
                f'<rect x="{tx}" y="{ty}" width="{tw:.0f}" height="24" rx="12" '
                f'fill="{theme["pill_bg"]}" stroke="{theme["pill_stroke"]}" stroke-width="1"/>'
                f'<text x="{tx + tw/2:.0f}" y="{ty + 16}" font-size="10" '
                f'fill="{theme["pill_text"]}" text-anchor="middle">{html.escape(t)}</text>'
            )
            tx += tw + 8

        donut = build_donut(p["langs"], x + 480, y + 82, theme["title_color"], radius=32, stroke_w=7)
        legend = build_lang_legend(p["langs"], x + 355, y + 62, theme["body_color"])

        cards_xml.append(f'''
    <!-- CARD {idx+1}: {html.escape(p["title"])} -->
    <g opacity="0">
      <!-- Card background -->
      <rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="14"
            fill="{theme["card_fill"]}" stroke="{theme["card_border"]}" stroke-width="1">
        <animate attributeName="stroke-opacity" values="0.18;0.40;0.18" dur="4s" repeatCount="indefinite"/>
      </rect>

      <!-- Repo path header -->
      <circle cx="{x + 14}" cy="{y + 18}" r="2.5" fill="{theme["dot_accent"]}" opacity="0.6"/>
      <text x="{x + 24}" y="{y + 22}" font-size="11" fill="{theme["muted_color"]}">{html.escape(p["repo"])}</text>

      <!-- Status dot (top-right) -->
      <circle cx="{x + card_w - 16}" cy="{y + 18}" r="3.5" fill="#10B981" opacity="0.7">
        <animate attributeName="opacity" values="0.4;0.9;0.4" dur="3s" repeatCount="indefinite"/>
      </circle>

      <!-- Icon box -->
      <rect x="{x + 14}" y="{y + 38}" width="52" height="52" rx="14"
            fill="{theme["icon_bg"]}" stroke="{p["icon_color"]}" stroke-width="1.2"/>
      <g transform="translate({x + 28},{y + 52}) scale(1.05)">
        {p["icon"]}
      </g>

      <!-- Title -->
      <text x="{x + 78}" y="{y + 60}" font-size="18" font-weight="bold" fill="{theme["title_color"]}">
        {html.escape(p["title"])}</text>

      <!-- Description -->
      <text x="{x + 78}" y="{y + 82}" font-size="11" fill="{theme["body_color"]}">
        {html.escape(p["desc"])}</text>

      <!-- Language legend (stacked dots) -->
      {legend}

      <!-- Donut chart (multi-segment) -->
      {donut}

      <!-- Tag pills -->
      {"".join(tag_pills)}

      <!-- Stars + updated -->
      <text x="{x + 18}" y="{y + 188}" font-size="11" fill="#F59E0B">★</text>
      <text x="{x + 32}" y="{y + 188}" font-size="11" font-weight="bold" fill="{theme["body_color"]}">
        {p["stars"]}</text>
      <text x="{x + 56}" y="{y + 188}" font-size="11" fill="{theme["muted_color"]}">
        {html.escape(p["updated"])}</text>

      <!-- Entrance animation -->
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay:.2f}s" fill="freeze"/>
    </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="960" viewBox="0 0 1180 960"
     font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
     role="img" aria-label="Projects List">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{theme["bg_start"]}"/>
      <stop offset="1" stop-color="{theme["bg_end"]}"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1180" height="960" rx="16" fill="url(#bgGrad)"/>

  <!-- Header -->
  <g opacity="0">
    <text x="32" y="34" font-size="12" font-weight="bold" letter-spacing="2.5" fill="{theme["header_color"]}">
      PROJECTS.LIST
      <tspan fill="{theme["muted_color"]}" letter-spacing="1"> ./projects.sh --all</tspan>
    </text>
    <line x1="32" y1="44" x2="1148" y2="44" stroke="{theme["line_stroke"]}"/>
    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.05s" fill="freeze"/>
  </g>

  <!-- Cards -->
{"".join(cards_xml)}
</svg>'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Saved {output_path}")


if __name__ == "__main__":
    sync_from_github_api(projects)
    build_projects_svg(OUTPUT_DARK, mode="dark")
    build_projects_svg(OUTPUT_LIGHT, mode="light")
