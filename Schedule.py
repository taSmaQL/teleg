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
url = 'https://timetable.vsuet.ru/'

"""
Выбирать расписание на день, неделю, 
выгружать это в excel файл, узнавать есть ли изменения в расписание,
узнавать какая пара будет у другой группы
"""
