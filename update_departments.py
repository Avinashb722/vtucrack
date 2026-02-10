import re

departments = {
    'civil.html': 'Civil Engineering',
    'mech.html': 'Mechanical Engineering',
    'eee.html': 'Electrical Engineering'
}

coming_soon_template = """    <main class="main-content">
        <div class='page-header' style='text-align:center; padding:80px 20px; min-height:60vh; display:flex; flex-direction:column; align-items:center; justify-content:center;'>
            <div style='width:140px; height:140px; background:rgba(123,0,255,0.1); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 40px; animation: pulse 2s infinite;'>
                <i class='fas fa-clock' style='color:#7b00ff; font-size:4rem;'></i>
            </div>
            <h1 style='font-size:3rem; margin-bottom:25px; background: linear-gradient(135deg, #7b00ff, #c471ed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{dept_name}</h1>
            <p style='font-size:1.3rem; color:#94a3b8; max-width:700px; margin:0 auto 50px; line-height:1.8;'>
                Content for this department is currently being prepared. Our team is working hard to bring you comprehensive study materials. Meanwhile, explore our CSE and AIML sections for quality resources.
            </p>
            <div style='display:flex; gap:20px; justify-content:center; flex-wrap:wrap;'>
                <a href='cse.html' class='btn-glow' style='padding:15px 35px; font-size:1.1rem;'>
                    <i class='fas fa-laptop-code'></i> Browse CSE
                </a>
                <a href='aiml.html' class='btn-glow' style='padding:15px 35px; font-size:1.1rem; background:rgba(255,255,255,0.05);'>
                    <i class='fas fa-robot'></i> Browse AIML
                </a>
            </div>
        </div>
        <style>
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
            }}
        </style>
    </main>"""

for filename, dept_name in departments.items():
    filepath = filename
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the main content section
    # Pattern: from <main class="main-content"> to </main>
    pattern = r'<main class="main-content">.*?</main>'
    replacement = coming_soon_template.format(dept_name=dept_name)
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated {filename} with Coming Soon message")

print("\nAll department pages updated successfully!")
