import os
import subprocess

COMMIT_SHA = os.getenv("COMMIT_SHA")
COMMIT_MESSAGE = os.getenv("COMMIT_MESSAGE")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

def get_commit_diff():
    """Holt die Änderungen des aktuellen Commits ab."""
    result = subprocess.run(["git", "show", "--unified=0", COMMIT_SHA], capture_output=True, text=True)
    return result.stdout

def generate_ai_changelog(diff):
    """
    Hier kannst du die KI-Logik einbauen (z. B. OpenAI API oder GitHub Copilot API, 
    sofern ein entsprechender API-Schlüssel als GitHub Secret hinterlegt ist).
    """
    # Fallback-Generierung basierend auf der Commit-Nachricht
    entry = f"- {COMMIT_MESSAGE} (Commit: {COMMIT_SHA[:7]})"
    return entry

def update_changelog_file(entry):
    """Fügt den Eintrag der CHANGELOG.md hinzu und pusht ihn."""
    changelog_path = "CHANGELOG.md"
    
    if os.path.exists(changelog_path):
        with open(changelog_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = "# Changelog\n\n"

    new_content = f"# Changelog\n\n## Neueste Einträge\n{entry}\n\n" + content.replace("# Changelog\n\n", "")

    with open(changelog_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    # Git-Konfiguration für den Bot
    subprocess.run(["git", "config", "--global", "user.name", "GitHub Actions Bot"])
    subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"])
    
    # Authentifizierte Remote-URL für den Push
    remote_url = f"https://x-access-token:{GITHUB_TOKEN}@github.com/{GITHUB_REPOSITORY}.git"
    
    subprocess.run(["git", "add", changelog_path])
    subprocess.run(["git", "commit", "-m", "docs: automatischer Changelog-Eintrag [skip ci]"])
    
    # Auf den aktuellen Branch pushen
    branch = os.getenv("GITHUB_REF_NAME")
    subprocess.run(["git", "push", remote_url, f"HEAD:{branch}"])

if __name__ == "__main__":
    diff = get_commit_diff()
    entry = generate_ai_changelog(diff)
    update_changelog_file(entry)