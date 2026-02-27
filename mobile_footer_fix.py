import os
import re

# Configuration
DOMAIN = "https://www.vtucrack.com"

def polish_footer_and_mobile_layout(root_dir):
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if any(d in root for d in ['.git', 'node_modules']): continue
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))

    print(f"Applying Mobile Row-Wise Footer Fix for {len(html_files)} files...")

    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. CLEAN UP FOOTER GRID
            # Replace inline grid styles with the new .footer-grid class
            # Target both forms of grid injection we did earlier
            content = re.sub(r'<div class="grid-container" style="grid-template-columns: repeat\(auto-fit, minmax\(200px, 1fr\)\); gap: 40px;">', '<div class="footer-grid">', content)
            content = re.sub(r'<div class="grid-container" style="grid-template-columns: 2fr 1fr 1fr; gap: 40px;">', '<div class="footer-grid">', content)
            
            # Target any generic grid-container inside footer
            if '<footer' in content:
                footer_regex = r'<footer.*?<div class="nav-container">\s*<div class="grid-container"(.*?)>'
                content = re.sub(footer_regex, r'<footer class="site-footer"><div class="nav-container"><div class="footer-grid"\1>', content, flags=re.DOTALL)

            # 2. ENSURE CONSISTENCY IN FOOTER STRUCTURE
            # (In case some files used different classes)
            content = content.replace('class="grid-container" style="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));', 'class="footer-grid" style="')

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            # print(f"✅ Fixed Footer: {os.path.basename(file_path)}")

        except Exception as e:
            print(f"❌ Error in {file_path}: {e}")

    print("\n--- MOBILE FOOTER UPGRADE COMPLETE ---")

if __name__ == "__main__":
    polish_footer_and_mobile_layout(".")
