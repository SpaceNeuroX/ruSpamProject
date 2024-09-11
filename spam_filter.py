import re
import json
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = 'NeuroSpaceX/ruSpamNS_V2'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=1).to(device).eval()
tokenizer = AutoTokenizer.from_pretrained(model_name)

def clean_text(text):
    return text

def classify_message(message):
    message = clean_text(message)
    encoding = tokenizer(message, padding='max_length', truncation=True, max_length=128, return_tensors='pt')
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask).logits
        pred = torch.sigmoid(outputs).cpu().numpy()[0][0]
    return pred

def process_file(input_file, output_file, threshold=0.8):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    non_spam_messages = []

    for item in tqdm(data, desc="Processing Messages"):
        message = item.get('message', '')
        pred = classify_message(message)
        if pred < threshold:
            non_spam_messages.append(item)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(non_spam_messages, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    input_file = 'output1.json'
    output_file = 'non_spam_messages.json'
    process_file(input_file, output_file)
