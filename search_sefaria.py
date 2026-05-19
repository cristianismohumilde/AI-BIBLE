import requests
r = requests.get('https://www.sefaria.org/api/index/').json()
import re
def find_title(node, query):
    titles = []
    if isinstance(node, dict):
        title = node.get("title")
        if title and re.search(query, title, re.IGNORECASE):
            titles.append(title)
        for k, v in node.items():
            titles.extend(find_title(v, query))
    elif isinstance(node, list):
        for item in node:
            titles.extend(find_title(item, query))
    return titles

print(find_title(r, "Dead Sea Scrolls"))
