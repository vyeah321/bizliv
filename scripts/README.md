# BizLiv Sitemap Auto-Generator

このプロジェクトは、BizLivウェブサイトのサイトマップを自動生成するためのPythonスクリプトとGitHub Actionsの設定を含んでいます。

## 🚀 機能

- **自動サイトマップ生成**: すべてのHTMLファイルを自動検出してサイトマップを作成
- **多言語対応**: 日本語、英語、中国語（簡体字・繁体字）のhreflang属性を自動設定
- **SEO最適化**: ページタイプに応じた優先度と更新頻度の自動設定
- **GitHub Actions統合**: HTMLファイルの変更時に自動実行

## 📁 ファイル構成

```
.github/workflows/generate-sitemap.yml  # GitHub Actionsワークフロー
scripts/generate_sitemap.py             # サイトマップ生成スクリプト
sitemap.xml                             # 生成されるサイトマップ（自動更新）
```

## ⚙️ 自動実行トリガー

GitHub Actionsは以下の場合に自動実行されます：

1. **HTMLファイルの変更時**: `main`ブランチに`.html`ファイルがプッシュされた時
2. **スクリプト変更時**: サイトマップ生成スクリプトが変更された時
3. **手動実行**: GitHub Actionsタブから手動でトリガー可能
4. **定期実行**: 毎週月曜日の2:00 UTC（11:00 JST）に自動実行

## 🔧 ローカルでの実行

```bash
# リポジトリのルートディレクトリで実行
python3 scripts/generate_sitemap.py
```

## 📋 生成される設定

### 優先度 (Priority)
- **ルートページ**: 1.0
- **ブログ・ポッドキャスト**: 0.9
- **アプリページ**: 0.8
- **プライバシー・サポート**: 0.7

### 更新頻度 (Change Frequency)
- **ルートページ**: daily
- **ブログ・ポッドキャスト**: daily
- **アプリページ**: monthly
- **プライバシー・サポート**: yearly

### 多言語対応 (hreflang)
各ページに対して適切な言語代替URLを自動設定：
- `ja`: 日本語
- `en`: 英語  
- `zh-Hans`: 中国語簡体字
- `zh-Hant`: 中国語繁体字
- `x-default`: デフォルト言語

## 🛠️ カスタマイズ

`scripts/generate_sitemap.py`内の以下の設定を変更することで、動作をカスタマイズできます：

```python
# ドメイン設定
DOMAIN = "https://bizliv.life"

# 優先度マッピング
PRIORITY_MAP = {
    "": "1.0",  # ルートページ
    "blog": "0.9",
    "nomireco": "0.8",
    # ...
}

# 更新頻度マッピング
CHANGEFREQ_MAP = {
    "": "daily",  # ルートページ
    "blog": "daily",
    "nomireco": "monthly",
    # ...
}
```

## 🚨 注意事項

- サイトマップは自動生成されるため、手動で編集しないでください
- 新しいアプリやページを追加した場合、スクリプトが自動的に検出して追加します
- `_includes`ディレクトリ内のファイルは自動的に除外されます

## 📊 生成結果

現在のサイトマップには以下が含まれています：
- **総ページ数**: 37ページ
- **対応アプリ**: NomiReco, Shopping List, Go Home Navi, Online Meetings Schedule
- **多言語対応**: 日本語、英語、中国語（簡体字・繁体字）
- **自動更新**: HTMLファイル変更時および定期実行