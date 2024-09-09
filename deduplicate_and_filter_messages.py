import json
import re
from typing import List, Dict
from tqdm import tqdm
import multiprocessing as mp

def is_valid_message(message: str) -> bool:
    if message is None or len(message) < 20:
        return False
    cyrillic_chars = len(re.findall(r'[а-яА-Я]', message))
    return cyrillic_chars >= 10

def load_dataset(file_path: str) -> List[Dict]:
    dataset = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in tqdm(file, desc="Loading dataset"):
            line = line.strip()
            if line:
                try:
                    dataset.append(json.loads(line.replace("},", "}")))
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid line: {line}. Error: {e}")
    return dataset

def save_dataset(data: List[Dict], file_path: str):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in tqdm(data, desc="Saving dataset"):
            json.dump(item, file, ensure_ascii=False)
            file.write('\n')

def process_chunk(chunk):
    seen = set()
    deduplicated = []
    for item in chunk:
        message = item['message']
        if message and message not in seen and is_valid_message(message):
            seen.add(message)
            deduplicated.append(item)
    return deduplicated

def deduplicate(data: List[Dict]) -> List[Dict]:
    chunk_size = 100000
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = list(tqdm(pool.imap(process_chunk, chunks), total=len(chunks), desc="Deduplicating"))
    
    final_dedup = []
    seen = set()
    for chunk in results:
        for item in chunk:
            if item['message'] not in seen:
                seen.add(item['message'])
                final_dedup.append(item)
    
    return final_dedup

if __name__ == "__main__":
    input_file = 'shuffled_balanced_messages (1).json'
    output_file = 'shuffled_balanced_messages.json'

    dataset = load_dataset(input_file)

    deduplicated_dataset = deduplicate(dataset)

    save_dataset(deduplicated_dataset, output_file)

    print(f"Original dataset size: {len(dataset)}")
    print(f"Deduplicated and filtered dataset size: {len(deduplicated_dataset)}")
