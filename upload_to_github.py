import os
from github import Github
from dotenv import load_dotenv

def upload_files_to_github():
    # Load .env file and token
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise Exception("GitHub token not found in environment variables.")

    repo_name = "quandri01/rileys-reef-puzzles"
    local_folder = "rileys_reef_puzzles"
    target_folder = ""  # Empty means upload to the root of the repo

    g = Github(token)
    repo = g.get_repo(repo_name)

    for root, _, files in os.walk(local_folder):
        for filename in files:
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, local_folder)
            github_path = os.path.join(target_folder, relative_path).replace("\\", "/")

            with open(local_path, "rb") as file:
                content = file.read()

            try:
                contents = repo.get_contents(github_path)
                repo.update_file(contents.path, f"Update {github_path}", content, contents.sha)
                print(f"Updated: {github_path}")
            except:
                repo.create_file(github_path, f"Create {github_path}", content)
                print(f"Created: {github_path}")

if __name__ == "__main__":
    upload_files_to_github()
