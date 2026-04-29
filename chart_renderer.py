from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

from i18n import t
from logic import PatternData
from olympus_convert import dmc_to_olympus

CELL_SIZE = 24
MARGIN_LEFT = 50
MARGIN_TOP = 50
MARGIN_RIGHT = 20
MARGIN_BOTTOM = 20
BOLD_INTERVAL = 10
THIN_LINE_COLOR = (200, 200, 200)
BOLD_LINE_COLOR = (60, 60, 60)
BG_COLOR = (255, 255, 255)


def _get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/msgothic.ttc",
        "C:/Windows/Fonts/meiryo.ttc",
        "C:/Windows/Fonts/YuGothR.ttc",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def render_chart(pattern: PatternData) -> Image.Image:
    w = pattern.width_stitches
    h = pattern.height_stitches
    canvas_w = MARGIN_LEFT + w * CELL_SIZE + MARGIN_RIGHT
    canvas_h = MARGIN_TOP + h * CELL_SIZE + MARGIN_BOTTOM

    img = Image.new("RGB", (canvas_w, canvas_h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    font_sym = _get_font(int(CELL_SIZE * 0.6))
    font_num = _get_font(11)

    for row in range(h):
        for col in range(w):
            color_idx = int(pattern.grid[row, col])
            x0 = MARGIN_LEFT + col * CELL_SIZE
            y0 = MARGIN_TOP + row * CELL_SIZE
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE

            if color_idx < 0:
                draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255))
                continue

            dmc = pattern.colors[color_idx]
            draw.rectangle([x0, y0, x1, y1], fill=dmc.rgb)

            sym = pattern.symbols[color_idx]
            brightness = (dmc.r * 299 + dmc.g * 587 + dmc.b * 114) / 1000
            text_color = (255, 255, 255) if brightness < 128 else (0, 0, 0)
            bbox = draw.textbbox((0, 0), sym, font=font_sym)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            tx = x0 + (CELL_SIZE - tw) // 2 - bbox[0]
            ty = y0 + (CELL_SIZE - th) // 2 - bbox[1]
            draw.text((tx, ty), sym, fill=text_color, font=font_sym)

    grid_x0 = MARGIN_LEFT
    grid_y0 = MARGIN_TOP
    grid_x1 = MARGIN_LEFT + w * CELL_SIZE
    grid_y1 = MARGIN_TOP + h * CELL_SIZE

    for col in range(w + 1):
        x = grid_x0 + col * CELL_SIZE
        is_bold = col % BOLD_INTERVAL == 0
        color = BOLD_LINE_COLOR if is_bold else THIN_LINE_COLOR
        width = 2 if is_bold else 1
        draw.line([(x, grid_y0), (x, grid_y1)], fill=color, width=width)

    for row in range(h + 1):
        y = grid_y0 + row * CELL_SIZE
        is_bold = row % BOLD_INTERVAL == 0
        color = BOLD_LINE_COLOR if is_bold else THIN_LINE_COLOR
        width = 2 if is_bold else 1
        draw.line([(grid_x0, y), (grid_x1, y)], fill=color, width=width)

    for col in range(0, w + 1, BOLD_INTERVAL):
        if col == 0:
            continue
        x = grid_x0 + col * CELL_SIZE
        label = str(col)
        bbox = draw.textbbox((0, 0), label, font=font_num)
        tw = bbox[2] - bbox[0]
        draw.text((x - tw // 2, grid_y0 - 16), label, fill=(0, 0, 0), font=font_num)
        draw.text((x - tw // 2, grid_y1 + 4), label, fill=(0, 0, 0), font=font_num)

    for row in range(0, h + 1, BOLD_INTERVAL):
        if row == 0:
            continue
        y = grid_y0 + row * CELL_SIZE
        label = str(row)
        bbox = draw.textbbox((0, 0), label, font=font_num)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((grid_x0 - tw - 6, y - th // 2), label, fill=(0, 0, 0), font=font_num)
        draw.text((grid_x1 + 6, y - th // 2), label, fill=(0, 0, 0), font=font_num)

    _draw_center_arrows(draw, w, h, grid_x0, grid_y0, grid_x1, grid_y1)

    return img


def _draw_center_arrows(
    draw: ImageDraw.ImageDraw,
    w: int, h: int,
    grid_x0: int, grid_y0: int,
    grid_x1: int, grid_y1: int,
) -> None:
    cx = grid_x0 + (w * CELL_SIZE) // 2
    cy = grid_y0 + (h * CELL_SIZE) // 2
    arrow_size = 6
    color = (200, 0, 0)

    draw.polygon(
        [(cx, grid_y0 - 2), (cx - arrow_size, grid_y0 - arrow_size - 2),
         (cx + arrow_size, grid_y0 - arrow_size - 2)],
        fill=color,
    )
    draw.polygon(
        [(cx, grid_y1 + 2), (cx - arrow_size, grid_y1 + arrow_size + 2),
         (cx + arrow_size, grid_y1 + arrow_size + 2)],
        fill=color,
    )
    draw.polygon(
        [(grid_x0 - 2, cy), (grid_x0 - arrow_size - 2, cy - arrow_size),
         (grid_x0 - arrow_size - 2, cy + arrow_size)],
        fill=color,
    )
    draw.polygon(
        [(grid_x1 + 2, cy), (grid_x1 + arrow_size + 2, cy - arrow_size),
         (grid_x1 + arrow_size + 2, cy + arrow_size)],
        fill=color,
    )


def render_legend(
    pattern: PatternData, thread_system: str = "both", lang: str = "ja"
) -> Image.Image:
    n = len(pattern.colors)
    row_h = 30
    header_h = 60
    legend_h = header_h + n * row_h + 20
    legend_w = 860

    img = Image.new("RGB", (legend_w, legend_h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = _get_font(13)
    font_title = _get_font(15)

    strand_text = t("header_strand", lang).format(n=pattern.strand_count)
    draw.text((10, 8), strand_text, fill=(0, 0, 0), font=font_title)

    y = header_h - 20
    if thread_system == "olympus":
        headers = [
            t("header_symbol", lang),
            t("header_oly", lang),
            t("header_color_name", lang),
            t("header_thread_amount", lang),
        ]
        col_x = [10, 50, 350, 700]
    elif thread_system == "both":
        headers = [
            t("header_symbol", lang),
            t("header_dmc", lang),
            t("header_oly", lang),
            t("header_color_name", lang),
            t("header_thread_amount", lang),
        ]
        col_x = [10, 50, 100, 360, 700]
    else:
        headers = [
            t("header_symbol", lang),
            t("header_dmc", lang),
            t("header_color_name", lang),
            t("header_thread_amount", lang),
        ]
        col_x = [10, 50, 100, 600]

    for i, hdr in enumerate(headers):
        if i < len(col_x):
            draw.text((col_x[i], y), hdr, fill=(80, 80, 80), font=font)
    y += row_h

    draw.line([(10, y - 4), (legend_w - 10, y - 4)], fill=(180, 180, 180), width=1)

    substitute_label = t("substitute_mark", lang)

    for i, dmc in enumerate(pattern.colors):
        sym = pattern.symbols[i]
        length = pattern.thread_lengths[i]
        is_sub = pattern.substitutes[i] if i < len(pattern.substitutes) else False

        draw.rectangle(
            [col_x[0], y + 2, col_x[0] + 20, y + row_h - 4],
            fill=dmc.rgb, outline=(0, 0, 0),
        )
        bbox = draw.textbbox((0, 0), sym, font=font)
        sw_box = bbox[2] - bbox[0]
        draw.text(
            (col_x[0] + 10 - sw_box // 2, y + 4), sym,
            fill=(255, 255, 255) if sum(dmc.rgb) < 384 else (0, 0, 0),
            font=font,
        )

        ci = 1
        if thread_system == "olympus":
            entry = dmc_to_olympus(dmc.dmc)
            if entry is None:
                oly_text = "-"
            elif entry.name_ja and lang == "ja":
                oly_text = f"{entry.number}  {entry.name_ja}"
            else:
                oly_text = entry.number
            if is_sub:
                oly_text = f"{oly_text}  ({substitute_label})"
            draw.text(
                (col_x[ci], y + 4), oly_text,
                fill=(180, 80, 0) if is_sub else (0, 0, 0),
                font=font,
            )
            ci += 1
        else:
            draw.text((col_x[ci], y + 4), dmc.dmc, fill=(0, 0, 0), font=font)
            ci += 1
            if thread_system == "both":
                entry = dmc_to_olympus(dmc.dmc)
                if entry is None:
                    oly_text = "-"
                elif entry.name_ja and lang == "ja":
                    oly_text = f"{entry.number}  {entry.name_ja}"
                else:
                    oly_text = entry.number
                draw.text(
                    (col_x[ci], y + 4), oly_text,
                    fill=(0, 0, 0), font=font,
                )
                ci += 1

        draw.text((col_x[ci], y + 4), dmc.name, fill=(0, 0, 0), font=font)
        ci += 1

        length_str = f"{length:.1f}m" if length < 10 else f"{length:.0f}m"
        draw.text((col_x[ci], y + 4), length_str, fill=(0, 0, 0), font=font)

        y += row_h

    return img


def render_info(pattern: PatternData, lang: str = "ja") -> Image.Image:
    lines = [
        f"{t('info_title', lang)}: {pattern.title}",
        f"{t('info_fabric', lang)}: {pattern.fabric_count}-count {t('info_aida', lang)}",
        f"{t('info_stitches', lang)}: {pattern.width_stitches} × {pattern.height_stitches}",
        f"{t('info_finished', lang)}: {pattern.finished_size_cm[0]} × {pattern.finished_size_cm[1]} cm",
        f"{t('info_colors', lang)}: {len(pattern.colors)}{t('color_count_unit', lang)}",
    ]
    line_h = 24
    img_h = len(lines) * line_h + 20
    img = Image.new("RGB", (400, img_h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = _get_font(13)

    for i, line in enumerate(lines):
        draw.text((10, 10 + i * line_h), line, fill=(0, 0, 0), font=font)

    return img


def render_preview(pattern: PatternData, scale: int = 4) -> Image.Image:
    h, w = pattern.grid.shape
    img = Image.new("RGB", (w, h), (255, 255, 255))
    pixels = img.load()
    for row in range(h):
        for col in range(w):
            color_idx = int(pattern.grid[row, col])
            if color_idx < 0:
                pixels[col, row] = (255, 255, 255)
            else:
                pixels[col, row] = pattern.colors[color_idx].rgb
    return img.resize((w * scale, h * scale), Image.NEAREST)
