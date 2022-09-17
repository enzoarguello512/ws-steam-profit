from selenium.webdriver.support.ui import WebDriverWait

class BasePageElement(object):
    def __set__(self, obj, value):
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_name(self.locator))
        driver.find_element_by_name(self.locator).clear()
        driver.find_element_by_name(self.locator).send_keys(value)

    def __get__(self, obj, owner):
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_name(self.locator))
        element = driver.find_element_by_name(self.locator)
        return element.get_attribute("value")


#######################################
from selenium.webdriver.support.ui import WebDriverWait

class BasePageElement:
    try:
        def __set__(self, obj, value):
            driver = obj.driver
            WebDriverWait (driver, 600).until (
                lambda driver: driver.get_attribute(self.locator))
            driver.get_attribute(self.locator).clear()
            driver.get_attribute(self.locator).send_keys(value)
            print("TextoDeEjemplo")
    except:
        print("No se pudo settear")

    def __get__(self, obj, owner):
        try:
            driver = obj.driver
            WebDriverWait (driver, 600).until (
                lambda driver: driver.get_attribute(self.locator))
            print ("TextoDeEjemplo")
        except:
            print("No se pudo obtener")


