import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

from Pages.AuthPage import AuthPage


def test_add_employee(driver, login: str, password: str, test_email: str):
    auth_page = AuthPage(driver)
    auth_page.go()
    auth_page.login_as(login, password)
    auth_page.go_to_my_company()
    auth_page.add_employee(test_email)

    assert test_email in driver.page_source, "Текст отсутствует в HTML"
    auth_page.del_employee(test_email)


def test_del_employee(driver, login: str, password: str, test_email: str):
    auth_page = AuthPage(driver)
    auth_page.go()
    auth_page.login_as(login, password)
    auth_page.go_to_my_company()
    auth_page.add_employee(test_email)
    auth_page.del_employee(test_email)

    assert test_email not in driver.page_source, "Текст присутствует в HTML"


def test_employee_to_new_projet(driver, login: str, password: str, test_email: str, project: str):
    auth_page = AuthPage(driver)
    auth_page.go()
    auth_page.login_as(login, password)
    auth_page.go_to_my_company()
    auth_page.add_employee(test_email)
    auth_page.create_project(project)
    auth_page.go_to_my_company()
    auth_page.employee_to_project(test_email, project)
    auth_page.employee_page(test_email, project)

    # Проверка по наличию роли в проекте (галочка не является чек-боксом)
    check = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.XPATH, "//div[@class='prj-invite prj-invite--user']//div[1]//div[2]//div[1]//div[1]//div[1]")))
    assert check.is_displayed()
    driver.find_element(By.XPATH, "//div[@class='prj-invite__close']").click()

    auth_page.del_employee(test_email)
    auth_page.del_project(project)


def test_employee_role(driver, login: str, password: str, test_email: str, project: str):
    auth_page = AuthPage(driver)
    auth_page.go()
    auth_page.login_as(login, password)
    auth_page.go_to_my_company()
    auth_page.add_employee(test_email)
    auth_page.create_project(project)
    auth_page.go_to_my_company()
    auth_page.employee_to_project(test_email, project)
    auth_page.employee_page(test_email, project)
    current_role_old = auth_page.employee_current_role()
    auth_page.employee_change_role()
    auth_page.employee_page(test_email, project)
    current_role_new = auth_page.employee_current_role()

    assert current_role_old not in current_role_new
    driver.find_element(By.XPATH, "//div[@class='prj-invite__close']").click()

    auth_page.del_employee(test_email)
    auth_page.del_project(project)


def test_employee_to_department(driver, login: str, password: str, test_email: str, depart: str):
    auth_page = AuthPage(driver)
    auth_page.go()
    auth_page.login_as(login, password)
    auth_page.go_to_my_company()
    auth_page.add_employee(test_email)
    auth_page.create_department(depart)
    auth_page.employee_to_department(test_email, depart)
    auth_page.employee_current_department(test_email, depart)

    # Проверка по наличию роли в проекте (галочка не является чек-боксом)
    check = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "(//div[@class='prj-invite-role__name'])[1]")))
    assert check.is_displayed()
    driver.find_element(By.XPATH, "//div[@class='prj-invite__close']").click()

    auth_page.del_employee(test_email)
    auth_page.del_department(depart)
