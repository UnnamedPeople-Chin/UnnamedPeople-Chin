import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DARK_COLOR_MAP = {
    "#0d1117": "#0A101F",
    "#8b949e": "#94A3B8",
    "#161b22": "#131C31",
    "#0e4429": "#1E3A8A",
    "#006d32": "#7C3AED",
    "#26a641": "#22D3EE",
    "#39d353": "#10B981",
}

LIGHT_COLOR_MAP = {
    "#ffffff": "#F8FAFC",
    "#57606a": "#475569",
    "#ebedf0": "#E2E8F0",
    "#9be9a8": "#93C5FD",
    "#40c463": "#A78BFA",
    "#30a14e": "#06B6D4",
    "#216e39": "#059669",
}

# 2.4x slowdown converts default 100ms/frame (10 steps/sec) to 240ms/frame (~4.2 steps/sec normal arcade speed)
TEMPO_MULTIPLIER = 2.4


def scale_duration(match):
    ms = int(match.group(1))
    if ms == 500:
        # Bomb fuse pulse duration
        return 'dur="800ms"'
    if ms == 800:
        return match.group(0)
    return f'dur="{int(round(ms * TEMPO_MULTIPLIER))}ms"'


def recolor_svg(path, is_dark):
    """Apply README multi-color palette, normal arcade tempo, and padded 1180px terminal frame."""
    color_map = DARK_COLOR_MAP if is_dark else LIGHT_COLOR_MAP
    bg_color = "#0A101F" if is_dark else "#F8FAFC"
    border_color = "rgba(34,211,238,0.22)" if is_dark else "rgba(8,145,178,0.28)"
    pattern = re.compile("|".join(re.escape(k) for k in color_map), re.IGNORECASE)

    with open(path, "r", encoding="utf-8") as f:
        svg = f.read()

    # 1. Remap contribution colors
    svg = pattern.sub(lambda m: color_map[m.group(0).lower()], svg)

    # 2. Slow down animation tempo (only once if not already framed)
    if 'viewBox="-18 -18 1200 203"' not in svg:
        svg = re.sub(r'dur="(\d+)ms"', scale_duration, svg)

    # 3. Expand SVG canvas with 18px breathing room and terminal border
    svg = re.sub(
        r'<svg\s+width="1166"\s+height="169"',
        '<svg width="1180" height="205" viewBox="-18 -18 1200 203"',
        svg,
        count=1,
    )
    svg = re.sub(
        r'<rect\s+width="100%"\s+height="100%"(?:\s+rx="\d+")?\s+fill="[^"]+"\s*/>',
        f'<rect x="-17" y="-17" width="1198" height="201" rx="16" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5"/>',
        svg,
        count=1,
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Recolored & slowed {'dark' if is_dark else 'light'}: {path}")


def main():
    dist_dir = os.path.join(BASE_DIR, "dist")
    targets = sorted(glob.glob(os.path.join(dist_dir, "*.svg")))
    if not targets:
        print(f"No SVG files found in {dist_dir}")
        return
    for svg_path in targets:
        is_dark = svg_path.endswith("-dark.svg")
        recolor_svg(svg_path, is_dark=is_dark)


if __name__ == "__main__":
    main()
