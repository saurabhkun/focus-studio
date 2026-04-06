import os
import re
import glob

# folders
os.makedirs("styles", exist_ok=True)
os.makedirs("logic", exist_ok=True)
os.makedirs("views", exist_ok=True)

open("styles/__init__.py", "w").close()
open("logic/__init__.py", "w").close()
open("views/__init__.py", "w").close()

styles = ["theme"]
logic = ["database", "auth", "utils", "badges"]
views = ["app", "timer", "planner", "music", "social", "leaderboard", "analytics", "settings", "main"]

def patch_content(content):
    content = re.sub(r'^import theme\b', 'from styles import theme', content, flags=re.MULTILINE)
    content = re.sub(r'^import database\b', 'from logic import database', content, flags=re.MULTILINE)
    content = re.sub(r'^import auth\b', 'from logic import auth', content, flags=re.MULTILINE)
    content = re.sub(r'^import utils\b', 'from logic import utils', content, flags=re.MULTILINE)
    content = re.sub(r'^import badges\b', 'from logic import badges', content, flags=re.MULTILINE)
    
    content = re.sub(r'^import app\b', 'from views import app', content, flags=re.MULTILINE)
    content = re.sub(r'^import timer\b', 'from views import timer', content, flags=re.MULTILINE)
    content = re.sub(r'^import planner\b', 'from views import planner', content, flags=re.MULTILINE)
    content = re.sub(r'^import music\b', 'from views import music', content, flags=re.MULTILINE)
    content = re.sub(r'^import social\b', 'from views import social', content, flags=re.MULTILINE)
    content = re.sub(r'^import leaderboard\b', 'from views import leaderboard', content, flags=re.MULTILINE)
    content = re.sub(r'^import analytics\b', 'from views import analytics', content, flags=re.MULTILINE)
    content = re.sub(r'^import settings\b', 'from views import settings', content, flags=re.MULTILINE)
    content = re.sub(r'^import main\b', 'from views import main', content, flags=re.MULTILINE)
    
    content = re.sub(r'^from database import', 'from logic.database import', content, flags=re.MULTILINE)
    
    content = content.replace('os.path.join(os.path.dirname(__file__), "focus_studio.db")', 'os.path.join(os.path.dirname(os.path.dirname(__file__)), "focus_studio.db")')
    content = content.replace('os.path.join(os.path.dirname(__file__), "settings.json")', 'os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.json")')
    
    return content

for f in glob.glob("*.py"):
    if f == "refactor.py": continue
    name = f.replace(".py", "")
    with open(f, "r", encoding='utf-8') as file:
        content = file.read()
    content = patch_content(content)
    
    if name in styles:
        dest = f"styles/{f}"
    elif name in logic:
        dest = f"logic/{f}"
    elif name in views:
        dest = f"views/{f}"
    else:
        continue
        
    with open(dest, "w", encoding='utf-8') as file:
        file.write(content)
    os.remove(f)

with open("run.py", "w", encoding="utf-8") as file:
    file.write("from views.main import LoginApp\n\nif __name__ == '__main__':\n    app = LoginApp()\n    app.mainloop()\n")
