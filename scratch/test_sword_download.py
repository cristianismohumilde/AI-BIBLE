import urllib.request
import urllib.error

# Common CrossWire rawzip mirror URLs for Ge'ez/Ethiopic modules
urls = [
    "https://crosswire.org/ftpmaint/directory/mods.d/index.jsp",
    "http://ftp.crosswire.org/pub/sword/packages/rawzip/Geez.zip",
    "https://crosswire.org/ftpmaint/directory/rawzip/Geez.zip",
    "http://www.crosswire.org/ftpmaint/directory/rawzip/Geez.zip",
    "http://www.crosswire.org/ftpmaint/directory/rawzip/Ethiopic.zip",
    "https://crosswire.org/ftpmaint/directory/rawzip/Ethiopic.zip"
]

for url in urls:
    try:
        req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            print(f"[FOUND] {url} - Status: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"[FAILED] {url} - HTTP {e.code}")
    except Exception as e:
        print(f"[ERROR] {url} - {e}")
