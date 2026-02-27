import os
import re

# Standard Snippets
GA4_TAG = "G-TWQDNJ2KXV"
PRODUCTION_HEAD = f"""    <!-- VTUCrack Production Head -->
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png?v=2">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png?v=2">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=2">
    <link rel="shortcut icon" href="/favicon.ico?v=2">
    <link rel="manifest" href="/site.webmanifest?v=2">
    <meta name="theme-color" content="#0a0a0f">
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_TAG}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA4_TAG}');
    </script>"""

def deep_clean_head(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Brutal cleanup of ALL duplicate/leaked tags
    # This removes any link or script that looks like a favicon or analytics tag
    content = re.sub(r'<!-- (Production|Global|VTUCrack).*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'<link rel="(icon|apple-touch-icon|shortcut icon|manifest|canonical)".*?>', '', content)
    content = re.sub(r'<meta name="theme-color".*?>', '', content)
    content = re.sub(r'<script.*?googletagmanager.*?<\/script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>\s*window\.dataLayer = .*?<\/script>', '', content, flags=re.DOTALL)
    
    # 2. Re-insert Canonical
    filename = os.path.basename(filepath)
    clean_name = filename.replace(".html", "")
    if clean_name == "index":
        canonical_url = "https://www.vtucrack.com/"
    else:
        canonical_url = f"https://www.vtucrack.com/{clean_name}"
    
    canonical_tag = f'    <link rel="canonical" href="{canonical_url}">'
    
    # 3. Final Re-insertion
    # Place everything right before </head>
    new_head_block = f"\n{canonical_tag}\n{PRODUCTION_HEAD}\n"
    
    content = content.replace("</head>", f"{new_head_block}</head>")
    
    # 4. Global URL fix: ensure og:image and twitter:image are correct
    content = content.replace("https://www.vtucrack.com/web/image/1108-96d96707/logo-png.webp", "https://www.vtucrack.com/favicon-512x512.png")

    # Final cleanup of double newlines
    content = re.sub(r'\n\s*\n', '\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                deep_clean_head(os.path.join(root, file))
                count += 1
    print(f"Deep Cleaned and Standardized {count} files.")

if __name__ == "__main__":
    main()
