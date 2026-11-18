"""Edit this scene compositor for the subject of each new film."""
import math
from PIL import Image, ImageDraw
import motion as m


def node_asset(node, media, t, at):
    if node.get("type") == "coins":
        return m.coins(node.get("count", 5))
    if node.get("path"):
        source = media.frame(node["path"], node.get("in", 0) + max(0, t - at),
                             node.get("center", [.5, .5]))
        return m.card(source, node.get("width", 290), node.get("height", 430))
    layer = Image.new("RGBA", (220, 260))
    draw = ImageDraw.Draw(layer)
    draw.ellipse((73, 30, 147, 104), fill=m.WHITE)
    draw.rounded_rectangle((42, 125, 178, 228), 45, fill=(212, 224, 252))
    return layer


def document_chain(t, host, scene, media):
    start = scene["start"]
    shrink_at = scene["shrink_at"]
    second_at, last_at = scene["second_at"], scene["last_at"]
    shrink = m.smooth((t - shrink_at) / .4)
    layout = m.smooth((t - shrink_at - .14) / .26)
    entry = m.ease((t - start) / .28)
    frame = m.stage(t)
    # Presenter composition is applied centrally by render.frame.
    orbit_alpha = 1 - m.smooth((t - shrink_at) / .28)
    if orbit_alpha > 0:
        orbit = Image.new("RGBA", (1080, 1920))
        draw = ImageDraw.Draw(orbit)
        for radius in (405, 332):
            draw.ellipse((540 - radius, 850 - radius, 540 + radius, 850 + radius),
                         outline=(39, 48, 80), width=2)
        for angle in (0, 120, 240):
            a = math.radians(angle + t * 14)
            x, y = 540 + 405 * math.cos(a), 850 + 405 * math.sin(a)
            draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=m.BLUE)
        m.put(frame, orbit, (540, 960), opacity=orbit_alpha)
    focus1 = m.smooth((t - second_at + .07) / .58)
    focus2 = m.smooth((t - last_at + .08) / .45)
    camera = m.mix(m.mix(430, 1060, focus1), 1470, focus2)
    scale = m.mix(m.mix(1.32, 1.02, focus1), .92, focus2)
    world = Image.new("RGBA", (2300, 1000))
    nodes = scene["nodes"]
    labels = []
    for j, (x, at, left, right) in enumerate(
            [(1080, second_at, 594, 900), (1750, last_at, 1240, 1570)], start=1):
        reveal = m.ease((t - at) / .26)
        if reveal <= 0:
            continue
        m.connector(world, (left, 470), (right, 470), m.ease((t - at) / .5))
        m.put(world, node_asset(nodes[j], media, t, at), (x, 450),
              .85 + .15 * reveal, reveal)
        if nodes[j].get("label"):
            labels.append((nodes[j]["label"], x, reveal))
        for k in range(3):
            q = (t - at - .1 - k * .09) / .42
            if 0 < q < 1:
                px = m.mix(left, right, m.ease(q))
                ImageDraw.Draw(world).ellipse((px - 7, 463, px + 7, 477), fill=m.WHITE)
    if nodes[0].get("label"):
        labels.append((nodes[0]["label"], 430, layout))
    vw, vh = 1080 / scale, 850 / scale
    view = world.transform((1080, 850), Image.Transform.EXTENT,
                           (camera - vw / 2, 410 - vh / 2, camera + vw / 2, 410 + vh / 2),
                           resample=Image.Resampling.BICUBIC)
    frame.paste(view, (0, 215), view)
    # Place text after the camera transform so readable labels cannot be
    # carried underneath platform controls by the world-space animation.
    for text, world_x, opacity in labels:
        screen_x = 540 + (world_x - camera) * scale
        visibility = m.clamp(screen_x / 180) * m.clamp((1080 - screen_x) / 180)
        if visibility <= 0:
            continue
        layer = m.label(text)
        layer = layer.resize((round(layer.width * scale), round(layer.height * scale)),
                             Image.Resampling.LANCZOS)
        m.put_safe_text(frame, layer, (screen_x, 640 + (190 - 410) * scale),
                        opacity=opacity * visibility)
    document = scene.get("document", {})
    stamp = document.get("stamp", "") if t >= scene["stamp_at"] else ""
    paper = m.document(document.get("title", "DOCUMENT"),
                       document.get("subtitle", ""), stamp)
    x = m.mix(540, 540 + (430 - camera) * scale, shrink)
    y = m.mix(690 + 60 * (1 - entry), 640 + 40 * scale, shrink)
    size = m.mix(.78 + .06 * entry, .58 * scale, shrink)
    angle = m.mix(-6 + math.sin((t - start) * 1.1) * 2, 0, shrink)
    m.put(frame, paper, (x, y), size, entry, angle)
    return frame, scene.get("caption_y", m.CAPTION_Y)


def relation(t, host, scene, media):
    frame = m.stage(t)
    second_at = scene.get("second_at", scene["start"] + .6)
    for j, (x, at) in enumerate(((330, scene["start"]), (750, second_at))):
        reveal = m.ease((t - at) / .3)
        if reveal <= 0:
            continue
        node = scene["nodes"][j]
        m.put(frame, node_asset(node, media, t, at), (x, 575), .82 + .18 * reveal, reveal)
        if node.get("label"):
            m.put_safe_text(frame, m.label(node["label"], 28), (x, 880), opacity=reveal)
    m.connector(frame, (500, 575), (580, 575), m.ease((t - second_at + .2) / .45))
    return frame, scene.get("caption_y", m.CAPTION_Y)


def compose(t, host, scene, media):
    kind = scene.get("type", "host")
    if kind == "document_chain":
        return document_chain(t, host, scene, media)
    if kind == "relation":
        return relation(t, host, scene, media)
    if kind == "broll":
        source = media.frame(scene["path"], scene.get("in", 0) + t - scene["start"],
                             scene.get("center", [.5, .5]))
        image = m.fit(source, (1080, 1920), scene.get("center", [.5, .5]))
        return (m.shade(image) if scene.get("shade", True) else image), scene.get("caption_y", m.CAPTION_Y)
    frame = host
    zooms = scene.get("zoom", [1, 1])
    progress = m.clamp((t - scene.get("start", 0)) /
                       max(.001, scene.get("end", 1) - scene.get("start", 0)))
    zoom = m.mix(zooms[0], zooms[-1], progress)
    if zoom > 1:
        width, height = round(1080 / zoom), round(1920 / zoom)
        cx, cy = 540, 960
        frame = host.crop((cx - width // 2, cy - height // 2,
                           cx + width // 2, cy + height // 2)).resize(
                               (1080, 1920), Image.Resampling.LANCZOS)
    return m.shade(frame), scene.get("caption_y", m.CAPTION_Y)
