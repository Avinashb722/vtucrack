import os
import re

def clean_titles(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith(".html")]
    
    for filename in html_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Clean <title> - ensure it has only one " | VTUCrack"
        new_content = re.sub(r'<title>(.*?) \| vtucrack \| VTUCrack</title>', r'<title>\1 | VTUCrack</title>', content, flags=re.IGNORECASE)
        new_content = re.sub(r'<title>(.*?) \| VTUCrack \| VTUCrack</title>', r'<title>\1 | VTUCrack</title>', new_content, flags=re.IGNORECASE)
        
        # Clean og:title
        new_content = re.sub(r'property="og:title" content="(.*?) \| vtucrack \| VTUCrack"', r'property="og:title" content="\1 | VTUCrack"', new_content, flags=re.IGNORECASE)
        new_content = re.sub(r'property="og:title" content="(.*?) \| VTUCrack \| VTUCrack"', r'property="og:title" content="\1 | VTUCrack"', new_content, flags=re.IGNORECASE)

        # Clean twitter:title
        new_content = re.sub(r'property="twitter:title" content="(.*?) \| vtucrack \| VTUCrack"', r'property="twitter:title" content="\1 | VTUCrack"', new_content, flags=re.IGNORECASE)
        new_content = re.sub(r'property="twitter:title" content="(.*?) \| VTUCrack \| VTUCrack"', r'property="twitter:title" content="\1 | VTUCrack"', new_content, flags=re.IGNORECASE)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Cleaned titles in {filename}")

if __name__ == "__main__":
    clean_titles(".")
