import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from datetime import datetime

# サイトURLとページ情報
pages = [
    {'loc': '/', 'priority': 1.0, 'changefreq': 'daily'},
    {'loc': '/ja/', 'priority': 0.8, 'changefreq': 'monthly'},
    {'loc': '/en/', 'priority': 0.8, 'changefreq': 'monthly'},
    {'loc': '/zhhans/', 'priority': 0.8, 'changefreq': 'monthly'},
    {'loc': '/zhhant/', 'priority': 0.8, 'changefreq': 'monthly'},
    {'loc': '/privacy/', 'priority': 0.8, 'changefreq': 'monthly'},
    {'loc': '/support/', 'priority': 0.8, 'changefreq': 'monthly'},
    {'loc': '/blog/ja/', 'priority': 0.8, 'changefreq': 'monthly'},
    {'loc': '/shopping-list/', 'priority': 0.8, 'changefreq': 'monthly'},
    {'loc': '/go-home-navi/', 'priority': 0.8, 'changefreq': 'monthly'},
    {'loc': '/nomireco/', 'priority': 0.8, 'changefreq': 'monthly'},
    {'loc': '/podcast/ja/', 'priority': 0.8, 'changefreq': 'monthly'},
    {'loc': '/online-meetings-schedule/', 'priority': 0.8, 'changefreq': 'monthly'},
]

# hreflang マッピング
hreflangs = {
    'ja': '/ja/',
    'en': '/en/',
    'zhhans': '/zhhans/',
    'zhhant': '/zhhant/',
}

base_url = "https://bizliv.life"

# XML生成
urlset = Element('urlset', {
    'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
    'xmlns:xhtml': 'http://www.w3.org/1999/xhtml'
})

today = datetime.today().strftime('%Y-%m-%d')

for page in pages:
    # _includes などの内部ファイルは無視
    if '_includes' in page['loc']:
        continue

    url = SubElement(urlset, 'url')
    SubElement(url, 'loc').text = base_url + page['loc']
    SubElement(url, 'lastmod').text = today
    SubElement(url, 'changefreq').text = page['changefreq']
    SubElement(url, 'priority').text = str(page['priority'])

    # hreflang タグを付与
    for lang, path in hreflangs.items():
        link = SubElement(url, '{http://www.w3.org/1999/xhtml}link', {
            'rel': 'alternate',
            'hreflang': lang,
            'href': base_url + path
        })

# 見やすいXMLに整形
xml_str = minidom.parseString(tostring(urlset)).toprettyxml(indent="  ", encoding="utf-8")

# ファイル保存
with open('sitemap.xml', 'wb') as f:
    f.write(xml_str)

print("sitemap.xml を生成しました。")
