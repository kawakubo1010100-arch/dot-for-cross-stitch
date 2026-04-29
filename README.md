# クロスステッチ図案メーカー / Cross Stitch Pattern Maker

写真や画像をアップロードしてクロスステッチ図案に変換する Web アプリです。
Upload an image and convert it into a cross stitch pattern.

## 機能 / Features

- 画像から自動的にドット絵化＋減色（K-meansクラスタリング、LAB色空間）
- DMC糸489色に自動マッピング（CIEDE2000色差）
- DMC ↔ オリンパス糸番号の変換テーブル付き
- 背景除去エディタ（連結同色フィル / 矩形ドラッグ / 1ドット選択 / +/-モード切替 / アンドゥ・リドゥ）
- マスクをPNGで保存・読込（ブラウザバック対策）
- 仕上がりサイズのリアルタイム表示（cm）
- PDF / PNG ダウンロード
- 日本語 / 英語UI（ブラウザ言語自動判定）

## 起動方法 / Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## テスト / Tests

```bash
pytest tests/ -v
```

## ライセンス / License

MIT
