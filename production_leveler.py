import os
import re

# GA4 Snippet
GA4_TAG = "G-TWQDNJ2KXV"
GA4_SNIPPET = f"""    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_TAG}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA4_TAG}');
    </script>"""

# Production Favicon Block
FAVICON_BLOCK = """    <!-- Production Favicon Setup -->
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png?v=2">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png?v=2">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=2">
    <link rel="shortcut icon" href="/favicon.ico?v=2">
    <link rel="manifest" href="/site.webmanifest?v=2">
    <meta name="theme-color" content="#0a0a0f">"""

def patch_head(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Standardize Canonical URL
    filename = os.path.basename(filepath)
    clean_name = filename.replace(".html", "")
    if clean_name == "index":
        canonical_url = "https://www.vtucrack.com/"
    else:
        canonical_url = f"https://www.vtucrack.com/{clean_name}"
    
    # Remove existing canonicals
    content = re.sub(r'<link rel="canonical".*?>', '', content)
    # Re-insert canonical before </head>
    canonical_tag = f'<link rel="canonical" href="{canonical_url}">'
    
    # 2. Add Analytics if missing or re-standardize
    content = re.sub(r'<!-- Global site tag.*?js\?id=G-.*?<\/script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script async src="https://www.googletagmanager.com/gtag/js\?id=G-.*?<\/script>', '', content, flags=re.DOTALL)
    
    # 3. Handle Favicon Duplication
    # Remove all known favicon patterns
    content = re.sub(r'<link rel="icon".*?>', '', content)
    content = re.sub(r'<link rel="apple-touch-icon".*?>', '', content)
    content = re.sub(r'<link rel="shortcut icon".*?>', '', content)
    content = re.sub(r'<link rel="manifest".*?>', '', content)
    content = re.sub(r'<meta name="theme-color".*?>', '', content)
    content = re.sub(r'<!-- Production Favicon Setup -->', '', content)

    # 4. Final Head Re-assembly
    # We'll stick the canonical, analytics, and favicon block just before </head>
    head_insertion = f"\n{canonical_tag}\n{FAVICON_BLOCK}\n{GA4_SNIPPET}\n"
    
    if "</head>" in content:
        content = content.replace("</head>", f"{head_insertion}</head>")
    
    # Clean up empty lines created by removals
    content = re.sub(r'\n\s*\n', '\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                patch_head(os.path.join(root, file))
                count += 1
    print(f"Standardized {count} files for production (Canonical, Analytics, Favicon).")

if __name__ == "__main__":
    main()
