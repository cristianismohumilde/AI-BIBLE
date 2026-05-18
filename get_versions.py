import requests
r = requests.get('https://www.sefaria.org/api/texts/versions/Genesis.1').json()
for v in r:
    if v['language'] == 'he':
        print(f"Hebrew version: {v['versionTitle']}")
