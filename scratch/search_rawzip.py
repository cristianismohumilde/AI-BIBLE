import urllib.request
import re
import urllib.error

# We check the CrossWire rawzip directory
url = "https://crosswire.org/ftpmaint/directory/mods.d/"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as r:
        html = r.read().decode('utf-8')
        links = re.findall(r'href="([^"]+)"', html)
        res = [l for l in links if 'gez' in l.lower() or 'eth' in l.lower() or 'amharic' in l.lower()]
        print("Mods.d links found:", res)
except Exception as e:
    print("Error:", e)
