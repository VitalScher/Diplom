import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(4)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def login():
    return "vitsch2@yandex.ru"


@pytest.fixture
def password():
    return "F)94jU/A;U@fv4Q-"


@pytest.fixture
def company():
    return "QA 134.2"


@pytest.fixture
def test_email():
    return "vitsch@yandex.ru"


@pytest.fixture
def project():
    return "123"


@pytest.fixture
def depart():
    return "456"


@pytest.fixture
def base_url():
    return "https://ru.yougile.com"
