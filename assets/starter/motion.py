"""Portable drawing primitives distilled from the approved Babayaga edit."""
from pathlib import Path
import bisect
import functools
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent
W, H = 1080, 1920
BLUE, INK, PAPER = (93, 113, 252), (5, 7, 11), (244, 245, 249)
WHITE, GRAY = (255, 255, 255), (160, 160, 160)
# Conservative shared working area, not a universal platform specification.
# See references/plateformes.md. Coordinates include the complete text layer.
TEXT_SAFE_BOX = (90, 280, 850, 1240)
CAPTION_Y = 1060
CAPTION_WIDTH = TEXT_SAFE_BOX[2] - TEXT_SAFE_BOX[0]
CAPTION_TEXT_WIDTH = CAPTION_WIDTH - 40
CAPTION_STYLES = {
    "legacy": {
        "size": 58, "min_size": 48, "width": 760, "center": (470, 1148),
        "safe_box": TEXT_SAFE_BOX,
    },
    "small-center": {
        "size": 44, "min_size": 40, "width": 640, "center": (540, 1080),
        "safe_box": (90, 280, 900, 1240),
    },
    "large-bottom": {
        "size": 58, "min_size": 48, "width": 760, "center": (540, 1450),
        "safe_box": (90, 280, 940, 1600),
    },
}


def caption_style(name):
    if name not in CAPTION_STYLES:
        raise ValueError(f"Style de sous-titres inconnu : {name}. "
                         "Choisir small-center ou large-bottom.")
    return CAPTION_STYLES[name]


def caption_mode(name):
    if name not in ("group", "word"):
        raise ValueError(f"Mode de sous-titres inconnu : {name}. Choisir group ou word.")
    return name


def clamp(x):
    return max(0., min(1., x))


def ease(x):
    return 1 - (1 - clamp(x)) ** 3


def smooth(x):
    p = clamp(x)
    return p * p * (3 - 2 * p)


def mix(a, b, p):
    return a + (b - a) * p


@functools.lru_cache(maxsize=80)
def font(size, bold=False):
    filename = "SomeoneExtended-Bold.ttf" if bold else "SomeoneExtended.ttf"
    return ImageFont.truetype(str(ROOT / "assets/fonts" / filename), int(size))


def fit(image, size, center=(.5, .5)):
    return ImageOps.fit(image, size, Image.Resampling.LANCZOS, centering=tuple(center))


@functools.lru_cache(maxsize=1)
def shade_layer():
    yy = np.arange(H) / H
    alpha = np.interp(yy, [0, .18, .4, .50, .57, .65, .75, .90, 1],
                      [20, 0, 0, 20, 110, 110, 35, 40, 30])
    array = np.zeros((H, W, 4), np.uint8)
    array[:, :, :3] = INK
    array[:, :, 3] = alpha[:, None]
    return Image.fromarray(array)


def shade(image):
    image = image.copy()
    layer = shade_layer()
    image.paste(layer, (0, 0), layer)
    return image


def put(image, layer, center, scale=1, opacity=1, angle=0):
    if opacity <= 0 or scale <= 0:
        return
    layer = layer.convert("RGBA")
    if abs(scale - 1) > .001:
        layer = layer.resize((max(1, round(layer.width * scale)),
                              max(1, round(layer.height * scale))), Image.Resampling.LANCZOS)
    if angle:
        layer = layer.rotate(angle, Image.Resampling.BICUBIC, expand=True)
    if opacity < .999:
        layer = layer.copy()
        layer.putalpha(layer.getchannel("A").point(lambda a: round(a * clamp(opacity))))
    image.paste(layer, (round(center[0] - layer.width / 2),
                        round(center[1] - layer.height / 2)), layer)


def put_safe_text(image, layer, center, opacity=1):
    """Keep a static label, including its background/glow, inside the safe area."""
    left, top, right, bottom = TEXT_SAFE_BOX
    if layer.width > right - left or layer.height > bottom - top:
        raise ValueError("Libellé trop grand : raccourcir le texte ou recomposer le schéma.")
    x = max(left, min(round(center[0] - layer.width / 2), right - layer.width))
    y = max(top, min(round(center[1] - layer.height / 2), bottom - layer.height))
    put(image, layer, (x + layer.width / 2, y + layer.height / 2), opacity=opacity)


def safe_zone_guide(image, style="legacy"):
    """Preview only: tint reserved areas; never simulate an official app UI."""
    result = image.convert("RGBA")
    overlay = Image.new("RGBA", image.size, (240, 55, 80, 80))
    left, top, right, bottom = caption_style(style)["safe_box"]
    draw = ImageDraw.Draw(overlay)
    draw.rectangle((left, top, right - 1, bottom - 1), fill=(0, 0, 0, 0),
                   outline=(100, 255, 180, 255), width=3)
    if style != "legacy":
        cx, cy = caption_style(style)["center"]
        draw.line((cx, top, cx, bottom), fill=(100, 255, 180, 180), width=2)
        draw.line((left, cy, right, cy), fill=(100, 255, 180, 180), width=2)
    result.alpha_composite(overlay)
    return result.convert("RGB")


@functools.lru_cache(maxsize=1)
def background():
    yy, xx = np.mgrid[0:H, 0:W]
    glow = np.exp(-(((xx - 540) / 540) ** 2 + ((yy - 820) / 1050) ** 2) * 2)
    array = np.zeros((H, W, 3), np.uint8)
    for channel, value in enumerate(INK):
        array[:, :, channel] = value + glow * (4 if channel < 2 else 8)
    return Image.fromarray(array)


def stage(t):
    image = background().copy()
    draw = ImageDraw.Draw(image)
    for y in range(45, 1900, 25):
        for x in range(25, 1080, 25):
            edge = math.exp(-(((x - 540) / 395) ** 2 + ((y - 870) / 1120) ** 2) * 1.6)
            dx = 7 * math.sin(y / 170 + t * .28) * edge
            dy = 3 * math.cos(x / 130 + t * .22) * edge
            light = int(16 + 64 * edge)
            draw.ellipse((x + dx - 1, y + dy - 1, x + dx + 1, y + dy + 1),
                         fill=(light, light + 2, light + 9))
    return image


@functools.lru_cache(maxsize=30)
def rounded_mask(width, height, radius):
    mask = Image.new("L", (width * 2, height * 2))
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width * 2 - 1, height * 2 - 1),
                                           radius * 2, fill=255)
    return mask.resize((width, height), Image.Resampling.LANCZOS)


def panel(image, source, box=(42, 1320, 996, 552), radius=48, opacity=1, center=(.5, .37)):
    x, y, width, height = map(round, box)
    layer = fit(source, (width, height), center).convert("RGBA")
    layer.putalpha(rounded_mask(width, height, radius))
    put(image, layer, (x + width / 2, y + height / 2), opacity=opacity)


def popout_panel(image, source):
    """Same host framing, with only the person extending above the rounded set."""
    alpha = source.info.get("matte")
    if alpha is None:
        raise ValueError("Masque vidéo de détourage manquant pour la fenêtre orateur.")
    settings = source.info.get("popout", {})
    x, width, radius = settings.get("x", 42), settings.get("width", 996), 48
    top = settings.get("foreground_top", 1090)
    bottom = settings.get("background_bottom", 1872)
    background_top = settings.get("background_top", 1320)
    crop_width = source.width / settings.get("source_zoom", 1.02)
    crop_left = (source.width - crop_width) / 2
    scale = width / crop_width
    source_origin = (settings.get("screen_anchor_y", 1425)
                     - settings.get("source_anchor_y", 780) * scale)
    source_top = (top - source_origin) / scale
    source_bottom = (bottom - source_origin) / scale
    size = (width, bottom - top)
    extent = (crop_left, source_top, crop_left + crop_width, source_bottom)
    rgb = source.transform(size, Image.Transform.EXTENT, extent,
                           Image.Resampling.BICUBIC).convert("RGBA")
    sx, sy = alpha.width / source.width, alpha.height / source.height
    mask = alpha.transform(size, Image.Transform.EXTENT,
                           (crop_left * sx, source_top * sy, (crop_left + crop_width) * sx, source_bottom * sy),
                           Image.Resampling.BICUBIC)
    # Suppress background dust while preserving semi-transparent hair edges.
    mask = mask.point(lambda a: max(0, min(255, round((a - 3) * 255 / 250))))
    foreground = np.asarray(mask).copy()
    foreground[background_top - top + radius:] = 0
    background = Image.new("L", size)
    background.paste(rounded_mask(width, bottom - background_top, radius),
                     (0, background_top - top))
    rgb.putalpha(Image.fromarray(np.maximum(np.asarray(background), foreground)))
    image.paste(rgb, (x, top), rgb)


ANIMATION_HOST_MODES = ("hidden", "popout", "inset", "behind")


def animation_host_settings(config):
    """One presenter treatment for the whole film, including custom animations."""
    settings = config.get("animation_host")
    legacy = config.get("host_popout", {})
    if settings is not None and legacy.get("enabled"):
        raise ValueError("Conserver un seul réglage global : animation_host.")
    if settings is None:
        settings = ({"mode": "popout", "alpha": legacy["alpha"], "popout": legacy}
                    if legacy.get("enabled") else {"mode": "inset"})
    if settings.get("mode") not in ANIMATION_HOST_MODES:
        raise ValueError("animation_host.mode : hidden, popout, inset ou behind.")
    for scene in config.get("scenes", []):
        if any(key in scene for key in ("animation_host", "host_mode", "host_popout")):
            raise ValueError("Le mode orateur est global : aucun changement par scène.")
    return settings


def animation_presenter(image, source, settings):
    """Place the presenter after all animation layers and before the captions."""
    mode = settings["mode"]
    if mode == "hidden":
        return
    if mode == "inset":
        inset = settings.get("inset", {})
        panel(image, source, inset.get("box", (42, 1320, 996, 552)),
              radius=inset.get("radius", 48), center=inset.get("center", (.5, .37)))
        return
    if mode == "popout":
        source.info["popout"] = settings.get("popout", {})
        popout_panel(image, source)
        return
    if mode != "behind":
        raise ValueError(f"Mode orateur inconnu : {mode}")
    alpha = source.info.get("matte")
    if alpha is None:
        raise ValueError("Masque temporel requis pour placer la simulation derrière l’orateur.")
    # Keep the entire silhouette, not just the head above a panel boundary.
    layer = source.convert("RGBA")
    mask = alpha.resize(source.size, Image.Resampling.BICUBIC)
    layer.putalpha(mask.point(lambda a: max(0, min(255, round((a - 3) * 255 / 250)))))
    framing = settings.get("behind", {})
    scale = framing.get("scale", 1.0)
    if scale <= 0:
        raise ValueError("animation_host.behind.scale doit être positif.")
    center = (framing.get("x", 0) + source.width * scale / 2,
              framing.get("y", 0) + source.height * scale / 2)
    put(image, layer, center, scale=scale)


def soft_glow(layer, strength=.28):
    glow = Image.new("RGBA", layer.size, BLUE + (0,))
    glow.putalpha(layer.getchannel("A").filter(ImageFilter.GaussianBlur(10))
                  .point(lambda a: round(a * strength)))
    glow.alpha_composite(layer)
    return glow


@functools.lru_cache(maxsize=80)
def label(text, size=32):
    """Only semantic node labels; intentionally no bright outline."""
    f = font(size, True)
    width, height = math.ceil(f.getlength(text)) + 46, size + 42
    layer = Image.new("RGBA", (width, height), BLUE + (255,))
    layer.putalpha(rounded_mask(width, height, 10))
    centered_text(layer, text, (width / 2, height / 2), size)
    outer = Image.new("RGBA", (width + 36, height + 36))
    outer.alpha_composite(layer, (18, 18))
    return outer


def centered_text(image, text, center, size, bold=True, fill=WHITE):
    """Center visible letters rather than the font's ascender/descender box."""
    face = font(size, bold)
    left, top, right, bottom = face.getbbox(text)
    glyph = Image.new("RGBA", (right - left + 8, bottom - top + 8))
    ImageDraw.Draw(glyph).text((4 - left, 4 - top), text, font=face, fill=fill)
    box = glyph.getbbox()
    if box:
        put(image, glyph.crop(box), center)


def card(source, width=290, height=430):
    layer = fit(source, (width, height)).convert("RGBA")
    layer.putalpha(rounded_mask(width, height, 18))
    # Borders on image nodes are distinct from removed title borders.
    ImageDraw.Draw(layer).rounded_rectangle((1, 1, width - 2, height - 2),
                                            18, outline=(220, 228, 250), width=2)
    outer = Image.new("RGBA", (width + 40, height + 40))
    outer.alpha_composite(layer, (20, 20))
    return soft_glow(outer, .24)


def connector(image, start, end, progress):
    if progress <= 0:
        return
    point = (mix(start[0], end[0], clamp(progress)), mix(start[1], end[1], clamp(progress)))
    draw = ImageDraw.Draw(image)
    draw.line((start, point), fill=BLUE, width=4)
    for x, y in (start, point):
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=WHITE)


@functools.lru_cache(maxsize=12)
def document(title="DOCUMENT", subtitle="D’EXPÉDITION", stamp="FAUX ?"):
    layer = Image.new("RGBA", (560, 740), PAPER + (255,))
    draw = ImageDraw.Draw(layer)
    draw.rectangle((0, 0, 18, 740), fill=(189, 198, 224))
    draw.rectangle((18, 0, 27, 740), fill=(218, 223, 238))
    draw.rectangle((27, 0, 559, 739), outline=(139, 150, 179), width=2)
    for text, y, size, bold in ((title, 65, 29, True), (subtitle, 112, 23, False)):
        while font(size, bold).getlength(text) > 425 and size > 12:
            size -= 1
        draw.text((68, y), text, font=font(size, bold), fill=(50, 60, 84), anchor="lt")
    draw.line((68, 176, 492, 176), fill=BLUE, width=3)
    for j, length in enumerate((350, 385, 305, 375, 290)):
        draw.line((68, 242 + j * 49, 68 + length, 242 + j * 49), fill=(170, 179, 200), width=4)
    draw.rectangle((68, 528, 255, 610), outline=(165, 175, 198), width=2)
    for x in range(71, 250, 12):
        draw.line((x, 536, x, 597), fill=(138, 149, 176), width=2)
    if stamp:
        stamp_layer = Image.new("RGBA", (248, 104))
        ds = ImageDraw.Draw(stamp_layer)
        ds.rounded_rectangle((3, 3, 244, 100), 8, fill=(225, 230, 253), outline=BLUE, width=4)
        size = 31
        while font(size, True).getlength(stamp) > 220 and size > 12:
            size -= 1
        ds.text((124, 52), stamp, font=font(size, True), fill=BLUE, anchor="mm")
        stamp_layer = stamp_layer.rotate(-9, Image.Resampling.BICUBIC, expand=True)
        layer.alpha_composite(stamp_layer, (255, 518))
    return layer


@functools.lru_cache(maxsize=8)
def coins(count=5):
    layer = Image.new("RGBA", (340, 330))
    draw = ImageDraw.Draw(layer)
    for j in range(max(1, min(8, count))):
        y = 270 - j * 31
        draw.rounded_rectangle((69, y - 34, 271, y + 9), 7, fill=(36, 49, 112),
                               outline=(180, 196, 255), width=2)
        draw.ellipse((69, y - 54, 271, y - 7), fill=(70, 88, 194),
                     outline=(219, 228, 255), width=2)
        draw.ellipse((90, y - 47, 250, y - 13), outline=(137, 158, 246), width=2)
    return soft_glow(layer)


@functools.lru_cache(maxsize=300)
def caption_layout(words, style="legacy"):
    preset = caption_style(style)
    words = tuple(word.upper().rstrip(".,") for word in words)
    text_width = preset["width"] - 40
    size = preset["size"]
    while size >= preset["min_size"]:
        f, fb = font(size), font(size, True)
        gap = f.getlength(" ")
        lines, line, width = [], [], 0
        for i, word in enumerate(words):
            ww = max(f.getlength(word), fb.getlength(word))
            if line and width + gap + ww > text_width:
                lines.append(line)
                line, width = [], 0
            line.append((i, word, ww))
            width += ww + (gap if len(line) > 1 else 0)
        if line:
            lines.append(line)
        if len(lines) <= 2 and all(x[2] <= text_width for row in lines for x in row):
            return size, gap, lines
        size -= 1
    raise ValueError(f"Groupe trop long pour {style} à {preset['min_size']} px sur deux lignes : "
                     "le découper aux vrais temps des mots.")


@functools.lru_cache(maxsize=300)
def word_caption_geometry(words, style):
    normalized = tuple(word.upper().rstrip(".,") for word in words)
    # Use one font size and canvas for the whole group, sized for its longest word.
    size = min(caption_layout((word,), style)[0] for word in normalized)
    face = font(size, True)
    bounds = tuple(face.getbbox(word, anchor="ls") for word in normalized)
    # A constant canvas keeps the screen anchor identical across every group.
    height = caption_style(style)["size"] + 44
    return normalized, size, bounds, height


@functools.lru_cache(maxsize=300)
def word_caption_card(words, active, style):
    words, size, bounds, height = word_caption_geometry(words, style)
    width = caption_style(style)["width"]
    layer = Image.new("RGBA", (width, height))
    l, t, r, b = bounds[active]
    ImageDraw.Draw(layer).text(
        ((width - l - r) / 2, (height - t - b) / 2), words[active],
        font=font(size, True), fill=WHITE, anchor="ls",
    )
    # Center the rasterized letters too: font side bearings can otherwise shift
    # short words several pixels even when their metric bounds are centered.
    glyph = layer.crop(layer.getbbox())
    layer = Image.new("RGBA", (width, height))
    layer.alpha_composite(glyph, ((width - glyph.width) // 2,
                                  (height - glyph.height) // 2))
    shadow = Image.new("RGBA", layer.size)
    shadow.putalpha(layer.getchannel("A").filter(ImageFilter.GaussianBlur(3)))
    shadow.alpha_composite(layer)
    return shadow


@functools.lru_cache(maxsize=300)
def caption_card(words, active, style="legacy", mode="group"):
    if caption_mode(mode) == "word":
        return word_caption_card(words, active, style)
    size, gap, lines = caption_layout(words, style)
    f, fb = font(size), font(size, True)
    width = caption_style(style)["width"]
    if style == "legacy":
        height = len(lines) * (size + 18) + 24
        origins = [(width - sum(w[2] for w in row) - gap * (len(row)-1)) / 2
                   for row in lines]
        baselines = [size + 12 + k * (size + 18) for k in range(len(lines))]
    else:
        # Use the union of Regular/Bold ink bounds for the entire group:
        # true centering, accents included, with no drift as words activate.
        line_step = size + 14
        envelopes = []
        top, bottom = math.inf, -math.inf
        for k, row in enumerate(lines):
            x = 0
            left, right = math.inf, -math.inf
            for _, word, reserved in row:
                for face in (f, fb):
                    offset = (reserved - face.getlength(word)) / 2
                    l, t, r, b = face.getbbox(word, anchor="ls")
                    left, right = min(left, x+offset+l), max(right, x+offset+r)
                    top, bottom = min(top, k*line_step+t), max(bottom, k*line_step+b)
                x += reserved + gap
            envelopes.append((left, right))
        height = math.ceil(bottom - top) + 24
        origins = [(width - left - right) / 2 for left, right in envelopes]
        baselines = [12 - top + k*line_step for k in range(len(lines))]
    layer = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(layer)
    for k, row in enumerate(lines):
        x = origins[k]
        for i, word, width in row:
            face = fb if i == active else f
            offset = 0 if style == "legacy" else (width - face.getlength(word)) / 2
            draw.text((x + offset, baselines[k]), word,
                      font=face, fill=WHITE if i == active else GRAY,
                      anchor="ls")
            x += width + gap
    shadow = Image.new("RGBA", layer.size)
    shadow.putalpha(layer.getchannel("A").filter(ImageFilter.GaussianBlur(3)))
    shadow.alpha_composite(layer)
    return shadow


def caption_position(layer, y=None, style="legacy"):
    preset = caption_style(style)
    left, top, right, bottom = preset["safe_box"]
    x = round(preset["center"][0] - layer.width / 2)
    if y is None:
        y = CAPTION_Y if style == "legacy" else preset["center"][1] - layer.height / 2
    if (not math.isfinite(y) or not left <= x <= right - layer.width
            or not top <= round(y) <= bottom - layer.height):
        raise ValueError(f"Sous-titres hors zone {style} : x={x}, y={y}, "
                         f"dimensions={layer.size}, zone={preset['safe_box']}.")
    return x, round(y)


@functools.lru_cache(maxsize=12)
def caption_backdrop(width, height):
    # Only used over busy, pale pages: feathered locally inside the safe box.
    yy, xx = np.mgrid[0:height, 0:width]
    dx = np.minimum(xx, width-1-xx) / 32
    dy = np.minimum(yy, height-1-yy) / 18
    alpha = (np.clip(np.minimum(dx,dy),0,1) * 172).astype(np.uint8)
    data = np.zeros((height,width,4),np.uint8)
    data[:,:,:3] = INK
    data[:,:,3] = alpha
    return Image.fromarray(data)


def captions(image, t, groups, y=None, style="legacy", mode="group"):
    index = bisect.bisect_right([g["start"] for g in groups], t) - 1
    if index < 0 or t >= groups[index]["end"]:
        return
    group = groups[index]
    active = bisect.bisect_right([w["start"] for w in group["words"]], t) - 1
    if active < 0:
        return
    layer = caption_card(tuple(w["word"] for w in group["words"]), active, style, mode)
    position = caption_position(layer, group.get("y", y), style)
    if group.get("backdrop"):
        background = caption_backdrop(*layer.size)
        image.paste(background, position, background)
    image.paste(layer, position, layer)
