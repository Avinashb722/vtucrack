import os
import re

def check_broken_links(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith(".html")]
    file_slugs = {f[:-5] for f in html_files}
    file_slugs.add("") # root
    file_slugs.add("/") # root
    
    # Ignore these
    ignore = ["css/style.css", "${item.url}", "web/image", "_vercel/insights/script.js"]
    
    broken_links = {}
    
    for filename in html_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex to find href="..."
        links = re.findall(r'href="([^"]+)"', content)
        
        for link in links:
            if link.startswith("http") or link.startswith("#") or link.startswith("tel:") or link.startswith("mailto:"):
                continue
            
            clean_link = link.split('?')[0].split('#')[0]
            if clean_link in ignore or any(clean_link.startswith(ig) for ig in ignore):
                continue
                
            if clean_link not in file_slugs:
                if filename not in broken_links:
                    broken_links[filename] = []
                broken_links[filename].append(link)
                
    if broken_links:
        print("Found potentially broken links:")
        for file, links in sorted(broken_links.items()):
            print(f"File: {file}")
            for l in sorted(set(links)):
                print(f"  - {l}")
    else:
        print("No broken links found!")

if __name__ == "__main__":
    check_broken_links(".")
