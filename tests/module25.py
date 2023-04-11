import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome()
    # переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.implicitly_wait(5)
    pytest.driver.find_element(By.ID, 'email').send_keys('ascddrtf@mail.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('11235813')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    images = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-img-top')))
    names = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-title')))
    descriptions = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-text')))

    for i in range(len(names)):
        assert images[i].get_attribute('src') != '', 'Image not found'
        assert names[i].text != '', 'Name not found'
        assert descriptions[i].text != '', 'Description not found'
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
