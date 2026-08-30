import requests
import allure


class ApiPage:
    def __init__(self, base_url: str) -> None:
        """
        Конструктор задает неизменную часть URL запросов.

        :param base_url: str — часть адреса веб-страницы постоянная для всех запосов.
        """
        self.url = base_url

    @allure.step("API. Получение ключа компании через API")
    def get_company_id(self, login: str, password: str, company: str) -> str:
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
    def get_client_id(self, headers: str) -> int:
        """
        Метод служит для получения id сотрудника.

        :param headers: str - ключ авторизации.
        """
        resp = requests.get(self.url + "/api-v2/users", headers=headers)
        assert resp.json()["paging"]["count"] > 0
        user_id = resp.json()["content"][0]["id"]
        return user_id

    @allure.step("API. Получение id проекта")
    def get_project_id(self, headers: str, numProject: int) -> int:
        """
        Метод служит для получения id проекта.

        :param headers: str - ключ авторизации.
        :param numProject: int - индекс проекта из списка проектов.
        """
        resp = requests.get(self.url + "/api-v2/projects", headers=headers)
        project_id = resp.json()["content"][numProject]["id"]
        return project_id

    @allure.step("API. Получение индекса проекта из списка проектов")
    def get_project_number(self, headers: str, projectApi: str) -> int:
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
    def get_department_number(self, headers: str, departmentApi: str) -> int:
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
    def get_department_id(self, headers: str, numDepart: int) -> int:
        """
        Метод служит для id тестового отдела.

        :param headers: str - ключ авторизации.
        :param numDepart: str - наименование тестового отдела в API.
        """
        resp = requests.get(self.url + "/api-v2/departments", headers=headers)
        department_id = resp.json()["content"][numDepart]["id"]
        return department_id
