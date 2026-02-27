import os
import re

def check_structure():
    errors = []
    html_files = []
    links_found = set()
    
    # 1. Collect all valid HTML files (clean names)
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(file.replace('.html', ''))

    # 2. Scan every file for links
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Find all internal links (ignoring http, mailto, etc.)
                    links = re.findall(r'href=["\']([^"\'#]*)["\']', content)
                    for link in links:
                        # Normalize link
                        link = link.strip('/')
                        if link and '.' not in link and not link.startswith('http'):
                            if link not in html_files and link != "":
                                errors.append(f"Broken Link in {file}: '{link}' not found.")
    
    # 3. Check for mandatory production files
    must_have = ['robots.txt', 'sitemap.xml', 'favicon.ico', 'site.webmanifest']
    for fh in must_have:
        if not os.path.exists(fh):
            errors.append(f"Missing Production File: {fh}")

    if not errors:
        print("✅ WEBSITE STRUCTURE IS PERFECT. No broken internal links found.")
    else:
        print(f"❌ Found {len(errors)} Structure Errors:")
        for err in errors[:10]: # Show first 10
            print(err)
            
if __name__ == "__main__":
    check_structure()
