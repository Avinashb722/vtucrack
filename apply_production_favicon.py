import os
import re

# New professional favicon block
FAVICON_BLOCK = """    <!-- Production Favicon Setup -->
    <link rel="icon" type="image/png" href="/favicon.png">
    <link rel="apple-touch-icon" href="/favicon.png">
    <link rel="manifest" href="/site.webmanifest">"""

def patch_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the existing favicon link
    # It might look like: <link rel="icon" type="image/x-icon" href="...">
    pattern = r'<link rel="icon".*?>'
    
    # Replace old favicon with the new production block
    new_content = re.sub(pattern, FAVICON_BLOCK, content)

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
                if patch_html(os.path.join(root, file)):
                    modified += 1
    print(f"Patched {modified} HTML files with production favicon setup.")

if __name__ == "__main__":
    main()
