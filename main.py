"""Passport spread generator for make.fun the-passport-page-of-a-countr-2-20261121-0318.

Renders one 1024x1024 invented passport spread (open book: data page left,
visa/stamp page right) with PIL. Deterministic, offline, stdlib + PIL only.
Usage: python3 gen_passport.py <variant> <out.png>

Winner of the local 5-candidate tournament: v1-kestrelia (see tournament.md).
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
MONO = os.path.join(FONT_DIR, "DejaVuSansMono.ttf")
MONO_B = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- countries
COUNTRIES = {
    "v1-kestrelia": {
        "country": "KESTRELIA",
        "country_code": "KES",
        "nationality": "KESTRELIAN",
        "capital": "ALDOR",
        "surname": "VREN",
        "given": "MARA",
        "dob": "14 JUN 1988",
        "dob_mrz": "880614",
        "pob": "ALDOR",
        "sex": "F",
        "number": "K7319042",
        "issue": "12 MAR 2023",
        "expiry": "11 MAR 2033",
        "expiry_mrz": "330311",
        "authority": "MINISTRY OF THE INTERIOR",
        "accent": (38, 68, 104),      # deep alpine blue
        "accent_light": (198, 210, 226),
        "neighbours": [
            ("ALDOVIA", "ENTRY", "02 APR 2024", (30, 80, 160)),
            ("BRENMARK", "EXIT", "19 APR 2024", (150, 40, 40)),
            ("TARNOVIA", "ENTRY", "07 OCT 2025", (40, 110, 60)),
            ("ALDOVIA", "EXIT", "23 OCT 2025", (30, 80, 160)),
        ],
        "visa": ("TARNOVIA", "TRANSIT VISA", "07 OCT 2025", "06 NOV 2025", "No. T-8841"),
        "endorsement": ("ENDORSEMENT", "Mountain transit permit — valid for the Three Valleys only. Holder may not work without a permit."),
        "hair": (58, 40, 28),
        "skin": (214, 178, 148),
        "jacket": (44, 52, 66),
    },
    "v2-zanzamar": {
        "country": "ZANZAMAR",
        "country_code": "ZNZ",
        "nationality": "ZANZAMARI",
        "capital": "QESH",
        "surname": "HARUN",
        "given": "LAYLA",
        "dob": "03 NOV 1991",
        "dob_mrz": "911103",
        "pob": "QESH",
        "sex": "F",
        "number": "Z2904157",
        "issue": "12 MAR 2023",
        "expiry": "11 MAR 2033",
        "expiry_mrz": "330311",
        "authority": "MINISTRY OF THE INTERIOR",
        "accent": (146, 96, 32),      # sand / ochre
        "accent_light": (236, 214, 176),
        "neighbours": [
            ("QESH", "ENTRY", "15 MAY 2024", (30, 80, 160)),
            ("HARUN", "EXIT", "02 JUN 2024", (150, 40, 40)),
            ("ILTAMAR", "ENTRY", "11 JAN 2026", (40, 110, 60)),
            ("QESH", "EXIT", "28 JAN 2026", (30, 80, 160)),
        ],
        "visa": ("ILTAMAR", "VISITOR VISA", "11 JAN 2026", "10 FEB 2026", "No. I-5520"),
        "endorsement": ("ENDORSEMENT", "Water ration card attached — see page 14. Holder may not work without a permit."),
        "hair": (28, 22, 18),
        "skin": (198, 158, 122),
        "jacket": (96, 64, 32),
    },
    "v3-valdoria": {
        "country": "VALDORIA",
        "country_code": "VAL",
        "nationality": "VALDORIAN",
        "capital": "KESSLAND",
        "surname": "NORR",
        "given": "ELIN",
        "dob": "27 FEB 1985",
        "dob_mrz": "850227",
        "pob": "KESSLAND",
        "sex": "F",
        "number": "V5187730",
        "issue": "12 MAR 2023",
        "expiry": "11 MAR 2033",
        "expiry_mrz": "330311",
        "authority": "MINISTRY OF THE INTERIOR",
        "accent": (16, 96, 96),       # baltic teal
        "accent_light": (186, 220, 216),
        "neighbours": [
            ("KESSLAND", "ENTRY", "08 JUN 2024", (30, 80, 160)),
            ("NORVIA", "EXIT", "25 JUN 2024", (150, 40, 40)),
            ("OSTMARK", "ENTRY", "14 SEP 2025", (40, 110, 60)),
            ("KESSLAND", "EXIT", "30 SEP 2025", (30, 80, 160)),
        ],
        "visa": ("OSTMARK", "FERRY VISA", "14 SEP 2025", "13 OCT 2025", "No. O-3107"),
        "endorsement": ("ENDORSEMENT", "Ferry crossing only — no road border. Holder may not work without a permit."),
        "hair": (120, 92, 52),
        "skin": (222, 190, 162),
        "jacket": (24, 64, 64),
    },
    "v4-aerthys": {
        "country": "AERTHYS",
        "country_code": "AER",
        "nationality": "AERTHIAN",
        "capital": "CORVINA",
        "surname": "SELMA",
        "given": "TOMAS",
        "dob": "19 AUG 1979",
        "dob_mrz": "790819",
        "pob": "CORVINA",
        "sex": "M",
        "number": "A6642098",
        "issue": "12 MAR 2023",
        "expiry": "11 MAR 2033",
        "expiry_mrz": "330311",
        "authority": "MINISTRY OF THE INTERIOR",
        "accent": (34, 96, 52),       # island green
        "accent_light": (192, 220, 196),
        "neighbours": [
            ("CORVINA", "ENTRY", "21 JUL 2024", (30, 80, 160)),
            ("SELMA", "EXIT", "05 AUG 2024", (150, 40, 40)),
            ("PORTIS", "ENTRY", "02 MAR 2026", (40, 110, 60)),
            ("CORVINA", "EXIT", "18 MAR 2026", (30, 80, 160)),
        ],
        "visa": ("PORTIS", "ISLAND VISA", "02 MAR 2026", "01 APR 2026", "No. P-7712"),
        "endorsement": ("ENDORSEMENT", "Island residency — mainland travel requires a permit. Holder may not work without a permit."),
        "hair": (40, 36, 34),
        "skin": (206, 168, 138),
        "jacket": (30, 70, 46),
    },
    "v5-tarnovia": {
        "country": "TARNOVIA",
        "country_code": "TAR",
        "nationality": "TARNOVIAN",
        "capital": "VOSTOK",
        "surname": "DURN",
        "given": "ANNA",
        "dob": "30 DEC 1994",
        "dob_mrz": "941230",
        "pob": "VOSTOK",
        "sex": "F",
        "number": "T9053318",
        "issue": "12 MAR 2023",
        "expiry": "11 MAR 2033",
        "expiry_mrz": "330311",
        "authority": "MINISTRY OF THE INTERIOR",
        "accent": (122, 32, 40),      # steppe burgundy
        "accent_light": (228, 196, 198),
        "neighbours": [
            ("VOSTOK", "ENTRY", "10 MAY 2024", (30, 80, 160)),
            ("KESTRELIA", "EXIT", "27 MAY 2024", (150, 40, 40)),
            ("DURNIA", "ENTRY", "19 NOV 2025", (40, 110, 60)),
            ("VOSTOK", "EXIT", "05 DEC 2025", (30, 80, 160)),
        ],
        "visa": ("DURNIA", "STEPPE VISA", "19 NOV 2025", "18 DEC 2025", "No. D-2094"),
        "endorsement": ("ENDORSEMENT", "Steppe transit — horse permit required. Holder may not work without a permit."),
        "hair": (70, 46, 24),
        "skin": (216, 182, 152),
        "jacket": (84, 30, 36),
    },
}


# ---------------------------------------------------------------- MRZ
_MRZ_W = (7, 3, 1)


def _mrz_val(ch):
    if ch == "<":
        return 0
    if ch.isdigit():
        return int(ch)
    return ord(ch) - 55  # A=10 ... Z=35


def mrz_check(s):
    total = 0
    for i, ch in enumerate(s):
        total += _mrz_val(ch) * _MRZ_W[i % 3]
    return str(total % 10)


def mrz_lines(c):
    surname = c["surname"].upper().replace(" ", "<")
    given = c["given"].upper().replace(" ", "<")
    line1 = ("P<" + c["country_code"] + surname + "<<" + given).ljust(44, "<")[:44]
    # TD3 line 2 (44 chars): doc no 9 (padded) + check + nationality 3 +
    # DOB 6 + check + sex 1 + expiry 6 + check + personal no 14 + check + composite check
    doc = c["number"].ljust(9, "<")
    dob = c["dob_mrz"]
    exp = c["expiry_mrz"]
    pnum = "<" * 14
    body = (doc + mrz_check(doc) + c["country_code"]
            + dob + mrz_check(dob) + c["sex"]
            + exp + mrz_check(exp) + pnum)
    body = body + mrz_check(pnum)
    # composite check covers doc+check, dob+check, expiry+check, pnum+check
    comp_src = doc + mrz_check(doc) + dob + mrz_check(dob) + exp + mrz_check(exp) + pnum + mrz_check(pnum)
    line2 = body + mrz_check(comp_src)
    assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
    return line1, line2


# ---------------------------------------------------------------- helpers
def arc_text(draw, cx, cy, r, text, fnt, color, start_deg, end_deg):
    """Draw text along a circular arc (top of circle), centred on the arc."""
    n = len(text)
    if n == 0:
        return
    step = (end_deg - start_deg) / max(n - 1, 1)
    for i, ch in enumerate(text):
        ang = math.radians(start_deg + i * step)
        x = cx + r * math.sin(ang)
        y = cy - r * math.cos(ang)
        # draw char on a small tile then rotate it
        tile = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        w = td.textlength(ch, font=fnt)
        td.text(((40 - w) / 2, (40 - fnt.size) / 2), ch, font=fnt, fill=color + (255,))
        rot = tile.rotate(-math.degrees(ang), resample=Image.BICUBIC, center=(20, 20))
        draw._image.paste(rot, (int(x - 20), int(y - 20)), rot)


def stamp_circle(draw, img, cx, cy, r, label_top, label_bottom, mid, color, date):
    """A round border-control stamp, slightly rotated, in faded ink."""
    # draw on a layer so we can rotate the whole stamp a touch
    layer = Image.new("RGBA", (2 * r + 40, 2 * r + 40), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    cc = r + 20
    ld.ellipse([cc - r, cc - r, cc + r, cc + r], outline=color + (200,), width=3)
    ld.ellipse([cc - r + 9, cc - r + 9, cc + r - 9, cc + r - 9], outline=color + (170,), width=1)
    f_small = font(SANS_B, 13)
    f_mid = font(SANS_B, 16)
    f_date = font(MONO_B, 14)
    arc_text(ld, cc, cc, r - 16, label_top, f_small, color, -62, 62)
    arc_text(ld, cc, cc, r - 16, label_bottom, f_small, color, 118, 242)
    ld.text((cc, cc - 8), mid, font=f_mid, fill=color + (210,), anchor="mm")
    ld.text((cc, cc + 16), date, font=f_date, fill=color + (210,), anchor="mm")
    # a small star between the words
    ld.text((cc, cc - 26), "*", font=font(SERIF_B, 18), fill=color + (200,), anchor="mm")
    layer = layer.rotate(8, resample=Image.BICUBIC, expand=False)
    img.paste(layer, (cx - r - 20, cy - r - 20), layer)


def guilloche(draw, w, h, color):
    """Faint wavy security lines across the page."""
    for y0 in range(0, h, 26):
        pts = []
        for x in range(0, w + 1, 16):
            pts.append((x, y0 + 4 * math.sin(x / 46.0 + y0 / 30.0)))
        draw.line(pts, fill=color, width=1)


def draw_portrait(draw, box, c):
    """Stylised passport portrait: bust silhouette in the country's tones."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # background: soft vertical gradient in the accent's light tone
    for i in range(h):
        t = i / max(h - 1, 1)
        col = tuple(int(c["accent_light"][k] * (1 - 0.25 * t) + 255 * 0.25 * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=col)
    cx = (x0 + x1) // 2
    # shoulders / jacket
    draw.pieslice([cx - 78, y0 + h - 96, cx + 78, y0 + h + 40], 180, 360, fill=c["jacket"])
    # shirt + tie
    draw.polygon([(cx - 16, y0 + h - 78), (cx + 16, y0 + h - 78), (cx, y0 + h - 30)], fill=(245, 245, 240))
    draw.polygon([(cx - 6, y0 + h - 66), (cx + 6, y0 + h - 66), (cx + 4, y0 + h - 34), (cx - 4, y0 + h - 34)], fill=c["accent"])
    # neck
    draw.rectangle([cx - 15, y0 + h - 118, cx + 15, y0 + h - 78], fill=c["skin"])
    # head
    draw.ellipse([cx - 42, y0 + 26, cx + 42, y0 + 122], fill=c["skin"])
    # hair: top arc + side sweep
    draw.pieslice([cx - 44, y0 + 20, cx + 44, y0 + 96], 180, 360, fill=c["hair"])
    draw.ellipse([cx - 44, y0 + 52, cx - 18, y0 + 92], fill=c["hair"])
    draw.ellipse([cx + 18, y0 + 52, cx + 44, y0 + 92], fill=c["hair"])
    # simple facial marks: eyes + brows + mouth, very light
    eye = (60, 44, 32)
    draw.ellipse([cx - 24, y0 + 74, cx - 12, y0 + 80], fill=eye)
    draw.ellipse([cx + 12, y0 + 74, cx + 24, y0 + 80], fill=eye)
    draw.line([(cx - 26, y0 + 66), (cx - 10, y0 + 64)], fill=c["hair"], width=2)
    draw.line([(cx + 10, y0 + 64), (cx + 26, y0 + 66)], fill=c["hair"], width=2)
    draw.arc([cx - 10, y0 + 98, cx + 10, y0 + 110], 0, 180, fill=(150, 90, 70), width=2)
    # frame
    draw.rectangle([x0, y0, x1, y1], outline=c["accent"], width=3)
    draw.rectangle([x0 + 4, y0 + 4, x1 - 4, y1 - 4], outline=(255, 255, 255), width=1)


def emblem(draw, cx, cy, r, c):
    """Small coat of arms: shield + star in the accent colour."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c["accent"], width=3)
    draw.polygon([(cx, cy - r + 4), (cx + r - 6, cy - 2), (cx + r - 10, cy + r - 6),
                  (cx - r + 10, cy + r - 6), (cx - r + 6, cy - 2)], fill=c["accent_light"], outline=c["accent"])
    # star
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = (r - 12) if i % 2 == 0 else (r - 22)
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=c["accent"])


# ---------------------------------------------------------------- render
def render(variant, out_path):
    c = COUNTRIES[variant]
    W, H = 1024, 1024
    paper = (245, 241, 230)
    ink = (32, 32, 30)
    grey = (110, 106, 96)
    accent = c["accent"]
    img = Image.new("RGB", (W, H), paper)
    d = ImageDraw.Draw(img, "RGBA")
    guilloche(d, W, H, (200, 192, 172))
    # gutter + outer border
    d.line([(512, 0), (512, H)], fill=(150, 140, 120), width=2)
    d.rectangle([6, 6, W - 7, H - 7], outline=(120, 110, 92), width=2)

    # ================= LEFT PAGE: data page (x 8..510) =================
    L = 26
    # header
    d.text((L, 34), "PASSPORT", font=font(SERIF_B, 30), fill=accent)
    d.text((L, 70), "PASSEPORT", font=font(SERIF, 15), fill=grey)
    emblem(d, 470, 58, 26, c)
    d.text((L, 100), c["country"], font=font(SERIF_B, 26), fill=ink)
    d.text((L, 128), "REPUBLIC  ·  " + c["capital"], font=font(SANS, 13), fill=grey)
    d.line([(L, 152), (486, 152)], fill=accent, width=2)

    # portrait
    draw_portrait(d, (L, 168, L + 158, 168 + 196), c)
    # data fields, right of portrait
    fx, fy = L + 178, 168
    fields = [
        ("SURNAME / NOM", c["surname"]),
        ("GIVEN NAMES / PRÉNOMS", c["given"]),
        ("NATIONALITY / NATIONALITÉ", c["nationality"]),
        ("DATE OF BIRTH", c["dob"]),
        ("PLACE OF BIRTH", c["pob"]),
        ("SEX / SEXE", c["sex"]),
    ]
    y = fy
    for label, value in fields:
        d.text((fx, y), label, font=font(SANS, 11), fill=grey)
        d.text((fx, y + 14), value, font=font(SANS_B, 17), fill=ink)
        y += 34
    # second block under portrait + fields
    y = 392
    fields2 = [
        ("PASSPORT No. / No. DU PASSEPORT", c["number"]),
        ("DATE OF ISSUE / DATE DE DÉLIVRANCE", c["issue"]),
        ("DATE OF EXPIRY / DATE D'EXPIRATION", c["expiry"]),
        ("AUTHORITY / AUTORITÉ", c["authority"]),
    ]
    for label, value in fields2:
        d.text((L, y), label, font=font(SANS, 11), fill=grey)
        d.text((L, y + 14), value, font=font(SANS_B, 16), fill=ink)
        y += 34
    d.line([(L, 540), (486, 540)], fill=accent, width=1)
    # signature line
    d.text((L, 556), "HOLDER'S SIGNATURE / SIGNATURE DU TITULAIRE", font=font(SANS, 10), fill=grey)
    # script-like signature
    d.text((L + 8, 578), c["given"].title() + " " + c["surname"].title(),
           font=font(SERIF, 22), fill=(60, 60, 80))
    d.line([(L, 612), (L + 240, 612)], fill=ink, width=1)
    # MRZ
    line1, line2 = mrz_lines(c)
    d.rectangle([L, 640, 486, 700], fill=(232, 228, 216))
    d.text((L + 6, 648), line1, font=font(MONO, 15), fill=ink)
    d.text((L + 6, 672), line2, font=font(MONO, 15), fill=ink)
    d.text((L, 716), "TYPE P   ·   CODE " + c["country_code"] + "   ·   " + c["number"],
           font=font(SANS, 12), fill=grey)
    d.text((L, 736), "This passport is the property of " + c["country"].title() + ".",
           font=font(SERIF, 13), fill=grey)

    # ================= RIGHT PAGE: visas / stamps (x 538..998) =================
    R = 538
    d.text((R, 34), "VISAS", font=font(SERIF_B, 30), fill=accent)
    d.text((R, 70), "ENTRÉES  ·  SORTIES  ·  STAMPS", font=font(SERIF, 15), fill=grey)
    d.line([(R, 100), (998, 100)], fill=accent, width=2)

    # visa sticker (rectangular, top right area)
    vx, vy, vw, vh = R, 120, 460, 150
    d.rectangle([vx, vy, vx + vw, vy + vh], outline=c["accent"], width=2, fill=(255, 255, 255))
    d.rectangle([vx + 5, vy + 5, vx + vw - 5, vy + vh - 5], outline=c["accent"], width=1)
    vname, vtype, vfrom, vto, vno = c["visa"]
    d.text((vx + 14, vy + 10), vname, font=font(SERIF_B, 20), fill=accent)
    d.text((vx + 14, vy + 38), vtype, font=font(SANS_B, 15), fill=ink)
    d.text((vx + 14, vy + 62), "VALID  " + vfrom + "  —  " + vto, font=font(SANS, 14), fill=ink)
    d.text((vx + 14, vy + 86), vno + "   ·   SINGLE ENTRY", font=font(MONO, 13), fill=grey)
    d.text((vx + 14, vy + 112), "ISSUED AT " + c["capital"] + "  ·  FEE PAID", font=font(SANS, 12), fill=grey)

    # circular stamps, 2x2 grid
    positions = [(R + 105, 380), (R + 355, 380), (R + 105, 570), (R + 355, 570)]
    for (cx, cy), (place, kind, date, col) in zip(positions, c["neighbours"]):
        stamp_circle(d, img, cx, cy, 78, place, "BORDER CONTROL", kind, col, date)

    # endorsement box — the telling paperwork detail
    ex, ey, ew, eh = R, 690, 460, 130
    d.rectangle([ex, ey, ex + ew, ey + eh], outline=accent, width=2, fill=(255, 252, 240))
    title, body = c["endorsement"]
    d.text((ex + 14, ey + 10), title, font=font(SANS_B, 14), fill=accent)
    # wrap body to two/three lines
    words = body.split()
    lines, cur = [], ""
    f_body = font(SANS, 14)
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=f_body) <= ew - 28:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    yy = ey + 34
    for ln in lines[:4]:
        d.text((ex + 14, yy), ln, font=f_body, fill=ink)
        yy += 20
    # small fee stamp in the corner of the endorsement
    d.text((ex + ew - 96, ey + eh - 26), "FEE 40 K", font=font(MONO_B, 13),
           fill=(150, 40, 40))
    d.rectangle([ex + ew - 104, ey + eh - 30, ex + ew - 8, ey + eh - 6],
                outline=(150, 40, 40), width=1)

    d.text((R, 850), "PAGES 12–13  ·  " + c["country"] + "  ·  " + c["number"],
           font=font(SANS, 12), fill=grey)
    d.text((R, 872), "Any alteration voids this document.",
           font=font(SERIF, 13), fill=grey)

    img.save(out_path, "PNG", optimize=True)
    return out_path


WINNER = "v1-kestrelia"  # tournament winner; the program always renders this one


if __name__ == "__main__":
    # The entry program: render the tournament-winning variant, deterministically.
    os.makedirs("/output", exist_ok=True)
    render(WINNER, "/output/entry.png")
    print("wrote /output/entry.png", os.path.getsize("/output/entry.png"), "bytes")
