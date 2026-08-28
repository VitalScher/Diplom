from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


class AuthPage:
    def __init__(self, driver: webdriver):
        self.__url = "https://ru.yougile.com/team/"
        self.__driver = driver

    def go(self):
        self.__driver.get(self.__url)

    def login_as(self, email: str, password: str):
        # Находим поле с логином. Передаем в него значение переменной email:
        self.__driver.find_element(By.CSS_SELECTOR,
                                   "input[placeholder='example@mail.ru']").send_keys(email)

        # Находим поле «Введите пароль», передаем ему значение переменной password:
        self.__driver.find_element(By.CSS_SELECTOR,
                                   "input[placeholder='Введите пароль']").send_keys(password)

        # Находим кнопку «Войти» и нажимаем на нее
        self.__driver.find_element(By.CSS_SELECTOR, "div[role='button']").click()

        # Ожидаем когда загрузится страница входа в аккаунт
        WebDriverWait(self.__driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".truncate.ml-6.text-14.leading-4")))

    def go_to_my_company(self):
        # Ожиданием пока кнопка перехода на страницу Моя компания станет активной
        WebDriverWait(self.__driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="my-company-item"]')))

        # Переходим на страницу Моя компания
        self.__driver.find_element(By.CSS_SELECTOR, '[data-testid="my-company-item"]').click()

    def add_employee(self, email: str):
        # Добавляем сотрудника
        wait = WebDriverWait(self.__driver, 20)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//span[normalize-space() = "Добавить сотрудника"]')))

        actions = ActionChains(self.__driver)
        actions.move_to_element(element).perform()

        self.__driver.find_element(
            By.XPATH, '//span[normalize-space() = "Добавить сотрудника"]').click()

        # Ожидаем когда загрузится всплывающее окно Приглашения в компанию
        WebDriverWait(self.__driver, 20).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="company-invite-popup-email-list"]')))

        # Вводим email сотрудника
        self.__driver.find_element(
            By.CSS_SELECTOR,
            "textarea[placeholder='Введите адреса электронной почты, например, user1@mail.ru, user2@mail.ru']").send_keys(email)

        self.__driver.find_element(By.CSS_SELECTOR, '[data-testid="company-invite-popup-email-list"]').click()

        # Ожиданием пока кнопка Пригласить сотрудника не станет активной
        WebDriverWait(self.__driver, 20).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, '[data-testid="company-invite-popup-submit-button"]')))

        # Нажимаем на кнопку Пригласить сотрудника
        self.__driver.find_element(
            By.CSS_SELECTOR, '[data-testid="company-invite-popup-submit-button"]').click()

        # Ожидание появления сотрудника на странице
        WebDriverWait(self.__driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{email}"]')))

    def del_employee(self, email: str):
        # Ищем сотрудника и скролим экран до нужной позиции
        wait = WebDriverWait(self.__driver, 20)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{email}"]')))

        actions = ActionChains(self.__driver)
        actions.move_to_element(element).perform()

        self.__driver.find_element(By.XPATH, f'//div[normalize-space() = "{email}"]').click()

        # Ожидание появления всплывающего окна
        WebDriverWait(self.__driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH, '//div[normalize-space() = "Удалить сотрудника из компании"]')))

        # Нажать на кнопку Удалить сотрудника
        self.__driver.find_element(
            By.XPATH, '//div[normalize-space() = "Удалить сотрудника из компании"]').click()

        # Ожидание появления всплывающего окна на подтверждение удаления сотрудника
        WebDriverWait(self.__driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[normalize-space() = "Удалить сотрудника"]')))

        # Нажать на кнопку Удалить сотрудника
        self.__driver.find_element(
            By.XPATH, '//div[normalize-space() = "Удалить сотрудника"]').click()

        # Ожидание появления всплывающего окна с сообщением об удалении сотрудника
        WebDriverWait(self.__driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[normalize-space() = "Назад в Мою компанию"]')))

        # Нажать на кнопку Назад в мою компанию
        self.__driver.find_element(
            By.XPATH, '//div[normalize-space() = "Назад в Мою компанию"]').click()

        # Ожидание обновления станицы
        WebDriverWait(self.__driver, 20).until(
            EC.staleness_of(self.__driver.find_element(
                By.XPATH, f'//div[normalize-space() = "{email}"]')))

    def create_project(self, project: str):
        # Нажимаем на кнопку добавить проект
        wait = WebDriverWait(self.__driver, 20)
        element = wait.until(
            EC.element_to_be_clickable((
                By.XPATH, '//span[contains(normalize-space(), "Добавить проект")]')))

        actions = ActionChains(self.__driver)
        actions.move_to_element(element).perform()

        self.__driver.find_element(
            By.XPATH, '//span[contains(normalize-space(), "Добавить проект")]').click()

        # Ожидание появления всплывающего окна выбора типа проекта
        WebDriverWait(self.__driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH, "//div[contains(text(),'Проект с задачами')]")))

        # Выбор проекта с задачами
        self.__driver.find_element(
            By.XPATH, "//div[contains(text(),'Проект с задачами')]").click()

        # Ожидание появления всплывающего окна настройки проекта
        WebDriverWait(self.__driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH, "//input[@placeholder='Введите название проекта…']")))

        # Ввести название проекта
        self.__driver.find_element(
            By.XPATH, "//input[@placeholder='Введите название проекта…']").send_keys(project)

        # Нажать на кнопку добавить проект
        self.__driver.find_element(
            By.XPATH, '//div[normalize-space() = "Добавить проект с задачами"]').click()

        # Ожидание открытия страницы проекта
        WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, f'//div[normalize-space() = "{project}"]')))

    def employee_to_project(self, email: str, project: str):
        # Выбор сотрудника
        wait = WebDriverWait(self.__driver, 20)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{email}"]')))

        actions = ActionChains(self.__driver)
        actions.move_to_element(element).perform()

        self.__driver.find_element(
            By.XPATH, f'//div[normalize-space() = "{email}"]').click()

        # Ожидание появления всплывающего окна свойств сотрудника
        WebDriverWait(self.__driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'span[title="{email}"]')))

        # Скрол до чек бокса тестового проекта
        wait = WebDriverWait(self.__driver, 20)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, f'//span[normalize-space()="{project}"]')))

        actions = ActionChains(self.__driver)
        actions.move_to_element(element).perform()

        self.__driver.find_element(
            By.XPATH, f'//span[normalize-space()="{project}"]').click()

        # Ожидание активизации кнопки Сохранить изменения
        WebDriverWait(self.__driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH, '//div[@role="button"][contains(normalize-space(), "Сохранить изменения")]')))

        # Нажать на кнопку Сохранить изменения
        self.__driver.find_element(
            By.XPATH, '//div[@role="button"][contains(normalize-space(), "Сохранить изменения")]').click()

    def employee_page(self, email: str, project: str):
        # Выбор сотрудника
        wait = WebDriverWait(self.__driver, 20)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{email}"]')))

        actions = ActionChains(self.__driver)
        actions.move_to_element(element).perform()

        self.__driver.find_element(By.XPATH, f'//div[normalize-space() = "{email}"]').click()

        # Ожидание появления всплывающего окна свойств сотрудника
        WebDriverWait(self.__driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'span[title="{email}"]')))

        # Скрол до чек бокса тестового проекта
        wait = WebDriverWait(self.__driver, 20)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, f'//span[normalize-space()="{project}"]')))

        actions = ActionChains(self.__driver)
        actions.move_to_element(element).perform()

    def del_project(self, project: str):
        # Выбор проекта
        wait = WebDriverWait(self.__driver, 20)
        element = wait.until(
            EC.presence_of_element_located((
                By.XPATH, f'//div[@data-testid="project-title" and normalize-space()="{project}"]')))

        actions = ActionChains(self.__driver)
        actions.move_to_element(element).perform()

        self.__driver.find_element(
            By.CSS_SELECTOR, '[data-testid="project-card-menu-button"]').click()

        # Ожидание появления всплывающего меню
        WebDriverWait(self.__driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//div[normalize-space() = "Удалить"]')))

        # Нажать на кнопку удалить проект
        self.__driver.find_element(By.XPATH, '//div[normalize-space() = "Удалить"]').click()

        # Ожидание появления запроса на потдверждение удаления
        WebDriverWait(self.__driver, 20).until(
            EC.visibility_of_element_located((
                By.XPATH, '//div[@role="button" and normalize-space() = "Удалить"]')))

        # Нажать на кнопку удалить
        self.__driver.find_element(
            By.XPATH, '//div[@role="button" and normalize-space() = "Удалить"]').click()

        # Ожидание обновления станицы
        WebDriverWait(self.__driver, 20).until(
            EC.staleness_of(self.__driver.find_element(
                By.XPATH, f'//div[normalize-space() = "{project}"]')))

    def employee_change_role(self):
        # Ожидание видимости кнопки роль сотрудника в проекте
        WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, "//div[@class='prj-invite prj-invite--user']//div[1]//div[2]//div[1]//div[1]//div[1]")))

        # Нажатие на выбор роли сотрудника в проекте
        self.__driver.find_element(
            By.XPATH, "//div[@class='prj-invite prj-invite--user']//div[1]//div[2]//div[1]//div[1]//div[1]").click()

        # ожидание появления выпадающего меню
        WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, '//div[contains(@class, "project-role__option")]')))

        # Выбор другой роли отлично от текущей
        self.__driver.find_element(
            By.XPATH, '//div[contains(@class, "project-role__option") and not(contains(@class, "project-role__option--current"))]').click()

        # Ожидание активизации кнопки Сохранить изменения
        WebDriverWait(self.__driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH, '//div[@role="button"][contains(normalize-space(), "Сохранить изменения")]')))

        # Нажать на кнопку Сохранить изменения
        self.__driver.find_element(
            By.XPATH, '//div[@role="button"][contains(normalize-space(), "Сохранить изменения")]').click()

    def employee_current_role(self):
        # Ожидание видимости кнопки роль сотрудника в проекте
        WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, "//div[@class='prj-invite prj-invite--user']//div[1]//div[2]//div[1]//div[1]//div[1]")))

        # Нажатие на выбор роли сотрудника в проекте
        self.__driver.find_element(
            By.XPATH, "//div[@class='prj-invite prj-invite--user']//div[1]//div[2]//div[1]//div[1]//div[1]").click()

        # ожидание появления выпадающего меню
        WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "project-role__option")]')))

        # Получение наименования и описания текущей роли
        locator = (By.XPATH, '//div[contains(@class, "project-role__option--current")]')
        elem = WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located(locator))
        role_text = elem.text.strip()

        # Закрытие выпадающего меню без изменений
        self.__driver.find_element(
            By.XPATH, '//div[(contains(@class, "project-role__option--current"))]').click()

        return role_text

    def create_department(self, depart: str):
        # Нажатие на конпку создать отдел
        wait = WebDriverWait(self.__driver, 20)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[normalize-space() = "Добавить отдел"]')))

        actions = ActionChains(self.__driver)
        actions.move_to_element(element).perform()

        self.__driver.find_element(
            By.XPATH, '//div[normalize-space() = "Добавить отдел"]').click()

        # Ожидание появления всплывающего окна Создания отдела
        WebDriverWait(self.__driver, 20).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'input[placeholder="Введите название отдела"]')))

        # Ввод названия отдела
        self.__driver.find_element(
            By.CSS_SELECTOR, 'input[placeholder="Введите название отдела"]').send_keys(depart)

        # Нажать на кнопку Создать отдел
        self.__driver.find_element(
            By.XPATH, '//div[@role="button" and normalize-space() = "Создать отдел"]').click()

    def employee_to_department(self, email: str, depart: str):
        # Выбор отдела
        wait = WebDriverWait(self.__driver, 20)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{depart}"]')))

        actions = ActionChains(self.__driver)
        actions.move_to_element(element).perform()

        self.__driver.find_element(
            By.XPATH, f'//div[normalize-space() = "{depart}"]').click()

        # Ожидание открытия всплывающего окна отдела
        WebDriverWait(self.__driver, 20).until(
            EC.visibility_of_element_located((
                By.XPATH, '//div[normalize-space() = "Редактирование отдела"]')))

        # Назначение сотрудника в отдел
        self.__driver.find_element(By.XPATH,
                                   f'//div[contains(@class, "department-users-table__item")]'
                                   f'//span[@title="{email}" and normalize-space(.) = "{email}"]').click()

        # Нажать на кнопку Сохранить изменения
        self.__driver.find_element(
            By.XPATH, '//div[@role="button" and normalize-space() = "Сохранить изменения"]').click()

    def employee_current_department(self, email: str, depart: str):
        # Выбор сотрудника
        wait = WebDriverWait(self.__driver, 20)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{email}"]')))

        actions = ActionChains(self.__driver)
        actions.move_to_element(element).perform()

        self.__driver.find_element(By.XPATH, f'//div[normalize-space() = "{email}"]').click()

        # Ожидание появления всплывающего окна свойств сотрудника
        WebDriverWait(self.__driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'span[title="{email}"]')))

        # Скрол до чек бокса тестового проекта
        wait = WebDriverWait(self.__driver, 20)
        element = wait.until(EC.presence_of_element_located((By.XPATH,
                                                             f'//div[contains(@class, "prj-invite__participate-item")]'
                                                             f'//span[contains(@class, "prj-invite__item-text") and normalize-space(.) = "{depart}"]')))

        actions = ActionChains(self.__driver)
        actions.move_to_element(element).perform()

    def del_department(self, depart: str):
        # Выбор отдела
        wait = WebDriverWait(self.__driver, 20)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{depart}"]')))

        actions = ActionChains(self.__driver)
        actions.move_to_element(element).perform()

        self.__driver.find_element(By.XPATH, f'//div[normalize-space() = "{depart}"]').click()

        # Ожидание открытия всплывающего окна отдела
        WebDriverWait(self.__driver, 20).until(
            EC.visibility_of_element_located((
                By.XPATH, '//div[normalize-space() = "Редактирование отдела"]')))

        # Нажать на кнопку удалить отдел
        self.__driver.find_element(By.XPATH, '//div[normalize-space() = "Удалить отдел"]').click()

        # Ожидание появления всплывающего окна подтверждения на удаление
        WebDriverWait(self.__driver, 20).until(
            EC.visibility_of_element_located((
                By.XPATH, '//div[@role="button" and normalize-space() = "Удалить"]')))

        # Нажать на кнопку удалить отдел
        self.__driver.find_element(
            By.XPATH, '//div[@role="button" and normalize-space() = "Удалить"]').click()

        # Ожидание обновления станицы
        WebDriverWait(self.__driver, 20).until(
            EC.staleness_of(self.__driver.find_element(By.XPATH, f'//div[normalize-space() = "{depart}"]')))
