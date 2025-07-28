import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys

# === EMAIL CONFIG ===
GMAIL_USER = "yourgmail@gmail.com"
GMAIL_PASS = "your_app_password"
TO_EMAIL = "yourpreviewemail@gmail.com"

# === ZAPIER WEBHOOK LINKS ===
APPROVE_LINK = "https://hooks.zapier.com/hooks/catch/123456/approve"
REJECT_LINK = "https://hooks.zapier.com/hooks/catch/123456/reject"

REPO_BASE_URL = "https://github.com/quandri01/rileys_reef/blob/main"

def send_preview(creature):
    subject = f"Riley's Reef Preview – {creature}"

    story_file = os.path.join("stories", f"story_{creature.lower()}.html")
    with open(story_file, "r", encoding="utf-8") as f:
        story_html = f.read()

    easy_link = f"{REPO_BASE_URL}/puzzles/easy/{creature.lower()}_easy.html"
    medium_link = f"{REPO_BASE_URL}/puzzles/medium/{creature.lower()}_medium.html"
    tricky_link = f"{REPO_BASE_URL}/puzzles/tricky_fish/{creature.lower()}_tricky_fish.html"

    html_content = f"""
    <html>
    <body>
    <h2>Riley's Reef Preview</h2>
    <p><strong>Creature:</strong> {creature}</p>
    <h3>Story</h3>
    {story_html}
    <h3>Puzzles</h3>
    <ul>
        <li><a href="{easy_link}">Easy Puzzle</a></li>
        <li><a href="{medium_link}">Medium Puzzle</a></li>
        <li><a href="{tricky_link}">Tricky Fish Puzzle</a></li>
    </ul>
    <p>
    <a href="{APPROVE_LINK}?creature={creature}" style="background:green;color:white;padding:10px;text-decoration:none;margin-right:10px;">✅ Approve & Send</a>
    <a href="{REJECT_LINK}?creature={creature}" style="background:red;color:white;padding:10px;text-decoration:none;">❌ Reject</a>
    </p>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(GMAIL_USER, GMAIL_PASS)
    server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())
    server.quit()

    print(f"✅ Preview email sent for {creature}")

if __name__ == "__main__":
    send_preview(sys.argv[1])
