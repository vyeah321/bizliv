import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

def indent(elem, level=0):
    """インデントを適用してXMLを見やすくする"""
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def normalize_url_path(url_path):
    """
    重複する言語プレフィックスを除去する
    例: /ja/ja/page -> /ja/page, /en/en/page -> /en/page
    """
    # 言語プレフィックスパターン
    lang_prefixes = ['ja', 'en', 'zhhans', 'zhhant']
    
    for lang in lang_prefixes:
        duplicate_pattern = f'/{lang}/{lang}/'
        if duplicate_pattern in url_path:
            url_path = url_path.replace(duplicate_pattern, f'/{lang}/')
    
    # 不正な/bizliv/プレフィックスを除去
    if '/bizliv/' in url_path:
        url_path = url_path.replace('/bizliv/', '/')
    
    return url_path

def get_language_alternatives(rel_path, base_url, root_dir):
    """
    指定されたページに対する言語別の代替URLを取得する
    実際に存在するファイルのみを返し、重複プレフィックスを避ける
    """
    alternatives = []
    lang_mapping = {
        'ja': 'ja',
        'en': 'en', 
        'zh-Hans': 'zhhans',
        'zh-Hant': 'zhhant'
    }
    
    # パスを分析して、言語ディレクトリ構造を理解する
    path_parts = rel_path.split('/')
    
    # ケース1: ルートページ (index.html)
    if rel_path == 'index.html':
        for hreflang, dir_name in lang_mapping.items():
            lang_file = f'{dir_name}/index.html'
            full_path = os.path.join(root_dir, lang_file)
            if os.path.exists(full_path):
                alt_url = f'{base_url}{dir_name}/'
                alternatives.append((hreflang, alt_url))
        return alternatives
    
    # ケース2: 既に言語ディレクトリ内のページ (ja/app/index.html, en/app/index.html, etc.)
    if len(path_parts) >= 2 and path_parts[0] in ['ja', 'en', 'zhhans', 'zhhant']:
        current_lang = path_parts[0]
        app_path = '/'.join(path_parts[1:])  # 言語プレフィックスを除去
        
        for hreflang, dir_name in lang_mapping.items():
            lang_file = f'{dir_name}/{app_path}'
            full_path = os.path.join(root_dir, lang_file)
            if os.path.exists(full_path):
                if app_path.endswith('index.html'):
                    alt_url = f'{base_url}{dir_name}/{app_path.replace("index.html", "")}'
                else:
                    alt_url = f'{base_url}{dir_name}/{app_path}'
                alternatives.append((hreflang, alt_url))
        return alternatives
    
    # ケース3: アプリのルートページ (app/index.html)
    if rel_path.endswith('/index.html') and len(path_parts) >= 2:
        app_name = path_parts[0]  # アプリ名
        
        for hreflang, dir_name in lang_mapping.items():
            # app/ja/index.html, app/en/index.html の形式で探す
            lang_file = f'{app_name}/{dir_name}/index.html'
            full_path = os.path.join(root_dir, lang_file)
            if os.path.exists(full_path):
                alt_url = f'{base_url}{app_name}/{dir_name}/'
                alternatives.append((hreflang, alt_url))
        return alternatives
    
    # ケース4: その他のファイル - 対応する言語ディレクトリ内で探す
    for hreflang, dir_name in lang_mapping.items():
        # 直接言語ディレクトリ内に配置されているファイルを探す
        lang_file = f'{dir_name}/{rel_path}'
        full_path = os.path.join(root_dir, lang_file)
        if os.path.exists(full_path):
            if rel_path.endswith('index.html'):
                alt_url = f'{base_url}{dir_name}/{rel_path.replace("index.html", "")}'
            else:
                alt_url = f'{base_url}{dir_name}/{rel_path}'
            alternatives.append((hreflang, alt_url))
    
    return alternatives

def create_sitemap(base_url, root_dir):
    # XML namespace宣言を正しく設定（重複を避ける）
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xhtml', 'http://www.w3.org/1999/xhtml')

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, root_dir).replace(os.path.sep, '/')
                
                # テンプレートファイルや不要なファイルを除外
                if ('_includes' in rel_path or 
                    rel_path.startswith('.') or
                    'template' in rel_path.lower()):
                    continue
                
                # URLの基本形を生成
                if rel_path.endswith('index.html'):
                    url = base_url + rel_path.replace('index.html', '')
                else:
                    url = base_url + rel_path

                # URLパスを正規化（重複プレフィックス除去）
                url = normalize_url_path(url)

                # URL要素の作成
                url_element = ET.SubElement(urlset, 'url')

                # locタグ
                loc = ET.SubElement(url_element, 'loc')
                loc.text = url

                # lastmodタグ
                lastmod = ET.SubElement(url_element, 'lastmod')
                lastmod.text = datetime.fromtimestamp(os.path.getmtime(file_path), timezone.utc).strftime('%Y-%m-%d')

                # priorityタグ
                priority = ET.SubElement(url_element, 'priority')
                priority.text = '1.0' if rel_path == 'index.html' else '0.8'

                # changefreqタグ
                changefreq = ET.SubElement(url_element, 'changefreq')
                changefreq.text = 'daily' if rel_path == 'index.html' else 'monthly'

                # hreflangリンクを追加（実際に存在するページのみ）
                alternatives = get_language_alternatives(rel_path, base_url, root_dir)
                for hreflang, alt_url in alternatives:
                    hreflang_link = ET.SubElement(
                        url_element,
                        '{http://www.w3.org/1999/xhtml}link',
                        rel="alternate",
                        hreflang=hreflang,
                        href=alt_url
                    )

    # インデントを適用して見やすくする
    indent(urlset)

    # XMLファイルとして保存
    tree = ET.ElementTree(urlset)
    tree.write('sitemap.xml', encoding='utf-8', xml_declaration=True)

# 使用例
if __name__ == "__main__":
    base_url = 'https://bizliv.life/'
    root_dir = '../'  # 親ディレクトリ（bizlivルート）を指定
    
    print(f"Scanning directory: {os.path.abspath(root_dir)}")
    print(f"Base URL: {base_url}")
    
    create_sitemap(base_url, root_dir)
    print("Sitemap generated successfully!")
