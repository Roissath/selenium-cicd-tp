import os
import subprocess
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from calculator_page import CalculatorPage


@pytest.fixture(scope="session", autouse=True)
def http_server():
    """Démarre un serveur HTTP local pour servir les fichiers statiques"""
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
    server = subprocess.Popen(
        ["python3", "-m", "http.server", "8000"],
        cwd=src_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)  # Attendre que le serveur démarre
    yield
    server.terminate()
    server.wait()


class TestCalculator:
	@pytest.fixture(scope="class")
	def driver(self):
		"""Configuration du driver Chrome pour les tests"""
		chrome_options = Options()

		if os.getenv("CI"):
			chrome_options.add_argument("--headless")
			chrome_options.add_argument("--no-sandbox")
			chrome_options.add_argument("--disable-dev-shm-usage")
			chrome_options.add_argument("--disable-gpu")
			chrome_options.add_argument("--window-size=1920,1080")

		try:
			service = Service(ChromeDriverManager().install())
			driver = webdriver.Chrome(service=service, options=chrome_options)
		except OSError:
			driver = webdriver.Chrome(options=chrome_options)
		driver.implicitly_wait(10)
		yield driver
		driver.quit()

	def test_page_loads(self, driver):
		"""Test 1: Vérifier que la page se charge correctement"""
		page = CalculatorPage(driver)
		page.load_page()

		assert "Calculatrice Simple" in driver.title
		assert page.num1.is_displayed()
		assert page.num2.is_displayed()
		assert page.operation.is_displayed()
		assert page.calculate_button.is_displayed()

	def test_addition(self, driver):
		"""Test 2: Tester l'addition"""
		page = CalculatorPage(driver)
		page.load_page()
		page.enter_first_number(10)
		page.enter_second_number(5)
		page.select_operation("add")
		page.click_calculate()
		assert "Résultat: 15" in page.get_result()

	def test_division_by_zero(self, driver):
		"""Test 3: Tester la division par zéro"""
		page = CalculatorPage(driver)
		page.load_page()
		page.enter_first_number(10)
		page.enter_second_number(0)
		page.select_operation("divide")
		page.click_calculate()
		assert "Erreur: Division par zéro" in page.get_result()

	def test_all_operations(self, driver):
		"""Test 4: Tester toutes les opérations"""
		page = CalculatorPage(driver)
		page.load_page()

		operations = [
			("add", 8, 2, "10"),
			("subtract", 8, 2, "6"),
			("multiply", 8, 2, "16"),
			("divide", 8, 2, "4"),
		]

		for op, num1, num2, expected in operations:
			page.enter_first_number(num1)
			page.enter_second_number(num2)
			page.select_operation(op)
			page.click_calculate()
			assert f"Résultat: {expected}" in page.get_result()
			time.sleep(1)

	def test_decimal_numbers(self, driver):
		"""Test 5: Tester les nombres décimaux"""
		page = CalculatorPage(driver)
		page.load_page()
		page.enter_first_number(1.5)
		page.enter_second_number(2.25)
		page.select_operation("add")
		# Soumettre via JS au lieu de click() car le bouton ne répond pas toujours
		driver.execute_script("document.getElementById('calculator').dispatchEvent(new Event('submit'))")
		time.sleep(1)
		result_text = page.get_result()
		assert "Résultat: 3.75" in result_text

	def test_negative_numbers(self, driver):
		"""Test 6: Tester les nombres négatifs"""
		page = CalculatorPage(driver)
		page.load_page()
		page.enter_first_number(-10)
		page.enter_second_number(4)
		page.select_operation("add")
		page.click_calculate()
		assert "Résultat: -6" in page.get_result()

	def test_ui_styles(self, driver):
		"""Test 7: Vérifier l'interface utilisateur (couleurs, tailles)"""
		page = CalculatorPage(driver)
		page.load_page()

		container = driver.find_element(By.CLASS_NAME, "container")
		result = driver.find_element(By.ID, "result")

		assert container.value_of_css_property("max-width") == "400px"
		assert result.value_of_css_property("background-color") in {
			"rgb(240, 240, 240)",
			"rgba(240, 240, 240, 1)",
		}

	def test_page_load_time(self, driver):
		"""Test 8: Mesurer le temps de chargement de la page"""
		page = CalculatorPage(driver)
		start_time = time.time()
		page.load_page()
		page.wait_ready()
		load_time = time.time() - start_time
		print(f"Temps de chargement: {load_time:.2f} secondes")
		assert load_time < 3.0, f"Page trop lente à charger: {load_time:.2f}s"


if __name__ == "__main__":
	pytest.main(["-v", "--html=report.html", "--self-contained-html"])