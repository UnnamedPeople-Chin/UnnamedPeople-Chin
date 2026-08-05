import os
import math
import random
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from scipy.optimize import linear_sum_assignment

IMAGE_PATH = r"C:\Users\HYPE AMD\.gemini\antigravity\brain\89b33594-076e-4d18-b417-66a597e698d0\media__1785948563280.jpg"
OUTPUT_DARK = r"d:\Git setup\dark.svg"
OUTPUT_LIGHT = r"d:\Git setup\light.svg"

GRID_W = 300
GRID_H = 340

PORTRAIT_X = 35
PORTRAIT_Y = 95
PORTRAIT_BOX_W = 380
PORTRAIT_BOX_H = 480

SCALE_X = PORTRAIT_BOX_W / GRID_W
SCALE_Y = PORTRAIT_BOX_H / GRID_H

def process_image(image_path):
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    
    crop_w = w
    crop_h = int(w * (GRID_H / GRID_W))
    if crop_h > h:
        crop_h = h
        crop_w = int(h * (GRID_W / GRID_H))
    
    left = (w - crop_w) // 2
    top = int(h * 0.04)
    right = left + crop_w
    bottom = top + crop_h

    img_cropped = img.crop((left, top, right, bottom))
    img_resized = img_cropped.resize((GRID_W, GRID_H), Image.Resampling.LANCZOS)
    
    enhancer = ImageEnhance.Contrast(img_resized)
    img_enhanced = enhancer.enhance(1.4)
    img_sharpened = img_enhanced.filter(ImageFilter.UnsharpMask(radius=3, percent=150))
    
    gray = np.array(img_sharpened.convert("L"), dtype=np.float32)
    rgb = np.array(img_sharpened, dtype=np.float32)
    
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    bg_mask = (r > g + 20) & (r > b + 20) & (g < 90)
    
    dither_dark = gray.copy()
    dither_light = gray.copy()
    
    dots_dark = []
    dots_light = []
    
    for y in range(GRID_H):
        x_range = range(GRID_W) if y % 2 == 0 else range(GRID_W - 1, -1, -1)
        for x in x_range:
            old_val = dither_dark[y, x]
            if bg_mask[y, x]:
                new_val = 0
            else:
                new_val = 255 if old_val > 110 else 0
            
            dither_dark[y, x] = new_val
            err = old_val - new_val
            
            if new_val == 255:
                dots_dark.append((x, y))
                
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

    for y in range(GRID_H):
        x_range = range(GRID_W) if y % 2 == 0 else range(GRID_W - 1, -1, -1)
        for x in x_range:
            old_val = dither_light[y, x]
            new_val = 255 if old_val > 130 else 0
            dither_light[y, x] = new_val
            err = old_val - new_val
            
            if new_val == 0:
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

    if len(dots_light) > 22000:
        step = len(dots_light) / 22000.0
        dots_light = [dots_light[int(i * step)] for i in range(22000)]

    return dots_dark, dots_light

def generate_logo_shapes(num_points=800):
    cx, cy = GRID_W / 2, GRID_H / 2
    r_base = min(GRID_W, GRID_H) * 0.32
    
    # 1. Python Logo Points
    pts_python = []
    for i in range(num_points // 2 - 30):
        t = i / (num_points // 2 - 30) * math.pi * 1.4
        r = r_base * (0.75 + 0.2 * math.cos(2*t))
        x = cx + r * math.cos(t - 0.5) - 12
        y = cy + r * math.sin(t - 0.5) - 15
        pts_python.append((x, y))
    for _ in range(30):
        pts_python.append((cx - 20, cy - 45))
        
    for i in range(num_points // 2 - 30):
        t = i / (num_points // 2 - 30) * math.pi * 1.4 + math.pi
        r = r_base * (0.75 + 0.2 * math.cos(2*t))
        x = cx + r * math.cos(t - 0.5) + 12
        y = cy + r * math.sin(t - 0.5) + 15
        pts_python.append((x, y))
    for _ in range(30):
        pts_python.append((cx + 20, cy + 45))

    # 2. React Logo Points
    pts_react = []
    num_nuc = 120
    for i in range(num_nuc):
        a = i / num_nuc * math.pi * 2
        r = 22 * (random.random()**0.5)
        pts_react.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        
    pts_per_ellipse = (num_points - num_nuc) // 3
    for deg in [0, 60, 120]:
        rad = math.radians(deg)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        rx, ry = r_base * 1.25, r_base * 0.45
        for i in range(pts_per_ellipse):
            t = i / pts_per_ellipse * math.pi * 2
            ex = rx * math.cos(t)
            ey = ry * math.sin(t)
            x = cx + ex * cos_a - ey * sin_a
            y = cy + ex * sin_a + ey * cos_a
            pts_react.append((x, y))
            
    while len(pts_react) < num_points:
        pts_react.append((cx, cy))

    # 3. MongoDB Logo Points
    pts_mongo = []
    num_spine = 150
    for i in range(num_spine):
        y = cy - r_base * 1.1 + (i / num_spine) * (r_base * 2.2)
        pts_mongo.append((cx, y))
        
    num_leaf = num_points - num_spine
    for i in range(num_leaf):
        t = i / num_leaf * math.pi * 2
        x = cx + (r_base * 0.85) * math.sin(t) * (math.sin(t / 2)**1.5 if t < math.pi else math.sin((2*math.pi - t) / 2)**1.5) * (1 if t < math.pi else -1)
        y = cy - (r_base * 1.1) * math.cos(t)
        pts_mongo.append((x, y))

    return pts_python, pts_react, pts_mongo

def match_points(pts1, pts2):
    P1 = np.array(pts1)
    P2 = np.array(pts2)
    dist = np.linalg.norm(P1[:, None, :] - P2[None, :, :], axis=-1)
    row_ind, col_ind = linear_sum_assignment(dist)
    return [pts2[j] for j in col_ind]

def clamp(val, min_v, max_v):
    return max(min_v, min(val, max_v))

def build_svg(dots_portrait, mode="dark"):
    is_dark = (mode == "dark")
    bg_color = "#0A101F" if is_dark else "#F8FAFC"
    border_color = "#22D3EE" if is_dark else "#0891B2"
    dot_color = "#A78BFA" if is_dark else "#7C3AED"
    text_color = "#F8FAFC" if is_dark else "#0F172A"
    sub_text_color = "#94A3B8" if is_dark else "#475569"
    accent_color = "#10B981" if is_dark else "#059669"
    panel_bg = "#070D18" if is_dark else "#FFFFFF"
    header_bg = "#0F172A" if is_dark else "#E2E8F0"
    
    # 1. LOGO SWARM POINTS & MATCHING
    num_travellers = 800
    pts_py, pts_react_raw, pts_mongo_raw = generate_logo_shapes(num_points=num_travellers)
    pts_react = match_points(pts_py, pts_react_raw)
    pts_mongo = match_points(pts_react, pts_mongo_raw)
    pts_py_return = match_points(pts_mongo, pts_py)

    # 2. PORTRAIT DISSOLVE DRIFT BANDS (~90 BANDS)
    num_bands = 90
    bands = [[] for _ in range(num_bands)]
    
    random.seed(42)
    for x, y in dots_portrait:
        noisy_y = y + random.gauss(0, 3.5)
        band_idx = int(clamp(noisy_y / GRID_H * num_bands, 0, num_bands - 1))
        sx = PORTRAIT_X + x * SCALE_X
        sy = PORTRAIT_Y + y * SCALE_Y
        bands[band_idx].append(f"M{sx:.1f},{sy:.1f}h1.3")

    portrait_band_groups = []
    cx_box, cy_box = PORTRAIT_X + PORTRAIT_BOX_W / 2, PORTRAIT_Y + PORTRAIT_BOX_H / 2
    
    for b_i, d_list in enumerate(bands):
        if not d_list: continue
        path_data = " ".join(d_list)
        
        band_y_center = PORTRAIT_Y + (b_i / num_bands) * PORTRAIT_BOX_H
        drift_dx = (cx_box - (PORTRAIT_X + PORTRAIT_BOX_W / 2)) * 0.45 + (random.random() - 0.5) * 30
        drift_dy = (cy_box - band_y_center) * 0.42 + (random.random() - 0.5) * 20
        
        # Interleaved intro delay for face (0.1s to 1.8s)
        intro_delay = 0.1 + (b_i % 30) / 30.0 * 1.5
        
        band_xml = f'''    <g opacity="0">
      <path d="{path_data}" stroke="{dot_color}" stroke-width="1.3" fill="none">
        <animate attributeName="transform" type="translate" 
                 values="0,0; 0,0; {drift_dx:.1f},{drift_dy:.1f}; {drift_dx:.1f},{drift_dy:.1f}; 0,0; 0,0" 
                 keyTimes="0; 0.176; 0.268; 0.810; 0.901; 1" 
                 dur="14.2s" repeatCount="indefinite" />
        <animate attributeName="opacity" 
                 values="1; 1; 0; 0; 1; 1" 
                 keyTimes="0; 0.176; 0.268; 0.810; 0.901; 1" 
                 dur="14.2s" repeatCount="indefinite" />
      </path>
      <animate attributeName="opacity" values="0;1" keyTimes="0;1" dur="1.5s" begin="{intro_delay:.2f}s" fill="freeze" />
    </g>'''
        portrait_band_groups.append(band_xml)

    # 3. TRAVELLERS SWARM
    traveller_elements = []
    pos_keytimes = "0; 0.176; 0.352; 0.444; 0.585; 0.676; 0.817; 0.908; 1"
    opacity_values = "0; 0; 1; 1; 1; 1; 1; 0; 0"
    
    for i in range(num_travellers):
        p1 = pts_py[i]
        p2 = pts_react[i]
        p3 = pts_mongo[i]
        p4 = pts_py_return[i]
        
        sx1, sy1 = PORTRAIT_X + p1[0] * SCALE_X, PORTRAIT_Y + p1[1] * SCALE_Y
        sx2, sy2 = PORTRAIT_X + p2[0] * SCALE_X, PORTRAIT_Y + p2[1] * SCALE_Y
        sx3, sy3 = PORTRAIT_X + p3[0] * SCALE_X, PORTRAIT_Y + p3[1] * SCALE_Y
        sx4, sy4 = PORTRAIT_X + p4[0] * SCALE_X, PORTRAIT_Y + p4[1] * SCALE_Y

        dot_xml = f'''    <rect width="2" height="2" fill="{border_color}" opacity="0">
      <animate attributeName="x" values="{sx1:.1f}; {sx1:.1f}; {sx1:.1f}; {sx2:.1f}; {sx2:.1f}; {sx3:.1f}; {sx3:.1f}; {sx4:.1f}; {sx4:.1f}" keyTimes="{pos_keytimes}" dur="14.2s" repeatCount="indefinite"/>
      <animate attributeName="y" values="{sy1:.1f}; {sy1:.1f}; {sy1:.1f}; {sy2:.1f}; {sy2:.1f}; {sy3:.1f}; {sy3:.1f}; {sy4:.1f}; {sy4:.1f}" keyTimes="{pos_keytimes}" dur="14.2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="{opacity_values}" keyTimes="{pos_keytimes}" dur="14.2s" repeatCount="indefinite"/>
    </rect>'''
        traveller_elements.append(dot_xml)

    # 4. SYSTEM INFO READOUT ROWS WITH STAGGERED INTRO FADE-IN
    info_data = [
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

    info_rows_xml = []
    y_base = 135
    row_height = 28
    
    for idx, (label, val) in enumerate(info_data):
        y_pos = y_base + idx * row_height
        dots_count = max(4, 45 - len(label) - len(val))
        dotted_str = ". " * dots_count
        
        # Staggered intro delay per line (0.4s to 2.2s)
        row_intro_delay = 0.4 + idx * 0.12
        
        info_rows_xml.append(f'''    <g opacity="0">
      <text x="460" y="{y_pos}" fill="{sub_text_color}" font-family="ui-monospace, Consolas, monospace" font-size="13">{label}</text>
      <text x="610" y="{y_pos}" fill="{sub_text_color}" font-family="ui-monospace, Consolas, monospace" font-size="13" opacity="0.35">{dotted_str}</text>
      <text x="1135" y="{y_pos}" fill="{text_color}" font-family="ui-monospace, Consolas, monospace" font-size="13" font-weight="bold" text-anchor="end">{val}</text>
      <animate attributeName="opacity" values="0;1" keyTimes="0;1" dur="0.6s" begin="{row_intro_delay:.2f}s" fill="freeze" />
    </g>''')

    # SVG COMPOSITION WITH FULL INTRO ANIMATIONS FOR ALL TEXT & CHROME
    svg_code = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 610" width="1180" height="610">
  <style>
    .terminal-bg {{ fill: {bg_color}; }}
    .panel-border {{ stroke: {border_color}; stroke-width: 1.5; fill: {panel_bg}; }}
    .header-bg {{ fill: {header_bg}; }}
    .title-text {{ fill: {text_color}; font-family: ui-monospace, Consolas, monospace; font-size: 14px; font-weight: bold; }}
    .pulse-live {{ animation: pulse 1.5s infinite alternate; }}
    @keyframes pulse {{ from {{ opacity: 0.3; }} to {{ opacity: 1; }} }}
  </style>

  <!-- Outer Window Frame -->
  <rect width="1180" height="610" rx="10" class="terminal-bg" />
  <rect x="2" y="2" width="1176" height="606" rx="9" fill="none" stroke="{border_color}" stroke-width="1.5" opacity="0.8" />
  
  <!-- Header Bar -->
  <path d="M 2 12 Q 2 2 12 2 L 1168 2 Q 1178 2 1178 12 L 1178 40 L 2 40 Z" class="header-bg" />
  <line x1="2" y1="40" x2="1178" y2="40" stroke="{border_color}" stroke-width="1.5" />
  
  <!-- Window Controls with Pop-in Intro -->
  <g opacity="0">
    <circle cx="25" cy="21" r="6" fill="#FF5F56" />
    <circle cx="45" cy="21" r="6" fill="#FFBD2E" />
    <circle cx="65" cy="21" r="6" fill="#27C93F" />
    <animate attributeName="opacity" values="0;1" dur="0.4s" begin="0.1s" fill="freeze" />
  </g>
  
  <!-- Header Title with Fade-in Intro -->
  <g opacity="0">
    <text x="590" y="26" class="title-text" text-anchor="middle">profile.sh --live</text>
    <animate attributeName="opacity" values="0;1" dur="0.5s" begin="0.2s" fill="freeze" />
  </g>

  <!-- LEFT PORTRAIT FRAME (VISUAL.MAP) -->
  <rect x="25" y="55" width="400" height="530" rx="6" class="panel-border" />
  <rect x="25" y="55" width="400" height="30" rx="6" class="header-bg" />
  <line x1="25" y1="85" x2="425" y2="85" stroke="{border_color}" stroke-width="1" />
  
  <!-- VISUAL.MAP Header Text with Intro Animation -->
  <g opacity="0">
    <text x="40" y="75" fill="{border_color}" font-family="ui-monospace, Consolas, monospace" font-size="12" font-weight="bold">VISUAL.MAP</text>
    <animate attributeName="opacity" values="0;1" dur="0.5s" begin="0.25s" fill="freeze" />
  </g>

  <!-- LIVE Badge & Handle with Intro Animation -->
  <g opacity="0">
    <rect x="270" y="62" width="50" height="16" rx="8" fill="#EF4444" opacity="0.2" />
    <circle cx="280" cy="70" r="4" fill="#EF4444" class="pulse-live" />
    <text x="290" y="73" fill="#EF4444" font-family="ui-monospace, Consolas, monospace" font-size="10" font-weight="bold">LIVE</text>
    <rect x="328" y="62" width="90" height="16" rx="8" fill="{border_color}" opacity="0.2" />
    <text x="373" y="73" fill="{border_color}" font-family="ui-monospace, Consolas, monospace" font-size="9" font-weight="bold" text-anchor="middle">@UnnamedPeople-Chin</text>
    <animate attributeName="opacity" values="0;1" dur="0.5s" begin="0.3s" fill="freeze" />
  </g>

  <!-- PORTRAIT DITHER DRIFT BANDS (FADE-IN INTRO & LOOP DISSOLVE) -->
  <g shape-rendering="crispEdges">
{"".join(portrait_band_groups)}
  </g>

  <!-- TRAVELLERS SWARM (LOGO MORPHING: PYTHON -> REACT -> MONGODB) -->
  <g>
{"".join(traveller_elements)}
  </g>

  <!-- RIGHT INFO PANEL (SYSTEM.INFO) -->
  <rect x="440" y="55" width="715" height="530" rx="6" class="panel-border" />
  <rect x="440" y="55" width="715" height="30" rx="6" class="header-bg" />
  <line x1="440" y1="85" x2="1155" y2="85" stroke="{border_color}" stroke-width="1" />
  
  <!-- SYSTEM.INFO Header Text & Status Badge with Intro Animation -->
  <g opacity="0">
    <text x="455" y="75" fill="{border_color}" font-family="ui-monospace, Consolas, monospace" font-size="12" font-weight="bold">SYSTEM.INFO</text>
    <text x="1140" y="75" fill="{accent_color}" font-family="ui-monospace, Consolas, monospace" font-size="11" font-weight="bold" text-anchor="end">STATUS: ONLINE</text>
    <animate attributeName="opacity" values="0;1" dur="0.5s" begin="0.35s" fill="freeze" />
  </g>

  <!-- Staggered Intro Fade-in Readout Rows -->
  <g>
{"".join(info_rows_xml)}
  </g>
</svg>'''
    return svg_code

def main():
    print("Processing portrait image...")
    dots_dark, dots_light = process_image(IMAGE_PATH)
    print(f"Extracted {len(dots_dark)} dots for dark mode, {len(dots_light)} dots for light mode.")
    
    print("Building updated dark.svg with full text intro animations...")
    svg_dark = build_svg(dots_dark, mode="dark")
    with open(OUTPUT_DARK, "w", encoding="utf-8") as f:
        f.write(svg_dark)
    print(f"Saved {OUTPUT_DARK}")

    print("Building updated light.svg with full text intro animations...")
    svg_light = build_svg(dots_light, mode="light")
    with open(OUTPUT_LIGHT, "w", encoding="utf-8") as f:
        f.write(svg_light)
    print(f"Saved {OUTPUT_LIGHT}")

if __name__ == "__main__":
    main()
