import requests
r = requests.get("https://bolls.life/get-books/LXX/").json()
print("First book dictionary structure:", r[0])
for b in r:
    print(f"Book ID: {b.get('bookid')}, Name: {b.get('name')}, Chapters: {b.get('chapters')}")
