import os
import xml.etree.ElementTree as ET
from datetime import datetime

def create_sitemap(base_url, root_dir):
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, root_dir)
                url = base_url + rel_path.replace(os.path.sep, '/')
                
                url_element = ET.SubElement(urlset, 'url')
                loc = ET.SubElement(url_element, 'loc')
                loc.text = url

                lastmod = ET.SubElement(url_element, 'lastmod')
                lastmod.text = datetime.utcnow().strftime('%Y-%m-%d')

    tree = ET.ElementTree(urlset)
    tree.write('sitemap.xml', encoding='utf-8', xml_declaration=True)

# 使用例
base_url = 'https://bizliv.life/'
root_dir = '.'  # カレントディレクトリを指定

create_sitemap(base_url, root_dir)