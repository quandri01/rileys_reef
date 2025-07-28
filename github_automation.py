import subprocess
import os
import json
import random
import requests
from datetime import datetime

# === CONFIG ===
REPO_PATH = r"C:\rileys_reef"
PUZZLE_DIR = os.path.join(REPO_PATH, "puzzles")
STORY_DIR = os.path.join(REPO_PATH, "stories")
CREATURE_FILE = os.path.join(REPO_PATH, "creatures.json")
USED_FILE = os.path.join(REPO_PATH, "used_creatures.json")

# === FOLDER SETUP ===
os.makedirs(PUZZLE_DIR, exist_ok=True)
for lvl in ["easy", "medium", "tricky_fish"]:
    os.makedirs(os.path.join(PUZZLE_DIR, lvl), exist_ok=True)
os.makedirs(STORY_DIR, exist_ok=True)

# === Load creatures ===
with open(CREATURE_FILE, "r", encoding="utf-8") as f:
    creatures = json.load(f)

used = []
if os.path.exists(USED_FILE):
    with open(USED_FILE, "r", encoding="utf-8") as f:
        used = json.load(f)

# === Helper: Fetch scientific name ===
def get_scientific_name(creature):
    try:
        response = requests.get(
            f"https://api.gbif.org/v1/species/match?name={creature}"
        )
        data = response.json()
        return data.get("scientificName", creature)
    except Exception as e:
        print(f"⚠️ Could not fetch scientific name for {creature}. Using fallback.")
        return creature

# === Helper: Clean old files ===
def clean_old_files():
    for root, dirs, files in os.walk(PUZZLE_DIR):
        for file in files:
            os.remove(os.path.join(root, file))
    for file in os.listdir(STORY_DIR):
        os.remove(os.path.join(STORY_DIR, file))
    print("🧹 Old puzzles and stories cleaned.")

# === Random Picker ===
def pick_random_creature():
    available = [c for c in creatures if c["name"] not in used]
    if not available:
        used.clear()
        available = creatures
    chosen = random.choice(available)
    used.append(chosen["name"])
    with open(USED_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f)
    return chosen

# === Prompt: Manual or Auto ===
manual = input("Manual run? (y/n): ").strip().lower() == "y"

if manual:
    clean_old_files()
    creature = input("Enter Creature Name: ").strip()
    scientific = get_scientific_name(creature)
    shopify = input("Enter Shopify URL: ").strip()
    image = input("Enter Image URL: ").strip()
    facts = input("Enter Fun Facts (comma separated): ").strip().split(",")
else:
    selected = pick_random_creature()
    creature = selected["name"]
    scientific = get_scientific_name(creature)
    shopify = selected.get("shopify", "")
    image = selected.get("image", "")
    facts = selected.get("facts", [])

print(f"\n🐠 Generating content for: {creature}\nScientific name: {scientific}\n")

# === Generate Puzzles ===
subprocess.run(["py", "puzzle_generator.py", creature], cwd=REPO_PATH, check=True)
print("✅ Puzzles generated")

# === Generate Story ===
story_cmd = ["py", "story_generator.py", creature, scientific, shopify, image] + facts
subprocess.run(story_cmd, cwd=REPO_PATH, check=True)
print("✅ Story generated")

# === Git Push ===
subprocess.run(["git", "add", "."], cwd=REPO_PATH, check=True)
commit_msg = f"Auto-update {creature} {datetime.now():%Y-%m-%d %H:%M:%S}"
subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_PATH)
subprocess.run(["git", "push", "origin", "main"], cwd=REPO_PATH)
print("🚀 GitHub updated successfully")

# === Send Preview Email ===
subprocess.run(["py", "send_preview_email.py", creature], cwd=REPO_PATH, check=True)
print("📧 Preview email sent successfully")
