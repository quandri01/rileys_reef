import os
from datetime import datetime

# === OUTPUT FOLDERS ===
OUTPUT_DIR = os.path.join(os.getcwd(), "puzzles")
SUDOKU_FILE = os.path.join(OUTPUT_DIR, f"sudoku_{datetime.now().strftime('%Y%m%d')}.txt")
CROSSWORD_FILE = os.path.join(OUTPUT_DIR, f"crossword_{datetime.now().strftime('%Y%m%d')}.txt")

# === ENSURE OUTPUT FOLDER EXISTS ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === GENERATE SIMPLE PLACEHOLDER PUZZLES ===
with open(SUDOKU_FILE, "w") as f:
    f.write("Sudoku Puzzle\n")
    f.write("Placeholder puzzle content\n")

with open(CROSSWORD_FILE, "w") as f:
    f.write("Crossword Puzzle\n")
    f.write("Placeholder puzzle content\n")

print("Puzzles generated successfully.")
