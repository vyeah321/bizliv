import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import urllib.request
import urllib.error
from urllib.parse import urljoin

def fetch_rss_last_updated(rss_url, timeout=10):
    """
    RSSフィードから最新記事の更新日時を取得する
    """
    try:
        req = urllib.request.Request(rss_url)
        req.add_header('User-Agent', 'BizLiv-SitemapGenerator/1.0')
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            rss_content = response.read().decode('utf-8')
            
        # XMLパース
        rss_root = ET.fromstring(rss_content)
        
        # RSS 2.0形式の場合
        items = rss_root.findall('.//item')
        if not items:
            # Atom形式の場合
            items = rss_root.findall('.//{http://www.w3.org/2005/Atom}entry')
        
        if not items:
            print(f"Warning: No items found in RSS feed: {rss_url}")
            return None
            
        # 最新記事の日付を取得
        latest_date = None
        for item in items:
            # RSS 2.0の場合
            pub_date = item.find('pubDate')
            if pub_date is None:
                # Atomの場合
                pub_date = item.find('.//{http://www.w3.org/2005/Atom}published')
                if pub_date is None:
                    pub_date = item.find('.//{http://www.w3.org/2005/Atom}updated')
            
            if pub_date is not None and pub_date.text:
                try:
                    # RFC 2822形式またはISO 8601形式をパース
                    date_str = pub_date.text.strip()
                    
                    if ',' in date_str:
                        # RFC 2822形式の処理
                        if 'GMT' in date_str:
                            # GMT形式: "Tue, 07 Oct 2025 15:30:00 GMT"
                            parsed_date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT")
                            parsed_date = parsed_date.replace(tzinfo=timezone.utc)
                        else:
                            # タイムゾーン付き形式: "Tue, 07 Oct 2025 15:30:00 +0900"
                            parsed_date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
                    else:
                        # ISO 8601形式の例: "2025-10-07T15:30:00+09:00"
                        parsed_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    
                    if latest_date is None or parsed_date > latest_date:
                        latest_date = parsed_date
                        
                except ValueError as e:
                    print(f"Warning: Could not parse date '{date_str}': {e}")
                    continue
        
        return latest_date
        
    except urllib.error.URLError as e:
        print(f"Warning: Could not fetch RSS feed {rss_url}: {e}")
        return None
    except ET.ParseError as e:
        print(f"Warning: Could not parse RSS feed {rss_url}: {e}")
        return None
    except Exception as e:
        print(f"Warning: Unexpected error fetching RSS feed {rss_url}: {e}")
        return None

def get_content_last_updated():
    """
    外部コンテンツ（note、STAND.FM）の最新更新日時を取得する
    """
    rss_feeds = {
        'note': 'https://note.com/vyeah/rss',
        'stand.fm': 'https://stand.fm/rss/673606cf69bc2015d03c44d8'
    }
    
    latest_update = None
    
    for source, rss_url in rss_feeds.items():
        print(f"Checking {source} RSS feed...")
        last_updated = fetch_rss_last_updated(rss_url)
        
        if last_updated:
            print(f"  Latest {source} update: {last_updated.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            if latest_update is None or last_updated > latest_update:
                latest_update = last_updated
        else:
            print(f"  Could not retrieve {source} update date")
    
    return latest_update

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
    
    # 外部コンテンツの最新更新日時を取得
    print("Checking external content updates...")
    content_last_updated = get_content_last_updated()
    
    if content_last_updated:
        content_last_updated_str = content_last_updated.strftime('%Y-%m-%d')
        print(f"External content last updated: {content_last_updated_str}")
    else:
        content_last_updated_str = None
        print("Could not determine external content update date")

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
                
                # ブログとポッドキャストページは外部コンテンツの更新日時を使用
                is_blog_or_podcast = (
                    'blog/' in rel_path or 
                    'podcast/' in rel_path or
                    (rel_path == 'index.html' and content_last_updated_str)  # トップページも外部コンテンツの影響を受ける
                )
                
                if is_blog_or_podcast and content_last_updated_str:
                    # 外部コンテンツの更新日時とファイルの更新日時を比較し、新しい方を使用
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path), timezone.utc)
                    file_mtime_str = file_mtime.strftime('%Y-%m-%d')
                    
                    if content_last_updated > file_mtime:
                        lastmod.text = content_last_updated_str
                        print(f"  Using external content date for {rel_path}: {content_last_updated_str}")
                    else:
                        lastmod.text = file_mtime_str
                else:
                    # 通常のファイル更新日時を使用
                    lastmod.text = datetime.fromtimestamp(os.path.getmtime(file_path), timezone.utc).strftime('%Y-%m-%d')

                # priorityタグ
                priority = ET.SubElement(url_element, 'priority')
                priority.text = '1.0' if rel_path == 'index.html' else '0.8'

                # changefreqタグ
                changefreq = ET.SubElement(url_element, 'changefreq')
                # ブログとポッドキャストページはより頻繁に更新される
                if 'blog/' in rel_path or 'podcast/' in rel_path:
                    changefreq.text = 'daily'
                elif rel_path == 'index.html':
                    changefreq.text = 'daily'
                else:
                    changefreq.text = 'monthly'

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
    root_dir = './'
    
    print(f"Scanning directory: {os.path.abspath(root_dir)}")
    print(f"Base URL: {base_url}")
    
    create_sitemap(base_url, root_dir)
    print("Sitemap generated successfully!")
