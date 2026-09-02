from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import allure


class AuthPage:
    def __init__(self, driver: webdriver) -> None:
        """
        Конструктор задает начальное значение параметра driver.

        :param driver: WebDriver — объект драйвера Selenium.
        """
        self.__url = "https://ru.yougile.com/team/"
        self.__driver = driver

    @allure.step("FT. Переход на страницу авторизации")
    def go(self) -> None:
        """
        Метод служит для перехода на страницу авторизации на портале YouGile
        """
        self.__driver.get(self.__url)

    @allure.step("FT. Авторизация на портале")
    def login_as(self, email: str, password: str) -> None:
        """
        Метод служит для авторизации на портале YouGile под заданными логином и паролем.
        :param email: str - логин для входа в личный кабинет.
        :param password: str - пароль для входа в личный кабинет.
        """
        with allure.step("FT. Находим поле с логином. Передаем в него значение переменной email"):
            self.__driver.find_element(By.CSS_SELECTOR,
                                       "input[placeholder='example@mail.ru']").send_keys(email)

        with allure.step("FT. Находим поле «Введите пароль», передаем ему значение переменной password"):
            self.__driver.find_element(By.CSS_SELECTOR,
                                       "input[placeholder='Введите пароль']").send_keys(password)

        with allure.step("FT. Находим кнопку «Войти» и нажимаем на нее"):
            self.__driver.find_element(By.CSS_SELECTOR, "div[role='button']").click()

        with allure.step("FT. Ожидаем когда загрузится страница входа в аккаунт"):
            WebDriverWait(self.__driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".truncate.ml-6.text-14.leading-4")))

    @allure.step("FT. Переход на страницу Моя компания")
    def go_to_my_company(self) -> None:
        """
        Метод служит для перехода на станицу Моя компания при нахождении на страницах личного кабинета.
        """
        with allure.step("FT. Ожиданием пока кнопка перехода на страницу Моя компания станет активной"):
            WebDriverWait(self.__driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="my-company-item"]')))

        with allure.step("FT. Переходим на страницу Моя компания"):
            self.__driver.find_element(By.CSS_SELECTOR, '[data-testid="my-company-item"]').click()

    @allure.step("FT. Добавление тестового сотрудника")
    def add_employee(self, email: str) -> None:
        """
        Метод служит для добавления тестового сотрудника.
        :param email: str - почта тестового сотрудника.
        """
        with allure.step("FT. Добавляем сотрудника"):
            wait = WebDriverWait(self.__driver, 20)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, '//span[normalize-space() = "Добавить сотрудника"]')))
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).perform()
            self.__driver.find_element(
                By.XPATH, '//span[normalize-space() = "Добавить сотрудника"]').click()

        with allure.step("FT. Ожидаем когда загрузится всплывающее окно Приглашения в компанию"):
            WebDriverWait(self.__driver, 20).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-testid="company-invite-popup-email-list"]')))

        with allure.step("FT. Вводим email сотрудника"):
            self.__driver.find_element(
                By.CSS_SELECTOR,
                "textarea[placeholder='Введите адреса электронной почты, например, user1@mail.ru, user2@mail.ru']").send_keys(email)
            self.__driver.find_element(By.CSS_SELECTOR, '[data-testid="company-invite-popup-email-list"]').click()

        with allure.step("FT. Ожиданием пока кнопка Пригласить сотрудника не станет активной"):
            WebDriverWait(self.__driver, 20).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, '[data-testid="company-invite-popup-submit-button"]')))

        with allure.step("FT. Нажимаем на кнопку Пригласить сотрудника"):
            self.__driver.find_element(
                By.CSS_SELECTOR, '[data-testid="company-invite-popup-submit-button"]').click()

        with allure.step("FT. Ожидание появления сотрудника на странице"):
            WebDriverWait(self.__driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{email}"]')))

    @allure.step("FT. Удаление сотрудника")
    def del_employee(self, email: str) -> None:
        """
        Метод служит для добавления тестового сотрудника.
        :param email: str - почта тестового сотрудника.
        """
        with allure.step("FT. Ищем сотрудника и скролим экран до нужной позиции"):
            wait = WebDriverWait(self.__driver, 20)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{email}"]')))
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).perform()
            self.__driver.find_element(By.XPATH, f'//div[normalize-space() = "{email}"]').click()

        with allure.step("FT. Ожидание появления всплывающего окна"):
            WebDriverWait(self.__driver, 20).until(
                EC.element_to_be_clickable((
                    By.XPATH, '//div[normalize-space() = "Удалить сотрудника из компании"]')))

        with allure.step("FT. Нажать на кнопку Удалить сотрудника"):
            self.__driver.find_element(
                By.XPATH, '//div[normalize-space() = "Удалить сотрудника из компании"]').click()

        with allure.step("FT. Ожидание появления всплывающего окна на подтверждение удаления сотрудника"):
            WebDriverWait(self.__driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div[normalize-space() = "Удалить сотрудника"]')))

        with allure.step("FT. Нажать на кнопку Удалить сотрудника"):
            self.__driver.find_element(
                By.XPATH, '//div[normalize-space() = "Удалить сотрудника"]').click()

        with allure.step("FT. Ожидание появления всплывающего окна с сообщением об удалении сотрудника"):
            WebDriverWait(self.__driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div[normalize-space() = "Назад в Мою компанию"]')))

        with allure.step("FT. Нажать на кнопку Назад в мою компанию"):
            self.__driver.find_element(
                By.XPATH, '//div[normalize-space() = "Назад в Мою компанию"]').click()

        with allure.step("FT. Ожидание обновления станицы"):
            WebDriverWait(self.__driver, 20).until(
                EC.staleness_of(self.__driver.find_element(
                    By.XPATH, f'//div[normalize-space() = "{email}"]')))

    @allure.step("FT. Добавление тестового проекта")
    def create_project(self, project: str) -> None:
        """
        Метод служит для добавления тестового проекта.
        :param project: str - наименование тестового проекта.
        """
        with allure.step("FT. Нажимаем на кнопку добавить проект"):
            wait = WebDriverWait(self.__driver, 20)
            element = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, '//span[contains(normalize-space(), "Добавить проект")]')))
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).perform()
            self.__driver.find_element(
                By.XPATH, '//span[contains(normalize-space(), "Добавить проект")]').click()

        with allure.step("FT. Ожидание появления всплывающего окна выбора типа проекта"):
            WebDriverWait(self.__driver, 20).until(
                EC.element_to_be_clickable((
                    By.XPATH, "//div[contains(text(),'Проект с задачами')]")))

        with allure.step("FT. Выбор проекта с задачами"):
            self.__driver.find_element(
                By.XPATH, "//div[contains(text(),'Проект с задачами')]").click()

        with allure.step("FT. Ожидание появления всплывающего окна настройки проекта"):
            WebDriverWait(self.__driver, 20).until(
                EC.element_to_be_clickable((
                    By.XPATH, "//input[@placeholder='Введите название проекта…']")))

        with allure.step("FT. Ввести название проекта"):
            self.__driver.find_element(
                By.XPATH, "//input[@placeholder='Введите название проекта…']").send_keys(project)

        with allure.step("FT. Нажать на кнопку добавить проект"):
            self.__driver.find_element(
                By.XPATH, '//div[normalize-space() = "Добавить проект с задачами"]').click()

        with allure.step("FT. Ожидание открытия страницы проекта"):
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH, f'//div[normalize-space() = "{project}"]')))

    @allure.step("FT. Добавление тестового сотрудника в тестовый проект")
    def employee_to_project(self, email: str, project: str) -> None:
        """
        Метод служит для добавления тестового сотрудника в тестовый проект.
        :param email: str - почта тестового сотрудника.
        :param project: str - наименование тестового проекта.
        """
        with allure.step("FT. Выбор сотрудника"):
            wait = WebDriverWait(self.__driver, 20)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{email}"]')))
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).perform()
            self.__driver.find_element(
                By.XPATH, f'//div[normalize-space() = "{email}"]').click()

        with allure.step("FT. Ожидание появления всплывающего окна свойств сотрудника"):
            WebDriverWait(self.__driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, f'span[title="{email}"]')))

        with allure.step("FT. Скрол до блока Участник проектов"):
            wait = WebDriverWait(self.__driver, 20)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, f'//span[normalize-space()="{project}"]')))
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).perform()
            self.__driver.find_element(
                By.XPATH, f'//span[normalize-space()="{project}"]').click()

        with allure.step("FT. Ожидание активизации кнопки Сохранить изменения"):
            WebDriverWait(self.__driver, 20).until(
                EC.element_to_be_clickable((
                    By.XPATH, '//div[@role="button"][contains(normalize-space(), "Сохранить изменения")]')))

        with allure.step("FT. Нажать на кнопку Сохранить изменения"):
            self.__driver.find_element(
                By.XPATH, '//div[@role="button"][contains(normalize-space(), "Сохранить изменения")]').click()

    @allure.step("FT. Открытие страницы сотрудника и переход до блока Проекты")
    def employee_page(self, email: str, project: str) -> list:
        """
        Метод служит для открытия личной страницы сотрудника и скрол до блока Участник проектов.
        Ищет и возвращает WebElement, обознаючающий включение сотрудника в проект.
        :param email: str - почта тестового сотрудника.
        :param project: str - наименование тестового проекта.
        """
        with allure.step("FT. Выбор сотрудника"):
            wait = WebDriverWait(self.__driver, 20)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{email}"]')))
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).perform()
            self.__driver.find_element(By.XPATH, f'//div[normalize-space() = "{email}"]').click()

        with allure.step("FT. Ожидание появления всплывающего окна свойств сотрудника"):
            WebDriverWait(self.__driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, f'span[title="{email}"]')))

        with allure.step("FT. Скрол до блока Участник проектов"):
            wait = WebDriverWait(self.__driver, 20)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, f'//span[normalize-space()="{project}"]')))
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).perform()
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH, "//div[@class='prj-invite prj-invite--user']//div[1]//div[2]//div[1]//div[1]//div[1]")))
            check = self.__driver.find_element(
                By.XPATH, "//div[@class='prj-invite prj-invite--user']//div[1]//div[2]//div[1]//div[1]//div[1]")
            return check

    @allure.step("FT. Удаление тестового проекта")
    def del_project(self, project: str) -> None:
        """
        Метод служит для удаления тестового проекта.
        :param project: str - наименование тестового проекта.
        """
        with allure.step("FT. Выбор проекта"):
            wait = WebDriverWait(self.__driver, 20)
            element = wait.until(
                EC.presence_of_element_located((
                    By.XPATH, f'//div[@data-testid="project-title" and normalize-space()="{project}"]')))
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).perform()
            self.__driver.find_element(
                By.CSS_SELECTOR, '[data-testid="project-card-menu-button"]').click()

        with allure.step("FT. Ожидание появления всплывающего меню"):
            WebDriverWait(self.__driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//div[normalize-space() = "Удалить"]')))

        with allure.step("FT. Нажать на кнопку удалить проект"):
            self.__driver.find_element(By.XPATH, '//div[normalize-space() = "Удалить"]').click()

        with allure.step("FT. Ожидание появления запроса на потдверждение удаления"):
            WebDriverWait(self.__driver, 20).until(
                EC.visibility_of_element_located((
                    By.XPATH, '//div[@role="button" and normalize-space() = "Удалить"]')))

        with allure.step("FT. Нажать на кнопку удалить"):
            self.__driver.find_element(
                By.XPATH, '//div[@role="button" and normalize-space() = "Удалить"]').click()

        with allure.step("FT. Ожидание обновления станицы"):
            WebDriverWait(self.__driver, 20).until(
                EC.staleness_of(self.__driver.find_element(
                    By.XPATH, f'//div[normalize-space() = "{project}"]')))

    @allure.step("FT. Изменение роли сотрудника в тестовом проекте")
    def employee_change_role(self) -> None:
        """
        Метод служит для изменения роли тестового сотрудника в тестовом проекте.
        """
        with allure.step("FT. Ожидание видимости кнопки роль сотрудника в проекте"):
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH, "//div[@class='prj-invite prj-invite--user']//div[1]//div[2]//div[1]//div[1]//div[1]")))

        with allure.step("FT. Нажатие на выбор роли сотрудника в проекте"):
            self.__driver.find_element(
                By.XPATH, "//div[@class='prj-invite prj-invite--user']//div[1]//div[2]//div[1]//div[1]//div[1]").click()

        with allure.step("FT. Ожидание появления выпадающего меню"):
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH, '//div[contains(@class, "project-role__option")]')))

        with allure.step("FT. Выбор другой роли отлично от текущей"):
            self.__driver.find_element(
                By.XPATH, '//div[contains(@class, "project-role__option") and not(contains(@class, "project-role__option--current"))]').click()

        with allure.step("FT. Ожидание активизации кнопки Сохранить изменения"):
            WebDriverWait(self.__driver, 20).until(
                EC.element_to_be_clickable((
                    By.XPATH, '//div[@role="button"][contains(normalize-space(), "Сохранить изменения")]')))

        with allure.step("FT. Нажать на кнопку Сохранить изменения"):
            self.__driver.find_element(
                By.XPATH, '//div[@role="button"][contains(normalize-space(), "Сохранить изменения")]').click()

    @allure.step("FT. Получение текущей роли сотрудника в проекте")
    def employee_current_role(self) -> str:
        """
        Метод служит для считывания и возвращения текущей роли сотрудника в тестовом проекте.
        """
        with allure.step("FT. Ожидание видимости кнопки роль сотрудника в проекте"):
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH, "//div[@class='prj-invite prj-invite--user']//div[1]//div[2]//div[1]//div[1]//div[1]")))

        with allure.step("FT. Нажатие на выбор роли сотрудника в проекте"):
            self.__driver.find_element(
                By.XPATH, "//div[@class='prj-invite prj-invite--user']//div[1]//div[2]//div[1]//div[1]//div[1]").click()

        with allure.step("FT. Ожидание появления выпадающего меню"):
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "project-role__option")]')))

        with allure.step("FT. Получение наименования и описания текущей роли"):
            locator = (By.XPATH, '//div[contains(@class, "project-role__option--current")]')
            elem = WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located(locator))
            role_text = elem.text.strip()

        with allure.step("FT. Закрытие выпадающего меню без изменений"):
            self.__driver.find_element(
                By.XPATH, '//div[(contains(@class, "project-role__option--current"))]').click()

        with allure.step("FT. Возврат текущей роли сотрудника в тестовом проекте"):
            return role_text

    @allure.step("FT. Создание тестового департамента")
    def create_department(self, depart: str) -> None:
        """
        Метод служит для создания тестового отдела.
        :param depart: str - наименование тестового отдела.
        """
        with allure.step("FT. Нажатие на конпку создать отдел"):
            wait = WebDriverWait(self.__driver, 20)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[normalize-space() = "Добавить отдел"]')))
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).perform()
            self.__driver.find_element(
                By.XPATH, '//div[normalize-space() = "Добавить отдел"]').click()

        with allure.step("FT. Ожидание появления всплывающего окна Создания отдела"):
            WebDriverWait(self.__driver, 20).until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR, 'input[placeholder="Введите название отдела"]')))

        with allure.step("FT. Ввод названия отдела"):
            self.__driver.find_element(
                By.CSS_SELECTOR, 'input[placeholder="Введите название отдела"]').send_keys(depart)

        with allure.step("FT. Нажать на кнопку Создать отдел"):
            self.__driver.find_element(
                By.XPATH, '//div[@role="button" and normalize-space() = "Создать отдел"]').click()

    @allure.step("FT. Добавление тестового сотрудника в созданный отдел")
    def employee_to_department(self, email: str, depart: str) -> None:
        """
        Метод служит для создания тестового отдела.
        :param email: str - почта тестового сотрудника.
        :param depart: str - наименование тестового отдела.
        """
        with allure.step("FT. Выбор отдела"):
            wait = WebDriverWait(self.__driver, 20)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{depart}"]')))
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).perform()
            self.__driver.find_element(
                By.XPATH, f'//div[normalize-space() = "{depart}"]').click()

        with allure.step("FT. Ожидание открытия всплывающего окна отдела"):
            WebDriverWait(self.__driver, 20).until(
                EC.visibility_of_element_located((
                    By.XPATH, '//div[normalize-space() = "Редактирование отдела"]')))

        with allure.step("FT. Назначение сотрудника в отдел"):
            self.__driver.find_element(By.XPATH,
                                       f'//div[contains(@class, "department-users-table__item")]'
                                       f'//span[@title="{email}" and normalize-space(.) = "{email}"]').click()

        with allure.step("FT. Нажать на кнопку Сохранить изменения"):
            self.__driver.find_element(
                By.XPATH, '//div[@role="button" and normalize-space() = "Сохранить изменения"]').click()

    @allure.step("FT. Открытие окна свойств сотрудника и переход до блока Состоит в отделах")
    def employee_current_department(self, email: str, depart: str) -> list:
        """
        Метод служит для открытия окна свойств тестового сотрудника и перехода до блока Состоит в отделах.
        Ищет и возвращает WebElement, обознаючающий включение сотрудника в отдел.
        :param email: str - почта тестового сотрудника.
        :param depart: str - наименование тестового отдела.
        """
        with allure.step("FT. Выбор сотрудника"):
            wait = WebDriverWait(self.__driver, 20)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{email}"]')))
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).perform()
            self.__driver.find_element(By.XPATH, f'//div[normalize-space() = "{email}"]').click()

        with allure.step("FT. Ожидание появления всплывающего окна свойств сотрудника"):
            WebDriverWait(self.__driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, f'span[title="{email}"]')))

        with allure.step("FT. Переход до блока Состоит в отделах"):
            wait = WebDriverWait(self.__driver, 20)
            element = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                 f'//div[contains(@class, "prj-invite__participate-item")]'
                                                                 f'//span[contains(@class, "prj-invite__item-text") and normalize-space(.) = "{depart}"]')))
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).perform()
            WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='prj-invite-role__name'])[1]")))
            check = self.__driver.find_element(By.XPATH, "(//div[@class='prj-invite-role__name'])[1]")
            return check

    @allure.step("FT. Удаление тестового отдела")
    def del_department(self, depart: str) -> None:
        """
        Метод служит для удаления тестового отдела.
        :param depart: str - наименование тестового отдела.
        """
        with allure.step("FT. Выбор отдела"):
            wait = WebDriverWait(self.__driver, 20)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, f'//div[normalize-space() = "{depart}"]')))
            actions = ActionChains(self.__driver)
            actions.move_to_element(element).perform()
            self.__driver.find_element(By.XPATH, f'//div[normalize-space() = "{depart}"]').click()

        with allure.step("FT. Ожидание открытия всплывающего окна отдела"):
            WebDriverWait(self.__driver, 20).until(
                EC.visibility_of_element_located((
                    By.XPATH, '//div[normalize-space() = "Редактирование отдела"]')))

        with allure.step("FT. Нажать на кнопку удалить отдел"):
            self.__driver.find_element(By.XPATH, '//div[normalize-space() = "Удалить отдел"]').click()

        with allure.step("FT. Ожидание появления всплывающего окна подтверждения на удаление"):
            WebDriverWait(self.__driver, 20).until(
                EC.visibility_of_element_located((
                    By.XPATH, '//div[@role="button" and normalize-space() = "Удалить"]')))

        with allure.step("FT. Нажать на кнопку удалить отдел"):
            self.__driver.find_element(
                By.XPATH, '//div[@role="button" and normalize-space() = "Удалить"]').click()

        with allure.step("FT. Ожидание обновления станицы"):
            WebDriverWait(self.__driver, 20).until(
                EC.staleness_of(self.__driver.find_element(By.XPATH, f'//div[normalize-space() = "{depart}"]')))

    @allure.step("FT. Закрытие окна свойств сотрудника")
    def close_employee_page(self) -> None:
        """
        Метод служит для закрывания окна свойств сотрудника.
        """
        with allure.step("FT. Нажатие на иконку закрытия"):
            self.__driver.find_element(By.XPATH, "//div[@class='prj-invite__close']").click()
