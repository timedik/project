import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@allure.feature("Поиск в Wikipedia")
@allure.story("Поиск статьи")
@allure.title("Поиск статьи 'Россия'")
def test_search_russia():
    driver = None
    try:
        with allure.step("Открыть браузер"):
            driver = webdriver.Chrome()
            wait = WebDriverWait(driver, 15)

        with allure.step("Открыть сайт Wikipedia"):
            driver.get("https://www.wikipedia.org")

        with allure.step("Ввести слово 'Россия' в поле поиска"):
            search = wait.until(
                EC.visibility_of_element_located((By.ID, "searchInput"))
            )
            search.send_keys("Россия")

        with allure.step("Нажать Enter"):
            search.send_keys(Keys.ENTER)

        with allure.step("Проверить заголовок статьи"):
            heading = wait.until(
                EC.visibility_of_element_located((By.ID, "firstHeading"))
            )
            assert "Россия" in heading.text, (
                f"В заголовке нет слова 'Россия': {heading.text!r}"
            )

        # Доп. задание: скриншот прикрепляется прямо в отчёт
        with allure.step("Сделать скриншот"):
            driver.save_screenshot("screenshot.png")
            allure.attach.file(
                "screenshot.png",
                name="Скриншот страницы",
                attachment_type=allure.attachment_type.PNG,
            )
    finally:
        with allure.step("Закрыть браузер"):
            if driver is not None:
                driver.quit()