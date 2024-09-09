"""
This Python script is designed to automate the process of
scraping web page content for specific dates using Selenium.
It navigates to each date-based URL, retrieves the page content, and saves it as HTML files.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import calendar

chrome_options = Options()
chrome_options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
service = Service(r'C:\Users\Kirill\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

start_date = (2, 10)
start_parsing = False

try:
    for month in range(1, 13):
        days_in_month = calendar.monthrange(2023, month)[1]
        for day in range(1, days_in_month + 1):
            if (month > start_date[0]) or (month == start_date[0] and day >= start_date[1]):
                start_parsing = True
            
            if start_parsing:
                url = f"https://lols.bot/2022/{calendar.month_name[month]}-{day:02d}/"
                
                try:
                    driver.get(url)
                    time.sleep(3)
                    
                    html_content = driver.page_source
                    
                    file_name = f'./spam/page_content_2022_{month:02d}_{day:02d}.html'
                    with open(file_name, 'w', encoding='utf-8') as file:
                        file.write(html_content)
                    
                    print(f"Данные за {day:02d} {calendar.month_name[month]} успешно сохранены в '{file_name}'")
                except Exception as e:
                    print(f"Ошибка при обработке {url}: {e}")
finally:
    driver.quit()
