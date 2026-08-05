import os
import math
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
try:
    from scipy.optimize import linear_sum_assignment
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

IMAGE_PATH = r"C:\Users\HYPE AMD\.gemini\antigravity\brain\89b33594-076e-4d18-b417-66a597e698d0\media__1785948563280.jpg"
OUTPUT_DARK = r"d:\Git setup\dark.svg"
OUTPUT_LIGHT = r"d:\Git setup\light.svg"

# Grid size for portrait dither
GRID_W = 300
GRID_H = 340

# Offset in SVG for portrait box
PORTRAIT_X = 35
PORTRAIT_Y = 65
SCALE_X = 380 / GRID_W  # Fit 300 grid into 380px width
SCALE_Y = 480 / GRID_H  # Fit 340 grid into 480px height

def process_image(image_path):
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    
    # Head & Shoulders crop (focus on upper 60% of the image)
    # The image is tall (vertical phone photo)
    crop_w = w
    crop_h = int(w * (GRID_H / GRID_W))
    if crop_h > h:
        crop_h = h
        crop_w = int(h * (GRID_W / GRID_H))
    
    left = (w - crop_w) // 2
    top = int(h * 0.05)  # Slightly from top to capture head and shoulders
    right = left + crop_w
    bottom = top + crop_h
    if bottom > h:
        bottom = h
        top = bottom - crop_h

    img_cropped = img.crop((left, top, right, bottom))
    img_resized = img_cropped.resize((GRID_W, GRID_H), Image.Resampling.LANCZOS)
    
    # Enhance contrast and sharpen
    enhancer = ImageEnhance.Contrast(img_resized)
    img_enhanced = enhancer.enhance(1.35)
    img_sharpened = img_enhanced.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    
    # Convert to grayscale numpy array
    gray = np.array(img_sharpened.convert("L"), dtype=np.float32)
    rgb = np.array(img_sharpened, dtype=np.float32)
    
    # Background Segmentation for Dark Mode:
    # Photo background is dark red / burgundy (high Red, low Green/Blue)
    # Let's segment out backdrop where Red > Green+30 and Red > Blue+30 or overall dark background
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    bg_mask = (r > g + 25) & (r > b + 25) & (g < 80)
    
    # Floyd-Steinberg Dithering (Serpentine order)
    dither_dark = gray.copy()
    dither_light = gray.copy()
    
    dots_dark = []
    dots_light = []
    
    # Dither for Dark Mode (dots represent lit subject)
    for y in range(GRID_H):
        x_range = range(GRID_W) if y % 2 == 0 else range(GRID_W - 1, -1, -1)
        for x in x_range:
            old_val = dither_dark[y, x]
            # In dark mode, if background -> set to black (no dot)
            if bg_mask[y, x]:
                new_val = 0
            else:
                new_val = 255 if old_val > 115 else 0
            
            dither_dark[y, x] = new_val
            err = old_val - new_val
            
            if new_val == 255:  # Lit pixel -> draw dot in dark mode
                dots_dark.append((x, y))
                
            # Distribute error
            if y % 2 == 0:
                if x + 1 < GRID_W: dither_dark[y, x + 1] += err * 7 / 16
                if y + 1 < GRID_H:
                    if x - 1 >= 0: dither_dark[y + 1, x - 1] += err * 3 / 16
                    dither_dark[y + 1, x] += err * 5 / 16
                    if x + 1 < GRID_W: dither_dark[y + 1, x + 1] += err * 1 / 16
            else:
                if x - 1 >= 0: dither_dark[y, x - 1] += err * 7 / 16
                if y + 1 < GRID_H:
                    if x + 1 < GRID_W: dither_dark[y + 1, x + 1] += err * 3 / 16
                    dither_dark[y + 1, x] += err * 5 / 16
                    if x - 1 >= 0: dither_dark[y + 1, x - 1] += err * 1 / 16

    # Dither for Light Mode (dots represent dark parts of photo)
    for y in range(GRID_H):
        x_range = range(GRID_W) if y % 2 == 0 else range(GRID_W - 1, -1, -1)
        for x in x_range:
            old_val = dither_light[y, x]
            new_val = 255 if old_val > 128 else 0
            dither_light[y, x] = new_val
            err = old_val - new_val
            
            if new_val == 0:  # Dark pixel -> draw dot in light mode
                dots_light.append((x, y))
                
            if y % 2 == 0:
                if x + 1 < GRID_W: dither_light[y, x + 1] += err * 7 / 16
                if y + 1 < GRID_H:
                    if x - 1 >= 0: dither_light[y + 1, x - 1] += err * 3 / 16
                    dither_light[y + 1, x] += err * 5 / 16
                    if x + 1 < GRID_W: dither_light[y + 1, x + 1] += err * 1 / 16
            else:
                if x - 1 >= 0: dither_light[y, x - 1] += err * 7 / 16
                if y + 1 < GRID_H:
                    if x + 1 < GRID_W: dither_light[y + 1, x + 1] += err * 3 / 16
                    dither_light[y + 1, x] += err * 5 / 16
                    if x - 1 >= 0: dither_light[y + 1, x - 1] += err * 1 / 16

    if len(dots_light) > 24000:
        step = len(dots_light) / 22000.0
        dots_light = [dots_light[int(i * step)] for i in range(22000)]

    return dots_dark, dots_light

def generate_logo_points(num_points=800):
    # Center of portrait frame
    cx, cy = GRID_W / 2, GRID_H / 2
    r_outer = min(GRID_W, GRID_H) * 0.35
    
    # 1. Python Logo Points (Two interlocking snakes/arcs)
    pts_python = []
    for i in range(num_points // 2):
        t = i / (num_points // 2) * math.pi * 1.5
        # Top snake
        r = r_outer * (0.6 + 0.3 * math.sin(t*2))
        x = cx + r * math.cos(t) - 15
        y = cy + r * math.sin(t) - 15
        pts_python.append((x, y))
    for i in range(num_points // 2):
        t = i / (num_points // 2) * math.pi * 1.5 + math.pi
        # Bottom snake
        r = r_outer * (0.6 + 0.3 * math.sin(t*2))
        x = cx + r * math.cos(t) + 15
        y = cy + r * math.sin(t) + 15
        pts_python.append((x, y))
        
    # 2. React Logo Points (Center nucleus + 3 ellipse orbits at 0, 60, 120 deg)
    pts_react = []
    # Nucleus
    for i in range(100):
        a = i / 100 * math.pi * 2
        r = 18 * (i / 100)**0.5
        pts_react.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    
    # 3 Ellipses
    pts_per_orbit = (num_points - 100) // 3
    for angle_deg in [0, 60, 120]:
        rad = math.radians(angle_deg)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        rx, ry = r_outer * 1.1, r_outer * 0.45
        for i in range(pts_per_orbit):
            t = i / pts_per_orbit * math.pi * 2
            ex = rx * math.cos(t)
            ey = ry * math.sin(t)
            # Rotate
            x = cx + ex * cos_a - ey * sin_a
            y = cy + ex * sin_a + ey * cos_a
            pts_react.append((x, y))
            
    # 3. MongoDB Logo Points (Leaf / Flame shape)
    pts_mongo = []
    for i in range(num_points):
        t = i / num_points * math.pi * 2
        # Leaf parametric equation
        r = r_outer * (1 + 0.4 * math.cos(t) - 0.5 * math.sin(2*t))
        x = cx + r * math.sin(t) * 0.75
        y = cy - r * math.cos(t) * 1.0 + 10
        pts_mongo.append((x, y))
        
    return pts_python, pts_react, pts_mongo

def match_points(pts1, pts2):
    P1 = np.array(pts1)
    P2 = np.array(pts2)
    if HAS_SCIPY:
        dist = np.linalg.norm(P1[:, None, :] - P2[None, :, :], axis=-1)
        row_ind, col_ind = linear_sum_assignment(dist)
        return [pts2[j] for j in col_ind]
    else:
        return pts2

def build_svg(dots_portrait, mode="dark"):
    is_dark = (mode == "dark")
    bg_color = "#0A101F" if is_dark else "#F8FAFC"
    border_color = "#22D3EE" if is_dark else "#0891B2"
    dot_color = "#A78BFA" if is_dark else "#7C3AED"
    text_color = "#E2E8F0" if is_dark else "#0F172A"
    sub_text_color = "#94A3B8" if is_dark else "#475569"
    accent_color = "#10B981" if is_dark else "#059669"
    panel_bg = "#070D18" if is_dark else "#FFFFFF"
    header_bg = "#0F172A" if is_dark else "#E2E8F0"
    
    pts_py, pts_react, pts_mongo = generate_logo_points(num_points=850)
    pts_react_matched = match_points(pts_py, pts_react)
    pts_mongo_matched = match_points(pts_react_matched, pts_mongo)
    
    # Sample portrait dots into ~60 interleaved intro groups
    num_dots = len(dots_portrait)
    groups = 60
    dots_by_group = [[] for _ in range(groups)]
    for idx, (gx, gy) in enumerate(dots_portrait):
        # Convert to SVG coordinates inside portrait box
        sx = PORTRAIT_X + gx * SCALE_X
        sy = PORTRAIT_Y + gy * SCALE_Y
        g_idx = (idx * 37) % groups  # Interleaved random distribution
        dots_by_group[g_idx].append(f"{sx:.1f},{sy:.1f}")
        
    intro_paths = []
    for g_i, d_list in enumerate(dots_by_group):
        if not d_list: continue
        # Format path M x y h 1.2
        path_data = " ".join([f"M{pt}h1.3" for pt in d_list])
        delay = (g_i / groups) * 2.0
        intro_paths.append(
            f'<path d="{path_data}" stroke="{dot_color}" stroke-width="1.3" fill="none">'
            f'<animate attributeName="opacity" values="0;1" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/>'
            f'</path>'
        )

    # Travellers morphing dots SVG animation
    traveller_elements = []
    for i in range(len(pts_py)):
        p1 = pts_py[i]
        p2 = pts_react_matched[i]
        p3 = pts_mongo_matched[i]
        
        sx1, sy1 = PORTRAIT_X + p1[0] * SCALE_X, PORTRAIT_Y + p1[1] * SCALE_Y
        sx2, sy2 = PORTRAIT_X + p2[0] * SCALE_X, PORTRAIT_Y + p2[1] * SCALE_Y
        sx3, sy3 = PORTRAIT_X + p3[0] * SCALE_X, PORTRAIT_Y + p3[1] * SCALE_Y
        
        # Keyframe animation for position & opacity
        path_anim = (
            f'<rect width="2" height="2" fill="{border_color}" opacity="0">'
            f'<animate attributeName="x" values="{sx1};{sx1};{sx2};{sx2};{sx3};{sx3};{sx1}" keyTimes="0;0.2;0.4;0.6;0.8;0.9;1" dur="14s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{sy1};{sy1};{sy2};{sy2};{sy3};{sy3};{sy1}" keyTimes="0;0.2;0.4;0.6;0.8;0.9;1" dur="14s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.9;0.9;0.9;0.9;0.9;0" keyTimes="0;0.15;0.35;0.55;0.75;0.9;1" dur="14s" repeatCount="indefinite"/>'
            f'</rect>'
        )
        traveller_elements.append(path_anim)

    info_rows = [
        ("Subject", "Alexios Mercer"),
        ("GitHub", "UnnamedPeople-Chin"),
        ("Role", "Full-Stack | AI Eng | Frontend"),
        ("Origin", "Salatiga, Indonesia"),
        ("Education", "Politeknik Negeri Semarang"),
        ("Status", "Building + Learning + Shipping"),
        ("Core.Lang", "JavaScript, Python, C++"),
        ("Core.Frontend", "React, Next.js, Tailwind CSS"),
        ("Core.Backend", "Node.js, Express"),
        ("Core.Database", "MongoDB, PostgreSQL"),
        ("ToolChain", "VS Code, Git, Figma"),
        ("Contact.Mail", "jizdanyr354@gmail.com"),
        ("Social.Insta", "instagram.com/jizdan.yr"),
        ("Social.TikTok", "tiktok.com/@jizdan.yr"),
    ]

    info_svg_rows = []
    y_start = 120
    for idx, (label, val) in enumerate(info_rows):
        y_pos = y_start + idx * 27
        # Dotted leader
        dots_count = max(5, 52 - len(label) - len(val))
        dots_str = "." * dots_count
        info_svg_rows.append(
            f'<text x="460" y="{y_pos}" fill="{sub_text_color}" font-family="monospace" font-size="13">{label}</text>'
            f'<text x="560" y="{y_pos}" fill="{sub_text_color}" font-family="monospace" font-size="13" opacity="0.4">{dots_str}</text>'
            f'<text x="1110" y="{y_pos}" fill="{text_color}" font-family="monospace" font-size="13" text-anchor="end" textLength="{len(val)*8.2:.0f}" lengthAdjust="spacingAndGlyphs">{val}</text>'
        )

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 610" width="1180" height="610">
  <style>
    .terminal-bg {{ fill: {bg_color}; }}
    .panel-border {{ stroke: {border_color}; stroke-width: 1.5; fill: {panel_bg}; }}
    .header-bg {{ fill: {header_bg}; }}
    .title-text {{ fill: {text_color}; font-family: monospace; font-size: 14px; font-weight: bold; }}
    .pulse-live {{ animation: pulse 1.5s infinite alternate; }}
    @keyframes pulse {{ from {{ opacity: 0.3; }} to {{ opacity: 1; }} }}
  </style>

  <!-- Outer Window Frame -->
  <rect width="1180" height="610" rx="10" class="terminal-bg" />
  <rect x="2" y="2" width="1176" height="606" rx="9" fill="none" stroke="{border_color}" stroke-width="1.5" opacity="0.8" />
  
  <!-- Header Bar -->
  <path d="M 2 12 Q 2 2 12 2 L 1168 2 Q 1178 2 1178 12 L 1178 40 L 2 40 Z" class="header-bg" />
  <line x1="2" y1="40" x2="1178" y2="40" stroke="{border_color}" stroke-width="1.5" />
  
  <!-- Window Controls -->
  <circle cx="25" cy="21" r="6" fill="#FF5F56" />
  <circle cx="45" cy="21" r="6" fill="#FFBD2E" />
  <circle cx="65" cy="21" r="6" fill="#27C93F" />
  
  <!-- Header Title -->
  <text x="590" y="26" class="title-text" text-anchor="middle">profile.sh --live</text>

  <!-- LEFT PORTRAIT FRAME (VISUAL.MAP) -->
  <rect x="25" y="55" width="400" height="530" rx="6" class="panel-border" />
  <rect x="25" y="55" width="400" height="30" rx="6" class="header-bg" />
  <line x1="25" y1="85" x2="425" y2="85" stroke="{border_color}" stroke-width="1" />
  <text x="40" y="75" fill="{border_color}" font-family="monospace" font-size="12" font-weight="bold">VISUAL.MAP</text>

  <!-- LIVE Badge & Handle -->
  <rect x="290" y="64" width="50" height="16" rx="8" fill="#EF4444" opacity="0.2" />
  <circle cx="300" cy="72" r="4" fill="#EF4444" class="pulse-live" />
  <text x="310" y="76" fill="#EF4444" font-family="monospace" font-size="10" font-weight="bold">LIVE</text>
  <rect x="350" y="64" width="65" height="16" rx="8" fill="{border_color}" opacity="0.2" />
  <text x="382" y="76" fill="{border_color}" font-family="monospace" font-size="9" text-anchor="middle">@UnnamedPeople-Chin</text>

  <!-- Portrait Dither Dots -->
  <g shape-rendering="crispEdges">
    {"".join(intro_paths)}
  </g>

  <!-- Travellers Morphing Dots -->
  <g>
    {"".join(traveller_elements)}
  </g>

  <!-- RIGHT INFO PANEL (SYSTEM.INFO) -->
  <rect x="440" y="55" width="715" height="530" rx="6" class="panel-border" />
  <rect x="440" y="55" width="715" height="30" rx="6" class="header-bg" />
  <line x1="440" y1="85" x2="1155" y2="85" stroke="{border_color}" stroke-width="1" />
  <text x="455" y="75" fill="{border_color}" font-family="monospace" font-size="12" font-weight="bold">SYSTEM.INFO</text>
  <text x="1140" y="75" fill="{accent_color}" font-family="monospace" font-size="11" text-anchor="end">STATUS: ONLINE</text>

  <!-- System Info Readout Rows -->
  <g>
    {"".join(info_svg_rows)}
  </g>
</svg>'''
    return svg_content

def main():
    print("Processing portrait image...")
    dots_dark, dots_light = process_image(IMAGE_PATH)
    print(f"Extracted {len(dots_dark)} dots for dark mode, {len(dots_light)} dots for light mode.")
    
    print("Building dark.svg...")
    svg_dark = build_svg(dots_dark, mode="dark")
    with open(OUTPUT_DARK, "w", encoding="utf-8") as f:
        f.write(svg_dark)
    print(f"Saved {OUTPUT_DARK}")

    print("Building light.svg...")
    svg_light = build_svg(dots_light, mode="light")
    with open(OUTPUT_LIGHT, "w", encoding="utf-8") as f:
        f.write(svg_light)
    print(f"Saved {OUTPUT_LIGHT}")

if __name__ == "__main__":
    main()
