import os
import json

SKIP_MANUSCRIPTS = {"WLC", "DSS", "SBLGNT", "TR", "Talmud"}
ALLOWED_NT_BOOKS = {
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", 
    "1Corinthians", "2Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", 
    "1Thessalonians", "2Thessalonians", "1Timothy", "2Timothy", "Titus", "Philemon", 
    "Hebrews", "James", "1Peter", "2Peter", "1John", "2John", "3John", "Jude", "Revelation",
    "1_Corinthians", "2_Corinthians", "1_Thessalonians", "2_Thessalonians", "1_Timothy", "2_Timothy", 
    "1_Peter", "2_Peter", "1_John", "2_John", "3_John", 
    "I Corinthians", "II Corinthians", "I Thessalonians", "II Thessalonians", "I Timothy", "II Timothy", 
    "I Peter", "II Peter", "I John", "II John", "III John", "Revelation of John"
}
ALLOWED_LXX_BOOKS = {
    "Isaiah", "Psalms", "1_Maccabees", "2_Maccabees", "3_Maccabees", "4_Maccabees", 
    "Baruch", "Bel_and_Dragon", "Judith", "Odes", "Psalms_of_Solomon", "Sirach", 
    "Susanna", "Tobit", "Wisdom_of_Solomon", "1_Esdras"
}
ALLOWED_GEEZ_BOOKS = {
    "የማቴዎስ ወንጌል", "የማርቆስ ወንጌል", "የሉቃስ ወንጌል", "የዮሐንስ ወንጌል", "የሐዋርያት ሥራ", 
    "ወደ ሮሜ ሰዎች", "1ኛ ወደ ቆሮንቶስ ሰዎች", "2ኛ ወደ ቆሮንቶስ ሰዎች", "ወደ ገላትያ ሰዎች", "ወደ ኤፌሶን ሰዎች", 
    "ወደ ፊልጵስዩስ ሰዎች", "ወደ ቆላስይስ ሰዎች", "1ኛ ወደ ተሰሎንቄ ሰዎች", "2ኛ ወደ ተሰሎንቄ ሰዎች", 
    "1ኛ ወደ ጢሞቴዎስ", "2ኛ ወደ ጢሞቴዎስ", "ወደ ቲቶ", "ወደ ፊልሞና", "ወደ ዕብራውያን", "የያዕቆብ መልእክት", 
    "1ኛ የጴጥሮስ መልእክት", "2ኛ የጴጥሮስ መልእክት", "1ኛ የዮሐንስ መልእክት", "2ዮሐ", "3ኛ የዮሐንስ መልእክት", 
    "የይሁዳ መልእክት", "የዮሐንስ ራእይ", "መጽሐፈ ሄኖክ", "መጽሐፈ ኩፋሌ"
}

total_chapters = 0

for root, dirs, files in os.walk("data"):
    for file in files:
        if file.endswith(".json"):
            input_file = os.path.join(root, file)
            parts = os.path.normpath(input_file).split(os.sep)
            
            if "Talmud" in parts:
                if "Talmud" in SKIP_MANUSCRIPTS: continue
            elif "ancient_versions" in parts:
                if file.startswith("targum_onkelos_"):
                    with open(input_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        total_chapters += len(data.get("text", []))
                elif file in ["peshitta_syriac.json", "coptic_sahidic.json", "armenian_eastern.json"]:
                    with open(input_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if isinstance(data, dict) and "books" in data:
                        for book_dict in data["books"]:
                            if book_dict.get("name") not in ALLOWED_NT_BOOKS: continue
                            total_chapters += len(book_dict.get("chapters", []))
                elif "geez_extracted" in parts:
                    book_name = file.replace(".json", "")
                    if "_" in book_name:
                        book_title, ch_num = book_name.rsplit("_", 1)
                    else:
                        book_title = book_name
                    if book_title in ALLOWED_GEEZ_BOOKS:
                        total_chapters += 1
            else:
                if len(parts) < 4: continue
                translation = parts[1]
                book = parts[2]
                if translation in SKIP_MANUSCRIPTS: continue
                if translation == "LXX" and book not in ALLOWED_LXX_BOOKS: continue
                if translation == "BYZ" and book not in ALLOWED_NT_BOOKS: continue
                total_chapters += 1

print(f"Total allowed chapters: {total_chapters}")
