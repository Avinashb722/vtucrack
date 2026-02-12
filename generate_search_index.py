import os
import json
import re

def generate_search_index(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith(".html")]
    search_data = []
    
    for filename in sorted(html_files):
        if filename in ["index.html", "404.html", "error.html"]:
            continue
            
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_match.group(1).replace(" | VTUCrack", "").replace(" | vtucrack", "").strip() if title_match else filename
        
        # Extract description
        desc_match = re.search(r'<meta name="description" content="(.*?)">', content, re.IGNORECASE)
        description = desc_match.group(1).strip() if desc_match else ""
        
        # Extract main text content (simplified)
        # Remove script and style tags
        clean_content = re.sub(r'<(script|style).*?>.*?</\1>', '', content, flags=re.DOTALL | re.IGNORECASE)
        # Remove all other tags
        clean_content = re.sub(r'<.*?>', ' ', clean_content)
        # Clean whitespace
        clean_content = re.sub(r'\s+', ' ', clean_content).strip()
        
        search_data.append({
            "title": title,
            "description": description,
            "url": filename[:-5], # cleanup .html
            "content": clean_content[:1000] # Limit content size for search.json efficiency
        })
        
    with open(os.path.join(directory, "search.json"), 'w', encoding='utf-8') as f:
        json.dump(search_data, f, indent=2)
        
    print(f"Generated search.json with {len(search_data)} entries.")

if __name__ == "__main__":
    generate_search_index(".")
