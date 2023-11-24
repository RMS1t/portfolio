from pathlib import Path

from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
import re

filepath = Path('out.csv')
options = webdriver.ChromeOptions()
useragent = UserAgent()
options.add_argument(
    f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

try:
    driver.get("https://listtravel.ru/country/russia/goroda-rossii")
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    elem = soup.find_all('td')
    data_array = []

    for article in elem:

        if 'class' in article.attrs or article.get_text() == '' or article.get_text().isdigit():
            continue

        if re.search('(\d+)', article.get_text()):

            match = re.search('\(\d+\)', article.get_text())
            data_array.append(article.get_text()[:match.start()])
            data_array.append(article.get_text()[match.start() + 1:match.end() - 1])

        else:
            data_array.append(article.get_text())

    data_array = np.array(data_array).reshape(len(data_array) // 4, 4)

    df = pd.DataFrame(data_array, columns=['Город', "Регион", "Население", "Год переписи"]).sort_values(
        by=['Год переписи', "Регион"])



    df.to_csv(filepath)


except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
