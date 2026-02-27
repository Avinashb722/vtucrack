import os
import re

# Cleaner, cache-busting production block
FAVICON_BLOCK = """    <!-- Production Favicon Setup -->
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png?v=2">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png?v=2">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=2">
    <link rel="shortcut icon" href="/favicon.ico?v=2">
    <link rel="manifest" href="/site.webmanifest?v=2">
    <meta name="theme-color" content="#0a0a0f">"""

def patch_html_v2(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the entire block between the "Favicon" comments or just the meta area
    # Looking for our previous production blocks to replace them cleanly
    pattern = r'<!-- Production Favicon Setup -->.*?<meta name="theme-color".*?>'
    
    # Also handle the old single links if any are left
    new_content = re.sub(pattern, FAVICON_BLOCK, content, flags=re.DOTALL)
    
    # Cleanup duplicate meta tags that might have been added
    new_content = re.sub(r'(<!-- Production Favicon Setup -->.*?){2,}', FAVICON_BLOCK, new_content, flags=re.DOTALL)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    modified = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                if patch_html_v2(os.path.join(root, file)):
                    modified += 1
    print(f"Patched {modified} HTML files with Cache-Busting Favicon setup (v=2).")

if __name__ == "__main__":
    main()
