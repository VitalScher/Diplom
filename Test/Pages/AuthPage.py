from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class AuthPage:
    def __init__(self, driver: webdriver):
        self.__url = "https://ru.yougile.com/team/"
        self.__driver = driver

    def go(self):
        self.__driver.get(self.__url)

    def login_as(self, email: str, password: str):
        #Находим поле с логином. Передаем в него значение переменной email:
        self.__driver.find_element(By.CSS_SELECTOR, "input[placeholder='example@mail.ru']").send_keys(email)

        #Находим поле «Введите пароль», передаем ему значение переменной password:
        self.__driver.find_element(By.CSS_SELECTOR, "input[placeholder='Введите пароль']").send_keys(password)
        
        #Находим кнопку «Войти» и нажимаем на нее
        self.__driver.find_element(By.CSS_SELECTOR, "div[role='button']").click()

        #Ожидаем когда загрузится страница входа в аккаунт
        WebDriverWait(self.__driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".truncate.ml-6.text-14.leading-4")))

    def go_to_my_company(self):
        #Переходим на страницу Моя компания
        self.__driver.find_element(By.CSS_SELECTOR, '[data-testid="my-company-item"]').click()

    def add_employee(self, email: str):
        #Добавляем сотрудника
        self.__driver.find_element(By.XPATH, '//span[normalize-space() = "Добавить сотрудника"]').click()

        #Ожидаем когда загрузится всплывающее окно Приглашения в компанию
        WebDriverWait(self.__driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="company-invite-popup-email-list"]')))

        #Вводим email сотрудника
        self.__driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='Введите адреса электронной почты, например, user1@mail.ru, user2@mail.ru']").send_keys(email)

        self.__driver.find_element(By.CSS_SELECTOR, '[data-testid="company-invite-popup-email-list"]').click()

        #Ожиданием пока кнопка Пригласить сотрудника не станет активной
        WebDriverWait(self.__driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="company-invite-popup-submit-button"]')))

        #Нажимаем на кнопку Пригласить сотрудника
        self.__driver.find_element(By.CSS_SELECTOR, '[data-testid="company-invite-popup-submit-button"]').click()
        
