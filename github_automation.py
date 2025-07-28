import os
import subprocess
import datetime

# --- CONFIG ---
REPO_PATH = r"C:\rileys_reef"  # Local repository path
BRANCH = "main"
COMMIT_MESSAGE = f"Auto-update puzzles {datetime.datetime.now():%Y-%m-%d %H:%M:%S}"

def run_command(command, cwd=None):
    """Run shell commands and print output."""
    result = subprocess.run(command, cwd=cwd, shell=True, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def generate_puzzles():
    """Run your puzzle generation script."""
    print("🔄 Generating puzzles...")
    return run_command("py puzzle_generator.py", cwd=REPO_PATH)

def git_commit_and_push():
    """Commit and push changes safely."""
    print("🔄 Adding changes...")
    run_command("git add .", cwd=REPO_PATH)

    print("🔄 Committing...")
    run_command(f'git commit -m "{COMMIT_MESSAGE}"', cwd=REPO_PATH)

    print("🚀 Pushing to GitHub...")
    run_command(f"git push -u origin {BRANCH}", cwd=REPO_PATH)

def main():
    print("🚀 Starting Riley's Reef Automation...")
    
    # Generate puzzles
    if generate_puzzles() == 0:
        print("✅ Puzzles generated successfully.")
    else:
        print("❌ Puzzle generation failed.")
        return

    # Commit and push
    git_commit_and_push()
    print("🎉 GitHub updated successfully!")

if __name__ == "__main__":
    main()
