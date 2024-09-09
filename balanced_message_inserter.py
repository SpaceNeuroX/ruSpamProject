"""
Скрипт предназначен для балансировки данных, чтобы сообщения с разными метками встречались
в результирующем наборе данных более равномерно.
"""

import json
import math

with open('shuffled_balanced_messages (1).json', 'r', encoding='utf-8') as file:
    data = [json.loads(line) for line in file]

label_0 = [entry for entry in data if entry['label'] == 0]
label_1 = [entry for entry in data if entry['label'] == 1]

if len(label_1) > 0:
    interval = math.ceil(len(label_0) / len(label_1))
else:
    interval = len(label_0)

alternated_data = []

index_0 = 0
index_1 = 0

while index_0 < len(label_0):
    alternated_data.append(label_0[index_0])
    index_0 += 1
    if index_1 < len(label_1) and index_0 % interval == 0:
        alternated_data.append(label_1[index_1])
        index_1 += 1

with open('alternated_data.json', 'w', encoding='utf-8') as file:
    for entry in alternated_data:
        json.dump(entry, file, ensure_ascii=False)
        file.write('\n')

print("Data has been alternated and saved.")
