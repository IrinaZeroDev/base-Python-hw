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
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # убрать, если нужен обычный режим
    return webdriver.Chrome(ChromeDriverManager().install(), options=options)


def input_choice(prompt, options):
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                return choice
        except:
            pass
        print("Введите корректный номер действия.")


def iterate_paragraphs(driver):
    paras = driver.find_elements(By.CSS_SELECTOR, "#mw-content-text p")
    current = 0
    while True:
        if current < 0: current = 0
        if current >= len(paras):
            print("Больше параграфов нет.")
            return
        print(f"\n--- Параграф {current+1} ---\n{paras[current].text}\n")
        act = input_choice("1 - следующий, 2 - предыдущий, 3 - выйти: ", ['следующий', 'предыдущий', 'выйти'])
        if act == 1: current += 1
        elif act == 2: current -= 1
        elif act == 3: return


def choose_internal_link(driver):
    links = driver.find_elements(By.CSS_SELECTOR, "#mw-content-text a[href^='/wiki/']")
    shown = []
    for l in links:
        text = l.text.strip()
        href = l.get_attribute("href")
        if text and href and ": " not in text and text not in shown:
            shown.append(text)
        if len(shown) >= 10:
            break
    if not shown:
        print("Внутренних ссылок не найдено.")
        return None
    for idx, t in enumerate(shown, 1):
        print(f"{idx}. {t}")
    while True:
        try:
            choice = int(input("Введите номер внутренней статьи для перехода (или 0 для отмены): "))
            if choice == 0:
                return None
            elif 1 <= choice <= len(shown):
                for l in links:
                    if l.text.strip() == shown[choice-1]:
                        return l.get_attribute("href")
        except:
            pass
        print("Попробуйте ещё раз.")


def wiki_search():
    driver = get_driver()
    print("=== Поиск по Википедии ===")
    base_url = "https://ru.wikipedia.org/wiki/"
    query = input("Ваш запрос: ").strip().replace(" ", "_")
    
    while True:
        driver.get(base_url + query)
        print(f"\nОткрыта статья: {driver.title}\n")
        act = input_choice("Что делать дальше? ", [
            "листать параграфы текущей статьи",
            "перейти на одну из внутренних статей",
            "выйти из программы"
        ])
        if act == 1:
            iterate_paragraphs(driver)
        elif act == 2:
            href = choose_internal_link(driver)
            if href:
                # Извлекаем только "имя статьи"
                new_query = href.split("/wiki/")[-1]
                query = new_query
            else:
                print("Отмена перехода к другой статье.")
        elif act == 3:
            print("До свидания!")
            break
    driver.quit()


if __name__ == "__main__":
    wiki_search()
