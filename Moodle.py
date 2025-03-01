from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import tkinter as tk
from tkinter import messagebox
import time
import requests
from PIL import Image, ImageTk
from fake_useragent import UserAgent
useragent = UserAgent()
option = webdriver.ChromeOptions()
option.add_argument(f'user-agent={useragent.chrome}')
driver = webdriver.Chrome(options = option)
url = 'https://education.vsuet.ru/login/index.php'

'''
task: Если существует "блок", то распарсить на отдельные вопросы. Если вылезают
сколько-то вопросов одновременно, то парсер засчитывает как один
Пример: output.txt
'''

def start_parsing():
    students_username = username_entry.get()
    students_password = password_entry.get()
    test_id = id_entry.get()
    count = int(count_entry.get())
    matan = matan_entry.get()

    print("Данные для парсинга:")
    print(f"Логин: {students_username}")
    print(f"Пароль: {students_password}")
    print(f"ID теста: {test_id}")
    print(f"Количество вопросов: {count}")
    print(f"Есть ли картинки? {matan}")

    messagebox.showinfo("Парсинг", "Парсинг запущен!\nДанные сохранены в консоль.")

def open_parser():
    parser_window = tk.Toplevel()
    parser_window.title("Парсер вопросов")
    parser_window.geometry("400x400")

    image_path = r"C:\Users\user\Desktop\asd\123.jpg"
    image = Image.open(image_path)
    image = image.resize((400, 400), Image.Resampling.LANCZOS)
    background_image = ImageTk.PhotoImage(image)

    canvas = tk.Canvas(parser_window, width=400, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_image, anchor="nw")

    def place_left(widget, y_offset, x_offset=20):
        widget.place(x=x_offset, y=y_offset)

    global username_entry, password_entry, id_entry, count_entry, matan_entry

    label_login = tk.Label(parser_window, text="Логин:")
    place_left(label_login, y_offset=50)
    username_entry = tk.Entry(parser_window)
    place_left(username_entry, y_offset=80)

    label_password = tk.Label(parser_window, text="Пароль:")
    place_left(label_password, y_offset=120)
    password_entry = tk.Entry(parser_window, show='*')
    place_left(password_entry, y_offset=150)

    label_id = tk.Label(parser_window, text="ID теста:")
    place_left(label_id, y_offset=190)
    id_entry = tk.Entry(parser_window)
    place_left(id_entry, y_offset=220)

    label_count = tk.Label(parser_window, text="Количество вопросов:")
    place_left(label_count, y_offset=260)
    count_entry = tk.Entry(parser_window)
    place_left(count_entry, y_offset=290)

    label_images = tk.Label(parser_window, text="Есть ли картинки? (Да/Нет):")
    place_left(label_images, y_offset=330)
    matan_entry = tk.Entry(parser_window)
    place_left(matan_entry, y_offset=360)

    start_button = tk.Button(parser_window, text="Начать парсинг", command=start_parsing, width=15, height=2)
    place_left(start_button, y_offset=330, x_offset=200)
    
    parser_window.mainloop()

def auth_fun():
    messagebox.showinfo("Авторизация", "Добро пожаловать! \n\nПароль: 12345\n(шутка)")

def open_schedule():
    schedule_window = tk.Toplevel()
    schedule_window.title("Расписание")
    schedule_window.geometry("300x200")

    schedule_text = ""

    schedule_label = tk.Label(schedule_window, text=schedule_text, justify=tk.LEFT)
    schedule_label.pack(pady=20)

root = tk.Tk()
root.title("Главное меню")
root.geometry("300x200")

label = tk.Label(root, text="Выберите действие:", font=("Helvetica", 14))
label.pack(pady=20)

auth_button = tk.Button(root, text="Авторизация", command=auth_fun, width=20, height=2)
auth_button.pack(pady=10)

parser_button = tk.Button(root, text="Парсер", command=open_parser, width=20, height=2)
parser_button.pack(pady=10)

schedule_button = tk.Button(root, text="Расписание", command=open_schedule, width=20, height=2)
schedule_button.pack(pady=10)

def start_parsing():
    students_username = username_entry.get()
    students_password = password_entry.get()
    test_id = id_entry.get()
    count = int(count_entry.get())
    matan = matan_entry.get()
    attempt = 0
    max_attempts = 8
    urlstest = f'https://education.vsuet.ru/mod/quiz/view.php?id={test_id}'
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
        login_input = driver.find_element(By.ID,'username')
        login_input.clear()
        login_input.send_keys(students_username)
        password_input = driver.find_element(By.ID,'password')
        password_input.clear()
        password_input.send_keys(students_password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(1)
        driver.get(url=urlstest)
        time.sleep(1)
        amgis = driver.find_element(By.XPATH,"//button[@class='btn btn-primary']").click()
        time.sleep(1)
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'moodle-dialogue')]")))
        except Exception as ex:
            pass
        time.sleep(2)
        try:
            start_attempt_button = driver.find_element(By.XPATH, "//input[@id='id_submitbutton']")
            start_attempt_button.click()
            driver.switch_to.window(driver.window_handles[1]) 
        except Exception as ex:
            pass
            time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        driver.maximize_window()
        time.sleep(2)
        answers = {}
        if matan in ['Да', 'ДА', 'да']:
            for i in range(1, count + 1):
                sigma = driver.find_element(By.XPATH,f"(//span[@class='thispageholder'])[{i}]").click()
                time.sleep(2)
                test_element = driver.find_element(By.XPATH, "//div[@class='formulation clearfix']")
                images = test_element.screenshot_as_png
                filename = f'image_{i}.png'
                with open(filename, 'wb') as f:
                    f.write(images)
        else:
            with open('output.txt', 'w', encoding='utf-8') as file:
                for i in range(1, count + 1):
                    sigma = driver.find_element(By.XPATH,f"(//span[@class='thispageholder'])[{i}]").click()
                    question_element = driver.find_element(By.XPATH, "//div[@class='qtext']")
                    question_text = question_element.text
                    file.write(f"Вопрос {i}: {question_text}")
                    try:
                        answer_element = driver.find_element(By.XPATH,'//div[@class="answer"]')
                        answer_text = answer_element.text 
                        file.write(f" Варианты ответов:\n{answer_text}\n")
                    except NoSuchElementException:
                        try:
                            answer_elements = driver.find_elements(By.XPATH, '//tr[@class="r0"]/td/p | //tr[@class="r1"]/td/p')
                            for index, answer_element in enumerate(answer_elements):
                                answer_text = answer_element.text
                                file.write(f"{index + 1}-ая переменная: {answer_text}\n")
                        except NoSuchElementException:
                            print('Элементы с классом answer не найдены.')
                    option_elements = driver.find_elements(By.XPATH, '//option')
                    options = {option.get_attribute('value'): option.text for option in option_elements}
                    for value, text in options.items():
                        file.write(f"{value}-ый вариант ответа: {text}\n")
                    line = '-' * 69
                    file.write(f"{line}|\n")
    except Exception as ex:
        print(ex)
    finally: 
        time.sleep(3)
        driver.close()
        driver.quit()

root.mainloop()
