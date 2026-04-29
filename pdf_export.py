from __future__ import annotations

from io import BytesIO

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from logic import PatternData


def generate_pdf(
    pattern: PatternData,
    chart_image: Image.Image,
    legend_image: Image.Image,
    info_image: Image.Image,
    preview_image: Image.Image,
) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    page_w, page_h = A4

    _draw_title_page(c, pattern, preview_image, legend_image, info_image, page_w, page_h)
    _draw_chart_pages(c, chart_image, page_w, page_h)

    c.save()
    buf.seek(0)
    return buf.read()


def _pil_to_reportlab(img: Image.Image) -> BytesIO:
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def _draw_title_page(
    c: canvas.Canvas,
    pattern: PatternData,
    preview: Image.Image,
    legend: Image.Image,
    info: Image.Image,
    page_w: float,
    page_h: float,
) -> None:
    from reportlab.lib.utils import ImageReader

    y = page_h - 30 * mm

    font_candidates = [
        "C:/Windows/Fonts/msgothic.ttc",
        "C:/Windows/Fonts/meiryo.ttc",
    ]
    font_registered = False
    for fpath in font_candidates:
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            pdfmetrics.registerFont(TTFont("JapaneseFont", fpath))
            c.setFont("JapaneseFont", 18)
            font_registered = True
            break
        except Exception:
            continue

    if not font_registered:
        c.setFont("Helvetica-Bold", 18)

    c.drawCentredString(page_w / 2, y, pattern.title)
    y -= 10 * mm

    if font_registered:
        c.setFont("JapaneseFont", 10)
    else:
        c.setFont("Helvetica", 10)
    c.drawCentredString(page_w / 2, y, "クロス・ステッチ図案")
    y -= 15 * mm

    preview_buf = _pil_to_reportlab(preview)
    pw, ph = preview.size
    max_preview_w = 140 * mm
    max_preview_h = 100 * mm
    scale = min(max_preview_w / pw, max_preview_h / ph)
    draw_w = pw * scale
    draw_h = ph * scale
    x = (page_w - draw_w) / 2
    c.drawImage(
        ImageReader(preview_buf), x, y - draw_h,
        width=draw_w, height=draw_h,
    )
    y -= draw_h + 10 * mm

    info_buf = _pil_to_reportlab(info)
    iw, ih = info.size
    info_scale = min(180 * mm / iw, 40 * mm / ih)
    info_draw_w = iw * info_scale
    info_draw_h = ih * info_scale
    c.drawImage(
        ImageReader(info_buf), 20 * mm, y - info_draw_h,
        width=info_draw_w, height=info_draw_h,
    )
    y -= info_draw_h + 10 * mm

    legend_buf = _pil_to_reportlab(legend)
    lw, lh = legend.size
    legend_scale = min(170 * mm / lw, (y - 20 * mm) / lh)
    legend_draw_w = lw * legend_scale
    legend_draw_h = lh * legend_scale
    c.drawImage(
        ImageReader(legend_buf), 20 * mm, y - legend_draw_h,
        width=legend_draw_w, height=legend_draw_h,
    )

    c.showPage()


def _draw_chart_pages(
    c: canvas.Canvas,
    chart_image: Image.Image,
    page_w: float,
    page_h: float,
) -> None:
    from reportlab.lib.utils import ImageReader

    margin = 15 * mm
    usable_w = page_w - 2 * margin
    usable_h = page_h - 2 * margin

    cw, ch = chart_image.size

    single_scale = min(usable_w / cw, usable_h / ch)
    if single_scale * cw >= cw * 0.3:
        draw_w = cw * single_scale
        draw_h = ch * single_scale
        x = (page_w - draw_w) / 2
        y = (page_h - draw_h) / 2
        chart_buf = _pil_to_reportlab(chart_image)
        c.drawImage(
            ImageReader(chart_buf), x, y,
            width=draw_w, height=draw_h,
        )
        c.showPage()
        return

    tile_w_px = int(usable_w / single_scale) if single_scale > 0 else cw
    tile_h_px = int(usable_h / single_scale) if single_scale > 0 else ch
    overlap = 50

    col_count = max(1, (cw + tile_w_px - overlap - 1) // (tile_w_px - overlap))
    row_count = max(1, (ch + tile_h_px - overlap - 1) // (tile_h_px - overlap))

    for tr in range(row_count):
        for tc in range(col_count):
            x0 = tc * (tile_w_px - overlap)
            y0 = tr * (tile_h_px - overlap)
            x1 = min(x0 + tile_w_px, cw)
            y1 = min(y0 + tile_h_px, ch)

            tile = chart_image.crop((x0, y0, x1, y1))
            tw, th = tile.size
            tile_scale = min(usable_w / tw, usable_h / th)
            draw_w = tw * tile_scale
            draw_h = th * tile_scale

            tile_buf = _pil_to_reportlab(tile)
            cx = (page_w - draw_w) / 2
            cy = (page_h - draw_h) / 2
            c.drawImage(
                ImageReader(tile_buf), cx, cy,
                width=draw_w, height=draw_h,
            )
            c.showPage()
