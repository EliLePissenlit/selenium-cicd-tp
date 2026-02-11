import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from calculator_page import CalculatorPage


def _create_driver():
    """Crée le driver Chrome ou Firefox selon la variable d'environnement BROWSER.
    Utilise le Selenium Manager intégré (Selenium 4.6+) pour éviter les soucis
    avec webdriver-manager sur macOS (mauvais fichier chromedriver HELP)."""
    browser = os.getenv("BROWSER", "chrome").lower()

    if browser == "firefox":
        from selenium.webdriver.firefox.options import Options as FirefoxOptions

        options = FirefoxOptions()
        if os.getenv("CI"):
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        from selenium.webdriver.chrome.options import Options

        options = Options()
        if os.getenv("CI"):
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)
    return driver


class TestCalculator:
    @pytest.fixture(scope="class")
    def driver(self):
        """Configuration du driver pour les tests (Chrome ou Firefox)."""
        driver = _create_driver()
        yield driver
        driver.quit()

    @pytest.fixture
    def page(self, driver):
        """Fixture Page Object."""
        return CalculatorPage(driver)

    def test_page_loads(self, driver, page):
        """Test 1: Vérifier que la page se charge correctement"""
        page.load_page()
        assert "Calculatrice Simple" in driver.title
        assert driver.find_element(By.ID, "num1").is_displayed()
        assert driver.find_element(By.ID, "num2").is_displayed()
        assert driver.find_element(By.ID, "operation").is_displayed()
        assert driver.find_element(By.ID, "calculate").is_displayed()

    def test_addition(self, page):
        """Test 2:addition"""
        page.load_page()
        page.enter_first_number(10)
        page.enter_second_number(5)
        page.select_operation("add")
        page.click_calculate()
        assert "Résultat: 15" in page.get_result()

    def test_division_by_zero(self, page):
        """Test 3: division par zéro"""
        page.load_page()
        page.enter_first_number(10)
        page.enter_second_number(0)
        page.select_operation("divide")
        page.click_calculate()
        assert "Erreur:" in page.get_result()

    def test_all_operations(self, page):
        """Test 4: tout"""
        page.load_page()
        operations = [
            ("add", "8", "2", "10"),
            ("subtract", "8", "2", "6"),
            ("multiply", "8", "2", "16"),
            ("divide", "8", "2", "4"),
        ]
        for op, num1, num2, expected in operations:
            page.enter_first_number(num1)
            page.enter_second_number(num2)
            page.select_operation(op)
            page.click_calculate()
            assert f"Résultat: {expected}" in page.get_result()
            time.sleep(0.3)

    def test_page_load_time(self, driver, page):
        """Test 5: Mesurer le temps de chargement"""
        start_time = time.time()
        page.load_page()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "calculator"))
        )
        load_time = time.time() - start_time
        print(f"Temps de chargement: {load_time:.2f} secondes")
        assert load_time < 3.0, f"Page trop lente à charger: {load_time:.2f}s"

    def test_decimal_numbers(self, page):
        """Test 6: nombres décimaux"""
        page.load_page()
        page.enter_first_number(2.5)
        page.enter_second_number(1.5)
        page.select_operation("add")
        page.click_calculate()
        assert "Résultat: 4" in page.get_result()

    def test_negative_numbers(self, page):
        """Test 7: nombres négatifs"""
        page.load_page()
        page.enter_first_number(-3)
        page.enter_second_number(5)
        page.select_operation("add")
        page.click_calculate()
        assert "Résultat: 2" in page.get_result()

    def test_ui_styles(self, driver, page):
        """Test 8: interface utilisateur"""
        page.load_page()
        container = driver.find_element(By.CLASS_NAME, "container")
        result_el = driver.find_element(By.ID, "result")

        # Vérifier la largeur max du container (400px)
        max_width = container.value_of_css_property("max-width")
        assert "400" in max_width, f"Container max-width attendu ~400px, obtenu: {max_width}"

        # Vérifier le fond de la zone résultat (#f0f0f0 en rgb ou hex)
        bg = result_el.value_of_css_property("background-color")
        assert "240" in bg or "f0" in bg.lower(), f"Résultat background attendu #f0f0f0, obtenu: {bg}"


if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
