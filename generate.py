import os
from PIL import Image, ImageDraw, ImageFont


def wrap_text(draw, text, font, max_width):
    """Wraps text cleanly into lines that fit within max_width pixels."""
    words = text.split()
    lines = []
    cur = []
    for w in words:
        trial = " ".join(cur + [w])
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] <= max_width or not cur:
            cur.append(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


def draw_hero_scene(draw, kind, x0, y0, w, h):
    """Draws custom editorial vector artwork for each hero story."""
    x1, y1 = x0 + w, y0 + h
    if kind == "nvidia":
        draw.rectangle([x0, y0, x1, y1], fill="#0C2431")
        # Grid lines
        for gx in range(x0 + 25, x1, 35):
            draw.line([(gx, y0), (gx, y1)], fill="#163A4D", width=1)
        for gy in range(y0 + 18, y1, 22):
            draw.line([(x0, gy), (x1, gy)], fill="#163A4D", width=1)
        # Stylized silicon die on left
        cx, cy = x0 + 54, y0 + h // 2
        draw.rounded_rectangle([cx - 26, cy - 26, cx + 26, cy + 26], radius=4, fill="#1E4D2B", outline="#52B788", width=2)
        draw.rectangle([cx - 13, cy - 13, cx + 13, cy + 13], fill="#D4A338")
        for off in (-16, -6, 6, 16):
            draw.line([(cx + off, cy - 32), (cx + off, cy - 26)], fill="#95D5B2", width=2)
            draw.line([(cx + off, cy + 26), (cx + off, cy + 32)], fill="#95D5B2", width=2)
            draw.line([(cx - 32, cy + off), (cx - 26, cy + off)], fill="#95D5B2", width=2)
            draw.line([(cx + 26, cy + off), (cx + 32, cy + off)], fill="#95D5B2", width=2)
        # Surge line chart
        pts = [
            (x0 + 100, y1 - 18),
            (x0 + 135, y1 - 24),
            (x0 + 165, y1 - 16),
            (x0 + 195, y1 - 36),
            (x0 + 230, y1 - 30),
            (x0 + 275, y0 + 16),
        ]
        draw.line(pts, fill="#40E082", width=4)
        ax, ay = pts[-1]
        draw.polygon([(ax + 8, ay - 6), (ax - 10, ay - 4), (ax + 1, ay + 12)], fill="#40E082")
    elif kind == "cop31":
        draw.rectangle([x0, y0, x1, y1], fill="#2C1317")
        # Warm heat glow bands
        draw.rectangle([x0, y1 - 26, x1, y1], fill="#591D1A")
        # Earth curve at bottom-left
        ex, ey = x0 + 68, y0 + h - 8
        draw.pieslice([ex - 54, ey - 54, ex + 54, ey + 54], 180, 360, fill="#2A6F97", outline="#89C2D9", width=2)
        draw.polygon([(ex - 26, ey - 10), (ex - 8, ey - 36), (ex + 14, ey - 24), (ex + 4, ey - 4)], fill="#52B788")
        # Cracked treaty document on right
        dx0, dy0 = x0 + 150, y0 + 12
        draw.rounded_rectangle([dx0, dy0, dx0 + 72, dy0 + 66], radius=3, fill="#F8F1E5", outline="#D6CCC2", width=2)
        for ly in range(dy0 + 14, dy0 + 54, 10):
            draw.line([(dx0 + 10, ly), (dx0 + 60, ly)], fill="#999999", width=2)
        # Big red X / deadlock slash
        draw.line([(dx0 + 12, dy0 + 12), (dx0 + 60, dy0 + 54)], fill="#D62828", width=4)
        draw.line([(dx0 + 60, dy0 + 12), (dx0 + 12, dy0 + 54)], fill="#D62828", width=4)
    elif kind == "conflict":
        draw.rectangle([x0, y0, x1, y1], fill="#1D222D")
        # Sea horizon at bottom
        draw.rectangle([x0, y1 - 22, x1, y1], fill="#11324D")
        draw.line([(x0, y1 - 22), (x1, y1 - 22)], fill="#457B9D", width=2)
        # City skyline silhouette on left
        heights = [28, 46, 34, 54, 30, 42]
        bx = x0 + 14
        for bh in heights:
            draw.rectangle([bx, y1 - 22 - bh, bx + 16, y1 - 22], fill="#343A40", outline="#495057", width=1)
            bx += 20
        # Incoming drone/radar arcs
        draw.arc([x0 + 30, y0 + 6, x0 + 150, y0 + 74], 200, 330, fill="#F77F00", width=3)
        draw.polygon([(x0 + 146, y0 + 26), (x0 + 134, y0 + 20), (x0 + 138, y0 + 34)], fill="#FCBF49")
        # Tanker / ship silhouette on right sea
        sx = x0 + 195
        sy = y1 - 22
        draw.polygon([(sx, sy), (sx + 84, sy), (sx + 94, sy - 12), (sx - 6, sy - 12)], fill="#D62828")
        draw.rectangle([sx + 16, sy - 22, sx + 34, sy - 12], fill="#EAE2B7")


def draw_region_icon(draw, kind, x, y):
    """Draws a crisp mini white icon inside a colored 24px region header bar."""
    if kind == "americas":
        draw.rectangle([x + 3, y + 3, x + 15, y + 15], outline="#FFFFFF", width=2)
        draw.line([(x + 6, y + 9), (x + 12, y + 9)], fill="#FFD166", width=2)
        draw.line([(x + 9, y + 6), (x + 9, y + 12)], fill="#FFD166", width=2)
    elif kind == "europe":
        draw.ellipse([x + 2, y + 2, x + 16, y + 16], outline="#FFD166", width=2)
        draw.ellipse([x + 7, y + 7, x + 11, y + 11], fill="#FFFFFF")
    elif kind == "war":
        draw.polygon([(x + 9, y + 2), (x + 16, y + 15), (x + 2, y + 15)], outline="#FFD166", width=2)
        draw.line([(x + 9, y + 6), (x + 9, y + 11)], fill="#FFFFFF", width=2)
    elif kind == "mideast":
        draw.polygon([(x + 2, y + 11), (x + 16, y + 11), (x + 13, y + 15), (x + 5, y + 15)], fill="#FFFFFF")
        draw.line([(x + 9, y + 4), (x + 9, y + 11)], fill="#FFD166", width=2)
    elif kind == "asia":
        draw.ellipse([x + 3, y + 3, x + 15, y + 15], fill="#EF476F")
        draw.ellipse([x + 6, y + 6, x + 12, y + 12], fill="#FFFFFF")
    elif kind == "africa":
        draw.polygon([(x + 5, y + 2), (x + 14, y + 4), (x + 12, y + 16), (x + 6, y + 12)], fill="#FFD166")
    elif kind == "biz":
        draw.rectangle([x + 2, y + 10, x + 5, y + 15], fill="#FFFFFF")
        draw.rectangle([x + 7, y + 6, x + 10, y + 15], fill="#FFD166")
        draw.rectangle([x + 12, y + 3, x + 15, y + 15], fill="#40E082")
    elif kind == "science":
        draw.ellipse([x + 6, y + 6, x + 12, y + 12], fill="#FFD166")
        draw.arc([x + 1, y + 4, x + 17, y + 14], 0, 360, fill="#A8DADC", width=1)
    elif kind == "sports":
        draw.polygon([(x + 4, y + 3), (x + 14, y + 3), (x + 11, y + 10), (x + 7, y + 10)], fill="#FFD166")
        draw.line([(x + 9, y + 10), (x + 9, y + 15)], fill="#FFFFFF", width=2)
        draw.line([(x + 6, y + 15), (x + 12, y + 15)], fill="#FFFFFF", width=2)


def render_world_news(out_path):
    W, H = 1024, 1024
    img = Image.new("RGB", (W, H), "#FAF7F2")
    draw = ImageDraw.Draw(img)

    fd = r"C:\Windows\Fonts"
    f_mast = ImageFont.truetype(os.path.join(fd, "georgiab.ttf"), 36)
    f_date = ImageFont.truetype(os.path.join(fd, "segoeuib.ttf"), 19)
    f_subbar = ImageFont.truetype(os.path.join(fd, "segoeuib.ttf"), 13)
    f_tag = ImageFont.truetype(os.path.join(fd, "segoeuib.ttf"), 11)
    f_hero_head = ImageFont.truetype(os.path.join(fd, "segoeuib.ttf"), 16)
    f_hero_body = ImageFont.truetype(os.path.join(fd, "calibri.ttf"), 13)
    f_hero_label = ImageFont.truetype(os.path.join(fd, "ariblk.ttf"), 13)

    f_stat_val = ImageFont.truetype(os.path.join(fd, "ariblk.ttf"), 18)
    f_stat_lbl = ImageFont.truetype(os.path.join(fd, "segoeuib.ttf"), 11)

    f_reg_hdr = ImageFont.truetype(os.path.join(fd, "segoeuib.ttf"), 14)
    f_bul_bold = ImageFont.truetype(os.path.join(fd, "calibrib.ttf"), 15)
    f_bul_body = ImageFont.truetype(os.path.join(fd, "calibri.ttf"), 14)
    f_foot = ImageFont.truetype(os.path.join(fd, "segoeuib.ttf"), 12)

    # 1. Masthead (0..54) + gold rule (54..57) + sub-ribbon (57..84)
    draw.rectangle([0, 0, W, 54], fill="#0D1B2A")
    draw.text((18, 7), "THE WORLD IN ONE DAY", fill="#FFFFFF", font=f_mast)

    # Date pill on right
    draw.rounded_rectangle([684, 8, 1008, 46], radius=5, fill="#9E1B1E")
    draw.text((702, 14), "TUESDAY, 24 NOVEMBER 2026", fill="#FFFFFF", font=f_date)

    draw.rectangle([0, 54, W, 57], fill="#D4A338")
    draw.rectangle([0, 57, W, 84], fill="#EAE4D8")
    draw.text((18, 62), "36 VERIFIED DISPATCHES  •  9 REGIONS  •  TUESDAY, 24 NOV 2026 (UTC)", fill="#0D1B2A", font=f_subbar)
    draw.text((696, 62), "TECH • WAR • TRADE • CLIMATE • SPACE • SPORT", fill="#7A1C1C", font=f_subbar)
    draw.line([(0, 84), (W, 84)], fill="#CFC7B8", width=1)

    # 2. Three Illustrated Hero Cards (Y: 92..312)
    heroes = [
        {
            "x": 16,
            "tag": "LEAD • MARKETS & SEMICONDUCTORS",
            "color": "#0F4C5C",
            "scene": "nvidia",
            "callout": "NVDA +31.5% (+$952B)  |  TAIEX +8.99%",
            "head": "HUANG REINSTATED AT NVIDIA; CHIP STOCKS SURGE",
            "body": "After President Trump intervened with Nvidia's board, Jensen Huang returns as CEO; record $952B surge sparks TAIEX & TSMC chip rally.",
        },
        {
            "x": 351,
            "tag": "FLASHPOINT • WAR & MARITIME SECURITY",
            "color": "#8C1D18",
            "scene": "conflict",
            "callout": "ZAPORIZHZHIA • POLAND • HORMUZ",
            "head": "STRIKES HIT ZAPORIZHZHIA; IRAN WARNS HORMUZ",
            "body": "Russian drones smash Zaporizhzhia homes (40+ hurt); NATO flags Poland breach; Iran decries US blockade & warns Hormuz tankers of mines.",
        },
        {
            "x": 686,
            "tag": "POLICY • GLOBAL TRADE & CLIMATE",
            "color": "#7A3E00",
            "scene": "cop31",
            "callout": "16-NATION TARIFFS  |  COP31 FALLOUT",
            "head": "US SETS SEC. 301 TARIFFS; COP31 DEADLOCK REAX",
            "body": "USTR readies subsidy tariffs on 16 economies (China, EU, India, Taiwan); Guterres & AILAC warn 1.5°C peril after Antalya COP31 collapse.",
        },
    ]

    cw = 322
    for h in heroes:
        hx = h["x"]
        draw.rounded_rectangle([hx, 92, hx + cw, 312], radius=5, fill="#FFFFFF", outline="#C9C1B2", width=1)
        # Header bar
        draw.rectangle([hx + 1, 93, hx + cw - 1, 114], fill=h["color"])
        draw.text((hx + 10, 96), h["tag"], fill="#FFFFFF", font=f_tag)
        # Illustrated vector artwork
        draw_hero_scene(draw, h["scene"], hx + 8, 118, cw - 16, 86)
        # Callout strip overlaid cleanly on bottom of art
        draw.rectangle([hx + 8, 183, hx + cw - 8, 204], fill="#0D1B2A")
        draw.text((hx + 14, 185), h["callout"], fill="#FFD166", font=f_hero_label)

        # Hero headline (2 lines max)
        h_lines = wrap_text(draw, h["head"], f_hero_head, cw - 16)
        cy = 208
        for line in h_lines[:2]:
            draw.text((hx + 9, cy), line, fill="#0D1B2A", font=f_hero_head)
            cy += 19

        # Hero body
        b_lines = wrap_text(draw, h["body"], f_hero_body, cw - 16)
        cy += 3
        for line in b_lines[:4]:
            draw.text((hx + 9, cy), line, fill="#22252A", font=f_hero_body)
            cy += 14

    # 3. Key Numbers Strip (Y: 319..360)
    draw.rounded_rectangle([16, 319, 1008, 360], radius=4, fill="#1B263B")
    stats = [
        ("+$952B", "Nvidia record gain (+31.5%)"),
        ("5,258", "England summer heat deaths"),
        ("$41B", "Sanofi–Insmed pharma buyout"),
        ("700K+", "Est. Russian soldier deaths"),
        ("630M yr", "Euclid oldest quasar age"),
    ]
    for idx, (val, lbl) in enumerate(stats):
        sx = 16 + idx * 198
        if idx > 0:
            draw.line([(sx, 326), (sx, 353)], fill="#415A77", width=1)
        draw.text((sx + 10, 321), val, fill="#FFD166", font=f_stat_val)
        draw.text((sx + 10, 343), lbl, fill="#F1FAEE", font=f_stat_lbl)

    # 4. 3x3 Regional Matrix (9 regions x 3 rich dispatches covering 36 verified events)
    regions = [
        (0, 0, "AMERICAS & US TRADE", "#1D3557", "americas", [
            ("Nvidia & Wall St:", "Trump backs Huang clearance; CEO reinstated as Nasdaq 100 & S&P surge."),
            ("Sec. 301 Tariffs:", "USTR probes 16 economies incl. China, EU, India, Japan & Taiwan subsidies."),
            ("Iowa & LatAm:", "Army sets IA lead-azide blasts; AILAC & Panama blast weak fossil text."),
        ]),
        (1, 0, "EUROPE & NATO", "#2A4D69", "europe", [
            ("Poland Breach:", "Merz warns Russia on provocations after missiles cross Polish skies."),
            ("EU Sanctions:", "Brussels blacklists Russian banks, crypto & ex-combatant visas."),
            ("UK & Baltics:", "UKHSA counts 5,258 English heat deaths; Kremlin warns Estonia."),
        ]),
        (2, 0, "RUSSIA–UKRAINE WAR", "#9E2A2B", "war", [
            ("Zaporizhzhia:", "Night drone/missile barrage hits 5-story block; 2+ dead, 40+ hurt."),
            ("Libya Sea Hit:", "Kremlin vows painful response after drone hits warship off Benghazi."),
            ("700K & ADIZ:", "Leaked stats put RU war dead >700K; Seoul scrambles jets vs RU planes."),
        ]),
        (0, 1, "MIDDLE EAST", "#9B5000", "mideast", [
            ("Hormuz Standoff:", "Iran slams US naval blockade; IRGC warns tankers on Strait mines."),
            ("Yemen Strikes:", "Houthis say Saudi-led strikes using US bombs killed 41 civilians."),
            ("Gaza & Missiles:", "Israeli strike kills Gaza chief Abu Nahel; ISW tracks Iran MaRV."),
        ]),
        (1, 1, "ASIA-PACIFIC", "#0F5257", "asia", [
            ("Shanghai Probe:", "Beijing investigates Politburo member & Shanghai chief Chen Jining."),
            ("TAIEX & Japan:", "TAIEX jumps +8.99%; Tokyo drafts Toyota suppliers into military drones."),
            ("Canberra & Pact:", "Australia eyes 5% tech harm fines; Solomon Is. ends China pact."),
        ]),
        (2, 1, "AFRICA & DIPLOMACY", "#4A5D23", "africa", [
            ("IMF Tanzania:", "Fund wraps Article IV review urging fiscal space & private-led jobs."),
            ("Somalia–UAE:", "President Mohamud escalates row with UAE amid Mogadishu pressure."),
            ("TRIPP & Rights:", "Armenia starts Syunik corridor; UK hits Myanmar; LDCs slam COP31."),
        ]),
        (0, 2, "BUSINESS & BIOPHARMA", "#3D405B", "biz", [
            ("Sanofi $41B Deal:", "French pharma agrees $41B acquisition of US rare-disease biotech Insmed."),
            ("Semis Whiplash:", "TSMC & global chipmakers swing between AI rally and tariff fears."),
            ("Clean Capital:", "Private green energy investment accelerates despite COP31 deadlock."),
        ]),
        (1, 2, "SCIENCE & SPACE", "#432371", "science", [
            ("Oldest Quasar:", "ESA Euclid spots Dun Aonghasa shining 630M yrs post-Big Bang."),
            ("Dual Black Holes:", "Astronomers unveil oldest compact pair 900M yrs post-Big Bang."),
            ("Mercury & Mars:", "BepiColombo enters Mercury orbit; NASA ESCAPADE images Earth."),
        ]),
        (2, 2, "WORLD SPORTS", "#8B2635", "sports", [
            ("FIFA U-17 Qatar:", "Dominican Rep. wins 1st FIFA match (2-1 Chile); VEN & IRL advance."),
            ("AFCON Restored:", "CAS overturns CAF ban, reinstating Senegal as 2025 champions."),
            ("NBA & Cricket:", "Tatum scores 41 for Celtics (131-116); Pistons win; BAN-SA Test."),
        ]),
    ]

    col_xs = [16, 351, 686]
    row_ys = [368, 574, 780]
    rh = 198

    for c_idx, r_idx, title, color, icon_kind, bullets in regions:
        rx = col_xs[c_idx]
        ry = row_ys[r_idx]
        draw.rounded_rectangle([rx, ry, rx + cw, ry + rh], radius=4, fill="#FFFFFF", outline="#CFC7B8", width=1)
        draw.rectangle([rx + 1, ry + 1, rx + cw - 1, ry + 27], fill=color)
        draw_region_icon(draw, icon_kind, rx + 7, ry + 4)
        draw.text((rx + 30, ry + 5), title, fill="#FFFFFF", font=f_reg_hdr)

        cur_y = ry + 32
        for b_head, b_text in bullets:
            draw.ellipse([rx + 8, cur_y + 6, rx + 13, cur_y + 11], fill=color)
            hb = draw.textbbox((0, 0), b_head, font=f_bul_bold)
            hw = hb[2] - hb[0]
            draw.text((rx + 18, cur_y), b_head, fill="#0D1B2A", font=f_bul_bold)
            first_avail = (cw - 26) - (hw + 5)
            words = b_text.split()
            line1 = []
            rest_idx = 0
            for idx_w, w in enumerate(words):
                trial = " ".join(line1 + [w])
                tb = draw.textbbox((0, 0), trial, font=f_bul_body)
                if tb[2] - tb[0] <= first_avail:
                    line1.append(w)
                    rest_idx = idx_w + 1
                else:
                    break
            if line1:
                draw.text((rx + 18 + hw + 5, cur_y + 1), " ".join(line1), fill="#22252A", font=f_bul_body)
            rem_text = " ".join(words[rest_idx:])
            cur_y += 17
            if rem_text:
                rem_lines = wrap_text(draw, rem_text, f_bul_body, cw - 26)
                for rl in rem_lines[:2]:
                    draw.text((rx + 18, cur_y), rl, fill="#22252A", font=f_bul_body)
                    cur_y += 16
            cur_y += 6

    # 5. Footer (Y: 988..1024)
    draw.rectangle([0, 988, W, H], fill="#0D1B2A")
    draw.text((18, 997), "THE WORLD IN ONE DAY  |  TUESDAY, 24 NOVEMBER 2026 (UTC)", fill="#FFFFFF", font=f_foot)
    draw.text((536, 997), "36 VERIFIED EVENTS  •  9 REGIONS  •  REUTERS / AP / ESA / NASA / FIFA", fill="#A8DADC", font=f_foot)

    img.save(out_path, format="PNG", optimize=True)
    # Create compact 300px preview for legibility verification
    preview_path = os.path.join(os.path.dirname(out_path), "preview_300.png")
    img.resize((300, 300), Image.Resampling.LANCZOS).save(preview_path, format="PNG")
    sz = os.path.getsize(out_path)
    print(f"Saved {out_path}: {sz} bytes ({sz/1024:.1f} KiB)")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    render_world_news(os.path.join(here, "entry.png"))
