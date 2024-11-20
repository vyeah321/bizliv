import os
import xml.etree.ElementTree as ET
from datetime import datetime

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

def create_sitemap(base_url, root_dir):
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9', 
                        attrib={'xmlns:xhtml': 'http://www.w3.org/1999/xhtml'})

    # 言語ごとのパスを定義
    hreflang_paths = {
        'ja': '/ja/',
        'en': '/en/',
        'zhhans': '/zhhans/',
        'zhhant': '/zhhant/'
    }

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, root_dir)
                
                # index.html の場合はルートディレクトリに変換
                if rel_path.endswith('index.html'):
                    url = base_url + rel_path.replace('index.html', '').replace(os.path.sep, '/')
                else:
                    url = base_url + rel_path.replace(os.path.sep, '/')
                
                # URL要素の作成
                url_element = ET.SubElement(urlset, 'url')
                
                # locタグの作成
                loc = ET.SubElement(url_element, 'loc')
                loc.text = url
                
                # lastmodタグの作成（ファイルの最終更新日時を取得）
                lastmod = ET.SubElement(url_element, 'lastmod')
                lastmod.text = datetime.utcfromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')

                # priorityタグ（トップページは1.0、それ以外は0.8）
                priority = ET.SubElement(url_element, 'priority')
                if rel_path == 'index.html':
                    priority.text = '1.0'
                else:
                    priority.text = '0.8'

                # changefreqタグ（トップページはdaily、それ以外はmonthly）
                changefreq = ET.SubElement(url_element, 'changefreq')
                if rel_path == 'index.html':
                    changefreq.text = 'daily'
                else:
                    changefreq.text = 'monthly'

                # hreflangリンクの追加
                for lang, path in hreflang_paths.items():
                    hreflang_link = ET.SubElement(url_element, '{http://www.w3.org/1999/xhtml}link', 
                                                  rel="alternate", hreflang=lang)
                    hreflang_link.set('href', base_url + lang + '/')

    # インデントを適用して見やすくする
    indent(urlset)

    # XMLファイルとして保存
    tree = ET.ElementTree(urlset)
    tree.write('sitemap.xml', encoding='utf-8', xml_declaration=True)

# 使用例
base_url = 'https://bizliv.life/'
root_dir = '.'  # カレントディレクトリを指定

create_sitemap(base_url, root_dir)