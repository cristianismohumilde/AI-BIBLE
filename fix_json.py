import json

with open('output/Aleppo/2_Kings_1.json', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\\\\"', '\\"')

with open('output/Aleppo/2_Kings_1.json', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed JSON.")
