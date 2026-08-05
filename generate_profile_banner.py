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

def sample_bezier(p0, p1, p2, p3, n_samples=25):
    pts = []
    for t in np.linspace(0, 1, n_samples):
        x = (1-t)**3 * p0[0] + 3*(1-t)**2 * t * p1[0] + 3*(1-t) * t**2 * p2[0] + t**3 * p3[0]
        y = (1-t)**3 * p0[1] + 3*(1-t)**2 * t * p1[1] + 3*(1-t) * t**2 * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts

def sample_line(p0, p1, n_samples=25):
    pts = []
    for t in np.linspace(0, 1, n_samples):
        x = (1-t) * p0[0] + t * p1[0]
        y = (1-t) * p0[1] + t * p1[1]
        pts.append((x, y))
    return pts

def generate_hitman_points(num_points=800):
    """Samples exact points from ic_hitman.svg geometry."""
    # viewBox: 0 0 48 48
    raw_pts = []
    
    # Outer circle badge outline
    for a in np.linspace(0, 2*math.pi, 250):
        r = 19.5
        raw_pts.append((24 + r * math.cos(a), 24 + r * math.sin(a)))

    # Central Hitman tie / emblem geometry
    # Polygon / Lines from top down to bottom tip (24, 39)
    raw_pts.extend(sample_line((13.11, 7.24), (24, 39), 80))
    raw_pts.extend(sample_line((34.89, 7.24), (24, 39), 80))
    raw_pts.extend(sample_line((22, 10), (19.97, 27.25), 50))
    raw_pts.extend(sample_line((26, 10), (28.03, 27.25), 50))
    raw_pts.extend(sample_line((19.97, 27.25), (24, 39), 50))
    raw_pts.extend(sample_line((28.03, 27.25), (24, 39), 50))

    cx, cy = GRID_W / 2, GRID_H / 2
    scale = 5.8  # Scale 48px box to ~260px
    
    pts = []
    for x, y in raw_pts:
        nx = cx + (x - 24.0) * scale + (random.random() - 0.5) * 3
        ny = cy + (y - 24.0) * scale + (random.random() - 0.5) * 3
        pts.append((nx, ny))

    if len(pts) > num_points:
        step = len(pts) / float(num_points)
        pts = [pts[int(i * step)] for i in range(num_points)]
    while len(pts) < num_points:
        pts.append((cx, cy))
        
    return pts

def generate_nike_points(num_points=800):
    """Samples exact points from ic_nike.svg path geometry."""
    # viewBox 0 0 50 50
    # M 6.406 16.800 C 3.152 20.621, 0 25.234, 0 28.902 C 0 31.019, 1.781 33.996, 6.132 33.996
    # C 8.484 33.996, 10.820 33.050, 12.648 32.320 C 15.730 31.085, 49.789 16.296, 49.789 16.296
    # C 50.117 16.132, 50.058 15.925, 49.644 16.027 C 49.480 16.070, 12.566 26.074, 12.566 26.074
    # C 11.855 26.273, 11.128 26.382, 10.421 26.382 C 7.230 26.382, 5.078 24.851, 5.078 21.503
    # C 5.078 20.207, 5.484 18.640, 6.406 16.800 Z
    raw_pts = []
    
    raw_pts.extend(sample_bezier((6.406, 16.800), (3.152, 20.621), (0, 25.234), (0, 28.902), 60))
    raw_pts.extend(sample_bezier((0, 28.902), (0, 31.019), (1.781, 33.996), (6.132, 33.996), 60))
    raw_pts.extend(sample_bezier((6.132, 33.996), (8.484, 33.996), (10.820, 33.050), (12.648, 32.320), 60))
    raw_pts.extend(sample_bezier((12.648, 32.320), (15.730, 31.085), (49.789, 16.296), (49.789, 16.296), 120))
    raw_pts.extend(sample_bezier((49.789, 16.296), (50.117, 16.132), (50.058, 15.925), (49.644, 16.027), 40))
    raw_pts.extend(sample_bezier((49.644, 16.027), (49.480, 16.070), (12.566, 26.074), (12.566, 26.074), 120))
    raw_pts.extend(sample_bezier((12.566, 26.074), (11.855, 26.273), (11.128, 26.382), (10.421, 26.382), 60))
    raw_pts.extend(sample_bezier((10.421, 26.382), (7.230, 26.382), (5.078, 24.851), (5.078, 21.503), 60))
    raw_pts.extend(sample_bezier((5.078, 21.503), (5.078, 20.207), (5.484, 18.640), (6.406, 16.800), 60))

    cx, cy = GRID_W / 2, GRID_H / 2
    scale = 5.2  # Scale 50px box to ~260px
    
    pts = []
    for x, y in raw_pts:
        nx = cx + (x - 25.0) * scale + (random.random() - 0.5) * 3
        ny = cy + (y - 25.0) * scale + (random.random() - 0.5) * 3
        pts.append((nx, ny))

    if len(pts) > num_points:
        step = len(pts) / float(num_points)
        pts = [pts[int(i * step)] for i in range(num_points)]
    while len(pts) < num_points:
        pts.append((cx, cy))
        
    return pts

def generate_ac_points(num_points=800):
    """Samples exact points from ic_assassins_creed.svg path geometry."""
    # viewBox 0 0 32 32
    raw_pts = []
    
    raw_pts.extend(sample_line((16.04, 0), (9, 17), 30))
    raw_pts.extend(sample_bezier((9, 17), (7, 21), (3, 18), (3, 18), 25))
    raw_pts.extend(sample_bezier((3, 18), (5, 23), (3, 25), (3, 25), 25))
    raw_pts.extend(sample_bezier((3, 25), (4, 23), (7, 26), (7, 26), 25))
    raw_pts.extend(sample_bezier((7, 26), (10, 29), (15, 29), (15, 29), 35))
    raw_pts.extend(sample_bezier((15, 29), (8, 28), (8.43, 25.043), (9, 23), 35))
    raw_pts.extend(sample_bezier((9, 23), (10.285, 18.391), (15.5, 5), (15.5, 5), 45))
    raw_pts.extend(sample_line((15.5, 5), (23, 23), 45))
    raw_pts.extend(sample_bezier((23, 23), (25, 28), (17, 29), (17, 29), 35))
    raw_pts.extend(sample_bezier((17, 29), (22, 29), (25, 26), (25, 26), 35))
    raw_pts.extend(sample_bezier((25, 26), (28, 23), (29, 25), (29, 25), 25))
    raw_pts.extend(sample_bezier((29, 25), (27, 22), (29, 18), (29, 18), 25))
    raw_pts.extend(sample_bezier((29, 18), (25, 21), (23, 17), (23, 17), 25))
    raw_pts.extend(sample_line((23, 17), (16.04, 0), 30))

    # Bottom Arc
    raw_pts.extend(sample_bezier((2, 25), (6.999, 32), (15.914, 32), (15.914, 32), 45))
    raw_pts.extend(sample_bezier((15.914, 32), (24.829, 32), (30, 25), (30, 25), 45))
    raw_pts.extend(sample_bezier((30, 25), (19, 35), (16, 29), (16, 29), 45))
    raw_pts.extend(sample_bezier((16, 29), (13, 35), (2, 25), (2, 25), 45))

    cx, cy = GRID_W / 2, GRID_H / 2
    scale = 8.5  # Scale 32px box to ~270px
    
    pts = []
    for x, y in raw_pts:
        nx = cx + (x - 16.0) * scale + (random.random() - 0.5) * 3
        ny = cy + (y - 16.0) * scale + (random.random() - 0.5) * 3
        pts.append((nx, ny))

    if len(pts) > num_points:
        step = len(pts) / float(num_points)
        pts = [pts[int(i * step)] for i in range(num_points)]
    while len(pts) < num_points:
        pts.append((cx, cy))
        
    return pts

def generate_logo_shapes(num_points=800):
    """Generates precise vector points for 1. Hitman, 2. Nike, 3. Assassin's Creed."""
    pts_hitman = generate_hitman_points(num_points=num_points)
    pts_nike = generate_nike_points(num_points=num_points)
    pts_ac = generate_ac_points(num_points=num_points)

    return pts_hitman, pts_nike, pts_ac

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
    
    # 1. LOGO SWARM POINTS (HITMAN -> NIKE -> ASSASSIN'S CREED)
    num_travellers = 800
    pts_hitman, pts_nike_raw, pts_ac_raw = generate_logo_shapes(num_points=num_travellers)
    pts_nike = match_points(pts_hitman, pts_nike_raw)
    pts_ac = match_points(pts_nike, pts_ac_raw)
    pts_hitman_return = match_points(pts_ac, pts_hitman)

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

    # 3. TRAVELLERS SWARM (HITMAN -> NIKE -> ASSASSIN'S CREED)
    traveller_elements = []
    pos_keytimes = "0; 0.176; 0.352; 0.444; 0.585; 0.676; 0.817; 0.908; 1"
    opacity_values = "0; 0; 1; 1; 1; 1; 1; 0; 0"
    
    for i in range(num_travellers):
        p1 = pts_hitman[i]
        p2 = pts_nike[i]
        p3 = pts_ac[i]
        p4 = pts_hitman_return[i]
        
        sx1, sy1 = PORTRAIT_X + p1[0] * SCALE_X, PORTRAIT_Y + p1[1] * SCALE_Y
        sx2, sy2 = PORTRAIT_X + p2[0] * SCALE_X, PORTRAIT_Y + p2[1] * SCALE_Y
        sx3, sy3 = PORTRAIT_X + p3[0] * SCALE_X, PORTRAIT_Y + p3[1] * SCALE_Y
        sx4, sy4 = PORTRAIT_X + p4[0] * SCALE_X, PORTRAIT_Y + p4[1] * SCALE_Y

        x_vals = f"{sx1:.1f}; {sx1:.1f}; {sx1:.1f}; {sx2:.1f}; {sx2:.1f}; {sx3:.1f}; {sx3:.1f}; {sx4:.1f}; {sx4:.1f}"
        y_vals = f"{sy1:.1f}; {sy1:.1f}; {sy1:.1f}; {sy2:.1f}; {sy2:.1f}; {sy3:.1f}; {sy3:.1f}; {sy4:.1f}; {sy4:.1f}"

        dot_xml = f'''    <rect width="2.2" height="2.2" fill="{border_color}" opacity="0">
      <animate attributeName="x" values="{x_vals}" keyTimes="{pos_keytimes}" dur="14.2s" repeatCount="indefinite"/>
      <animate attributeName="y" values="{y_vals}" keyTimes="{pos_keytimes}" dur="14.2s" repeatCount="indefinite"/>
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
        
        row_intro_delay = 0.4 + idx * 0.12
        
        info_rows_xml.append(f'''    <g opacity="0">
      <text x="460" y="{y_pos}" fill="{sub_text_color}" font-family="ui-monospace, Consolas, monospace" font-size="13">{label}</text>
      <text x="610" y="{y_pos}" fill="{sub_text_color}" font-family="ui-monospace, Consolas, monospace" font-size="13" opacity="0.35">{dotted_str}</text>
      <text x="1135" y="{y_pos}" fill="{text_color}" font-family="ui-monospace, Consolas, monospace" font-size="13" font-weight="bold" text-anchor="end">{val}</text>
      <animate attributeName="opacity" values="0;1" keyTimes="0;1" dur="0.6s" begin="{row_intro_delay:.2f}s" fill="freeze" />
    </g>''')

    svg_code = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 610" width="1180" height="610">
  <style>
    .terminal-bg {{ fill: {bg_color}; }}
    .panel-border {{ stroke: {border_color}; stroke-width: 1.5; fill: {panel_bg}; }}
    .header-bg {{ fill: {header_bg}; }}
    .title-text {{ fill: {text_color}; font-family: ui-monospace, Consolas, monospace; font-size: 14px; font-weight: bold; }}
    .pulse-live {{ animation: pulse 1.5s infinite alternate; }}
    @keyframes pulse {{ from {{ opacity: 0.3; }} to {{ opacity: 1; }} }}
  </style>

  <rect width="1180" height="610" rx="10" class="terminal-bg" />
  <rect x="2" y="2" width="1176" height="606" rx="9" fill="none" stroke="{border_color}" stroke-width="1.5" opacity="0.8" />
  
  <path d="M 2 12 Q 2 2 12 2 L 1168 2 Q 1178 2 1178 12 L 1178 40 L 2 40 Z" class="header-bg" />
  <line x1="2" y1="40" x2="1178" y2="40" stroke="{border_color}" stroke-width="1.5" />
  
  <g opacity="0">
    <circle cx="25" cy="21" r="6" fill="#FF5F56" />
    <circle cx="45" cy="21" r="6" fill="#FFBD2E" />
    <circle cx="65" cy="21" r="6" fill="#27C93F" />
    <animate attributeName="opacity" values="0;1" dur="0.4s" begin="0.1s" fill="freeze" />
  </g>
  
  <g opacity="0">
    <text x="590" y="26" class="title-text" text-anchor="middle">profile.sh --live</text>
    <animate attributeName="opacity" values="0;1" dur="0.5s" begin="0.2s" fill="freeze" />
  </g>

  <rect x="25" y="55" width="400" height="530" rx="6" class="panel-border" />
  <rect x="25" y="55" width="400" height="30" rx="6" class="header-bg" />
  <line x1="25" y1="85" x2="425" y2="85" stroke="{border_color}" stroke-width="1" />
  
  <g opacity="0">
    <text x="40" y="75" fill="{border_color}" font-family="ui-monospace, Consolas, monospace" font-size="12" font-weight="bold">VISUAL.MAP</text>
    <animate attributeName="opacity" values="0;1" dur="0.5s" begin="0.25s" fill="freeze" />
  </g>

  <g opacity="0">
    <rect x="270" y="62" width="50" height="16" rx="8" fill="#EF4444" opacity="0.2" />
    <circle cx="280" cy="70" r="4" fill="#EF4444" class="pulse-live" />
    <text x="290" y="73" fill="#EF4444" font-family="ui-monospace, Consolas, monospace" font-size="10" font-weight="bold">LIVE</text>
    <rect x="328" y="62" width="90" height="16" rx="8" fill="{border_color}" opacity="0.2" />
    <text x="373" y="73" fill="{border_color}" font-family="ui-monospace, Consolas, monospace" font-size="9" font-weight="bold" text-anchor="middle">@UnnamedPeople-Chin</text>
    <animate attributeName="opacity" values="0;1" dur="0.5s" begin="0.3s" fill="freeze" />
  </g>

  <g shape-rendering="crispEdges">
{"".join(portrait_band_groups)}
  </g>

  <g>
{"".join(traveller_elements)}
  </g>

  <rect x="440" y="55" width="715" height="530" rx="6" class="panel-border" />
  <rect x="440" y="55" width="715" height="30" rx="6" class="header-bg" />
  <line x1="440" y1="85" x2="1155" y2="85" stroke="{border_color}" stroke-width="1" />
  
  <g opacity="0">
    <text x="455" y="75" fill="{border_color}" font-family="ui-monospace, Consolas, monospace" font-size="12" font-weight="bold">SYSTEM.INFO</text>
    <text x="1140" y="75" fill="{accent_color}" font-family="ui-monospace, Consolas, monospace" font-size="11" font-weight="bold" text-anchor="end">STATUS: ONLINE</text>
    <animate attributeName="opacity" values="0;1" dur="0.5s" begin="0.35s" fill="freeze" />
  </g>

  <g>
{"".join(info_rows_xml)}
  </g>
</svg>'''
    return svg_code

def main():
    print("Processing portrait image...")
    dots_dark, dots_light = process_image(IMAGE_PATH)
    print(f"Extracted {len(dots_dark)} dots for dark mode, {len(dots_light)} dots for light mode.")
    
    print("Building updated dark.svg with HITMAN, NIKE, and ASSASSIN'S CREED SVG files...")
    svg_dark = build_svg(dots_dark, mode="dark")
    with open(OUTPUT_DARK, "w", encoding="utf-8") as f:
        f.write(svg_dark)
    print(f"Saved {OUTPUT_DARK}")

    print("Building updated light.svg with HITMAN, NIKE, and ASSASSIN'S CREED SVG files...")
    svg_light = build_svg(dots_light, mode="light")
    with open(OUTPUT_LIGHT, "w", encoding="utf-8") as f:
        f.write(svg_light)
    print(f"Saved {OUTPUT_LIGHT}")

if __name__ == "__main__":
    main()
