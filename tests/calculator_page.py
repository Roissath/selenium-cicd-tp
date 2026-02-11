import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver

    @property
    def num1(self):
        return self.driver.find_element(By.ID, "num1")

    @property
    def num2(self):
        return self.driver.find_element(By.ID, "num2")

    @property
    def operation(self):
        return self.driver.find_element(By.ID, "operation")

    @property
    def calculate_button(self):
        return self.driver.find_element(By.ID, "calculate")

    def load_page(self):
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "src", "index.html")
        )
        self.driver.get(f"file://{file_path}")

    def wait_ready(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "calculator"))
        )

    def enter_first_number(self, value):
        self.num1.clear()
        self.num1.send_keys(str(value))

    def enter_second_number(self, value):
        self.num2.clear()
        self.num2.send_keys(str(value))

    def select_operation(self, operation):
        select = Select(self.operation)
        select.select_by_value(operation)

    def click_calculate(self):
        self.calculate_button.click()

    def get_result(self):
        result = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        return result.text
