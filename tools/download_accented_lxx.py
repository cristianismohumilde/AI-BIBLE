import os
import json
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor

LXX_BOOK_MAPPING = {
    "1_Esdras": 67,
    "Tobit": 69,
    "Judith": 70,
    "1_Maccabees": 80,
    "2_Maccabees": 81,
    "3_Maccabees": 82,
    "4_Maccabees": 83,
    "Psalms": 19,
    "Wisdom_of_Solomon": 73,
    "Sirach": 74,
    "Isaiah": 23,
    "Baruch": 75,
    "Susanna": 77,
    "Bel_and_Dragon": 78
}

def ensure_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def download_book(book_name, test_mode=False):
    if book_name not in LXX_BOOK_MAPPING:
        print(f"Skipping {book_name}: no getBible ID mapping available.")
        return
        
    book_id = LXX_BOOK_MAPPING[book_name]
    url = f"https://api.getbible.net/v2/lxx/{book_id}.json"
    print(f"Downloading {book_name} from {url}...")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {book_name}. Status: {response.status_code}")
        return
        
    data = response.json()
    if "chapters" not in data:
        print(f"No chapters found for {book_name}.")
        return
        
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "LXX", book_name)
    ensure_dir(base_dir)
    
    for chapter_data in data["chapters"]:
        chapter_number = chapter_data["chapter"]
        verses_out = []
        
        for verse_data in chapter_data.get("verses", []):
            verse_num = verse_data["verse"]
            text = verse_data["text"]
            verses_out.append({
                "verse": verse_num,
                "text": text
            })
            
        if verses_out:
            file_path = os.path.join(base_dir, f"{chapter_number}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(verses_out, f, ensure_ascii=False, indent=2)
            print(f"Saved {book_name} Chapter {chapter_number}")
            
        if test_mode:
            break

def main():
    parser = argparse.ArgumentParser(description="Download Accented LXX from getBible V2")
    parser.add_argument("--books", nargs="*", help="Specific books to download")
    parser.add_argument("--test", action="store_true", help="Download only the first chapter of each book")
    args = parser.parse_args()

    books_to_download = args.books if args.books else list(LXX_BOOK_MAPPING.keys())
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_book, book, args.test) for book in books_to_download]
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
