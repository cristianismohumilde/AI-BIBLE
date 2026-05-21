import requests
import json
import re

r = requests.get('https://www.sefaria.org/api/index/').json()

def find_titles_and_versions(node, query):
    results = []
    if isinstance(node, dict):
        title = node.get("title")
        if title and re.search(query, title, re.IGNORECASE):
            results.append(title)
        # also search in categories
        heTitle = node.get("heTitle")
        if heTitle and re.search(query, heTitle, re.IGNORECASE):
            results.append(f"{title} (HE: {heTitle})")
        for k, v in node.items():
            results.extend(find_titles_and_versions(v, query))
    elif isinstance(node, list):
        for item in node:
            results.extend(find_titles_and_versions(item, query))
    return results

print("=== Greek ===")
print(list(set(find_titles_and_versions(r, "Greek"))))
print("=== Septuagint ===")
print(list(set(find_titles_and_versions(r, "Septuagint"))))
print("=== LXX ===")
print(list(set(find_titles_and_versions(r, "LXX"))))
