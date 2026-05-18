import requests
for branch in ["master", "main"]:
    try:
        r = requests.get(f"https://api.github.com/repos/scrollmapper/bible_databases/git/trees/{branch}?recursive=1", timeout=10).json()
        if "tree" in r:
            for f in r["tree"]:
                name = f["path"]
                if any(x in name.lower() for x in ["copsah", "arme", "pesh", "syr", "gez"]):
                    print(f"Branch: {branch}, Path: {name}")
    except Exception as e:
        print(f"Error on branch {branch}: {e}")
