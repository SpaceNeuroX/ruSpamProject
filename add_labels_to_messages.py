import json

def add_labels_to_messages(messages, label=0):
    labeled_messages = []
    for message in messages:
        if isinstance(message["text"], str):
            message_text = message["text"]
        elif isinstance(message["text"], list):
            try:
                message_text = " ".join([text_part["text"] for text_part in message["text"] if isinstance(text_part, dict) and "text" in text_part])
            except Exception as e:
                print(f"Error processing message id {message['id']}: {e}")
                message_text = ""
        else:
            print(f"Unexpected data type in message id {message['id']}: {type(message['text'])}")
            message_text = ""
        
        labeled_message = {
            "message": message_text,
            "label": label
        }
        labeled_messages.append(labeled_message)
    return labeled_messages

with open('result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

messages = data.get("messages", [])

labeled_messages = add_labels_to_messages(messages)

with open('labeled_messages.json', 'w', encoding='utf-8') as file:
    for labeled_message in labeled_messages:
        file.write(json.dumps(labeled_message, ensure_ascii=False) + '\n')

print("Лейблы успешно добавлены и сохранены в labeled_messages.json")
