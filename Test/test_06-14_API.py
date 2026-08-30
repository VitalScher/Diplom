import requests
from Pages.ApiPage import ApiPage
import allure


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
    headers = api.get_company_id(login, password, company)
    user_id = api.get_client_id(headers)
    with allure.step("API. Формирование JSON для тестового запроса"):
        project = {
            "title": "Новый проект",
            "users": {user_id: "worker"}
        }
    with allure.step("API. Отправка тестового запроса"):
        resp = requests.post(
            base_url + "/api-v2/projects", json=project, headers=headers)
    assert resp.status_code == 201


@allure.id("ТК-07. Проекты")
@allure.severity("Critical")
@allure.story("Получение списка проектов")
@allure.feature("Read")
@allure.title("ТК-07. Проекты. Положительная проверка. Получить список проектов")
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
    headers = api.get_company_id(login, password, company)
    with allure.step("API. Отправка тестового запроса"):
        resp = requests.get(base_url + "/api-v2/projects", headers=headers)
    assert resp.json()["paging"]["count"] > 0


@allure.id("ТК-08. Проекты")
@allure.severity("Critical")
@allure.story("Редактирование проекта")
@allure.feature("Edit")
@allure.title("ТК-08. Проекты. Положительная проверка. Изменить названия проекта")
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
    headers = api.get_company_id(login, password, company)
    numProject = api.get_project_number(headers, projectApi="Новый проект")
    project_id = api.get_project_id(headers, numProject)
    user_id = api.get_client_id(headers)
    with allure.step("API. Формирование JSON для тестового запроса"):
        project = {
            "title": "Измененный проект",
            "users": {user_id: "worker"}
        }
    with allure.step("API. Отправка тестового запроса"):
        resp = requests.put(
            base_url + "/api-v2/projects/" + project_id, json=project, headers=headers)
    assert resp.status_code == 200


@allure.id("ТК-09. Проекты")
@allure.severity("Critical")
@allure.story("Редактирование проекта")
@allure.feature("Edit")
@allure.title("ТК-09. Проекты. Отрицательная проверка. Указание некорректной роли участника проекта")
def test_role_client_negative(base_url: str, login: str, password: str, company: str) -> None:
    """
    Тест является отрицательной проверкой по редактиованию проекта методом указания некоректной роли участнику проекта.
    Проверка успешности выполнения теста осуществляется по возвращаемому статус коду - 400.

    :param base_url: str - часть адреса веб-страницы постоянная для всех запосов. Установлена в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param company: str - компания для проведения тестов. Установлена в фикстурах в файле conftest.py.
    """
    api = ApiPage(base_url)
    headers = api.get_company_id(login, password, company)
    numProject = api.get_project_number(headers, projectApi="Измененный проект")
    project_id = api.get_project_id(headers, numProject)
    user_id = api.get_client_id(headers)
    with allure.step("API. Формирование JSON для тестового запроса"):
        project = {
            "title": "Измененный проект",
            "users": {user_id: "Boss"}
        }
    with allure.step("API. Отправка тестового запроса"):
        resp = requests.put(
            base_url + "/api-v2/projects/" + project_id, json=project, headers=headers)
    assert resp.status_code == 400


@allure.id("ТК-10. Проекты")
@allure.severity("Critical")
@allure.story("Удаление проекта")
@allure.feature("Delete")
@allure.title("ТК-10. Проекты. Положительная проверка. Удаление добавленного проекта")
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
    headers = api.get_company_id(login, password, company)
    numProject = api.get_project_number(headers, projectApi="Измененный проект")
    project_id = api.get_project_id(headers, numProject)
    with allure.step("API. Формирование JSON для тестового запроса"):
        project = {
            "deleted": True
        }
    with allure.step("API. Отправка тестового запроса"):
        resp = requests.put(
            base_url + "/api-v2/projects/" + project_id, json=project, headers=headers)
    assert resp.status_code == 200


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
    headers = api.get_company_id(login, password, company)
    user_id = api.get_client_id(headers)
    with allure.step("API. Формирование JSON для тестового запроса"):
        department = {
            "title": "Отдел разработки",
            "users": {user_id: "manager"}
        }
    with allure.step("API. Отправка тестового запроса"):
        resp = requests.post(
            base_url + "/api-v2/departments", json=department, headers=headers)
    assert resp.status_code == 201


@allure.id("ТК-12. Отделы")
@allure.severity("Critical")
@allure.story("Редактирование отдела")
@allure.feature("Edit")
@allure.title("ТК-12. Отделы. Положительная проверка. Изменить название отдела")
def test_change_name_department(base_url: str, login: str, password: str, company: str) -> None:
    """
    Тест является положительной проверкой по редактированию отдела путем изменерия его наименования.
    Проверка успешности выполнения теста осуществляется по возвращаемому статус коду - 200.

    :param base_url: str - часть адреса веб-страницы постоянная для всех запосов. Установлена в фикстурах в файле conftest.py.

    :param login: str - логин для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param password: str - пароль для входа в личный кабинет. Установлен в фикстурах в файле conftest.py.

    :param company: str - компания для проведения тестов. Установлена в фикстурах в файле conftest.py.
    """
    api = ApiPage(base_url)
    headers = api.get_company_id(login, password, company)
    numDepartment = api.get_department_number(headers, departmentApi="Отдел разработки")
    department_id = api.get_department_id(headers, numDepartment)
    with allure.step("API. Формирование JSON для тестового запроса"):
        department = {
                "title": "Отдел тестирования"
                }
    with allure.step("API. Отправка тестового запроса"):
        resp = requests.put(
            base_url + "/api-v2/departments/" + department_id, json=department, headers=headers)
    assert resp.status_code == 200


@allure.id("ТК-13. Отделы")
@allure.severity("Critical")
@allure.story("Создание отдела")
@allure.feature("Create")
@allure.title("ТК-13. Отделы. Отрицательная проверка. Создание отдела в компании с ошибочным методом")
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
    headers = api.get_company_id(login, password, company)
    user_id = api.get_client_id(headers)
    with allure.step("API. Формирование JSON для тестового запроса"):
        department = {
            "title": "Отдел разработки",
            "users": {user_id: "manager"}
        }
    with allure.step("API. Отправка тестового запроса"):
        resp = requests.patch(
            base_url + "/api-v2/departments", json=department, headers=headers)
    assert resp.status_code == 404


@allure.id("ТК-14. Отделы")
@allure.severity("Critical")
@allure.story("Удаление отдела")
@allure.feature("Delete")
@allure.title("ТК-14. Отделы. Положительная проверка. Удаление добавленного отдела")
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
    headers = api.get_company_id(login, password, company)
    numDepartment = api.get_department_number(headers, departmentApi="Отдел тестирования")
    department_id = api.get_department_id(headers, numDepartment)
    with allure.step("API. Формирование JSON для тестового запроса"):
        department = {
            "deleted": True
            }
    with allure.step("API. Отправка тестового запроса"):
        resp = requests.put(
            base_url + "/api-v2/departments/" + department_id, json=department, headers=headers)
    assert resp.status_code == 200
