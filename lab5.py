from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select

BASE_URL = "https://the-internet.herokuapp.com"
TIMEOUT = 10


def test_dropdown():
    driver = webdriver.Chrome()
    try:
        wait = WebDriverWait(driver, TIMEOUT)
        driver.get(f"{BASE_URL}/dropdown")

        dropdown = wait.until(EC.element_to_be_clickable((By.ID, "dropdown")))
        select = Select(dropdown)
        select.select_by_visible_text("Option 1")

        selected = select.first_selected_option.text
        assert selected == "Option 1", f"Ожидали 'Option 1', выбрано: {selected!r}"
    finally:
        driver.quit()


def test_checkbox():
    driver = webdriver.Chrome()
    try:
        wait = WebDriverWait(driver, TIMEOUT)
        driver.get(f"{BASE_URL}/checkboxes")

        checkboxes = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")
            )
        )
        assert len(checkboxes) == 2, f"Ожидали 2 чекбокса, найдено: {len(checkboxes)}"

        first = checkboxes[0]
        state_before = first.is_selected()
        first.click()
        state_after = first.is_selected()

        assert state_after != state_before, (
            f"Состояние первого чекбокса не изменилось (было {state_before})"
        )
    finally:
        driver.quit()


def test_alert():
    driver = webdriver.Chrome()
    try:
        wait = WebDriverWait(driver, TIMEOUT)
        driver.get(f"{BASE_URL}/javascript_alerts")

        button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Click for JS Alert']")
            )
        )
        button.click()

        alert = wait.until(EC.alert_is_present())
        alert.accept()

        result = wait.until(EC.visibility_of_element_located((By.ID, "result")))
        assert "You successfully clicked an alert" in result.text, (
            f"Неожиданный текст результата: {result.text!r}"
        )
    finally:
        driver.quit()


def test_new_window():
    driver = webdriver.Chrome()
    try:
        wait = WebDriverWait(driver, TIMEOUT)
        driver.get(f"{BASE_URL}/windows")

        original_window = driver.current_window_handle

        link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here")))
        link.click()

        wait.until(EC.number_of_windows_to_be(2))
        new_window = [h for h in driver.window_handles if h != original_window][0]
        driver.switch_to.window(new_window)

        heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
        assert "New Window" in heading.text, (
            f"На новой вкладке нет текста 'New Window': {heading.text!r}"
        )

        driver.close()  # закрываем новую вкладку
        driver.switch_to.window(original_window)
        assert driver.current_window_handle == original_window, (
            "Не удалось вернуться на исходную вкладку"
        )
    finally:
        driver.quit()


if __name__ == "__main__":
    test_dropdown()
    test_checkbox()
    test_alert()
    test_new_window()
    print("Все тесты пройдены!")