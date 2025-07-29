import sys
import json
import os
import requests

CREATURES_FILE = "creatures.json"
STORY_OUTPUT_DIR = "stories"

def fetch_scientific_name_online(creature_name):
    """Fetches the scientific name from an online API (placeholder)."""
    try:
        response = requests.get(f"https://api.gbif.org/v1/species/match?name={creature_name}")
        data = response.json()
        if "scientificName" in data:
            return data["scientificName"]
    except Exception as e:
        print(f"⚠️ Online lookup failed: {e}")
    return None

def get_scientific_name(creature_name):
    """Checks JSON first, then fetches online if missing."""
    if os.path.exists(CREATURES_FILE):
        with open(CREATURES_FILE, "r") as f:
            creatures = json.load(f)
        for creature in creatures:
            if creature["name"].lower() == creature_name.lower() and "scientific_name" in creature:
                return creature["scientific_name"]

    # Fallback to online lookup
    sci_name = fetch_scientific_name_online(creature_name)
    return sci_name if sci_name else "Unknownus Oceanus"

def main():
    if len(sys.argv) < 2:
        print("❌ No creature name provided to story generator.")
        sys.exit(1)

    creature_name = sys.argv[1]
    scientific_name = get_scientific_name(creature_name)

    if not os.path.exists(STORY_OUTPUT_DIR):
        os.makedirs(STORY_OUTPUT_DIR)

    # Generate story HTML
    story_content = f"""
    <html>
    <head><title>{creature_name} Story</title></head>
    <body>
        <h1>{creature_name}</h1>
        <h2><i>{scientific_name}</i></h2>
        <p>Today, Riley encounters a fascinating {creature_name.lower()} in the ocean...</p>
    </body>
    </html>
    """

    output_path = os.path.join(STORY_OUTPUT_DIR, f"{creature_name.lower().replace(' ', '_')}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(story_content)

    print(f"✅ Story generated: {output_path}")

if __name__ == "__main__":
    main()
