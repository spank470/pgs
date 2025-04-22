from selenium.webdriver.common.by import By
import time

# Убедитесь, что ChromeDriver доступен
driver = webdriver.Chrome(executable_path="path/to/chromedriver")

# Откроем локальный сервер
driver.get("http://127.0.0.1:5000")  # или ваш локальный адрес, например http://localhost:8080

# Пример теста: проверим, что на главной странице есть заголовок
assert "Title of Your Web App" in driver.title

# Пример взаимодействия: находим элемент и выполняем действие
element = driver.find_element(By.ID, "some-element-id")
element.click()

# Подождем немного, чтобы убедиться, что действия выполнены
time.sleep(2)

# Закрытие браузера
driver.quit()