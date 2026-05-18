import requests
codes = ["syr", "PESH", "pesh", "gez", "gez_nt", "gez_ot", "cop", "Sahidic", "Bohairic", "Armenian", "hye", "ARM", "CopSahBible2", "ArmEastern"]
for code in codes:
    try:
        r = requests.get(f"https://bolls.life/get-text/{code}/1/1/1/", timeout=5)
        print(f"Code: {code}, Status: {r.status_code}, Text length: {len(r.text)}")
    except Exception as e:
        print(f"Code: {code}, Exception: {e}")
