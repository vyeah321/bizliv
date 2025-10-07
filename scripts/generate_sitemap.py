#!/usr/bin/env python3
"""
Sitemap Generator for BizLiv Website
Automatically generates sitemap.xml from HTML files in the repository
"""

import os
import glob
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Tuple

# Configuration
DOMAIN = "https://bizliv.life"
DEFAULT_CHANGEFREQ = "monthly"
DEFAULT_PRIORITY = "0.8"

# Priority mapping for different page types
PRIORITY_MAP = {
    "": "1.0",  # Root page
    "blog": "0.9",
    "podcast": "0.9",
    "nomireco": "0.8",
    "shopping-list": "0.8",
    "go-home-navi": "0.8",
    "online-meetings-schedule": "0.8",
    "privacy": "0.7",
    "support": "0.7"
}

# Change frequency mapping
CHANGEFREQ_MAP = {
    "": "daily",  # Root page
    "blog": "daily",
    "podcast": "daily",
    "nomireco": DEFAULT_CHANGEFREQ,
    "shopping-list": DEFAULT_CHANGEFREQ,
    "go-home-navi": DEFAULT_CHANGEFREQ,
    "online-meetings-schedule": DEFAULT_CHANGEFREQ,
    "privacy": "yearly",
    "support": "yearly"
}

def find_html_files(root_dir: str) -> List[str]:
    """Find all index.html files except those in _includes directories"""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip _includes directories
        if '_includes' in root:
            continue
        if 'index.html' in files:
            html_files.append(os.path.join(root, 'index.html'))
    return sorted(html_files)

def path_to_url(file_path: str, root_dir: str) -> str:
    """Convert file path to URL"""
    # Remove root directory and index.html
    relative_path = os.path.relpath(file_path, root_dir)
    url_path = os.path.dirname(relative_path)
    
    # Convert to URL format
    if url_path == '.':
        return f"{DOMAIN}/"
    else:
        return f"{DOMAIN}/{url_path}/"

def get_app_name(url_path: str) -> str:
    """Extract app name from URL path"""
    if url_path == f"{DOMAIN}/":
        return ""
    
    # Remove domain and trailing slash
    path = url_path.replace(f"{DOMAIN}/", "").rstrip("/")
    
    # Get the first part of the path (app name)
    return path.split('/')[0] if path else ""

def get_language_alternatives(file_path: str, root_dir: str, all_files: List[str]) -> List[Tuple[str, str]]:
    """Get language alternatives for a given file"""
    alternatives = []
    
    # Get the relative path without index.html
    relative_path = os.path.relpath(file_path, root_dir)
    base_dir = os.path.dirname(relative_path)
    
    # Determine the app and language structure
    if base_dir == '.':
        # Root page - check language variants
        lang_variants = {
            'ja': 'ja/',
            'en': 'en/', 
            'zh-Hans': 'zhhans/',
            'zh-Hant': 'zhhant/'
        }
        for hreflang, path in lang_variants.items():
            full_path = os.path.join(root_dir, path, 'index.html')
            if full_path in all_files:
                alternatives.append((hreflang, f"{DOMAIN}/{path}"))
    else:
        # App pages - find language variants within the same app
        parts = base_dir.split(os.sep)
        
        if len(parts) == 1:
            # App root page (e.g., nomireco/index.html)
            app_name = parts[0]
            lang_variants = {
                'ja': f'{app_name}/ja/',
                'en': f'{app_name}/en/',
                'zh-Hans': f'{app_name}/zhhans/',
                'zh-Hant': f'{app_name}/zhhant/',
                'x-default': f'{app_name}/'
            }
        elif len(parts) == 2:
            # App language page (e.g., nomireco/ja/index.html)
            app_name, current_lang = parts
            lang_variants = {
                'ja': f'{app_name}/ja/',
                'en': f'{app_name}/en/',
                'zh-Hans': f'{app_name}/zhhans/',
                'zh-Hant': f'{app_name}/zhhant/',
                'x-default': f'{app_name}/'
            }
        else:
            return alternatives
            
        for hreflang, path in lang_variants.items():
            full_path = os.path.join(root_dir, path, 'index.html')
            if full_path in all_files:
                alternatives.append((hreflang, f"{DOMAIN}/{path}"))
    
    return alternatives

def generate_sitemap(root_dir: str) -> str:
    """Generate sitemap XML content"""
    # Create XML structure
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xhtml', 'http://www.w3.org/1999/xhtml')
    urlset.set('xmlns:html', 'http://www.w3.org/1999/xhtml')
    
    # Find all HTML files
    html_files = find_html_files(root_dir)
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Process each HTML file
    for html_file in html_files:
        url_path = path_to_url(html_file, root_dir)
        app_name = get_app_name(url_path)
        
        # Create URL element
        url_elem = ET.SubElement(urlset, 'url')
        
        # Add location
        loc = ET.SubElement(url_elem, 'loc')
        loc.text = url_path
        
        # Add last modified date
        lastmod = ET.SubElement(url_elem, 'lastmod')
        lastmod.text = current_date
        
        # Add priority
        priority = ET.SubElement(url_elem, 'priority')
        priority.text = PRIORITY_MAP.get(app_name, DEFAULT_PRIORITY)
        
        # Add change frequency
        changefreq = ET.SubElement(url_elem, 'changefreq')
        changefreq.text = CHANGEFREQ_MAP.get(app_name, DEFAULT_CHANGEFREQ)
        
        # Add language alternatives
        alternatives = get_language_alternatives(html_file, root_dir, html_files)
        for hreflang, href in alternatives:
            link = ET.SubElement(url_elem, '{http://www.w3.org/1999/xhtml}link')
            link.set('rel', 'alternate')
            link.set('hreflang', hreflang)
            link.set('href', href)
    
    # Convert to string with pretty formatting
    ET.indent(urlset, space="  ")
    xml_str = ET.tostring(urlset, encoding='unicode', xml_declaration=True)
    
    # Add UTF-8 encoding to declaration
    xml_str = xml_str.replace("<?xml version='1.0' encoding='unicode'?>", 
                             "<?xml version='1.0' encoding='utf-8'?>")
    
    return xml_str

def main():
    """Main function"""
    # Get the repository root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    
    print(f"Generating sitemap for: {repo_root}")
    
    # Generate sitemap
    sitemap_content = generate_sitemap(repo_root)
    
    # Write to sitemap.xml
    sitemap_path = os.path.join(repo_root, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"Sitemap generated successfully: {sitemap_path}")
    
    # Print summary
    html_files = find_html_files(repo_root)
    print(f"Total pages included: {len(html_files)}")

if __name__ == "__main__":
    main()