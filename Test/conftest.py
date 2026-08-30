import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    """
    Фикстура используется в функциональном тестировании для задания webdriver
    """
    driver = webdriver.Chrome()
    driver.implicitly_wait(4)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def login():
    """
    Фикстура используется в тестировании для авторизации на портале YuoGile. Задет логин
    """
    return "vitsch2@yandex.ru"


@pytest.fixture
def password():
    """
    Фикстура используется в тестировании для авторизации на портале YuoGile. Задет пароль
    """
    return "F)94jU/A;U@fv4Q-"


@pytest.fixture
def company():
    """
    Фикстура используется в тестировании API. Задет наименование компании, созданной для тестирования
    """
    return "QA 134.2"


@pytest.fixture
def test_email():
    """
    Фикстура используется в функциональном тестировании для создания тестового сотрудника
    """
    return "vitsch@yandex.ru"


@pytest.fixture
def project():
    """
    Фикстура используется в функциональном тестировании для создания тестового проекта
    """
    return "123"


@pytest.fixture
def depart():
    """
    Фикстура используется в функциональном тестировании для создания тестового отдела
    """
    return "456"


@pytest.fixture
def base_url():
    """
    Фикстура используется в тестировании API для создания постоянной части запросов URL
    """
    return "https://ru.yougile.com"
