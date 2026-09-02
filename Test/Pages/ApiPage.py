import requests
import allure
from faker import Faker


fake = Faker("ru_RU")


class ApiPage:
    def __init__(self, base_url: str) -> None:
        """
        Конструктор задает неизменную часть URL запросов.

        :param base_url: str — часть адреса веб-страницы постоянная для всех запосов.
        """
        self.url = base_url

    @allure.step("API. Получение ключа компании через API")
    def _get_company_id(self, login: str, password: str, company: str) -> str:
        """
        Метод служит для получения токена авторизации для использования в тестовых запросах:
        1. В первом запросе возвращается id компании;
        2. Во втором запросе возвращается ключ авторизации для данной компании.

        :param login: str - логин для входа в личный кабинет.
        :param password: str - пароль для входа в личный кабинет.
        :param company: str - компания для проведения тестов.
        """
        with allure.step("API. Получение id компании через API"):
            login_date_id = {
                "login": login,
                "password": password,
                "name": company
                }

        headers = {"Content-Type": "application/json"}
        resp_id = requests.post(
            self.url + "/api-v2/auth/companies", json=login_date_id, headers=headers)

        id_company = resp_id.json()["content"][0]["id"]

        with allure.step("API. Получение ключа авторизации компании через API"):
            login_date_key = {
                "login": login,
                "password": password,
                "companyId": id_company
                }

        resp_key = requests.post(
            self.url + "/api-v2/auth/keys/get", json=login_date_key, headers=headers)
        key_company = resp_key.json()[0]["key"]

        headers["Authorization"] = f"Bearer {key_company}"
        return headers

    @allure.step("API. Получение id сотрудника")
    def _get_client_id(self, headers: str) -> int:
        """
        Метод служит для получения id сотрудника.

        :param headers: str - ключ авторизации.
        """
        resp = requests.get(self.url + "/api-v2/users", headers=headers)
        assert resp.json()["paging"]["count"] > 0
        user_id = resp.json()["content"][0]["id"]
        return user_id

    @allure.step("API. Получение id проекта")
    def _get_project_id(self, headers: str, numProject: int) -> int:
        """
        Метод служит для получения id проекта.

        :param headers: str - ключ авторизации.
        :param numProject: int - индекс проекта из списка проектов.
        """
        resp = requests.get(self.url + "/api-v2/projects", headers=headers)
        project_id = resp.json()["content"][numProject]["id"]
        return project_id

    @allure.step("API. Получение индекса проекта из списка проектов")
    def _get_project_number(self, headers: str, projectApi: str) -> int:
        """
        Метод служит для поиска индекса проекта в списке проектов.

        :param headers: str - ключ авторизации.
        :param projectApi: str - наименование тестового проекта в API.
        """
        resp = requests.get(self.url + "/api-v2/projects", headers=headers)
        data = resp.json()

        content = data.get("content", [])
        target_title = projectApi
        found_index = None

        for idx, proj in enumerate(content):
            if proj.get("title") == target_title:
                found_index = idx
                break

        assert found_index is not None, f"Проект с title='{target_title}' не найден"
        return found_index

    @allure.step("API. Получение индекса отдела из списка отделов")
    def _get_department_number(self, headers: str, departmentApi: str) -> int:
        """
        Метод служит для поиска индекса отдела в списке отделов.

        :param headers: str - ключ авторизации.
        :param departmentApi: str - наименование тестового отдела в API.
        """
        resp = requests.get(self.url + "/api-v2/departments", headers=headers)
        data = resp.json()

        content = data.get("content", [])

        target_title = departmentApi
        found_index = None

        for idx, depart in enumerate(content):
            if depart.get("title") == target_title:
                found_index = idx
                break

        assert found_index is not None, f"Департамент с title='{target_title}' не найден"
        return found_index

    @allure.step("API. Получение id отдела")
    def _get_department_id(self, headers: str, numDepart: int) -> int:
        """
        Метод служит для получения id тестового отдела.

        :param headers: str - ключ авторизации.
        :param numDepart: str - наименование тестового отдела в API.
        """
        resp = requests.get(self.url + "/api-v2/departments", headers=headers)
        department_id = resp.json()["content"][numDepart]["id"]
        return department_id

    @allure.step("API. Создание проекта")
    def create_projects(self, headers: str, project_name: str) -> int:
        """
        Метод используется для создания тестового проекта.
        :param headers: str - ключ авторизации.
        :param project_name: str - название проекта.
        """
        user_id = self._get_client_id(headers)
        with allure.step("API. Формирование JSON для тестового запроса"):
            project = {
                "title": project_name,
                "users": {user_id: "worker"}
                }
        with allure.step("API. Отправка тестового запроса"):
            resp = requests.post(
                self.url + "/api-v2/projects", json=project, headers=headers)
        return resp

    @allure.step("API. Удаление проекта")
    def delete_projects(self, headers: str, project_name: str) -> int:
        """
        Метод используется для удаления тестового проекта.
        :param headers: str - ключ авторизации.
        :param project_name: str - название проекта.
        """
        numProject = self._get_project_number(headers, project_name)
        project_id = self._get_project_id(headers, numProject)
        with allure.step("API. Формирование JSON для тестового запроса"):
            project = {
                "deleted": True
                }
        with allure.step("API. Отправка тестового запроса"):
            resp = requests.put(
                self.url + "/api-v2/projects/" + project_id, json=project, headers=headers)
        return resp

    @allure.step("API. Получение списка проектов")
    def list_projects(self, headers: str) -> dict:
        """
        Метод используется для получения списка проектов.
        :param headers: str - ключ авторизации.
        """
        with allure.step("API. Отправка тестового запроса"):
            resp = requests.get(self.url + "/api-v2/projects", headers=headers)
        return resp

    @allure.step("API. Изменение названия проекта")
    def edit_projects(self, headers: str, project_name: str, project_name_new: str, role: str) -> int:
        """
        Метод используется для изменения названия проекта и роли сотрудника.
        :param headers: str - ключ авторизации.
        :param project_name: str - название проекта.
        :param project_name_new: str - новое название проекта.
        :param role: str - роль сотрудника в проекте.
        """
        numProject = self._get_project_number(headers, project_name)
        project_id = self._get_project_id(headers, numProject)
        user_id = self._get_client_id(headers)
        with allure.step("API. Формирование JSON для тестового запроса"):
            project = {
                "title": project_name_new,
                "users": {user_id: role}
            }
        with allure.step("API. Отправка тестового запроса"):
            resp = requests.put(
                self.url + "/api-v2/projects/" + project_id, json=project, headers=headers)
        return resp

    @allure.step("API. Создание отдела")
    def create_departments(self, headers: str, department_name: str) -> int:
        """
        Метод используется для создания тестового отдела.
        :param headers: str - ключ авторизации.
        :param department_name: str - название отдела.
        """
        user_id = self._get_client_id(headers)
        with allure.step("API. Формирование JSON для тестового запроса"):
            department = {
                "title": department_name,
                "users": {user_id: "manager"}
                }
        with allure.step("API. Отправка тестового запроса"):
            resp = requests.post(
                self.url + "/api-v2/departments", json=department, headers=headers)
        return resp

    @allure.step("API. Удаление отдела")
    def delete_department(self, headers: str, department_name: str) -> int:
        """
        Метод используется для удаления тестового отдела.
        :param headers: str - ключ авторизации.
        :param department_name: str - название отдела.
        """
        numDepartment = self._get_department_number(headers, department_name)
        department_id = self._get_department_id(headers, numDepartment)
        with allure.step("API. Формирование JSON для тестового запроса"):
            department = {
                "deleted": True
                }
        with allure.step("API. Отправка тестового запроса"):
            resp = requests.put(
                self.url + "/api-v2/departments/" + department_id, json=department, headers=headers)
        return resp

    @allure.step("API. Изменение названия отдела")
    def edit_name_department(self, headers: str, department_name: str, department_name_new: str) -> int:
        """
        Метод используется для удаления тестового отдела.
        :param headers: str - ключ авторизации.
        :param department_name: str - название отдела.
        """
        numDepartment = self._get_department_number(headers, department_name)
        department_id = self._get_department_id(headers, numDepartment)
        with allure.step("API. Формирование JSON для тестового запроса"):
            department = {
                "title": department_name_new
                }
        with allure.step("API. Отправка тестового запроса"):
            resp = requests.put(
                self.url + "/api-v2/departments/" + department_id, json=department, headers=headers)
        return resp

    @allure.step("API. Создание отдела ошибочным методом (patch)")
    def create_departments_error(self, headers: str, department_name: str) -> int:
        """
        Метод используется для создания тестового отдела.
        :param headers: str - ключ авторизации.
        :param department_name: str - название отдела.
        """
        user_id = self._get_client_id(headers)
        with allure.step("API. Формирование JSON для тестового запроса"):
            department = {
                "title": department_name,
                "users": {user_id: "manager"}
                }
        with allure.step("API. Отправка тестового запроса"):
            resp = requests.patch(
                self.url + "/api-v2/departments", json=department, headers=headers)
        return resp
