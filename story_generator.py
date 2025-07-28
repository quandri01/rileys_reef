import os
import sys

def generate_story(creature, scientific_name, shopify_url, image_url, facts):
    shopify_section = (
        f'<p>Want your very own {creature.title()} figure? '
        f'<a href="{shopify_url}">Click here</a> to see it in our store!</p>'
        if shopify_url and "yourshopify" not in shopify_url else ""
    )

    image_section = (
        f'<img src="{image_url}" alt="{creature.title()}" style="width:200px;">'
        if image_url and "yourshopify" not in image_url else ""
    )

    facts_list = ''.join(f'<li>{fact}</li>' for fact in facts)

    return f"""<html>
<head><title>Riley’s Reef — {creature.title()} Spotlight</title></head>
<body>
<h1>Meet the Amazing {creature.title()}!</h1>
{image_section}
<p>Today's ocean star is the playful <strong>{creature.title()}</strong> (<em>{scientific_name}</em>).</p>

<h3>Fun Facts:</h3>
<ul>{facts_list}</ul>
{shopify_section}
</body>
</html>"""

def main():
    creature = sys.argv[1]
    scientific_name = sys.argv[2]
    shopify_url = sys.argv[3] if len(sys.argv) > 3 else ""
    image_url = sys.argv[4] if len(sys.argv) > 4 else ""
    facts = sys.argv[5:]
    
    os.makedirs("stories", exist_ok=True)
    filename = os.path.join("stories", f"story_{creature.lower()}.html")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(generate_story(creature, scientific_name, shopify_url, image_url, facts))
    
    print(f"✅ Story generated: {filename}")

if __name__ == "__main__":
    main()
