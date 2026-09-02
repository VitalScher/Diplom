from Pages.ApiPage import ApiPage
import allure
from faker import Faker


fake = Faker("ru_RU")


@allure.id("ТК-06. Проекты")
@allure.severity("Critical")
@allure.story("Создать новый проект")
@allure.feature("Create")
@allure.title("ТК-06. Проекты. Положительная проверка. Создать новый проект с корректными данными")
def test_create_projects_positive(base_url: str, login: str, password: str, company: str) -> None:
    """
    Тест является положительной проверкой по созданию проекта. В качестве тестового запроса отправляется имя компании и роль сотрудника в проекте.
    Проверка успешности выполнения теста осуществляется по возвращаемому статус коду - 201

    :param base_url: str - часть адреса веб-страницы постоянная для всех запосов. Установлена в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param company: str - компания для проведения тестов. Установлена в фикстурах в файле conftest.py.
    """
    api = ApiPage(base_url)
    with allure.step("API. Данные для проведения теста"):
        project_name = f"Проект {fake.city()}"

    with allure.step("API. Получение ключа авторизации"):
        headers = api._get_company_id(login, password, company)

    resp = api.create_projects(headers, project_name)
    with allure.step("API. Проверка возвращаемого статус кода"):
        assert resp.status_code == 201


@allure.id("ТК-07. Проекты")
@allure.severity("Critical")
@allure.story("Удаление проекта")
@allure.feature("Delete")
@allure.title("ТК-07. Проекты. Положительная проверка. Удаление добавленного проекта")
def test_del_project_positive(base_url: str, login: str, password: str, company: str) -> None:
    """
    Тест является положительной проверкой по удалению тестового проекта.
    Проверка успешности выполнения теста осуществляется по возвращаемому статус коду - 200.

    :param base_url: str - часть адреса веб-страницы постоянная для всех запосов. Установлена в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param company: str - компания для проведения тестов. Установлена в фикстурах в файле conftest.py.
    """
    api = ApiPage(base_url)
    with allure.step("API. Данные для проведения теста"):
        project_name = f"Проект {fake.city()}"

    with allure.step("API. Получение ключа авторизации"):
        headers = api._get_company_id(login, password, company)

    api.create_projects(headers, project_name)
    resp = api.delete_projects(headers, project_name)

    with allure.step("API. Проверка возвращаемого статус кода"):
        assert resp.status_code == 200


@allure.id("ТК-08. Проекты")
@allure.severity("Critical")
@allure.story("Получение списка проектов")
@allure.feature("Read")
@allure.title("ТК-08. Проекты. Положительная проверка. Получить список проектов")
def test_get_list_projects(base_url: str, login: str, password: str, company: str) -> None:
    """
    Тест является положительной проверкой по получению списка проектов в компании.
    Проверка успешности выполнения теста осуществляется длине возвращаемого списка. Она должна быть больше 0.

    :param base_url: str - часть адреса веб-страницы постоянная для всех запосов. Установлена в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param company: str - компания для проведения тестов. Установлена в фикстурах в файле conftest.py.
    """
    api = ApiPage(base_url)
    with allure.step("API. Данные для проведения теста"):
        project_name = f"Проект {fake.city()}"

    with allure.step("API. Получение ключа авторизации"):
        headers = api._get_company_id(login, password, company)

    api.create_projects(headers, project_name)
    resp = api.list_projects(headers)

    with allure.step("API. Проверка возвращаемого статус кода"):
        assert resp.json()["paging"]["count"] > 0

    api.delete_projects(headers, project_name)


@allure.id("ТК-09. Проекты")
@allure.severity("Critical")
@allure.story("Редактирование проекта")
@allure.feature("Edit")
@allure.title("ТК-09. Проекты. Положительная проверка. Изменить названия проекта")
def test_change_project_positive(base_url: str, login: str, password: str, company: str) -> None:
    """
    Тест является положительной проверкой по редактиованию названия проекта.
    Проверка успешности выполнения теста осуществляется по возвращаемому статус коду - 200.

    :param base_url: str - часть адреса веб-страницы постоянная для всех запосов. Установлена в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param company: str - компания для проведения тестов. Установлена в фикстурах в файле conftest.py.
    """
    api = ApiPage(base_url)
    with allure.step("API. Данные для проведения теста"):
        project_name = f"Проект {fake.city()}"
        project_name_new = f"Проект {fake.city()}"
        role = "worker"

    with allure.step("API. Получение ключа авторизации"):
        headers = api._get_company_id(login, password, company)

    api.create_projects(headers, project_name)
    resp = api.edit_projects(headers, project_name, project_name_new, role)

    with allure.step("API. Проверка возвращаемого статус кода"):
        assert resp.status_code == 200

    api.delete_projects(headers, project_name_new)


@allure.id("ТК-10. Проекты")
@allure.severity("Critical")
@allure.story("Редактирование проекта")
@allure.feature("Edit")
@allure.title("ТК-10. Проекты. Отрицательная проверка. Указание некорректной роли участника проекта")
def test_role_client_negative(base_url: str, login: str, password: str, company: str) -> None:
    """
    Тест является отрицательной проверкой по редактированию проекта методом указания некорректной роли участнику проекта.
    Проверка успешности выполнения теста осуществляется по возвращаемому статус коду - 400.

    :param base_url: str - часть адреса веб-страницы постоянная для всех запосов. Установлена в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param company: str - компания для проведения тестов. Установлена в фикстурах в файле conftest.py.
    """
    api = ApiPage(base_url)
    with allure.step("API. Данные для проведения теста"):
        project_name = f"Проект {fake.city()}"
        project_name_new = f"Проект {fake.city()}"
        role = "Boss"

    with allure.step("API. Получение ключа авторизации"):
        headers = api._get_company_id(login, password, company)

    api.create_projects(headers, project_name)
    resp = api.edit_projects(headers, project_name, project_name_new, role)

    with allure.step("API. Проверка возвращаемого статус кода"):
        assert resp.status_code == 400


@allure.id("ТК-11. Отделы")
@allure.severity("Critical")
@allure.story("Создание отдела")
@allure.feature("Create")
@allure.title("ТК-11. Отделы. Положительная проверка. Создать отдел в компании")
def test_create_department(base_url: str, login: str, password: str, company: str) -> None:
    """
    Тест является положительной проверкой по созданию отдела.
    Проверка успешности выполнения теста осуществляется по возвращаемому статус коду - 201.

    :param base_url: str - часть адреса веб-страницы постоянная для всех запосов. Установлена в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param company: str - компания для проведения тестов. Установлена в фикстурах в файле conftest.py.
    """
    api = ApiPage(base_url)
    with allure.step("API. Данные для проведения теста"):
        department_name = f"Отдел {fake.country()}"

    with allure.step("API. Получение ключа авторизации"):
        headers = api._get_company_id(login, password, company)

    resp = api.create_departments(headers, department_name)

    with allure.step("API. Проверка возвращаемого статус кода"):
        assert resp.status_code == 201


@allure.id("ТК-12. Отделы")
@allure.severity("Critical")
@allure.story("Удаление отдела")
@allure.feature("Delete")
@allure.title("ТК-12. Отделы. Положительная проверка. Удаление добавленного отдела")
def test_del_department_positive(base_url: str, login: str, password: str, company: str) -> None:
    """
    Тест является положительной проверкой по удалению тестового отдела.
    Проверка успешности выполнения теста осуществляется по возвращаемому статус коду - 200.

    :param base_url: str - часть адреса веб-страницы постоянная для всех запосов. Установлена в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param company: str - компания для проведения тестов. Установлена в фикстурах в файле conftest.py.
    """
    api = ApiPage(base_url)
    with allure.step("API. Данные для проведения теста"):
        department_name = f"Отдел {fake.country()}"

    with allure.step("API. Получение ключа авторизации"):
        headers = api._get_company_id(login, password, company)

    api.create_departments(headers, department_name)

    resp = api.delete_department(headers, department_name)
    with allure.step("API. Проверка возвращаемого статус кода"):
        assert resp.status_code == 200


@allure.id("ТК-13. Отделы")
@allure.severity("Critical")
@allure.story("Редактирование отдела")
@allure.feature("Edit")
@allure.title("ТК-13. Отделы. Положительная проверка. Изменить название отдела")
def test_change_name_department(base_url: str, login: str, password: str, company: str) -> None:
    """
    Тест является положительной проверкой по редактированию отдела путем изменения его наименования.
    Проверка успешности выполнения теста осуществляется по возвращаемому статус коду - 200.

    :param base_url: str - часть адреса веб-страницы постоянная для всех запосов. Установлена в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param company: str - компания для проведения тестов. Установлена в фикстурах в файле conftest.py.
    """
    api = ApiPage(base_url)
    with allure.step("API. Данные для проведения теста"):
        department_name = f"Отдел {fake.country()}"
        department_name_new = f"Отдел {fake.country()}"

    with allure.step("API. Получение ключа авторизации"):
        headers = api._get_company_id(login, password, company)

    api.create_departments(headers, department_name)

    resp = api.edit_name_department(headers, department_name, department_name_new)
    with allure.step("API. Проверка возвращаемого статус кода"):
        assert resp.status_code == 200

    api.delete_department(headers, department_name_new)


@allure.id("ТК-14. Отделы")
@allure.severity("Critical")
@allure.story("Создание отдела")
@allure.feature("Create")
@allure.title("ТК-14. Отделы. Отрицательная проверка. Создание отдела в компании с ошибочным методом")
def test_create_department_negative(base_url: str, login: str, password: str, company: str) -> None:
    """
    Тест является отрицательной проверкой по созданию отдела с использованием ошибочного метода.
    Проверка успешности выполнения теста осуществляется по возвращаемому статус коду - 404.

    :param base_url: str - часть адреса веб-страницы постоянная для всех запосов. Установлена в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param company: str - компания для проведения тестов. Установлена в фикстурах в файле conftest.py.
    """
    api = ApiPage(base_url)
    with allure.step("API. Данные для проведения теста"):
        department_name = f"Отдел {fake.country()}"

    with allure.step("API. Получение ключа авторизации"):
        headers = api._get_company_id(login, password, company)

    resp = api.create_departments_error(headers, department_name)

    with allure.step("API. Проверка возвращаемого статус кода"):
        assert resp.status_code == 404
