import os
import subprocess
import datetime
import json
import random
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CREATURES_FILE = "creatures.json"
USED_CREATURES_FILE = "used_creatures.json"
STORY_GENERATOR = "story_generator.py"
PUZZLE_GENERATOR = "puzzle_generator.py"
SEND_EMAIL_SCRIPT = "send_preview_email.py"

def pick_creature():
    """Pick a creature not used yet."""
    with open(CREATURES_FILE, "r") as f:
        creatures = json.load(f)

    if os.path.exists(USED_CREATURES_FILE):
        with open(USED_CREATURES_FILE, "r") as f:
            used_creatures = json.load(f)
    else:
        used_creatures = []

    available = [c for c in creatures if c["name"] not in used_creatures]

    # Reset if all creatures used
    if not available:
        print("♻️ All creatures used, resetting list.")
        available = creatures
        used_creatures = []

    creature = random.choice(available)
    used_creatures.append(creature["name"])

    with open(USED_CREATURES_FILE, "w") as f:
        json.dump(used_creatures, f)

    return creature["name"]

def run_script(script, *args):
    """Run Python script safely."""
    subprocess.run(["py", script, *args], check=True)

def main():
    print("🐠 Riley's Reef Automation Started")

    # --- Automatic or Manual selection ---
    if len(sys.argv) > 1:
        creature_name = " ".join(sys.argv[1:])  # Manual mode
        print(f"🦑 Manual creature selected: {creature_name}")
    else:
        creature_name = pick_creature()         # Auto mode
        print(f"🦑 Automatically picked: {creature_name}")

    # 1. Generate puzzles (easy/medium/tricky)
    run_script(PUZZLE_GENERATOR, creature_name)

    # 2. Generate story
    run_script(STORY_GENERATOR, creature_name)

    # 3. Commit changes
    subprocess.run(["git", "add", "."], check=True)
    commit_msg = f"Auto-update {creature_name} {datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    # 4. Push to GitHub
    subprocess.run(["git", "push", "origin", "main"], check=True)

    # 5. Send preview email
    run_script(SEND_EMAIL_SCRIPT, creature_name)

    print("✅ Riley's Reef automation finished successfully.")

if __name__ == "__main__":
    main()
