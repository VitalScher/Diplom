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
    return " "  # Здесь указать логин для входа на сайт YouGile


@pytest.fixture
def password():
    """
    Фикстура используется в тестировании для авторизации на портале YuoGile. Задет пароль
    """
    return " "  # Здесь указать пароль для входа на сайт YouGile


@pytest.fixture
def company():
    """
    Фикстура используется в тестировании API. Задет наименование компании, созданной для тестирования
    """
    return " "  # Здесь указать название тестовой компании на сайт YouGile


@pytest.fixture
def test_email():
    """
    Фикстура используется в функциональном тестировании для создания тестового сотрудника
    """
    return " "  # Здесь указать аккаунт для проведения тестов


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
