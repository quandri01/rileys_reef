import os
import sys

def generate(creature, level):
    html = f"<html><body><h1>{level.title()} Puzzle – {creature.title()}</h1>" \
           "<!-- puzzle grid here -->" \
           "</body></html>"
    outfolder = os.path.join("puzzles", level.lower())
    os.makedirs(outfolder, exist_ok=True)
    filename = os.path.join(outfolder, f"{creature.lower()}_{level.lower()}.html")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Puzzle generated: {filename}")

def main():
    creature = sys.argv[1]
    for level in ["easy", "medium", "tricky_fish"]:
        generate(creature, level)

if __name__ == "__main__":
    main()
