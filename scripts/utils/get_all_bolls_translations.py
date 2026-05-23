import requests
r = requests.get("https://bolls.life/get-translations/").json()
for lang, trans_list in r.items():
    print(f"=== Language: {lang} ===")
    for t in trans_list:
        print(f"  Short: {t['short']}, Name: {t['name']}, ID: {t['id']}")
