import os
import re

def fix_indexing(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Search for any robots meta tag
    # We want to force it to "index, follow" for production visibility
    pattern = r'<meta name="robots" content=".*?"\s*/?>'
    
    # Check if it exists
    if re.search(pattern, content):
        # Replace existing
        new_content = re.sub(pattern, '<meta name="robots" content="index, follow">', content)
    else:
        # Insert it before </head> if missing
        new_tag = '\n    <meta name="robots" content="index, follow">'
        new_content = content.replace("</head>", f"{new_tag}\n</head>")

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                if fix_indexing(os.path.join(root, file)):
                    count += 1
    print(f"Forced 'index, follow' on {count} files.")

if __name__ == "__main__":
    main()
