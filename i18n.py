from __future__ import annotations

TRANSLATIONS: dict[str, dict[str, str]] = {
    "ja": {
        "page_title": "クロスステッチ図案メーカー",
        "title": "クロスステッチ図案メーカー",
        "caption": "画像をアップロードしてクロスステッチの図案に変換します",
        "settings": "設定",
        "language": "言語 / Language",
        "upload": "画像をアップロード",
        "pattern_title": "図案タイトル",
        "default_title": "クロスステッチ図案",
        "size_settings": "サイズ設定",
        "size_mode": "サイズ指定方法",
        "size_mode_width": "幅を指定（高さ自動）",
        "size_mode_height": "高さを指定（幅自動）",
        "size_mode_both": "両方指定",
        "width_stitches": "幅（ステッチ数）",
        "height_stitches": "高さ（ステッチ数）",
        "fabric_count": "布カウント",
        "fabric_format": "{n}カウント（1インチに{n}目）",
        "max_colors": "最大色数",
        "strand_count": "本どり数",
        "thread_system": "糸番号表示",
        "thread_both": "DMC + オリンパス",
        "thread_dmc": "DMCのみ",
        "thread_olympus": "オリンパスのみ",
        "generate": "図案を生成",
        "regenerate_masked": "背景を除外して再生成",
        "edit_mode": "背景除去モード",
        "edit_help": "ドラッグして背景部分を塗り、編集が終わったら下のボタンで再生成してください。",
        "brush_size": "ブラシサイズ",
        "clear_mask": "マスクをリセット",
        "preview_color": "カラープレビュー",
        "pattern_info": "図案情報",
        "info_title": "タイトル",
        "info_stitches": "ステッチ数",
        "info_fabric": "布",
        "info_finished": "仕上がりサイズ",
        "info_canvas": "キャンパスサイズ",
        "info_drawn": "仕上がりサイズ（描画範囲）",
        "info_colors": "使用色数",
        "info_strand": "本どり",
        "info_aida": "アイーダ",
        "chart": "クロスステッチ図案",
        "legend": "色凡例",
        "downloads": "ダウンロード",
        "dl_chart_png": "図案をPNGでダウンロード",
        "dl_preview_png": "プレビューをPNGでダウンロード",
        "dl_pdf": "PDFでダウンロード",
        "info_message": "左のサイドバーから画像をアップロードしてください。",
        "generating": "図案を生成中...",
        "header_strand": "クロス・ステッチ（すべて{n}本どり）",
        "header_symbol": "記号",
        "header_dmc": "DMC",
        "header_oly": "OLY",
        "header_color_name": "色名",
        "header_thread_amount": "糸量",
        "substitute_mark": "代替",
        "pro_active": "✨ プロ機能を解放中",
        "unlock_section": "🔑 有料機能を解除",
        "unlock_intro": "解除コードは [note記事]({url}) で入手できます（1,000円・買い切り）",
        "unlock_code_label": "解除コード",
        "unlock_button": "解除する",
        "unlock_wrong": "コードが違います",
        "free_tier_summary": "💡 無料：{w}ステッチ × {c}色まで全機能。それ以上はプレビュー専用（透かし入り）",
        "over_size_limit": "🔒 {w}ステッチを超えるとプレビューのみ（DL不可・透かしあり）",
        "over_color_limit": "🔒 {c}色を超えるとプレビューのみ（DL不可・透かしあり）",
        "preview_only_notice": "🔒 現在のサイズ・色数は無料範囲（{w}st × {c}色）を超えています。プレビューは確認できますが、ダウンロードと記号入り図案は[解除コード]({url})が必要です。",
        "share_section": "シェア",
        "share_to_x": "Xで共有",
        "share_text": "クロスステッチの図案を作ったよ ✂️\n{fabric}ct / {w}×{h}st / {cm_w}×{cm_h}cm / {n_colors}色\n",
        "share_hint_pro": "ボタンを押すと投稿画面が開きます。ダウンロードした画像も一緒に添付できます。",
        "share_hint_free": "現在は無料版のため画像DL不可。テキストだけシェアできます（解除コードで画像も添付可能に）。",
        "tutorial_title": "はじめての方へ ─ 使い方ガイド",
        "tutorial_button": "❓ 使い方ガイドを見る",
        "tutorial_close": "✕ 閉じる",
        "tutorial_prev": "← 前へ",
        "tutorial_next": "次へ →",
        "tutorial_done": "✓ はじめる",
        "tutorial_step_1": """
#### ようこそ！🎨

このアプリは、お手持ちの **写真をクロスステッチの図案に自動変換** するツールです。

例えばペットの写真や好きな風景写真を投げ込むだけで、
- マス目に色や記号が割り当てられた図案
- 必要な糸の番号と色名のリスト
- 仕上がりサイズ（cm）

がパッと出てきます。プログラミングの知識は一切いりません。

このガイドでは全6ステップで使い方を説明していきます。**「次へ」ボタンで進んでください。**

---

🔰 **完全に初心者でも大丈夫です。** 用語が分からなくても、ガイド通り進めれば作れます。
""",
        "tutorial_step_2": """
#### ステップ1：写真をアップロードしましょう 📷

画面の **左側にあるサイドバー**（細長い縦のエリア）を見てください。

「**画像をアップロード**」というボタンがあります。ここをクリックして、図案にしたい写真を選びます。

##### こんな写真がうまくいきます

- ✅ 主役（人・動物・物）がはっきり写っている
- ✅ 背景がシンプル（or 後で除去できる）
- ✅ 明るすぎず暗すぎない

##### こんな写真は難しいかも

- ⚠️ ピンボケしてる写真
- ⚠️ 主役と背景が同じような色
- ⚠️ 細かいパターンの服や柄物

写真は **JPG / PNG** どちらでもOK。サイズはアプリ側で自動調整されるので、スマホで撮った大きい写真でも大丈夫です。

サイドバーが見えない場合は、画面左上の **「>」** マークをクリックすると開きます。
""",
        "tutorial_step_3": """
#### ステップ2：サイズと色数を決めましょう 📐

写真をアップしたら、サイドバーで **どのくらいの大きさ・何色で作るか** を決めます。

##### ステッチ数（マスの数）

「**幅（ステッチ数）**」のスライダーで、何マス × 何マスにするかを決めます。
- **20〜30**：ワッペン、ピンバッジサイズ（3〜5cm）
- **50〜80**：コースター、ミニ額（9〜14cm）
- **100以上**：壁掛け、本格作品（18cm〜）

スライダーを動かすたびに、サイドバー下に **「📐 キャンパスサイズ：12.0 × 14.5 cm」** みたいな表示が出ます。これが完成サイズの目安です。

##### 布カウント

「**布カウント**」は、布の目の細かさです。**14カウント** が標準（ホビー店で一番売ってます）。

数字が大きいほど目が細かく、繊細な仕上がりになりますが難易度も上がります。

##### 色数

「**最大色数**」で、何色の糸を使うか決めます。
- **2〜4色**：シンプルなロゴ・キャラクター向け
- **6〜10色**：標準的な絵柄
- **15色以上**：写真っぽいリアルな仕上がり

🔓 **無料版は 30ステッチ × 4色まで全機能使えます。** それ以上は note記事の解除コード（1,000円・買い切り）で全機能解放されます。
""",
        "tutorial_step_4": """
#### ステップ3：背景を消しましょう（とても便利） 🪄

写真には主役以外の余分な背景が写っていることが多いですよね。

このアプリでは **「1. 背景除去」タブ** で、背景を範囲指定して図案から除外できます。背景を消すと：

- 糸の使用量が減る
- 主役だけがくっきり浮き上がる
- 仕上がりが綺麗

##### 背景を消す3つの方法

**🟢 連結同色フィル（おすすめ）**
クリックすると、繋がっている同じ色の領域がパッと一括選択されます。背景が単色っぽい時はこれが最速。

**🟢 範囲選択（ドラッグ）**
画像の上で四角くドラッグすると、その範囲がまるごと選択されます。広いエリアを一気に消したい時に。

**🟢 1ドットトグル**
1マスずつ細かく調整したい時用。

##### 「＋ 除外に追加」と「ー 除外から戻す」

クリックの動作はボタンで切り替えます：
- **＋モード**：クリックした部分を背景として除外
- **ーモード**：間違って除外しちゃった部分を戻す

##### その他の便利機能

- ⏪ **アンドゥ／リドゥ**：直前の操作を取り消し・やり直し
- 🪄 **エッジ領域を自動マスク**：画像の端っこを一発で背景判定（だいたい背景は端から始まるので便利）
- 💾 **マスクをPNGで保存**：作業を保存して後で続きから

赤くなっている部分が「除外される（=刺さない）」マスです。
""",
        "tutorial_step_5": """
#### ステップ4：図案を生成して確認しましょう ✨

背景が消せたら、いよいよ図案の生成です。

**「2. 図案生成」タブ** に切り替えて、**「図案を再生成」ボタン**（紫のやつ）を押してください。

数秒待つと出てくるもの：

##### 1. カラープレビュー
仕上がりイメージ。実物に近い見た目で出ます。「あ、これ可愛い！」って判断する用。

##### 2. 図案情報
- **キャンパスサイズ**：用意する布のサイズ
- **仕上がりサイズ**：実際の作品サイズ（背景を除いた範囲）
- 使用色数、本どり数 など

##### 3. 図案本体（記号入り）
マス目に色と記号が入った、実際に刺すときに見るやつ。10マスごとに太い線が引いてあります。

##### 4. 色凡例
**「どの記号がどの糸か」** の対応表。糸を買うときはこれを見て注文します。

「DMC + オリンパス」を選んでおくと両メーカーの番号が出ます。日本のホビー店なら **オリンパス** で揃えやすいです。

##### 結果が気に入らなかったら？

サイドバーに戻ってサイズや色数を調整して、もう一度「図案を再生成」を押すだけ。何度でもやり直せます。
""",
        "tutorial_step_6": """
#### ステップ5：印刷して刺してみよう 🧵

気に入った図案ができたら、ダウンロードして印刷します。

##### ダウンロードできるもの

- 📷 **図案 PNG**：マス目に記号入りの画像
- 📷 **プレビュー PNG**：仕上がりイメージ画像
- 📄 **PDF**：印刷用に整えられた書類（複数ページにまたがる場合は自動分割）

A4サイズで印刷して、見ながら刺していきます。

##### 刺すときのコツ

- **中心から始める**：図案の四辺に矢印（▽▷）が入っているので、その交点の中心マスからスタート
- **1色ずつ進める**：同じ色をまとめて刺すと効率的
- **本どり数**：14countなら3本どりが標準。お好みで調整

##### Xでシェアもできます

完成した作品やプレビュー画面を **#クロスステッチ図案メーカー** で投稿してくれたら嬉しいです。図案生成画面の「Xで共有」ボタンから、本文付きの投稿画面が開きます。

---

🎉 **これでガイドは終わりです！** 「✓ はじめる」ボタンを押して、楽しんでください。

困った時はサイドバー上部の **「❓ 使い方ガイドを見る」** ボタンでいつでも再表示できます。
""",
        "color_count_unit": "色",
        "strand_unit": "本どり",
        "edit_no_pattern": "先に「図案を生成」ボタンで初期パターンを生成してください。",
        "tab_bg_editor": "1. 背景除去",
        "tab_pattern": "2. 図案生成",
        "bg_editor_help": "クリックすると連結した同色領域を一括選択します。背景の色をクリックして除外していきましょう。",
        "tool_mode": "ツール",
        "tool_flood": "連結同色フィル",
        "tool_pixel": "1ドットトグル",
        "tool_rect": "範囲選択（ドラッグ）",
        "rect_help": "ドラッグで矩形を描くと、その範囲のドットをまとめて選択／除外します",
        "tolerance": "色の許容差",
        "tolerance_help": "0=完全一致、大きいほど色の似た範囲も含めます",
        "auto_edge": "エッジ領域を自動マスク",
        "auto_edge_help": "画像の縁に接する領域を自動的に背景としてマスクします",
        "undo": "↶ アンドゥ",
        "redo": "↷ リドゥ",
        "reset_mask": "マスクを全リセット",
        "export_mask": "マスクをPNGで保存",
        "import_mask": "マスクをPNGから読込",
        "mask_status": "マスク状態",
        "masked_pixels": "除外ドット数",
        "history_position": "履歴位置",
        "click_image": "画像をクリックして背景部分を選択してください",
        "no_source": "先に画像をアップロードしてください。",
        "source_size": "ソースサイズ",
        "view_scale": "表示倍率",
        "current_view": "現在の編集状態",
        "preview_after_mask": "マスク適用後のプレビュー",
        "regenerate_pattern": "図案を再生成",
        "first_generate": "最初に図案を生成してください",
        "color_name_ja": "日本語色名",
        "click_mode": "クリック動作",
        "click_add": "＋ 除外に追加",
        "click_remove": "ー 除外から戻す",
        "click_mode_help": "＋モード: クリックした領域を除外マスクに追加 / ーモード: クリックした領域をマスクから外します",
    },
    "en": {
        "page_title": "Cross Stitch Pattern Maker",
        "title": "Cross Stitch Pattern Maker",
        "caption": "Upload an image to convert it to a cross stitch pattern",
        "settings": "Settings",
        "language": "Language / 言語",
        "upload": "Upload image",
        "pattern_title": "Pattern title",
        "default_title": "Cross Stitch Pattern",
        "size_settings": "Size settings",
        "size_mode": "Size mode",
        "size_mode_width": "By width (auto height)",
        "size_mode_height": "By height (auto width)",
        "size_mode_both": "Both width & height",
        "width_stitches": "Width (stitches)",
        "height_stitches": "Height (stitches)",
        "fabric_count": "Fabric count",
        "fabric_format": "{n}-count ({n} stitches/inch)",
        "max_colors": "Max colors",
        "strand_count": "Strand count",
        "thread_system": "Thread numbering",
        "thread_both": "DMC + Olympus",
        "thread_dmc": "DMC only",
        "thread_olympus": "Olympus only",
        "generate": "Generate pattern",
        "regenerate_masked": "Remove background & regenerate",
        "edit_mode": "Background removal",
        "edit_help": "Drag to paint over the background, then click the button below to regenerate.",
        "brush_size": "Brush size",
        "clear_mask": "Clear mask",
        "preview_color": "Color preview",
        "pattern_info": "Pattern info",
        "info_title": "Title",
        "info_stitches": "Stitch count",
        "info_fabric": "Fabric",
        "info_finished": "Finished size",
        "info_canvas": "Canvas size",
        "info_drawn": "Finished size (drawn area)",
        "info_colors": "Colors used",
        "info_strand": "Strands",
        "info_aida": "Aida",
        "chart": "Cross stitch chart",
        "legend": "Color legend",
        "downloads": "Downloads",
        "dl_chart_png": "Download chart PNG",
        "dl_preview_png": "Download preview PNG",
        "dl_pdf": "Download PDF",
        "info_message": "Please upload an image from the sidebar.",
        "generating": "Generating pattern...",
        "header_strand": "Cross stitch (all {n} strands)",
        "header_symbol": "Sym",
        "header_dmc": "DMC",
        "header_oly": "OLY",
        "header_color_name": "Color name",
        "header_thread_amount": "Thread",
        "substitute_mark": "alt",
        "pro_active": "✨ Pro features active",
        "unlock_section": "🔑 Unlock Pro",
        "unlock_intro": "Get the unlock code from the [note article]({url}) (¥1,000 one-time)",
        "unlock_code_label": "Unlock code",
        "unlock_button": "Unlock",
        "unlock_wrong": "Wrong code",
        "free_tier_summary": "💡 Free: up to {w} stitches × {c} colors. Above that = preview only (watermarked)",
        "over_size_limit": "🔒 Above {w} stitches: preview only (no DL, watermarked)",
        "over_color_limit": "🔒 Above {c} colors: preview only (no DL, watermarked)",
        "preview_only_notice": "🔒 Current size/color count exceeds free tier ({w}st × {c} colors). Preview is shown but downloads and symbol chart require [unlock code]({url}).",
        "share_section": "Share",
        "share_to_x": "Share on X",
        "share_text": "Made a cross-stitch pattern ✂️\n{fabric}ct / {w}×{h}st / {cm_w}×{cm_h}cm / {n_colors} colors\n",
        "share_hint_pro": "Click to open the share window. Attach the downloaded image too.",
        "share_hint_free": "Free tier — image DL disabled. Share text only (unlock to attach images).",
        "tutorial_title": "Quick Start Guide",
        "tutorial_button": "❓ Show usage guide",
        "tutorial_close": "✕ Close",
        "tutorial_prev": "← Prev",
        "tutorial_next": "Next →",
        "tutorial_done": "✓ Start",
        "tutorial_step_1": """
#### Welcome! 🎨

This app turns your photos into cross-stitch patterns automatically.

Drop in a pet photo or landscape, and you get:
- A grid pattern with colors and symbols
- A list of thread numbers and color names
- Finished size in cm

No coding knowledge needed. This 6-step guide will walk you through.
""",
        "tutorial_step_2": """
#### Step 1: Upload a photo 📷

Look at the **left sidebar**. Click **"Upload image"** and choose your photo.

##### Photos that work well
- ✅ Clear subject
- ✅ Simple background (or one you can mask later)
- ✅ Well-lit

##### Tricky photos
- ⚠️ Blurry images
- ⚠️ Subject and background too similar
- ⚠️ Busy patterns

JPG or PNG. Large files are auto-resized.
""",
        "tutorial_step_3": """
#### Step 2: Pick size and colors 📐

Use the sidebar sliders to set width/height in stitches.

- **20–30 stitches**: patch/pin size (~3–5 cm)
- **50–80**: coaster/mini frame (~9–14 cm)
- **100+**: wall art (~18 cm+)

A live cm preview appears below.

**Fabric count** = mesh density. **14ct** is standard.

**Max colors** = thread variety. 4 for simple, 10 for natural, 15+ for photo-realistic.

🔓 **Free tier: up to 30 stitches × 4 colors with full features.** Beyond that requires the unlock code (¥1,000 one-time, from the note article).
""",
        "tutorial_step_4": """
#### Step 3: Remove background 🪄

In the **"1. Background removal"** tab, mask out the background.

##### Three tools

- **Connected fill**: click to select a connected same-color region (fast)
- **Rectangle (drag)**: drag to mask a rectangular area
- **Single pixel**: precise pixel-by-pixel

##### Add/Remove modes
- **+ mode**: click adds to mask
- **− mode**: click removes from mask

##### Bonus
- **Undo/Redo** for any mistake
- **Auto-mask edges**: one click to flood from image borders
- **Export/Import mask PNG** to save your work

Red regions = will not be stitched.
""",
        "tutorial_step_5": """
#### Step 4: Generate your pattern ✨

Switch to the **"2. Pattern generation"** tab and click **"Regenerate pattern"**.

You get:
1. **Color preview** — what it looks like
2. **Pattern info** — canvas size, finished size, colors
3. **Symbol chart** — actual stitching guide with grid + symbols
4. **Color legend** — thread numbers and names (DMC and/or Olympus)

If unhappy, just adjust sliders and regenerate.
""",
        "tutorial_step_6": """
#### Step 5: Print and stitch! 🧵

Download options:
- **Chart PNG** (with symbols)
- **Preview PNG** (color only)
- **PDF** (auto-paginated for printing)

Tips:
- **Start from the center** (look for the arrow marks on chart edges)
- **One color at a time** is efficient
- **3 strands** is standard for 14-count

Tag your finished work **#クロスステッチ図案メーカー** on X — share button is on the pattern page.

---

🎉 You're ready! Click "✓ Start" to begin.

Need help later? Click "❓ Show usage guide" in the sidebar anytime.
""",
        "color_count_unit": " colors",
        "strand_unit": " strands",
        "edit_no_pattern": "Please generate an initial pattern first.",
        "tab_bg_editor": "1. Background removal",
        "tab_pattern": "2. Pattern generation",
        "bg_editor_help": "Click a pixel to select all connected pixels of the same color. Click background pixels to mark them for removal.",
        "tool_mode": "Tool",
        "tool_flood": "Connected fill",
        "tool_pixel": "Single pixel toggle",
        "tool_rect": "Rectangle (drag)",
        "rect_help": "Drag to draw a rectangle; all pixels inside are selected/removed at once",
        "tolerance": "Color tolerance",
        "tolerance_help": "0=exact match, higher includes similar colors",
        "auto_edge": "Auto-mask edge regions",
        "auto_edge_help": "Automatically mask regions touching the image edges",
        "undo": "↶ Undo",
        "redo": "↷ Redo",
        "reset_mask": "Reset mask",
        "export_mask": "Export mask as PNG",
        "import_mask": "Import mask from PNG",
        "mask_status": "Mask status",
        "masked_pixels": "Masked pixels",
        "history_position": "History position",
        "click_image": "Click on the image to select background regions",
        "no_source": "Please upload an image first.",
        "source_size": "Source size",
        "view_scale": "View scale",
        "current_view": "Current edit state",
        "preview_after_mask": "Preview after mask",
        "regenerate_pattern": "Regenerate pattern",
        "first_generate": "Generate the pattern first",
        "color_name_ja": "Japanese name",
        "click_mode": "Click action",
        "click_add": "+ Add to mask",
        "click_remove": "− Remove from mask",
        "click_mode_help": "+ mode: clicks add to the exclusion mask / − mode: clicks remove from the mask",
    },
}


def detect_browser_language() -> str:
    try:
        import streamlit as st
        accept_lang = ""
        try:
            accept_lang = st.context.headers.get("Accept-Language", "")
        except Exception:
            try:
                accept_lang = st.context.headers.get("accept-language", "")
            except Exception:
                pass
        if accept_lang:
            primary = accept_lang.split(",")[0].strip().lower()
            if primary.startswith("ja"):
                return "ja"
            return "en"
    except Exception:
        pass
    return "ja"


def t(key: str, lang: str) -> str:
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(
        key, TRANSLATIONS["en"].get(key, key)
    )
