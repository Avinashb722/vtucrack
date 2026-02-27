import re

# Read the sitemap
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove .html from all URLs
# Pattern: <loc>https://www.vtucrack.com/something.html</loc>
# Replace with: <loc>https://www.vtucrack.com/something</loc>
content = re.sub(r'(https://vtucrack\.vercel\.app/[^<]+)\.html', r'\1', content)

# Write back
with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Sitemap updated - all .html extensions removed")
print("URLs now use clean format without .html")
