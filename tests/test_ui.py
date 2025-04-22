from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import autoit
import pyautogui
import os
import json
import datetime
import allure
import pytest
import random
import string
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
import telebot


binary_yandex_driver_file = r'C:\yandex_driver\chromedriver.exe' # ПУТЬ К ДРАЙВЕРУ
extension_path = r"C:\yandex_driver\1.2.13_0.crx" # Путь к директории расширения
options = webdriver.ChromeOptions()
options.add_experimental_option('detach',True)
options.add_extension(extension_path)
options.add_argument('--enable-logging')
#options.add_argument("--headless=new")
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
options.add_argument('--force-device-scale-factor=0.75') # Установка масштаба 
service = ChromeService(executable_path=binary_yandex_driver_file)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(10)
driver.maximize_window()

log_file_path_1 = "C:\Логи\Авторизация\Ошибки_авторизации.txt"
log_file_path_2 = "C:\Логи\Запрос\Ошибки_при_отправке_запроса.txt"
log_file_path_3 = "C:\Логи\Добавление объекта\Ошибки_сохранения_нового_объекта.txt"
log_file_path_4 = "C:\Логи\Скачивание bpmn\Ошибки_при_скачивании_bpmn.txt"
log_file_path_5 = "C:\Логи\Добавление пользователя\Ошибки_добавления_пользователя.txt"
log_file_path_6 = "C:\Логи\Выгрузка стандарта\Ошибки_выгрузки_стандарта.txt"
log_file_path_7 = "C:\Логи\Процес (заявление на отпуск)\Ошибки_при_регистрации.txt"
log_file_path_8 = "C:\Логи\Процес (заявление на отпуск)\Ошибки_при_завершении.txt"
log_file_path_9 = "C:\Логи\Процес (заявление на отпуск)\Ошибки_при_аннулировнии.txt"
log_file_path_10 = "C:\Логи\Стандарт по мета регламенту (otherMetaReglament)\Ошибки_выгрузки.txt"
log_file_path_11 = "C:\Логи\Стандарт по мета регламенту (otherMetaReglament)\Ошибки_отправки_в_архив.txt"
log_file_path_12 = "C:\Логи\Загрузка модулей\Ошибки_загрузки_модулей.txt"
log_file_path_13 = "C:\Логи\Процес (заявление на отпуск)\Ошибки_при_формировании_ПФ.txt"
log_file_path_14 = "C:\Логи\Процес (заявление на отпуск)\Ошибки_при_скачивании_сформированного_архива.txt"
log_file_path_16 = "C:\Логи\Процес (заявление на отпуск)\Ошибки_при_подписании_документа.txt"
log_file_path_17 = "C:\Логи\Формирование, скачивание отчета\Ошибки_при_формировании_отчета.txt"
log_file_path_18 = "C:\Логи\Формирование, скачивание отчета\Ошибки_при_скачивании_отчета.txt"

cookies_file_path = os.path.join(r'D:\Allure\Allure_all', 'cookies.json')

# Функция для сохранения сессии (куков)
def save_session(driver, cookies_file_path):
    cookies = driver.get_cookies()
    with open(cookies_file_path, 'w') as cookie_file:
        json.dump(cookies, cookie_file, indent=4)
    print(f"Куки сохранены в '{cookies_file_path}'.")

#АВТОРИЗАЦИЯ###########################################################################################################################################################################################################
#region
@allure.title("01-Тест авторизации через ЕСИА")
@allure.description("Проверка авторизации через ЕСИА и запись сетевых логов.")
def test_esia_auth():
    global auth_test_passed
    failed_steps = 0  # Счетчик неудачных шагов
    try:
        with allure.step("Открытие страницы авторизации"):
            driver.get("https://auth.pgs.gosuslugi.ru/auth/realms/DigitalgovTorkndProd1Auth/protocol/openid-connect/auth?client_id=DigitalgovTorkndProd1Auth-Proxy&state=b6fa62fc48c9м04787fa5bf095da2bafa&nonce=8bf3d529b0af28816d18e97bf560c4d3&response_type=code&redirect_uri=https%3A%2F%2Fpgs.gosuslugi.ru%2Fopenid-connect-auth%2Fredirect_uri&scope=openid")
            allure.attach(driver.get_screenshot_as_png(), name="auth_page", attachment_type=allure.attachment_type.PNG)

        with allure.step("Нажатие кнопки 'Вход через ЕСИА'"):
            esia_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='kc-social-providers']/ul")))
            esia_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="esia_button_click", attachment_type=allure.attachment_type.PNG)

        driver.implicitly_wait(20)

        with allure.step("Ввод телефона"):
            login_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/esia-root/div/esia-login/div/div[1]/form/div[1]/esia-input/input")))
            login_input = driver.find_element(By.XPATH, "/html/body/esia-root/div/esia-login/div/div[1]/form/div[1]/esia-input/input")
            login_input.click()
            driver.implicitly_wait(20)
            login_input.send_keys("+79374426231")
            allure.attach(driver.get_screenshot_as_png(), name="phone_input", attachment_type=allure.attachment_type.PNG)

        with allure.step("Ввод пароля"):
            password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/esia-root/div/esia-login/div/div[1]/form/div[2]/esia-input-password/div/input")))
            password_input = driver.find_element(By.XPATH, "/html/body/esia-root/div/esia-login/div/div[1]/form/div[2]/esia-input-password/div/input")
            password_input.click()
            driver.implicitly_wait(20)
            password_input.send_keys("S.pank470")
            allure.attach(driver.get_screenshot_as_png(), name="password_input", attachment_type=allure.attachment_type.PNG)

        with allure.step("Нажатие кнопки 'Войти'"):
            login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/esia-root/div/esia-login/div/div[1]/form/div[4]/button")))
            login_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="login_button_click", attachment_type=allure.attachment_type.PNG)

        with allure.step("Генерация и ввод TOTP-кода"):
            driver.execute_script("window.open('https://piellardj.github.io/totp-generator/?secret=AFDQSZB3NFBUCTBRSUEZ6NWCQIWCR66S&digits=6&period=30&algorithm=SHA-1')")
            driver.switch_to.window(driver.window_handles[1])
            copy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[3]/div/div[2]/div[1]/button")))
            copy_button.click()
            driver.implicitly_wait(20)
            driver.switch_to.window(driver.window_handles[0])
            code_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/esia-root/div/esia-login/div/div/esia-enter-mfa/esia-ttp/form/div[2]/div/esia-code-input/div/code-input/span[1]/input")))
            code_input.click()
            driver.implicitly_wait(20)
            code_input.send_keys(Keys.CONTROL + 'v')
            allure.attach(driver.get_screenshot_as_png(), name="totp_input", attachment_type=allure.attachment_type.PNG)

        driver.implicitly_wait(20)

        with allure.step("Нажатие кнопки 'Далее'"):
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/form/div/button[2]/div")))
            next_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="next_button_click", attachment_type=allure.attachment_type.PNG)

        # Сохранение куков после успешной авторизации
        save_session(driver, cookies_file_path)

        driver.implicitly_wait(20)
        with allure.step("Сбор сетевых логов"):
            driver.execute_cdp_cmd('Network.enable', {})
            log_entries = driver.get_log("performance")
            log_file_path = "network_log.txt"
            with open(log_file_path, "w") as log_file:
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                log_file.write("Ошибки_при_авторизации\n\n")
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path, name="network_log", attachment_type=allure.attachment_type.TEXT)

        # Ожидание загрузки страницы по наличию определенного элемента  
        wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#default-theme > evolenta-main-menu > div > div.header > div.branch-container > div > div > a")))   
        print(f"Файл '{log_file_path}' с результатом теста создан.")

        # Проверка наличия элемента после авторизации
        with allure.step("Проверка авторизации"):
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-main-menu/div/div[1]/div[1]/div/div/a"))
                )
                print("Элемент найден. Тест продолжается.")
                allure.attach(driver.get_screenshot_as_png(), name="Скрин главного экрана", attachment_type=allure.attachment_type.PNG)
            except TimeoutException:
                print("Тест не пройден: Элемент не найден. Ошибка авторизации.")
                failed_steps += 1  # Увеличиваем счётчик неудачных шагов
            except Exception as e:
                print(f"Ошибка в шаге: {e}")
                failed_steps += 1  # Увеличиваем счётчик неудачных шагов

    finally:
        if failed_steps > 0:
            # Завершаем тест с ошибкой, чтобы Allure мог сформировать отчёт, затем закрываем браузер
            try:
                allure.attach(driver.get_screenshot_as_png(), name="Скрин ошибки", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Тест не пройден: {failed_steps} ОШИБКА АВТОРИЗАЦИИ!!!.")
            finally:
                driver.quit()  # Закрываем браузер после завершения отчёта
        else:
            auth_test_passed = True  # Если ошибок не было, отмечаем тест как успешный
            print("Авторизация прошла успешно")
#endregion

#Смена организации#####################################################################################################################################################################################################
#region
@allure.title('02-тест Смена организации')
@allure.description("Проверка смены КНО")
def test_change_kno():
    try:
        with allure.step("Нажатие кнопки Сменить"):
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-main-menu/div/div[1]/div[1]/div/div/a")))
            next_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
        with allure.step("Нажатие кнопки КНО"):
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-select-branch/div/div[2]/div[2]/div/div/div[1]")))
            next_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#default-theme > evolenta-main-menu > div > div.header > div.branch-container > div > div > a")))
    except Exception as e:
        print(f"Ошибка в шаге: {e}")
#endregion

#СКАЧИВАНИЕ ОТЧЕТА#####################################################################################################################################################################################################
#region
@allure.title('03-тест Формирование, скачивание отчета')
@allure.description("Проверка формирования и скачивания отчета")
def test_report():
    try:
        with allure.step("Переход в модуль Отчеты"):
            driver.get('https://pgs.gosuslugi.ru/reports/reports')
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#adaptive_navbar_undefined > div > div > button")))
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Нажатие кнопки Новый отчет"):
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/evolenta-adaptive-navbar/div/div/div/button/b")))
            next_button.click()
            time.sleep(5)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Выбор вида отчета"):
            # Активация, заполнение поля Поиск
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/evolenta-adaptive-navbar/div/div/div/div[1]/div/input")))
            input_field.click() 
            time.sleep(2)
            input_field.send_keys("Показатель Цифровой зрелости")
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/evolenta-adaptive-navbar/div/div/div/div[1]/div/div/button")))
            next_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
            time.sleep(3)
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/div[2]/div[2]/div/div/div[1]/div/evolenta-infinite-scrollbar/div/div/div[1]/div")))
            next_button.click()
            time.sleep(2)  
            element = driver.find_element(By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/div[2]/div[2]/div/div/div[1]/div/evolenta-infinite-scrollbar/div/div/div[1]/div[2]/button")
            element.click()
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#sidebar_wrapper_undefined > div.wrapper.sidebar-route-show.border-line.ng-star-inserted > div > div > div.heading-elements > button:nth-child(1)")))
    
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:        
        with allure.step("Нажатие кнопки Сформировать"):    
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-report-wrapper/evolenta-custom-report/div/evolenta-sidebar-wrapper/div/div[1]/div/div/div[2]/button[1]")))
            next_button.click()
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[contains(text(), 'Сформирован')]")))                                                                  
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
            print(f"Ошибка в шаге: {e}")

    try: 
        with allure.step("Сбор сетевых логов"):
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_17, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки при нажатии кнопки 'Сформировать отчет'\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_17, name="network_log", attachment_type=allure.attachment_type.TEXT)
            print(f"Файл '{log_file_path_17}' с результатом теста создан.")
            time.sleep(5)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:    
        with allure.step("Нажатие кнопки Скачать"):     
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-report-wrapper/evolenta-custom-report/div/evolenta-sidebar-wrapper/div/div[1]/div/div/div[2]/button[3]")))
            next_button.click()
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)

            with allure.step("Сбор сетевых логов"):
                driver.execute_cdp_cmd('Network.enable', {})
                # Запись записей в сетевом журнале
                log_entries = driver.get_log("performance") 
                # Открываем файл для записи ошибок
                with open(log_file_path_18, "w") as log_file:
                # Добавляем текущую дату и время перед записью логов
                    current_datetime = datetime.datetime.now()
                    log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                    # Записываем заголовок
                    log_file.write("Ошибки при нажатии кнопки 'Скачать отчет'\n\n")    
                    for entry in log_entries:
                        try:
                            message_obj = json.loads(entry.get("message"))
                            message = message_obj.get("message")
                            method = message.get("method")
                            if method == 'Network.responseReceived':
                                response = message.get('params', {}).get('response', {})
                                response_url = response.get('url', '')
                                response_status = response.get('status', 0)
                                response_headers = response.get('headers', {})
                                response_body = response.get('body', '')
                                if response_status >= 400:
                                    log_file.write("Response URL: {}\n".format(response_url))
                                    log_file.write("Response Status: {}\n".format(response_status))
                                    log_file.write("Response Headers: {}\n".format(response_headers))
                                    log_file.write("Response Body: {}\n".format(response_body))
                                    log_file.write("\n")
                        except Exception as e:
                            print(e)
                    # Добавляем разделитель в конце файла
                    log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
                allure.attach.file(log_file_path_17, name="network_log", attachment_type=allure.attachment_type.TEXT)
                print(f"Файл '{log_file_path_18}' с результатом теста создан.")
    except Exception as e:
        print(f"Ошибка в шаге: {e}")
        time.sleep(3)
#endregion

#ПРОЦЕСС###############################################################################################################################################################################################################
#region
@allure.title('04-тест Создание процесса "Заявление на отпуск"')
@allure.description("Проверка создания заявления")
def test_process():    
    try:    
        with allure.step("Переход в модуль Прочие процессы "):
            driver.get('https://pgs.gosuslugi.ru/other-processes/appeals')
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#default-theme > evolenta-sidebar > evolenta-section > common-appeals > div.navbar.navbar-default.no-padding.no-border-top.navbar-inside-component > button")))
            
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}") 

    try:
        with allure.step("Нажатие кнопки Добавить процесс"):
            button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Добавить процесс')]")))
            button.click()
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#default-theme > evolenta-sidebar > div > div > evolenta-navigator > evolenta-scrollbar > div > ul > li:nth-child(2) > label > a")))
            
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
            # Активация, заполнение поля Код
            input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Код...']")))
            input_field.click() 
            input_field.send_keys("53354")
            time.sleep(5)
            # Нажать на стандарт
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/services/div[2]/div[2]/div/div/div[1]/div/evolenta-infinite-scrollbar/div/div/div/div[1]/div[1]/div/div")))
            next_button.click()
            # Дождаться, когда появится скрытая кнопка
            hidden_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/services/div[2]/div[2]/div/div/div[1]/div/evolenta-infinite-scrollbar/div/div/div/div[1]/div[1]/div[2]/span")))
            
            #//button[text()='Создать']
            # Нажать на скрытую кнопку
            hidden_button.click()
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#default-theme > evolenta-sidebar > evolenta-section > common-appeal > div.page-container > div.sidebar.sidebar-secondary.sidebar-default > div > evolenta-scrollbar > div > evolenta-common-appeal-tabs > div:nth-child(2) > div")))
            
    except Exception as e:
           print(f"Ошибка в шаге: {e}") 

    try:
        with allure.step("Добавление работника"):
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/div/common-appeal-blocks/div[1]/div/common-appeal-common/div/common-appeal-subjects/div/fieldset/div/div/a")))
            next_button.click()
            # ФЛ
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/div/common-appeal-blocks/div[1]/div/common-appeal-common/div/common-appeal-subjects/common-appeal-subject-card/div/div[2]/div/div[2]/label")))
            next_button.click()
            # Активация, заполнение поля ФИО
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/div/common-appeal-blocks/div[1]/div/common-appeal-common/div/common-appeal-subjects/common-appeal-subject-card/div/div[2]/subject-form/div/form/fieldset[1]/div/div/div[1]/div[1]/div/input")))
            input_field.click() 
            input_field.send_keys("Иванов Иван Иванович")
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}") 

    try:
        with allure.step("Нажатие кнопки Применить"):    
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/div/common-appeal-blocks/div[1]/div/common-appeal-common/div/common-appeal-subjects/common-appeal-subject-card/div/div[1]/div[2]/button[1]")))
            next_button.click()
            time.sleep(4)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}") 

    try:    
        with allure.step("Добавление объекта"):  
            # Нажать Объекты
            span = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Объекты')]")))
            span.click()
            time.sleep(3)
            # Нажать Добавить
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/div/common-appeal-blocks/div[4]/div/common-appeal-objects/div/button[1]")))
            next_button.click()
            time.sleep(2)
             # Нажать Выбрать из реестра
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/div/common-appeal-blocks/div[4]/div/common-appeal-objects/common-appeal-object-card/div/div[2]/div[1]/div/div/div[2]/button")))
            next_button.click()
            time.sleep(3)
             # Нажать Активировать чекбокс
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/persons-transfer/app-ais-objects/div[2]/div[2]/div/div/div[1]/div/evolenta-infinite-scrollbar/div/div/div[1]/div[1]/div[2]/div/h6")))
            actions = ActionChains(driver)
            actions.double_click(element).perform()
            time.sleep(1)
             # Нажать Вернуться к операции
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/persons-transfer/app-ais-objects/div[1]/button")))
            next_button.click()
            time.sleep(3)
             # Нажать Применить
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/div/common-appeal-blocks/div[4]/div/common-appeal-objects/common-appeal-object-card/div/div[1]/div[2]/button[1]")))
            next_button.click()
            time.sleep(1)

            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")
        
    try:
        with allure.step("Нажатие кнопки Сохранить"):       
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[1]/button")))
            next_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
            # Ожидание завершения регистрации (замените XPATH на реальный элемент, который появляется после регистрации)
            registration_complete_element = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Регистрация')]"))) 
    except Exception as e:
           print(f"Ошибка в шаге: {e}") 

    try:
        with allure.step("Нажатие кнопки Регистрация"): 
            next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Регистрация')]")))
            next_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Сбор сетевых логов"):
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_7, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки при нажатии кнопки 'Регистрация'\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_7, name="network_log", attachment_type=allure.attachment_type.TEXT)
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#default-theme > evolenta-sidebar > evolenta-section > common-appeal > div.page-container > div.sidebar.sidebar-secondary.sidebar-default > div > evolenta-scrollbar > div > evolenta-entity-process-events > div > button")))
                   
            print(f"Файл '{log_file_path_7}' с результатом теста создан.")
    except Exception as e:
           print(f"Ошибка в шаге: {e}")
    driver.refresh
    # Ожидание загрузки страницы по наличию определенного элемента  
    wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#default-theme > evolenta-sidebar > evolenta-section > common-appeal > div.page-container > div.sidebar.sidebar-secondary.sidebar-default > div > evolenta-scrollbar > div > evolenta-entity-process-events > div > button")))
        
    try:        
        with allure.step("Переход во вкладку документы"):
            # Нажать документы
            span = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Документы')]")))             
            span.click()
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:       
        with allure.step("Добавление заявления"):     
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/div/common-appeal-blocks/div[3]/div/evolenta-common-appeal-documents/div/evolenta-common-appeal-subservice-document-groups[1]/div[1]/div[1]/div/button")))
            next_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Формирование ПФ"):     
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/div/common-appeal-blocks/div[3]/div/evolenta-common-appeal-documents/div/evolenta-common-appeal-subservice-document-groups[1]/div[1]/div[2]/evolenta-common-appeal-document-card/div/div[2]/button[1]")))
            next_button.click()
            time.sleep(10)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Сбор сетевых логов"):
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_13, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки при формировании ПФ\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_13, name="network_log", attachment_type=allure.attachment_type.TEXT)

            print(f"Файл '{log_file_path_13}' с результатом теста создан.")
            time.sleep(5)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:        
        with allure.step("Нажатие кнопки Прикрепить"):     
            # Нажать прикрепить
            file_input = driver.find_element(By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/div/common-appeal-blocks/div[3]/div/evolenta-common-appeal-documents/div/evolenta-common-appeal-subservice-document-groups[1]/div[1]/div[2]/evolenta-common-appeal-document-card/div/div[2]/label")
            file_input.click()
            time.sleep(2)
            # Найти поле загрузки файла и отправить путь к файлу
            file_input = driver.find_element(By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/div/common-appeal-blocks/div[3]/div/evolenta-common-appeal-documents/div/evolenta-common-appeal-subservice-document-groups[1]/div[1]/div[2]/evolenta-common-appeal-document-card/div/div[2]/input")
            file_input.send_keys(r"C:\Папка с файлами\blank-zayavleniya-na-otpusk.docx")
            # Подождать некоторое время перед переходом к следующему шагу
            time.sleep(3)
            # Закрыть окно выбора файла с помощью нажатия клавиши ESC
            pyautogui.press('esc')
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:    
        with allure.step("Скачивание сформированного файла"):   
            file_input = driver.find_element(By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/div/common-appeal-blocks/div[3]/div/evolenta-common-appeal-documents/div/evolenta-common-appeal-subservice-document-groups[1]/div[1]/div[2]/evolenta-common-appeal-document-card/evolenta-common-appeal-document-files/div/table/tbody/tr/div/div/td[1]/a")
            file_input.click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
            time.sleep(3)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:    
        with allure.step("Сбор сетевых логов"):
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_14, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки при скачивании сформированного архива\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_14, name="network_log", attachment_type=allure.attachment_type.TEXT)      
            print(f"Файл '{log_file_path_14}' с результатом теста создан.")
            time.sleep(3)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:        
        with allure.step("Нажатие кнопки Подписать"):   
            file_input = driver.find_element(By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/div/common-appeal-blocks/div[3]/div/evolenta-common-appeal-documents/div/evolenta-common-appeal-subservice-document-groups[1]/div[1]/div[2]/evolenta-common-appeal-document-card/evolenta-common-appeal-document-files/div/table/tbody/tr[1]/div/div/td[1]/evolenta-file-signing/span")
            file_input.click()
            time.sleep(3)
            # Переместить курсор мыши в центр экрана
            screen_width, screen_height = pyautogui.size()
            pyautogui.moveTo(screen_width / 2, screen_height / 2)
            # Выполнить клик мыши
            pyautogui.click()
            # Нажать клавишу TAB
            pyautogui.press('tab')
            time.sleep(1)
            # Нажать клавишу Enter
            pyautogui.press('enter')
            # Закрытие веб-драйвера
            time.sleep(4)
            #Нажать на радиокнопку
            file_input = driver.find_element(By.XPATH, "/html/body/modal-container/div/div/div[2]/div/label")
            file_input.click()
            #Нажать Выбрать
            file_input = driver.find_element(By.XPATH, "/html/body/modal-container/div/div/div[3]/button[2]")
            file_input.click()
            time.sleep(2)
            #Нажать НЕТ
            file_input = driver.find_element(By.XPATH, "/html/body/modal-container/div/div/div[3]/button[2]")
            file_input.click()
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")
    
    try:
        with allure.step("Сбор сетевых логов"):
            # Включить отслеживание сети
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_16, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки при подписании\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_16, name="network_log", attachment_type=allure.attachment_type.TEXT)        
            print(f"Файл '{log_file_path_16}' с результатом теста создан.")
            time.sleep(5)   
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:    
        with allure.step("Нажатие кнопки Сохранить"):     
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[1]/button")))
            next_button.click()
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин2", attachment_type=allure.attachment_type.PNG)          
            # Нажать Пользовательская задача
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[1]/div/evolenta-scrollbar/div/evolenta-entity-process-events/div/button")))
            next_button.click()
            time.sleep(5)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")
    

    #Заполнение поля с датой

    #date_input = driver.find_element(By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[2]/evolenta-scrollbar/div/div/evolenta-entity-process-events/div/div[2]/evolenta-entity-process-element-data/fieldset[1]/div/evolenta-entity-process-element-additional-data-tab/evolenta-dynamic-form/div/evolenta-form-render/form/formly-form/formly-field[1]/formly-wrapper-form-field/div/evolenta-form-render-date-picker/evolenta-datepicker/div/div/input[2]")
    # Получаем текущую дату в нужном формате
    #current_date = datetime.now().strftime("%d-%m-%Y")

    # Вставляем дату в поле
    #date_input.send_keys(current_date)

    # Нажатие  Завершить
    #next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Завершить')]")))
    #next_button.click()
    #time.sleep(5)

    try:    
        with allure.step("Нажатие кнопки Завершить 1"):
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[1]/div/evolenta-scrollbar/div/evolenta-entity-process-events/div/button[1]")))
            next_button.click()
            time.sleep(5)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:    
        with allure.step("Нажатие кнопки Завершить"):
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[1]/div/evolenta-scrollbar/div/common-appeal-actions/div/button[1]")))
            next_button.click()
            time.sleep(5)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:    
        with allure.step("Сбор сетевых логов"):
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_8, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки при нажатии кнопки 'Завершить'\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_8, name="network_log", attachment_type=allure.attachment_type.TEXT)
            
            print(f"Файл '{log_file_path_8}' с результатом теста создан.")
            #Ожидание завершения регистрации (замените XPATH на реальный элемент, который появляется после регистрации)
            #registration_complete_element = WebDriverWait(driver, 120).until(
                #EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Аннулировать')]")))
    except Exception as e:
           print(f"Ошибка в шаге: {e}")
           time.sleep(10)

    try:    
        with allure.step("Нажатие кнопки Аннулировать"):
            # Нажать Аннулировать
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/common-appeal/div[2]/div[1]/div/evolenta-scrollbar/div/common-appeal-actions/div/button")))
            next_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")        

    try:    
        with allure.step("Сбор сетевых логов"):
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_9, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки при нажатии кнопки 'Аннулировать'\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_9, name="network_log", attachment_type=allure.attachment_type.TEXT)
            
            print(f"Файл '{log_file_path_9}' с результатом теста создан.")
    except Exception as e:
           print(f"Ошибка в шаге: {e}")        
            
    try:
        with allure.step("Скопировать ссылку на процесс"):
            # Получить текущий URL страницы
            current_url = driver.current_url
            
            # Вывод ссылки в консоль для проверки
            print(f"Текущая ссылка: {current_url}")
            
            # Вложить ссылку в отчет Allure
            allure.attach(current_url, name="Ссылка на процесс", attachment_type=allure.attachment_type.TEXT)
            
            print("Ссылка на текущую страницу добавлена в отчет Allure")
            time.sleep(10)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")
#endregion

#СТАНДАРТ (otherMetaReglament)#########################################################################################################################################################################################
#region
@allure.title('05-тест Создание и выгрузка стандарта по мета регламенту "Типовой мета-регламент для прочих бизнес-процессов (отпуск) (otherMetaReglament)"')
@allure.description("Проверка создания и выгрузки стандарта")
def test_standart_otpusk():
    wait = WebDriverWait(driver, 30)  # <-- Добавь это в начале функции
    try:
        with allure.step("Переход в модуль Проектирование стандартов ---> Стандарты"):
            driver.get('https://pgs.gosuslugi.ru/specialist/common-standards/create')
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#default-theme > evolenta-sidebar > div > div > evolenta-navigator > evolenta-scrollbar > div > ul > li.tab.current > label > a")))
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Выбор мета-регламента"):    
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/div/evolenta-scrollbar/div/div/evolenta-catalogue/div/div[1]/input")))
            input_field.click()
            time.sleep(2)
            input_field.send_keys("для прочих бизнес-процессов")
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
            time.sleep(10)
            
            button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/div/evolenta-scrollbar/div/div/evolenta-catalogue/div/div[2]/ul/li")))
            button.click()
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#sidebar_wrapper_undefined > div > evolenta-common-standard-menu > div > evolenta-scrollbar > div > div:nth-child(3) > div")))
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Активация, заполнение поля Наименование"):    
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-common/div/div/div[1]/input")))
            input_field.click()
            input_field.send_keys("Заявление на отпуск (образец- auto-test)!!!")
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Активация, заполнение поля Краткое наименование"):       
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-common/div/div/div[2]/input")))
            input_field.click() 
            input_field.send_keys("Заявление на отпуск (auto-test)")
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")
           
    try:
        with allure.step("Переход во вкладку Работник"):
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-common-standard-menu/div/evolenta-scrollbar/div/div[2]/div")))
            next_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Заполнение вкладки"):
            # Активация, заполнение поля "Минимум"
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/div[1]/div/fieldset/div/div/div[1]/div/input")))
            input_field.click() 
            input_field.send_keys("1")
            # Активация, заполнение поля "Максимум"
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/div[1]/div/fieldset/div/div/div[2]/div/input")))
            input_field.click() 
            input_field.send_keys("1")
            # Выбрать параметр чекбокса 
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[1]/table/tbody/tr[1]/td[1]/label")))
            parameter_radio.click()
            # Выбрать параметр чекбокса 
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[1]/table/tbody/tr[1]/td[4]/label")))
            parameter_radio.click()
            # Выбрать параметр чекбокса
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[1]/table/tbody/tr[1]/td[5]/label")))
            parameter_radio.click()
            # Выбрать параметр чекбокса
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[1]/table/tbody/tr[2]/td[1]/label")))
            parameter_radio.click()
            # Выбрать параметр чекбокса 
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[1]/table/tbody/tr[2]/td[4]/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[1]/table/tbody/tr[2]/td[5]/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[1]/table/tbody/tr[3]/td[1]/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[1]/table/tbody/tr[3]/td[2]/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/div[10]/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[2]/evolenta-common-standard-statuses-permissions/div/table/tbody/tr[1]/td[1]/div/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[2]/evolenta-common-standard-statuses-permissions/div/table/tbody/tr[2]/td[1]/div/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[2]/evolenta-common-standard-statuses-permissions/div/table/tbody/tr[3]/td[1]/div/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[2]/evolenta-common-standard-statuses-permissions/div/table/tbody/tr[4]/td[1]/div/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[2]/evolenta-common-standard-statuses-permissions/div/table/tbody/tr[5]/td[1]/div/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[2]/evolenta-common-standard-statuses-permissions/div/table/tbody/tr[6]/td[1]/div/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[2]/evolenta-common-standard-statuses-permissions/div/table/tbody/tr[2]/td[2]/div/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[2]/evolenta-common-standard-statuses-permissions/div/table/tbody/tr[3]/td[2]/div/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[2]/evolenta-common-standard-statuses-permissions/div/table/tbody/tr[5]/td[2]/div/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[2]/evolenta-common-standard-statuses-permissions/div/table/tbody/tr[6]/td[2]/div/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[2]/evolenta-common-standard-statuses-permissions/div/table/tbody/tr[3]/td[3]/div/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[2]/evolenta-common-standard-statuses-permissions/div/table/tbody/tr[6]/td[3]/div/label")))
            parameter_radio.click()
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-subjects/div/evolenta-common-standard-subjects-common/fieldset[2]/evolenta-common-standard-statuses-permissions/div/table/tbody/tr[3]/td[4]/div/label")))
            parameter_radio.click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
            time.sleep(3)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Переход в вкладку Бизнес-процессы"):    
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-common-standard-menu/div/evolenta-scrollbar/div/div[4]/div")))
            next_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)

        with allure.step("Добавление нового процесса"):     
            # Нажать кнопку Добавить новый процесс
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-processes/evolenta-common-standard-bpmn-process/div/button[2]/b")))
            next_button.click()
            # Активация, заполнение поля "Наименование процесса"
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-processes/evolenta-common-standard-bpmn-process/evolenta-bpmn-process-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-scrollbar/div/div/div[2]/form/div[1]/div[1]/div/input")))
            input_field.click() 
            input_field.send_keys("Процесс согласования заявления работника на отпуск")
            # Нажать кнопку Уровень
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-processes/evolenta-common-standard-bpmn-process/evolenta-bpmn-process-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-scrollbar/div/div/div[2]/form/div[1]/div[2]/div/ng-select/div/div/div[2]")))
            next_button.click()
            # Нажать кнопку Региональный
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-processes/evolenta-common-standard-bpmn-process/evolenta-bpmn-process-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-scrollbar/div/div/div[2]/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
            next_button.click()
            # Нажать кнопку Загрузить
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-processes/evolenta-common-standard-bpmn-process/evolenta-bpmn-process-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-scrollbar/div/div/div[2]/div[2]/label")))
            next_button.click()                                                                
            # Найти поле загрузки файла и отправить путь к файлу
            file_input = driver.find_element(By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-processes/evolenta-common-standard-bpmn-process/evolenta-bpmn-process-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-scrollbar/div/div/div[2]/div[2]/input")
            file_input.send_keys(r"C:\Папка с файлами\225732309_bpmn1_задача с таймером.bpmn")
            # Подождать некоторое время перед переходом к следующему шагу
            time.sleep(3)
            # Закрыть окно выбора файла с помощью нажатия клавиши ESC
            pyautogui.press('esc')
            # Нажать кнопку Применить
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-processes/evolenta-common-standard-bpmn-process/evolenta-bpmn-process-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-scrollbar/div/div/div[1]/div/button[1]")))
            next_button.click()
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#sidebar_wrapper_undefined > evolenta-common-standard-blocks > evolenta-scrollbar > div > div > evolenta-common-standard-common > div > div > div.checkbox-block.no-padding-top.pb-20 > label")))
            # Нажать вкладку Бизнес-процессы
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-common-standard-menu/div/evolenta-scrollbar/div/div[4]/div")))
            next_button.click()
            time.sleep(3)
            # Нажать кнопку Формы дополнительных данных
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-processes/div/ul/li[2]")))
            next_button.click()
            # Нажать кнопку Добавить
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-processes/div[2]/div[1]/div/button")))
            next_button.click()
            # Активация, заполнение поля "Код"
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-processes/div/div[2]/div/div[1]/div[1]/div/input")))
            input_field.click() 
            input_field.send_keys("order")
            # Активация, заполнение поля "Наименование"
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-processes/div/div[2]/div/div[1]/div[2]/div/input")))
            input_field.click() 
            input_field.send_keys("Приказ")
            # Нажать кнопку Применить
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-processes/div/div[1]/div/button[1]")))
            next_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Добавление документов"):        
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-common-standard-menu/div/evolenta-scrollbar/div/div[3]/div")))
            next_button.click()
            # Нажать кнопку Добавить группу документов
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-documents/div/evolenta-common-standard-documents-list/button")))
            next_button.click()
            # Активация, заполнение поля "Наименование"
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-documents/div/evolenta-common-standard-documents-list/evolenta-common-standard-document-group-edit/div/div[2]/div/evolenta-dynamic-form/div/evolenta-form-render/form/formly-form/formly-field/formly-group/formly-field[1]/formly-wrapper-form-field/div/evolenta-form-render-input/input")))
            input_field.click() 
            input_field.send_keys("Заявление работника на отпуск")
            # Нажать Применить
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-documents/div/evolenta-common-standard-documents-list/evolenta-common-standard-document-group-edit/div/div[1]/div/button[1]")))
            parameter_radio.click()
            # Нажать Печатные формы
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-documents/div/ul/li[3]")))
            parameter_radio.click()
            # Нажать Выбрать ПФ
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-documents/div/evolenta-common-standard-print-forms/div/button")))
            parameter_radio.click()
            time.sleep(10)
            # Активация, заполнение поля "Наименование"
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/div[2]/div[1]/div/evolenta-filters-bar/evolenta-scrollbar/div/div/div/div/div[2]/div[2]/div/div/form/div/input")))
            input_field.click() 
            input_field.send_keys("Заявление на отпуск 3444")
            time.sleep(3)
            # Нажать на ПФ
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/div[2]/div[2]/div/div/div[1]/div/evolenta-infinite-scrollbar/div/div/div[1]/div[2]/div[2]/h6")))
            actions = ActionChains(driver)
            actions.double_click(element).perform()
            # Нажать Вернуться
            parameter_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/evolenta-adaptive-navbar/div/div/div/button")))
            parameter_radio.click()
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#sidebar_wrapper_undefined > div > evolenta-common-standard-menu > div > evolenta-scrollbar > div > div.mt-30 > div > div > ul > li:nth-child(1) > div > button.btn.btn-menu-action.no-white-space.bg-blue-800.text-center.p-5.width-100")))
            
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Добавление организации"):     
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-common-standard-menu/div/evolenta-scrollbar/div/div[5]/div")))
            next_button.click()
            # Нажать кнопку Выбрать организации
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-organizations/div/button")))
            next_button.click()
            time.sleep(3)
            # Активация, заполнение поля Поиск
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/evolenta-adaptive-navbar/div/div/div/div[1]/div/input")))
            input_field.click() 
            input_field.send_keys('QA Эволента (ООО "НТ")')
            time.sleep(3)
            # Нажать кнопку Поиск
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/evolenta-adaptive-navbar/div/div/div/div[1]/div/div/button")))
            next_button.click()
            time.sleep(3)
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/div[2]/div[2]/div/div/div[1]/div/evolenta-infinite-scrollbar/div/div/div[1]/div[2]/div[2]/h6")))
            actions = ActionChains(driver)
            actions.double_click(element).perform()
            time.sleep(3)
            # Нажать кнопку Вернуться к операции
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/evolenta-adaptive-navbar/div/div/div/button")))
            next_button.click()
            
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:       
        with allure.step("Нажатие кнопки Сохранить"):        
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/evolenta-adaptive-navbar/div/div/div/button")))
            next_button.click()
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
            time.sleep(7)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин2", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Нажатие кнопки Выгрузить"):       
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-common-standard-menu/div/evolenta-scrollbar/div/div[10]/div/div/ul/li[3]/button")))
            next_button.click()
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#toast-container > div")))
            
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин2", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")  

    try:
        with allure.step("Сбор сетевых логов"):
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_10, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки при нажатии кнопки 'Выгрузить'\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_10, name="network_log", attachment_type=allure.attachment_type.TEXT)
            
            print(f"Файл '{log_file_path_10}' с результатом теста создан.")
            time.sleep(1)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")  

    try:
        with allure.step("Нажатие кнопки Отправить в архив"): 
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-common-standard-menu/div/evolenta-scrollbar/div/div[10]/div/div/ul/li[2]/div/button[2]")))
            next_button.click()
            time.sleep(1)
            # Подтверждение
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/modal-container/div/div/div[3]/button[1]")))
            next_button.click()
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")  
            
    try:        
        with allure.step("Сбор сетевых логов"):
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_11, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки при нажатии кнопки 'Отправить в архив'\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_10, name="network_log", attachment_type=allure.attachment_type.TEXT)
            
            print(f"Файл '{log_file_path_11}' с результатом теста создан.")
            time.sleep(10)
    except Exception as e:
           print(f"Ошибка в шаге: {e}")  

    try:
        with allure.step("Скопировать ссылку на стандарт"):
            # Получить текущий URL страницы
            current_url = driver.current_url
            
            # Вывод ссылки в консоль для проверки
            print(f"Текущая ссылка: {current_url}")
            
            # Вложить ссылку в отчет Allure
            allure.attach(current_url, name="Ссылка на остандарт", attachment_type=allure.attachment_type.TEXT)
            
            print("Ссылка на текущую страницу добавлена в отчет Allure")
            time.sleep(2)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")
#endregion

#СКАЧИВАНИЕ BPMN########################################################################################################################################################################################################
#region
#СКАЧИВАНИЕ BPMN 
@allure.title('06-тест Скачивание bpmn')
@allure.description("Проверка скачивания bpmn схемы")
def test_bpmn():
    try:
        with allure.step("Переход в стандарт"):
            driver.get('https://pgs.gosuslugi.ru/other-processes/common-standards/edit/65e1c3cbc920852fd9170f15')
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#sidebar_wrapper_undefined > div > evolenta-common-standard-menu > div > evolenta-scrollbar > div > div:nth-child(2) > div")))
            
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Переход во вкладку Бизнес процессы"):
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-common-standard-menu/div/evolenta-scrollbar/div/div[4]/div")))
            next_button.click()
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Нажатие кнопки Скачать"):    
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/evolenta-common-standard-blocks/evolenta-scrollbar/div/div/evolenta-common-standard-processes/evolenta-common-standard-bpmn-process/div/evolenta-common-bpmn-card/div/div[1]/h4/div/a[1]")))
            next_button.click()
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Сбор сетевых логов"):    
            # Включить отслеживание сети
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_4, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки при скачивании Bpmn схемы\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_4, name="network_log", attachment_type=allure.attachment_type.TEXT)
            print(f"Файл '{log_file_path_4}' с результатом теста создан.")
            time.sleep(3)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")
#endregion

#ВЫГРУЗКА СТАНДАРТА#####################################################################################################################################################################################
#region
@allure.title('07-тест Выгрузка стандарта')
@allure.description("Проверка скачивания выгрузки стандарта")
def test_standart():
    try:
        with allure.step("Нажатие кнопки Выгрузить"): 
            # Нажать выгрузить
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-common-standard-edit/div/evolenta-sidebar-wrapper/div/div/evolenta-common-standard-menu/div/evolenta-scrollbar/div/div[10]/div/div/ul/li[4]/button")))
            next_button.click()
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин2", attachment_type=allure.attachment_type.PNG)
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин3", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Сбор сетевых логов"):    
            # Включить отслеживание сети
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_6, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки_при_нажатии_'Выгрузить'\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_6, name="network_log", attachment_type=allure.attachment_type.TEXT)
            print(f"Файл '{log_file_path_6}' с результатом теста создан.")
            time.sleep(15)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")  
    
#endregion


#ДОБАВЛЕНИЕ ОБЪЕКТА#####################################################################################################################################################################################################
#region
@allure.title('08-тест Добавление объекта')
@allure.description("Проверка добавления объекта")
def test_new_object():
    try:
        with allure.step("Переход в модуль Объекты"):
            driver.get('https://pgs.gosuslugi.ru/registers/objects/kno')
            # Ожидание загрузки страницы по наличию определенного элемента  
            wait = WebDriverWait(driver, 30)  # Таймаут 30 секунд
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#default-theme > evolenta-sidebar > evolenta-section > persons-transfer > app-ais-objects > div.navbar.navbar-default.no-padding-left.no-border-top.navbar-inside-component > button")))
            
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)       
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/persons-transfer/app-ais-objects/div[1]/button")))
            next_button.click()
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Нажать кнопку Не выбрано"):
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/persons-transfer/app-ais-object-edit/div[2]/div[2]/evolenta-scrollbar/div/div/div/form/div/div/span")))
            next_button.click()
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)  
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Активация, заполнение поля Код"):    
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/div[2]/div[1]/div/evolenta-filters-bar/evolenta-scrollbar/div/div/div/div/div[1]/div[2]/div/div/form/div/input")))
            input_field.click() 
            input_field.send_keys("2626")
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)  

            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/div[2]/div[2]/div/div/div[1]/div/evolenta-infinite-scrollbar/div/div/div[1]/div[2]/div[2]/h6")))
            actions = ActionChains(driver)                                                     
            actions.double_click(element).perform()
            # Нажать кнопку "Вернуться к операции"
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/evolenta-adaptive-navbar/div/div/div/button")))                                                                                    
            next_button.click()
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:        
        with allure.step("Активация, заполнение поля Наименование"):
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/persons-transfer/app-ais-object-edit/div[2]/div[2]/evolenta-scrollbar/div/div/div/form/div[2]/div[1]/div[1]/div/div[1]/input")))
            input_field.click() 
            input_field.send_keys("Тестовый объект")
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)     
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:        
        with allure.step("Заполнение поля Краткое Наименование"):
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/persons-transfer/app-ais-object-edit/div[2]/div[2]/evolenta-scrollbar/div/div/div/form/div[2]/div[1]/div[2]/div/div[1]/input")))
            input_field.click()
            input_field.send_keys("тест")
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:        
        with allure.step("Заполнение поля Адрес объекта"):
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/persons-transfer/app-ais-object-edit/div[2]/div[2]/evolenta-scrollbar/div/div/div/form/div[2]/div[2]/div[2]/div/evolenta-address-gar/div/div[2]/div/div/input")))
            input_field.click()
            input_field.send_keys("г. Москва, ул. Большая Бронная, д. 2/6")
            time.sleep(3)
            element_to_hover_over = driver.find_element(By.XPATH, '/html/body/app-root/div/evolenta-sidebar/evolenta-section/persons-transfer/app-ais-object-edit/div[2]/div[2]/evolenta-scrollbar/div/div/div/form/div[2]/div[2]/div[2]/div/evolenta-address-gar/div/div[2]/div/div[2]/ul/li[1]')
            hover = ActionChains(driver).move_to_element(element_to_hover_over)
            hover.perform()
            hidden_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/persons-transfer/app-ais-object-edit/div[2]/div[2]/evolenta-scrollbar/div/div/div/form/div[2]/div[2]/div[2]/div/evolenta-address-gar/div/div[2]/div/div[2]/ul/li[1]")))
            hidden_button.click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG) 
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:        
        with allure.step("Нажатие Сохранить"):
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/persons-transfer/app-ais-object-edit/div[1]/button")))
            next_button.click()
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:        
        with allure.step("Сбор сетевых логов"):
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_3, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки при сохранении нового объекта\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
                allure.attach.file(log_file_path_3, name="network_log", attachment_type=allure.attachment_type.TEXT)
    except Exception as e:
      print(f"Ошибка в шаге: {e}")
      time.sleep(3)
#endregion

#ОТПРАВКА ЗАПРОСА####
#region
# Тестовый метод с использованием pytest и allure
@allure.title("09-тест Отправка запроса")
@allure.description("Проверка отправки запроса и запись сетевых логов")
def test_zapros():
    try:
        with allure.step("Переход в модуль Настройки системы новый"):
            driver.get('https://pgs.gosuslugi.ru/system-settings/requests/envelopes')
            time.sleep(5)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-section/evolenta-universal-collection-page/evolenta-adaptive-navbar/div/div/div/button"))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-section/envelope-edit/div[2]/div[2]/evolenta-scrollbar/div/div/div/envelope-main-info/dl/dd/div/span"))).click()

            input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-section/envelope-edit/div[2]/div[2]/evolenta-scrollbar/div/div/div/envelope-main-info/dl/dd/div/div[1]/div/input")))
            input_field.click()
            time.sleep(2)
            input_field.send_keys("Тестовая организация (тестирование ВС)")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-section/envelope-edit/div[2]/div[2]/evolenta-scrollbar/div/div/div/envelope-main-info/dl/dd/div/div[2]/div/label"))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-section/envelope-edit/div[2]/div[2]/evolenta-scrollbar/div/div/div/envelope-main-info/dl/dd[2]/div/evolenta-infinite-scrollbar/div/div[2]/div/label"))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-section/envelope-edit/div[2]/div[1]/div/div[2]/div"))).click()
            time.sleep(3)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Ввод запроса в поле"):
            input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-section/envelope-edit/div[2]/div[2]/evolenta-scrollbar/div/div/div/evolenta-envelope-data/div/div/form/div/div[1]/div[2]/div/div/div/div/div/div/div[1]/textarea")))
            input_field.click()
            time.sleep(2)
            input_field.send_keys("""<tns:VisLicenseActRequest xmlns:tns="http://tor.knd.evolenta.ru/license_act/1.0.0">
    <tns:IssuedLicense>
        <tns:Sender>
            <tns:name>ТЕСТ_ФОИВ</tns:name>
        </tns:Sender>
        <tns:Licensee>
            <tns:LegalData>
                <tns:legalFullName>ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ЛЕВ"</tns:legalFullName>
                <tns:legalShortName>ООО "ЛЕВ"</tns:legalShortName>
                <tns:ogrn>1054700113368</tns:ogrn>
                <tns:inn>4703082653</tns:inn>
                <tns:kpp>470301001</tns:kpp>
                <tns:legalAddress>
                    <tns:fullAddress>ОБЛАСТЬ ЛЕНИНГРАДСКАЯ, РАЙОН ВСЕВОЛОЖСКИЙ, ДЕРЕВНЯ ГАРБОЛОВО, 1/34</tns:fullAddress>
                </tns:legalAddress>
                <tns:workingPosition>ГЕНЕРАЛЬНЫЙ ДИРЕКТОР</tns:workingPosition>
                <tns:lastName>Иванов</tns:lastName>
                <tns:firstName>Михаил</tns:firstName>
            </tns:LegalData>
        </tns:Licensee>
        <tns:LicenseData>
            <tns:Activity>
                <tns:code>1130000</tns:code>
                <tns:name>ОТДЕЛЬНЫЕ ВИДЫ ДЕЯТЕЛЬНОСТИ, ЛИЦЕНЗИРУЕМЫЕ ФЕДЕРАЛЬНОЙ СЛУЖБОЙ ПО НАДЗОРУ В СФЕРЕ ТРАНСПОРТА (Ространснадзор)</tns:name>
            </tns:Activity>
            <tns:Number>АК-00-000046</tns:Number>
            <tns:IssueDate>2019-04-16</tns:IssueDate>
        </tns:LicenseData>
    </tns:IssuedLicense>
</tns:VisLicenseActRequest>""")
            time.sleep(5)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Нажать кнопку действие"):    
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-section/envelope-edit/div[1]/div[1]/button"))).click()
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")
    
    try:
        with allure.step("Нажатие кнопки Отправить"):
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-section/envelope-edit/div[1]/div[1]/ul/li[2]/a"))).click()
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
            time.sleep(15)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")

    try:
        with allure.step("Запись Логов сетевой активности"):
            # Включить отслеживание сети
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_2, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки отправки запроса\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_2, name="network_log", attachment_type=allure.attachment_type.TEXT)
            time.sleep(3)
            print(f"Файл '{log_file_path_2}' с результатом теста создан.")
    except Exception as e:
        print(f"Ошибка в шаге: {e}")
        time.sleep(5)
        
    try:
        with allure.step("Обновление страницы"): 
                # Переходим на страницу Кабинет администратора
                driver.get('https://pgs.gosuslugi.ru/system-settings/requests/envelopes')
                # Ждем, пока страница загрузится
                ready_state = driver.execute_script("return document.readyState")
                time.sleep(5)
                # Нажать на 1 запрос
                send_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-section/evolenta-universal-collection-page/div[2]/div[2]/div/div/div[1]/div/evolenta-infinite-scrollbar/div/div/div[1]/div/div[2]/h6")))
                send_button.click()
                time.sleep(1)
                # Нажать на редактировать
                send_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-section/evolenta-universal-collection-page/div[2]/div[2]/div/div/div[2]/envelope-preview/div/div[1]/div/a")))                                                                                   
                send_button.click()
                time.sleep(3)
    except Exception as e:
                print(f"Ошибка в шаге: {e}")
    
    with allure.step("Проверка статуса запроса"):
        try:
            error_element = driver.find_element(By.XPATH, "//span[contains(@class, 'badge') and contains(@class, 'bg-danger-600') and text()=' Ошибка при отправке ']")
            if error_element:
                allure.attach(driver.page_source, name="скрин", attachment_type=allure.attachment_type.PNG)
                pytest.fail("Тест не пройден: Статус запроса Ошибка при отправке")
        except NoSuchElementException:
            print("Элемент 'Ошибка при отправке' не найден. Тест продолжается.")
            allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    
        except Exception as e:
            print(f"Ошибка в шаге: {e}")
            time.sleep(2)
    
    try:
        with allure.step("Скопировать ссылку на запрос"):
            # Получить текущий URL страницы
            current_url = driver.current_url
            
            # Вывод ссылки в консоль для проверки
            print(f"Текущая ссылка: {current_url}")
            
            # Вложить ссылку в отчет Allure
            allure.attach(current_url, name="Ссылка на запрос", attachment_type=allure.attachment_type.TEXT)
            
            print("Ссылка на текущую страницу добавлена в отчет Allure")
            time.sleep(2)
    except Exception as e:
        print(f"Ошибка в шаге: {e}")
    finally:        
        driver.quit()
#endregion