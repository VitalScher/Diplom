import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from time import sleep

from Pages.AuthPage import AuthPage


def test_auth(driver):	
    auth_page = AuthPage(driver)
    auth_page.go()
    auth_page.login_as("vitsch2@yandex.ru", "F)94jU/A;U@fv4Q-")
    auth_page.go_to_my_company()
    auth_page.add_employee("vitsch@yandex.ru")

    sleep (10)
    



