from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import tkinter as tk
from tkinter import messagebox
import time
import requests
from PIL import Image, ImageTk
from fake_useragent import UserAgent

# Указываем ссылку; юзерагента; переменные, связанные с попыток входа на сайт.

useragent = UserAgent()
option = webdriver.ChromeOptions()
option.add_argument(f'user-agent={useragent.chrome}')
driver = webdriver.Chrome(options = option)
url = 'https://code-basics.com/ru/session/new'

user = 'kosmosmakmelov4@gmail.com'
password = 'kosmosmakmelov4@gmail.com'

attempt = 0
max_attempts = 8


# Входим в систему.

while attempt < max_attempts:
        try:
            driver.get(url=url)
            break
        except WebDriverException:
            attempt += 1
            print(f"Не удалось зайти на сайт. Попытка входа {attempt} из {max_attempts}.")
            time.sleep(5)
        else:
            driver.quit()
try:
    login_input = driver.find_element(By.ID,'user_sign_in_form_email')
    login_input.clear()
    login_input.send_keys(user)
    password_input = driver.find_element(By.ID,'user_sign_in_form_password')
    password_input.clear()
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
except Exception as ex:
            pass

# Входим на вкладку с Java.

time.sleep(2)
rrr = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@href='/ru/languages/java']"))
)
driver.execute_script("arguments[0].scrollIntoView();", rrr)
time.sleep(2)
rrr.click()

# Решаем задания с AI

taskBlock_InGeneral = driver.find_element(By.XPATH, "//div[@class='mb-5']")
taskBlock = taskBlock_InGeneral.find_element(By.XPATH, "//div[@class='list-group']")
tasks = taskBlock.find_elements(By.XPATH, "//div[@class='list-group-item']")

for i in range(len(tasks)):
    try:
        tasks[i].find_element(By.XPATH, ".//i[@class='bi bi-check-lg']")
    except NoSuchElementException:
        driver.execute_script("arguments[0].scrollIntoView();", tasks[i])
        time.sleep(1)
        tasks[i].click()
        time.sleep(2)
        # Here

        try:
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="view-line"]'))
            )
            print("Текстовое поле найдено.")

            # Ждём ввода пользователя
            user_input = input("Введите текст для вставки: ")

            if user_input == "Да":
            
                driver.back()
                time.sleep(5)

                taskBlock_InGeneral = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='mb-5']"))
                )

                taskBlock = taskBlock_InGeneral.find_element(By.XPATH, ".//div[@class='list-group']")
                tasks = taskBlock.find_elements(By.XPATH, ".//div[@class='list-group-item']")
        except TimeoutException:
            print("Текстовое поле не найдено.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


# Спим.

driver.quit()