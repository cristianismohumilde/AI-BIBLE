import urllib.request
import re
import urllib.error

url = "https://ebible.org/Scriptures/"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as r:
        html = r.read().decode('utf-8')
        links = re.findall(r'href="([^"]+)"', html)
        gez_links = [l for l in links if 'gez' in l.lower()]
        print("Ge'ez links in ebible:", gez_links)
except Exception as e:
    print("Error:", e)
