# import time
# from selenium.webdriver.common.by import By
#
# def test_petfriends(selenium):
#     # Open PetFriends base page:
#     selenium.get("https://petfriends.skillfactory.ru/")
#
#     time.sleep(5)  # just for demo purposes, do NOT repeat it on real projects!
#
#     # click on the new user button
#     btn_newuser = selenium.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
#
#     btn_newuser.click()
#
#     # click existing user button
#     btn_exist_acc = selenium.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")
#     btn_exist_acc.click()
#
#     # add email
#     field_email = selenium.find_element(By.ID, "email")
#     field_email.clear()
#     field_email.send_keys("ascddrtf@mail.ru")
#
#     # add password
#     field_pass = selenium.find_element(By.ID, "pass")
#     field_pass.clear()
#     field_pass.send_keys("11235813")
#
#     # click submit button
#     btn_submit = selenium.find_element(By.XPATH, "//button[@type='submit']")
#     btn_submit.click()
#
#     time.sleep(10)  # just for demo purposes, do NOT repeat it on real projects!
#     if selenium.current_url == 'https://petfriends.skillfactory.ru/all_pets':
#         # Make the screenshot of browser window:
#         selenium.save_screenshot('result_petfriends.png')
#     else:
#         raise Exception("login error")

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"


images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

for i in range(len(names)):
    assert images[i].get_attribute('src') != ''
    assert names[i].text != ''
    assert descriptions[i].text != ''
    assert ', ' in descriptions[i]
    parts = descriptions[i].text.split(", ")
    assert len(parts[0]) > 0
    assert len(parts[1]) > 0
