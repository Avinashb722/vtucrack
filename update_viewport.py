import os
import re

def update_viewport(directory):
    pattern = re.compile(r'<meta\s+name=["\']viewport["\']\s+content=["\']width=640px,\s*initial-scale=1\.0["\']\s*/?>', re.IGNORECASE)
    replacement = '<meta name="viewport" content="width=640">'
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = pattern.sub(replacement, content)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {path}")

if __name__ == "__main__":
    update_viewport(r"c:\Users\Hp\Desktop\vtucrack-main")
