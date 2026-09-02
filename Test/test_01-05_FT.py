from Pages.AuthPage import AuthPage
import allure


@allure.id("ТК-01. Сотрудники")
@allure.severity("Critical")
@allure.story("Добавить нового сотрудника")
@allure.feature("Create")
@allure.title("ТК-01. Сотрудники. Положительная проверка. Добавить нового сотрудника")
def test_add_employee(driver, login: str, password: str, test_email: str) -> None:
    """
    Тест является положительной проверкой по добавлению нового сотрудника в проект.
    В ходе теста в тестовую компанию добавляется новый сотрудник.
    После завершения теста добавленный аккаунт удаляется.
    Проверка успешного выполнения теста осуществляется по присутствию тестового аккаунта в HTML страницы.

    :param driver: WebDriver — объект драйвера Selenium. Установлен в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param test_email: str - тестовый аккаунт. Установлен в фикстурах в файле conftest.py.
    """
    auth_page = AuthPage(driver)
    auth_page.go()
    auth_page.login_as(login, password)
    auth_page.go_to_my_company()
    auth_page.add_employee(test_email)

    with allure.step("FT. Проверка наличия тестового аккаунта в HTML страницы"):
        assert test_email in driver.page_source, "Текст отсутствует в HTML"

    auth_page.del_employee(test_email)


@allure.id("ТК-02. Сотрудники")
@allure.severity("Critical")
@allure.story("Удаление сотрудника")
@allure.feature("Delete")
@allure.title("ТК-02. Сотрудники. Положительная проверка. Удаление сотрудника")
def test_del_employee(driver, login: str, password: str, test_email: str) -> None:
    """
    Тест является положительной проверкой по удалению сотрудника из проекта.
    В ходе теста в тестовую компанию добавляется тестовый аккаунт сотрудника. В ходе выполнения теста добавленный аккаунт удаляется.
    Проверка успешного выполнения теста осуществляется по отсутствию тестового аккаунта в HTML страницы.

    :param driver: WebDriver — объект драйвера Selenium. Установлен в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param test_email: str - тестовый аккаунт. Установлен в фикстурах в файле conftest.py.
    """
    auth_page = AuthPage(driver)
    auth_page.go()
    auth_page.login_as(login, password)
    auth_page.go_to_my_company()
    auth_page.add_employee(test_email)
    auth_page.del_employee(test_email)

    with allure.step("FT. Проверка отсутствия тестового аккаунта в HTML страницы"):
        assert test_email not in driver.page_source, "Текст присутствует в HTML"


@allure.id("ТК-03. Сотрудники")
@allure.severity("Critical")
@allure.story("Назначение сотрудника в проект")
@allure.feature("Edit")
@allure.title("ТК-03. Сотрудники. Положительная проверка. Назначение сотрудника в проект")
def test_employee_to_new_projet(driver, login: str, password: str, test_email: str, project: str) -> None:
    """
    Тест является положительной проверкой функции назначения сотрудника в проект.
    В ходе теста в компанию добавляется аккаунт сотрудника и новый проект.
    В ходе выполнения сотрудник назначается в проект.
    Проверка успешного выполнения теста осуществляется по наличию
    присвоенной роли у сотрудника в проекте (чек-боксы на странице являются просто графическими элементами).
    После выполнения проверки тестовые данные удаляются.

    :param driver: WebDriver — объект драйвера Selenium. Установлен в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param test_email: str - тестовый аккаунт. Установлен в фикстурах в файле conftest.py.

    :param project: str - тестовый проект. Установлен в фикстурах в файле conftest.py.
    """
    auth_page = AuthPage(driver)
    auth_page.go()
    auth_page.login_as(login, password)
    auth_page.go_to_my_company()
    auth_page.add_employee(test_email)
    auth_page.create_project(project)
    auth_page.go_to_my_company()
    auth_page.employee_to_project(test_email, project)
    check = auth_page.employee_page(test_email, project)

    with allure.step("FT. Проверка по наличию роли в проекте (галочка не является чек-боксом)"):
        assert check.is_displayed()

    auth_page.close_employee_page()
    auth_page.del_employee(test_email)
    auth_page.del_project(project)


@allure.id("ТК-04. Сотрудники")
@allure.severity("Critical")
@allure.story("Изменение роли сотрудника")
@allure.feature("Edit")
@allure.title("ТК-04. Сотрудники. Положительная проверка. Изменение роли сотрудника в проекте")
def test_employee_role(driver, login: str, password: str, test_email: str, project: str) -> None:
    """
    Тест является положительной проверкой функции изменения роли сотрудника в проекте.
    В ходе теста в компанию добавляется аккаунт сотрудника и новый проект.
    В ходе выполнения сотрудник назначается в проект и считывается его роль.
    Затем роль изменяется.
    Проверка успешного выполнения теста осуществляется по различию ролей до и после выполнения теста.
    После выполнения проверки тестовые данные удаляются.

    :param driver: WebDriver — объект драйвера Selenium. Установлен в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param test_email: str - тестовый аккаунт. Установлен в фикстурах в файле conftest.py.

    :param project: str - тестовый проект. Установлен в фикстурах в файле conftest.py.
    """
    auth_page = AuthPage(driver)
    auth_page.go()
    auth_page.login_as(login, password)
    auth_page.go_to_my_company()
    auth_page.add_employee(test_email)
    auth_page.create_project(project)
    auth_page.go_to_my_company()
    auth_page.employee_to_project(test_email, project)
    auth_page.employee_page(test_email, project)
    current_role_old = auth_page.employee_current_role()
    auth_page.employee_change_role()
    auth_page.employee_page(test_email, project)
    current_role_new = auth_page.employee_current_role()

    with allure.step("FT. Проверка соответствия ролей сотрудника в проекте до и после теста"):
        assert current_role_old not in current_role_new

    auth_page.close_employee_page()
    auth_page.del_employee(test_email)
    auth_page.del_project(project)


@allure.id("ТК-05. Сотрудники")
@allure.severity("Critical")
@allure.story("Назначение сотрудника в отдел")
@allure.feature("Edit")
@allure.title("ТК-05. Сотрудники. Положительная проверка. Назначение сотрудника в отдел")
def test_employee_to_department(driver, login: str, password: str, test_email: str, depart: str) -> None:
    """
    Тест является положительной проверкой функции назначения сотрудника в отдел.
    В ходе теста в компанию добавляется аккаунт сотрудника и новый отдел.
    В ходе выполнения сотрудник назначается в отдел.
    Проверка успешного выполнения теста осуществляется по наличию
    должности в отделе у сотрудника (чек-боксы на странице являются просто графическими элементами).
    После выполнения проверки тестовые данные удаляются.

    :param driver: WebDriver — объект драйвера Selenium. Установлен в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param test_email: str - тестовый аккаунт. Установлен в фикстурах в файле conftest.py.

    :param depart: str - тестовый отдел. Установлен в фикстурах в файле conftest.py.
    """
    auth_page = AuthPage(driver)
    auth_page.go()
    auth_page.login_as(login, password)
    auth_page.go_to_my_company()
    auth_page.add_employee(test_email)
    auth_page.create_department(depart)
    auth_page.employee_to_department(test_email, depart)
    check = auth_page.employee_current_department(test_email, depart)

    with allure.step("FT. Проверка по наличию роли в проекте (галочка не является чек-боксом)"):
        assert check.is_displayed()

    auth_page.close_employee_page()
    auth_page.del_employee(test_email)
    auth_page.del_department(depart)
