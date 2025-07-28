import subprocess
import sys
import os
from datetime import datetime

# ANSI colors for Windows (enabled by default in Python 3.13+)
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
CHECK = "\u2705"  # ✅
WARN = "\u26A0"   # ⚠️
FAIL = "\u274C"   # ❌

def print_section(title, color=YELLOW):
    print(f"\n{color}{'='*10} {title} {'='*10}{RESET}\n")

def run_command(command, success_msg=None, error_msg=None):
    try:
        subprocess.run(command, check=True)
        if success_msg:
            print(f"{GREEN}{CHECK} {success_msg}{RESET}")
    except subprocess.CalledProcessError:
        if error_msg:
            print(f"{RED}{FAIL} {error_msg}{RESET}")
        sys.exit(1)

print_section("Starting Riley's Reef Automation", GREEN)

# 1. Generate puzzles
print_section("Generating Puzzles")
try:
    subprocess.run(["py", "puzzle_generator.py"], check=True)
    print(f"{GREEN}{CHECK} Puzzles generated successfully.{RESET}")
except subprocess.CalledProcessError:
    print(f"{RED}{FAIL} Puzzle generation failed.{RESET}")
    sys.exit(1)

# 2. Add changes
print_section("Adding Changes")
run_command(["git", "add", "."], "Changes added to Git.", "Failed to add changes.")

# 3. Commit changes
print_section("Committing")
commit_message = f"Auto-update puzzles {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
run_command(["git", "commit", "-m", commit_message],
            "Commit successful.",
            "Nothing to commit or commit failed.")

# 4. Push to GitHub
print_section("Pushing to GitHub", GREEN)
run_command(["git", "push", "origin", "main"],
            "GitHub updated successfully!",
            "Failed to push to GitHub.")
