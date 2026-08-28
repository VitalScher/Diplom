import requests
from Pages.ApiPage import ApiPage


# ТК-06. Положительная проверка. Создать новый проект с корректными данными
def test_create_projects_positive(base_url: str, login: str, password: str, company: str):
    api = ApiPage(base_url)
    headers = api.get_company_id(login, password, company)
    user_id = api.get_client_id(headers)
    project = {
        "title": "Новый проект",
        "users": {user_id: "worker"}
    }
    resp = requests.post(
        base_url + "/api-v2/projects", json=project, headers=headers)
    assert resp.status_code == 201


# ТК-07. Положительная проверка. Получить список проектов
def test_get_list_projects(base_url: str, login: str, password: str, company: str):
    api = ApiPage(base_url)
    headers = api.get_company_id(login, password, company)
    resp = requests.get(base_url + "/api-v2/projects", headers=headers)
    assert resp.json()["paging"]["count"] > 0


# ТК-08. Положительная проверка. Изменить названия проекта
def test_change_project_positive(base_url: str, login: str, password: str, company: str):
    api = ApiPage(base_url)
    headers = api.get_company_id(login, password, company)
    numProject = api.get_project_number(headers, projectApi="Новый проект")
    project_id = api.get_list_projects(headers, numProject)
    user_id = api.get_client_id(headers)
    project = {
        "title": "Измененный проект",
        "users": {user_id: "worker"}
    }
    resp = requests.put(
        base_url + "/api-v2/projects/" + project_id, json=project, headers=headers)
    assert resp.status_code == 200


# ТК-09. Отрицательная проверка. Указание некорректной роли участника проекта.
def test_role_client_negative(base_url: str, login: str, password: str, company: str):
    api = ApiPage(base_url)
    headers = api.get_company_id(login, password, company)
    numProject = api.get_project_number(headers, projectApi="Измененный проект")
    project_id = api.get_list_projects(headers, numProject)
    user_id = api.get_client_id(headers)
    project = {
        "title": "Измененный проект",
        "users": {user_id: "Boss"}
    }
    resp = requests.put(
        base_url + "/api-v2/projects/" + project_id, json=project, headers=headers)
    assert resp.status_code == 400


# ТК-10. Положительная проверка. Создать отдел в компании
def test_create_department(base_url: str, login: str, password: str, company: str):
    api = ApiPage(base_url)
    headers = api.get_company_id(login, password, company)
    user_id = api.get_client_id(headers)
    department = {
        "title": "Отдел разработки",
        "users": {user_id: "manager"}
    }
    resp = requests.post(
        base_url + "/api-v2/departments", json=department, headers=headers)
    assert resp.status_code == 201


# ТК-11. Положительная проверка. Изменить название отдела
def test_change_name_department(base_url: str, login: str, password: str, company: str):
    api = ApiPage(base_url)
    headers = api.get_company_id(login, password, company)
    numDepartment = api.get_department_number(headers, departmentApi="Отдел разработки")
    department_id = api.get_department_id(headers, numDepartment)
    department = {
            "title": "Отдел тестирования"
            }
    resp = requests.put(
        base_url + "/api-v2/departments/" + department_id, json=department, headers=headers)
    assert resp.status_code == 200


# ТК-12. Отрицательная проверка. Создание отдела в компании с ошибочным методом
def test_create_department_negative(base_url: str, login: str, password: str, company: str):
    api = ApiPage(base_url)
    headers = api.get_company_id(login, password, company)
    user_id = api.get_client_id(headers)
    department = {
        "title": "Отдел разработки",
        "users": {user_id: "manager"}
    }
    resp = requests.patch(
        base_url + "/api-v2/departments", json=department, headers=headers)
    assert resp.status_code == 404


# ТК-13. Положительная проверка. Удаление добавленного проекта
def test_del_project_positive(base_url: str, login: str, password: str, company: str):
    api = ApiPage(base_url)
    headers = api.get_company_id(login, password, company)
    numProject = api.get_project_number(headers, projectApi="Измененный проект")
    project_id = api.get_list_projects(headers, numProject)
    project = {
        "deleted": True
    }
    resp = requests.put(
        base_url + "/api-v2/projects/" + project_id, json=project, headers=headers)
    assert resp.status_code == 200


# ТК-14. Положительная проверка. Удаление добавленного отдела
def test_del_department_positive(base_url: str, login: str, password: str, company: str):
    api = ApiPage(base_url)
    headers = api.get_company_id(login, password, company)
    numDepartment = api.get_department_number(headers, departmentApi="Отдел тестирования")
    department_id = api.get_department_id(headers, numDepartment)
    department = {
        "deleted": True
        }
    resp = requests.put(
        base_url + "/api-v2/departments/" + department_id, json=department, headers=headers)
    assert resp.status_code == 200
