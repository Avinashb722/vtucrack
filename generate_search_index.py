import os
import json
import re
from html import unescape

def generate_search_index():
    index = []
    print("Generating fresh search index...")
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            # Skip non-subject/branch pages or system files
            if not file.endswith('.html') or file in ['404.html', 'privacy-policy.html', 'terms-and-conditions.html', 'disclaimer.html']:
                continue
                
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extract Title
                title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
                title = title_match.group(1).split('|')[0].strip() if title_match else file
                
                # Extract Description
                desc_match = re.search(r'<meta name="description" content="(.*?)"', content, re.IGNORECASE)
                description = desc_match.group(1) if desc_match else ""
                
                # Clean URL (Vercel cleanUrls)
                url = file.replace('.html', '')
                if url == 'index': url = ''
                
                index.append({
                    "title": unescape(title),
                    "description": unescape(description),
                    "url": url
                })

    with open('search.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    
    print(f"✅ Created search.json with {len(index)} searchable pages.")

if __name__ == "__main__":
    generate_search_index()
