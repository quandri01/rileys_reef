import os
import subprocess
from datetime import datetime

# === SETTINGS ===
REPO_PATH = r"C:\rileys_reef"
PUZZLE_GENERATOR_SCRIPT = os.path.join(REPO_PATH, "puzzle_generator.py")
COMMIT_MESSAGE = f"Daily puzzle update - {datetime.now().strftime('%Y-%m-%d')}"

# === GENERATE PUZZLES ===
subprocess.run(["py", PUZZLE_GENERATOR_SCRIPT])

# === GIT OPERATIONS ===
os.chdir(REPO_PATH)
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE])
subprocess.run(["git", "push"])

print("✅ GitHub updated successfully.")
