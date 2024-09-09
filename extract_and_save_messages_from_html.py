import json
import os
from bs4 import BeautifulSoup

def extract_messages_from_html(file_path):
    """
    Извлекает сообщения из HTML файла и возвращает их в виде списка словарей.

    Параметры:
    - file_path (str): Путь к HTML файлу, из которого необходимо извлечь сообщения.

    Возвращает:
    - messages (list): Список сообщений, где каждое сообщение представлено в виде словаря с ключами:
        - 'message': текст сообщения с добавленным временем отправки.
        - 'label': метка сообщения (в данном случае всегда 1).
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    messages = []
    for message_div in soup.find_all('div', class_='message'):
        message_content = message_div.find('div', class_='message__text__content')
        user = message_content.find('a').get_text(strip=True)
        message_text = message_content.get_text(strip=True).replace(user, '', 1).strip()
        time = message_div.find('div', class_='message__time').get_text(strip=True)
        
        full_message = f"{message_text} {time}"
        
        messages.append({
            'message': full_message,
            'label': 1
        })
    return messages

def process_folder(folder_path):
    """
    Обрабатывает все HTML файлы в указанной папке, извлекает из них сообщения и сохраняет в файл 'messages.json'.

    Параметры:
    - folder_path (str): Путь к папке, в которой находятся HTML файлы для обработки.
    
    Вывод:
    - Сообщения сохраняются в файл 'messages.json', каждое сообщение записывается в формате JSON построчно.
    """
     
    with open('messages.json', 'w', encoding='utf-8') as json_file:
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.html'):
                file_path = os.path.join(folder_path, file_name)
                print(f"Processing {file_path}...")
                messages = extract_messages_from_html(file_path)
                
                for message in messages:
                    json_file.write(json.dumps(message, ensure_ascii=False) + '\n')

    print("Messages have been saved to messages.json.")

folder_path = './spam'
process_folder(folder_path)
