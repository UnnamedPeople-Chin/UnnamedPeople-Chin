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


def recolor_svg(path, is_dark):
    """Apply full README multi-color palette and rounded outer corners to an arcade SVG."""
    color_map = DARK_COLOR_MAP if is_dark else LIGHT_COLOR_MAP
    pattern = re.compile("|".join(re.escape(k) for k in color_map), re.IGNORECASE)

    with open(path, "r", encoding="utf-8") as f:
        svg = f.read()

    svg = pattern.sub(lambda m: color_map[m.group(0).lower()], svg)
    svg = re.sub(
        r'<rect\s+width="100%"\s+height="100%"(\s+fill="[^"]+")\s*/>',
        r'<rect width="100%" height="100%" rx="16"\1/>',
        svg,
        count=1,
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Recolored {'dark' if is_dark else 'light'}: {path}")


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
