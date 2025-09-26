from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get("https://en.wikipedia.org/wiki/Document_Object_Model")
#В кавычках указываем URL сайта, на который нам нужно зайти
time.sleep(10)
#Задержка в 10 секунд
#browser.quit()
#Закрываем браузер

browser.get("https://ru.wikipedia.org/wiki/Selenium")

browser.get("https://en.wikipedia.org/wiki/Document_Object_Model")
#browser.save_screenshot("dom.png")
#В кавычках указываем название, которое присвоится скриншоту
#time.sleep(10)
#rowser.get("https://ru.wikipedia.org/wiki/Selenium")
#browser.save_screenshot("selenium.png")

#Добавляем перезагрузку страницы:

browser.get("https://en.wikipedia.org/wiki/Document_Object_Model")
browser.save_screenshot("dom.png")
time.sleep(5)
browser.get("https://ru.wikipedia.org/wiki/Selenium")
# browser.save_screenshot("selenium.png")
#time.sleep(3)
#browser.refresh()

from selenium import webdriver
from selenium.webdriver import Keys
#Библиотека, которая позволяет вводить данные на сайт с клавиатуры
from selenium.webdriver.common.by import By
#Библиотека с поиском элементов на сайте
import time