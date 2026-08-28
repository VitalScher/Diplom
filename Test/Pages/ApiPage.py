import requests


class ApiPage:
    def __init__(self, base_url):
        self.url = base_url

# Получение ключа компании
    def get_company_id(self, login: str, password: str, company: str):

        login_date_id = {
            "login": login,
            "password": password,
            "name": company
            }

        headers = {"Content-Type": "application/json"}
        resp_id = requests.post(
            self.url + "/api-v2/auth/companies", json=login_date_id, headers=headers)

        id_company = resp_id.json()["content"][0]["id"]

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

    def get_client_id(self, headers: dict[str, str]):
        resp = requests.get(self.url + "/api-v2/users", headers=headers)
        assert resp.json()["paging"]["count"] > 0
        user_id = resp.json()["content"][0]["id"]
        return user_id

    def get_list_projects(self, headers: dict[str, str], numProject: int):
        resp = requests.get(self.url + "/api-v2/projects", headers=headers)
        project_id = resp.json()["content"][numProject]["id"]
        return project_id

    def get_project_number(self, headers: dict[str, str], projectApi: str):
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

    def get_department_number(self, headers: dict[str, str], departmentApi: str):
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

    def get_department_id(self, headers: dict[str, str], numDepart: int):
        resp = requests.get(self.url + "/api-v2/departments", headers=headers)
        department_id = resp.json()["content"][numDepart]["id"]
        return department_id
