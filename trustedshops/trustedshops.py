import re
import time
import typing
import warnings
import unittest
import random as rd
import HTMLTestRunner
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from webdriver_manager.chrome import ChromeDriverManager


warnings.filterwarnings("ignore")

Driver = webdriver.Chrome


def get_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-popup-blocking')
    options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    return driver


class TestCase(unittest.TestCase):
    driver: WebDriver
    wait: WebDriverWait

    url = "https://www.trustedshops.de/bewertung/info_X77B11C1B8A5ABA16DDEC0C30E7996C21.html"

    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = get_driver()
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.driver.get(cls.url)
        try:
            cls.wait.until(ec.presence_of_element_located((By.XPATH, "//button[@id='uc-btn-deny-banner']"))).click()
        except WebDriverException:
            pass

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    def get_element(self,
                    xpath: str,
                    condition: ec = ec.presence_of_element_located) -> typing.Union[WebElement, list[WebElement]]:
        return self.wait.until(condition((By.XPATH, xpath)))

    def test_for_page_title(self) -> None:
        print("\nTesting for page title ...")
        title = self.driver.title.strip()
        self.assertNotEqual(title, "")
        print("Page title test pass!")

    def test_grade_visibility(self) -> None:
        print("\nTesting grade visibility ...")
        grade = self.get_element("//span[@class='sc-3a77ab16-6 kohtTt']").text.strip()
        grade = float(grade.replace(",", "."))
        self.assertGreater(grade, 0)
        print("Grade visibility test pass!")

    def test_relevant_information(self) -> None:
        print("\nTesting relevant information ...")
        self.get_element("//div[contains(text(), 'Sehr gut')]")
        self.get_element("//a[contains(text(), 'Wie berechnet sich die Note')]", ec.element_to_be_clickable).click()
        self.get_element("//div[@data-test='modal-dialogue']")
        modal_text = self.get_element("(//div[contains(@data-title, 'Lesen Sie die Bewertungen')]//h2)[1]/following-sibling::div[1]").text.strip()
        print(modal_text)
        self.assertIn("Sehr gut", modal_text)
        self.get_element("//div[@data-test='modal-dialogue']//span[contains(@class, 'action-dismiss')]").click()
        print("Relevant test information test pass!")

    def test_stars_filter(self) -> None:
        print("\nTesting stars filter ...")
        self.get_element("(//a[contains(@href, '/bewertung/') and contains(@href, 'stars=2')])[1]").click()
        page = 2
        while True:
            results = self.get_element("//div[@class='sc-2e7612c5-0 sc-f836bc46-0 kyZgbN chcERM']//div[contains(@class, 'Starsstyles__Stars')]", ec.presence_of_all_elements_located)
            for elm in results:
                spans = elm.find_elements(By.XPATH, ".//span[@style='display: inline; color: rgb(255, 220, 15);']")
                self.assertEqual(len(spans), 2)

            try:
                self.get_element(f"(//div[@id='pagination']/a/span[contains(text(), '{page}')])[last()]").click()
            except WebDriverException:
                break

            page += 1
            time.sleep(rd.randint(2, 3))
        print("Stars test filter pass!")

    def test_percentage_sum(self) -> None:
        print("\nTesting percentage sum ...")
        results = self.get_element("(//a[contains(@href, '/bewertung/') and contains(@href, 'stars=')])/div/span[contains(text(), '%')]/parent::node()", ec.presence_of_all_elements_located)
        lst, pattern = [], re.compile(r"[0-9]+")
        for elm in results:
            text = elm.text.strip()
            try:
                lst.append(float("".join(pattern.findall(text))))
            except (ValueError, TypeError):
                pass
        self.assertEqual(sum(lst), 100)
        print("Percentage sum test pass!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-report":
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestCases))
        dateTimeStamp = time.strftime('%Y%m%d_%H_%M_%S')
        runner = HTMLTestRunner.HTMLTestRunner(log=True,title='Test the Report',
                            description='Result of tests', open_in_browser=True)
        runner.run(suite)
    else:
        unittest.main()