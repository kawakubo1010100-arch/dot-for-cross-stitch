from __future__ import annotations

import hashlib
import io
import urllib.parse

import numpy as np
import streamlit as st
from PIL import Image
from PIL import ImageDraw, ImageFont
from streamlit_image_coordinates import streamlit_image_coordinates

import background_editor as bg
from chart_renderer import render_chart, render_info, render_legend, render_preview, _get_font
from i18n import detect_browser_language, t
from logic import SourceData, generate_pattern, prepare_source
from pdf_export import generate_pdf

HISTORY_LIMIT = 30

SECRET_CODE = "stitch-pro-2026"
WIDTH_FREE = 30
COLORS_FREE = 4
NOTE_URL_JA = "https://note.com/1010100_nohunohu/n/n671e09605d99"
GUMROAD_URL_EN = "https://nohunohu.gumroad.com/l/aguat"
APP_SHARE_URL = "https://dot-cross-stitch.streamlit.app/"


def _purchase_url(lang: str) -> str:
    return GUMROAD_URL_EN if lang == "en" else NOTE_URL_JA


def _check_pro() -> bool:
    if st.session_state.get("is_pro"):
        return True
    code = st.query_params.get("key", "")
    if code == SECRET_CODE:
        st.session_state.is_pro = True
        return True
    return False


def _is_within_free_limit(
    slider_w: int | None, slider_h: int | None, max_colors: int
) -> bool:
    if max_colors > COLORS_FREE:
        return False
    if slider_w is not None and slider_w > WIDTH_FREE:
        return False
    if slider_h is not None and slider_h > WIDTH_FREE:
        return False
    return True


def _add_watermark(img: Image.Image, text: str = "サンプル") -> Image.Image:
    base = img.convert("RGBA")
    overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    font_size = max(70, int(min(base.size) * 0.11))
    font = _get_font(font_size)
    step_x = int(font_size * 4.2)
    step_y = int(font_size * 2.5)
    for y in range(-step_y * 2, base.height + step_y * 2, step_y):
        for x in range(-step_x * 2, base.width + step_x * 2, step_x):
            draw.text(
                (x, y), text,
                fill=(180, 10, 10, 220),
                font=font,
                stroke_width=2,
                stroke_fill=(120, 0, 0, 220),
            )
    overlay = overlay.rotate(28, expand=False)
    out = Image.alpha_composite(base, overlay)
    return out.convert("RGB")


TUTORIAL_TOTAL_STEPS = 6


def _init_state() -> None:
    if "lang" not in st.session_state:
        st.session_state.lang = detect_browser_language()
    if "show_tutorial" not in st.session_state:
        seen = st.query_params.get("seen", "")
        st.session_state.show_tutorial = (seen != "1")
    if "tutorial_step" not in st.session_state:
        st.session_state.tutorial_step = 0
    if "source" not in st.session_state:
        st.session_state.source = None
    if "source_hash" not in st.session_state:
        st.session_state.source_hash = None
    if "history" not in st.session_state:
        st.session_state.history = []
    if "history_idx" not in st.session_state:
        st.session_state.history_idx = -1
    if "pattern" not in st.session_state:
        st.session_state.pattern = None
    if "widget_seq" not in st.session_state:
        st.session_state.widget_seq = 0
    if "last_click_sig" not in st.session_state:
        st.session_state.last_click_sig = None
    if "last_drag_sig" not in st.session_state:
        st.session_state.last_drag_sig = None


def _push_history(mask: np.ndarray) -> None:
    h = st.session_state.history
    idx = st.session_state.history_idx
    h = h[: idx + 1]
    h.append(mask.copy())
    if len(h) > HISTORY_LIMIT:
        h = h[-HISTORY_LIMIT:]
    st.session_state.history = h
    st.session_state.history_idx = len(h) - 1


def _current_mask() -> np.ndarray | None:
    h = st.session_state.history
    idx = st.session_state.history_idx
    if 0 <= idx < len(h):
        return h[idx]
    return None


def _apply_mask_change(new_mask: np.ndarray) -> None:
    _push_history(new_mask)
    if st.session_state.source is not None:
        st.session_state.source.mask = new_mask


def _on_new_image(image_bytes: bytes) -> None:
    src = prepare_source(image_bytes)
    st.session_state.source = src
    st.session_state.source_hash = hashlib.md5(image_bytes).hexdigest()
    st.session_state.history = [src.mask.copy()]
    st.session_state.history_idx = 0
    st.session_state.pattern = None
    st.session_state.widget_seq += 1
    st.session_state.last_click_sig = None
    st.session_state.last_drag_sig = None
    st.session_state.last_imported_mask = None


def _render_tutorial(lang: str) -> None:
    if not st.session_state.show_tutorial:
        return
    step = st.session_state.tutorial_step

    def _close():
        st.session_state.show_tutorial = False
        st.session_state.tutorial_step = 0
        st.query_params["seen"] = "1"

    with st.container(border=True):
        top_l, top_r = st.columns([5, 1])
        with top_l:
            st.markdown(
                f"### 📖 {t('tutorial_title', lang)} "
                f"（{step + 1} / {TUTORIAL_TOTAL_STEPS}）"
            )
        with top_r:
            if st.button(t("tutorial_close", lang), key=f"tut_close_{step}",
                         use_container_width=True):
                _close()
                st.rerun()

        st.markdown(t(f"tutorial_step_{step + 1}", lang))

        nav_l, nav_c, nav_r = st.columns([1, 3, 1])
        with nav_l:
            if step > 0:
                if st.button(t("tutorial_prev", lang), key=f"tut_prev_{step}",
                             use_container_width=True):
                    st.session_state.tutorial_step -= 1
                    st.rerun()
        with nav_r:
            if step < TUTORIAL_TOTAL_STEPS - 1:
                if st.button(t("tutorial_next", lang), key=f"tut_next_{step}",
                             use_container_width=True, type="primary"):
                    st.session_state.tutorial_step += 1
                    st.rerun()
            else:
                if st.button(t("tutorial_done", lang), key=f"tut_done_{step}",
                             use_container_width=True, type="primary"):
                    _close()
                    st.rerun()


def _render_sidebar() -> dict:
    lang = st.session_state.lang
    is_pro = _check_pro()

    with st.sidebar:
        if st.button(
            t("tutorial_button", lang), use_container_width=True,
            key="tutorial_open_btn",
        ):
            st.session_state.show_tutorial = True
            st.session_state.tutorial_step = 0
            if "seen" in st.query_params:
                del st.query_params["seen"]
            st.rerun()

        if is_pro:
            st.success(t("pro_active", lang))
        else:
            with st.expander(t("unlock_section", lang), expanded=False):
                st.markdown(t("unlock_intro", lang).format(url=_purchase_url(lang)))
                code = st.text_input(t("unlock_code_label", lang), type="password")
                if st.button(t("unlock_button", lang), use_container_width=True):
                    if code == SECRET_CODE:
                        st.session_state.is_pro = True
                        st.query_params["key"] = code
                        st.rerun()
                    else:
                        st.error(t("unlock_wrong", lang))

        st.caption(
            t("free_tier_summary", lang).format(w=WIDTH_FREE, c=COLORS_FREE)
        )

        st.header(t("settings", lang))

        new_lang = st.selectbox(
            t("language", lang),
            ["ja", "en"],
            index=["ja", "en"].index(lang),
            format_func=lambda x: {"ja": "日本語", "en": "English"}[x],
        )
        if new_lang != lang:
            st.session_state.lang = new_lang
            st.rerun()

        uploaded = st.file_uploader(
            t("upload", lang), type=["jpg", "jpeg", "png", "bmp", "webp"]
        )
        if uploaded is not None:
            image_bytes = uploaded.read()
            new_hash = hashlib.md5(image_bytes).hexdigest()
            if new_hash != st.session_state.source_hash:
                _on_new_image(image_bytes)

        title = st.text_input(t("pattern_title", lang), value=t("default_title", lang))

        st.subheader(t("size_settings", lang))
        size_mode = st.radio(
            t("size_mode", lang),
            ["width", "height", "both"],
            format_func=lambda x: {
                "width": t("size_mode_width", lang),
                "height": t("size_mode_height", lang),
                "both": t("size_mode_both", lang),
            }[x],
        )

        width_stitches: int | None = None
        height_stitches: int | None = None
        if size_mode == "width":
            width_stitches = st.slider(t("width_stitches", lang), 20, 300, 30)
        elif size_mode == "height":
            height_stitches = st.slider(t("height_stitches", lang), 20, 300, 30)
        else:
            width_stitches = st.slider(t("width_stitches", lang), 20, 300, 30)
            height_stitches = st.slider(t("height_stitches", lang), 20, 300, 30)

        fabric_count = st.selectbox(
            t("fabric_count", lang),
            [11, 14, 16, 18, 22],
            index=1,
            format_func=lambda x: t("fabric_format", lang).format(n=x),
        )

        src = st.session_state.source
        proj_w, proj_h = None, None
        if src is not None:
            sh, sw = src.shape
            aspect = sw / sh
            cw = width_stitches
            ch = height_stitches
            if cw and not ch:
                ch = max(1, round(cw / aspect))
            elif ch and not cw:
                cw = max(1, round(ch * aspect))
            proj_w, proj_h = cw, ch
            if cw and ch:
                w_cm = cw / fabric_count * 2.54
                h_cm = ch / fabric_count * 2.54
                st.info(
                    f"📐 {t('info_canvas', lang)}: "
                    f"**{w_cm:.1f} × {h_cm:.1f} cm**  "
                    f"({cw} × {ch})"
                )

        if not is_pro and (
            (width_stitches and width_stitches > WIDTH_FREE)
            or (height_stitches and height_stitches > WIDTH_FREE)
        ):
            st.warning(t("over_size_limit", lang).format(w=WIDTH_FREE))

        max_colors = st.slider(t("max_colors", lang), 2, 30, 4)
        if not is_pro and max_colors > COLORS_FREE:
            st.warning(t("over_color_limit", lang).format(c=COLORS_FREE))
        strand_count = st.selectbox(t("strand_count", lang), [2, 3, 4], index=1)
        thread_system = st.selectbox(
            t("thread_system", lang),
            ["both", "dmc", "olympus"],
            format_func=lambda x: {
                "both": t("thread_both", lang),
                "dmc": t("thread_dmc", lang),
                "olympus": t("thread_olympus", lang),
            }[x],
        )

    return {
        "lang": lang,
        "is_pro": is_pro,
        "title": title,
        "width_stitches": width_stitches,
        "height_stitches": height_stitches,
        "fabric_count": fabric_count,
        "max_colors": max_colors,
        "strand_count": strand_count,
        "thread_system": thread_system,
    }


def _render_bg_editor_tab(params: dict) -> None:
    lang = params["lang"]
    src: SourceData | None = st.session_state.source

    if src is None:
        st.info(t("no_source", lang))
        return

    st.caption(t("bg_editor_help", lang))

    sh, sw = src.shape
    mask = _current_mask()
    if mask is None:
        mask = np.zeros((sh, sw), dtype=bool)

    col_l, col_r = st.columns([3, 1])

    with col_r:
        st.markdown(f"**{t('source_size', lang)}**: {sw} × {sh}")
        masked_count = int(mask.sum())
        total = sh * sw
        st.markdown(
            f"**{t('masked_pixels', lang)}**: {masked_count} / {total} "
            f"({masked_count / total * 100:.1f}%)"
        )
        st.markdown(
            f"**{t('history_position', lang)}**: "
            f"{st.session_state.history_idx + 1} / {len(st.session_state.history)}"
        )

        scale = st.slider(t("view_scale", lang), 1, 6, 3)

        tool_mode = st.radio(
            t("tool_mode", lang),
            ["flood", "pixel", "rect"],
            format_func=lambda x: {
                "flood": t("tool_flood", lang),
                "pixel": t("tool_pixel", lang),
                "rect": t("tool_rect", lang),
            }[x],
        )

        click_mode = st.radio(
            t("click_mode", lang),
            ["add", "remove"],
            format_func=lambda x: {
                "add": t("click_add", lang),
                "remove": t("click_remove", lang),
            }[x],
            help=t("click_mode_help", lang),
            horizontal=True,
        )

        prev_tool = st.session_state.get("prev_tool_mode")
        if prev_tool != tool_mode:
            st.session_state.prev_tool_mode = tool_mode
            st.session_state.widget_seq += 1
            st.session_state.last_click_sig = None
            st.session_state.last_drag_sig = None

        tolerance = st.slider(
            t("tolerance", lang), 0, 80, 10,
            help=t("tolerance_help", lang),
        )

        st.markdown("---")

        def _bump():
            st.session_state.widget_seq += 1
            st.session_state.last_click_sig = None
            st.session_state.last_drag_sig = None

        c1, c2 = st.columns(2)
        with c1:
            if st.button(t("undo", lang), use_container_width=True):
                if st.session_state.history_idx > 0:
                    st.session_state.history_idx -= 1
                    src.mask = _current_mask().copy()
                    _bump()
                    st.rerun()
        with c2:
            if st.button(t("redo", lang), use_container_width=True):
                if st.session_state.history_idx < len(st.session_state.history) - 1:
                    st.session_state.history_idx += 1
                    src.mask = _current_mask().copy()
                    _bump()
                    st.rerun()

        if st.button(t("auto_edge", lang), use_container_width=True,
                     help=t("auto_edge_help", lang)):
            new_mask = bg.auto_mask_edges(src.pixels, mask, tolerance=max(tolerance, 10))
            _apply_mask_change(new_mask)
            _bump()
            st.rerun()

        if st.button(t("reset_mask", lang), use_container_width=True):
            new_mask = np.zeros((sh, sw), dtype=bool)
            _apply_mask_change(new_mask)
            _bump()
            st.rerun()

        st.markdown("---")

        png_bytes = bg.mask_to_png_bytes(mask)
        st.download_button(
            t("export_mask", lang),
            data=png_bytes,
            file_name="mask.png",
            mime="image/png",
            use_container_width=True,
        )

        imported = st.file_uploader(
            t("import_mask", lang), type=["png"], key="mask_upload"
        )
        if imported is not None:
            file_id = (imported.name, imported.size)
            if st.session_state.get("last_imported_mask") != file_id:
                st.session_state.last_imported_mask = file_id
                new_mask = bg.png_bytes_to_mask(imported.read(), (sh, sw))
                if new_mask is not None:
                    _apply_mask_change(new_mask)
                    _bump()
                    st.rerun()

    with col_l:
        view_img = bg.render_editor_view(src.pixels, mask, scale=scale)

        widget_key = (
            f"editor_{tool_mode}_{sh}x{sw}_{scale}_{st.session_state.widget_seq}"
        )

        if tool_mode == "rect":
            st.caption(t("rect_help", lang))
            result = streamlit_image_coordinates(
                view_img,
                key=widget_key,
                click_and_drag=True,
                image_format="JPEG",
                jpeg_quality=70,
            )
            if result is not None and all(
                k in result for k in ("x1", "y1", "x2", "y2")
            ):
                sig = (result["x1"], result["y1"], result["x2"], result["y2"])
                if (
                    sig != st.session_state.last_drag_sig
                    and result["x1"] != result["x2"]
                    and result["y1"] != result["y2"]
                ):
                    st.session_state.last_drag_sig = sig
                    x0 = max(0, min(sw, int(result["x1"]) // scale))
                    y0 = max(0, min(sh, int(result["y1"]) // scale))
                    x1 = max(0, min(sw, int(result["x2"]) // scale + 1))
                    y1 = max(0, min(sh, int(result["y2"]) // scale + 1))
                    new_mask = bg.apply_rect(
                        mask, x0, y0, x1, y1, value=(click_mode == "add")
                    )
                    _apply_mask_change(new_mask)
                    st.session_state.widget_seq += 1
                    st.rerun()
        else:
            clicked = streamlit_image_coordinates(
                view_img,
                key=widget_key,
                image_format="JPEG",
                jpeg_quality=70,
            )
            if clicked is not None:
                cx = max(0, min(sw - 1, int(clicked["x"]) // scale))
                cy = max(0, min(sh - 1, int(clicked["y"]) // scale))
                sig = (cx, cy)
                if sig != st.session_state.last_click_sig:
                    st.session_state.last_click_sig = sig
                    if tool_mode == "flood":
                        if click_mode == "add":
                            new_mask = bg.flood_fill_add(
                                src.pixels, mask, cx, cy, tolerance=tolerance
                            )
                        else:
                            new_mask = bg.flood_fill_remove(
                                src.pixels, mask, cx, cy, tolerance=tolerance
                            )
                    else:
                        new_mask = bg.set_pixel(
                            mask, cx, cy, value=(click_mode == "add")
                        )
                    _apply_mask_change(new_mask)
                    st.rerun()


def _render_pattern_tab(params: dict) -> None:
    lang = params["lang"]
    src: SourceData | None = st.session_state.source

    if src is None:
        st.info(t("no_source", lang))
        return

    mask = _current_mask()
    if mask is not None:
        src.mask = mask

    if st.button(
        t("regenerate_pattern", lang), type="primary", use_container_width=False
    ):
        with st.spinner(t("generating", lang)):
            pattern = generate_pattern(
                source=src,
                width_stitches=params["width_stitches"],
                height_stitches=params["height_stitches"],
                max_colors=params["max_colors"],
                fabric_count=params["fabric_count"],
                strand_count=params["strand_count"],
                title=params["title"],
                thread_system=params["thread_system"],
            )
            st.session_state.pattern = pattern

    pattern = st.session_state.pattern
    if pattern is None:
        st.info(t("first_generate", lang))
        return

    preview_img = render_preview(pattern)
    chart_img = render_chart(pattern)
    legend_img = render_legend(
        pattern, thread_system=params["thread_system"], lang=lang
    )
    info_img = render_info(pattern, lang=lang)

    is_pro = params["is_pro"]
    within_free = _is_within_free_limit(
        params["width_stitches"], params["height_stitches"], params["max_colors"]
    )
    can_export = is_pro or within_free
    show_watermark = not can_export

    chart_display = _add_watermark(chart_img) if show_watermark else chart_img

    if not can_export:
        st.info(t("preview_only_notice", lang).format(
            w=WIDTH_FREE, c=COLORS_FREE, url=_purchase_url(lang)
        ))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("preview_color", lang))
        st.image(preview_img)
    with col2:
        st.subheader(t("pattern_info", lang))
        canvas_cm = pattern.canvas_size_cm
        drawn_cm = pattern.drawn_size_cm
        drawn_w_st, drawn_h_st = pattern.drawn_bbox_stitches
        st.markdown(
            f"""
            - **{t('info_title', lang)}**: {pattern.title}
            - **{t('info_stitches', lang)}**: {pattern.width_stitches} × {pattern.height_stitches}
            - **{t('info_fabric', lang)}**: {pattern.fabric_count}-count {t('info_aida', lang)}
            - **{t('info_canvas', lang)}**: {canvas_cm[0]} × {canvas_cm[1]} cm
            - **{t('info_drawn', lang)}**: {drawn_cm[0]} × {drawn_cm[1]} cm  ({drawn_w_st} × {drawn_h_st})
            - **{t('info_colors', lang)}**: {len(pattern.colors)}{t('color_count_unit', lang)}
            - **{t('info_strand', lang)}**: {pattern.strand_count}{t('strand_unit', lang)}
            """
        )

    st.subheader(t("chart", lang))
    st.image(chart_display)

    st.subheader(t("legend", lang))
    st.image(legend_img)

    st.subheader(t("downloads", lang))
    d1, d2, d3 = st.columns(3)

    chart_for_dl = chart_display
    with d1:
        buf = io.BytesIO()
        chart_for_dl.save(buf, format="PNG")
        label = t("dl_chart_png", lang)
        if not can_export:
            label = f"{label}（{t('with_watermark', lang)}）"
        st.download_button(
            label, data=buf.getvalue(),
            file_name=f"{params['title']}_chart.png", mime="image/png",
            use_container_width=True,
        )

    with d2:
        buf = io.BytesIO()
        preview_img.save(buf, format="PNG")
        st.download_button(
            t("dl_preview_png", lang), data=buf.getvalue(),
            file_name=f"{params['title']}_preview.png", mime="image/png",
            use_container_width=True,
        )

    with d3:
        if can_export:
            pdf_bytes = generate_pdf(
                pattern, chart_img, legend_img, info_img, preview_img
            )
            st.download_button(
                t("dl_pdf", lang), data=pdf_bytes,
                file_name=f"{params['title']}.pdf", mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.button(
                f"🔒 {t('dl_pdf', lang)}", disabled=True,
                use_container_width=True,
                help=t("pdf_paid_only", lang),
            )

    st.subheader(t("share_section", lang))
    s1, s2 = st.columns([1, 3])
    with s1:
        canvas_cm = pattern.canvas_size_cm
        share_text = t("share_text", lang).format(
            fabric=pattern.fabric_count,
            w=pattern.width_stitches,
            h=pattern.height_stitches,
            cm_w=canvas_cm[0],
            cm_h=canvas_cm[1],
            n_colors=len(pattern.colors),
        )
        share_url_x = (
            "https://x.com/intent/tweet?"
            f"text={urllib.parse.quote(share_text)}&"
            f"url={urllib.parse.quote(APP_SHARE_URL)}&"
            f"hashtags={urllib.parse.quote('クロスステッチ図案メーカー')}"
        )
        st.link_button(
            t("share_to_x", lang), share_url_x, use_container_width=True
        )
    with s2:
        if can_export:
            st.caption(t("share_hint_pro", lang))
        else:
            st.caption(t("share_hint_free", lang))


def main() -> None:
    _init_state()
    lang = st.session_state.lang
    st.set_page_config(page_title=t("page_title", lang), layout="wide")
    st.title(t("title", lang))
    st.caption(t("caption", lang))

    params = _render_sidebar()
    _render_tutorial(lang)

    if st.session_state.source is None:
        st.info(t("info_message", lang))
        return

    tab_bg, tab_pat = st.tabs(
        [t("tab_bg_editor", lang), t("tab_pattern", lang)]
    )
    with tab_bg:
        _render_bg_editor_tab(params)
    with tab_pat:
        _render_pattern_tab(params)


main()
