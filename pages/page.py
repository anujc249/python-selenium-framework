import time

from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Page(object):

    def __init__(self, browser):
        self.browser = browser

    def browser(self):
        return self.browser

    def close(self):
        self.browser.close()

    def maximize_window(self):
        self.browser.maximize_window()

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)

    def quit(self):
        self.browser.quit()

    def find_element(self, locator, waiting_time=5):
        self.is_visible(locator, waiting_time)
        visible_element = self.get_visible_element_from_list(self.browser.find_elements(*locator))
        return visible_element[0] if len(visible_element) > 0 else False

    def find_elements(self, locator):
        visible_elements = self.get_visible_element_from_list(self.browser.find_elements(*locator))
        return visible_elements if len(visible_elements) > 0 else False

    def wait_for_page_to_load(self, timeout=40):
        wait = WebDriverWait(self.browser, timeout, poll_frequency=1)
        wait.until(lambda s: self.browser.execute_script("return document.readyState") == "complete")

    def is_clickable(self, locator, timeout=40):
        wait = WebDriverWait(self.browser, timeout, poll_frequency=1,
                             ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        try:
            wait.until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    def is_visible(self, locator, timeout=5):
        try:
            wait = WebDriverWait(self.browser, timeout, poll_frequency=1)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_any_element_to_visible(self, locator, timeout=5):
        wait = WebDriverWait(self.browser, timeout, poll_frequency=1)
        if isinstance(locator, tuple):
            element = wait.until(EC.visibility_of_any_elements_located(locator))
        else:
            element = wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, locator)))
        return element

    def is_invisible(self, locator, timeout=40):
        wait = WebDriverWait(self.browser, timeout, poll_frequency=1)
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, locator)))
        return True

    def is_all_element_invisible(self, locator, timeout=40):
        for t in range(1, timeout, 1):
            element_list = self.browser.find_elements_by_css_selector(locator)
            if len(element_list) == 0:
                return True
            del element_list[:]
            self.sleep(1)
        return False

    def is_present(self, locator, timeout=40):
        """
        This method checks whether the item is present or not on the page, it does not checks for visibility or clickability
        :param locator:
        :param timeout:
        :return:
        """
        wait = WebDriverWait(self.browser, timeout, poll_frequency=1)
        try:
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_till_element_clickable(self, locator, timeout=40):
        """
        Checks whether the element is clickable or not
        :param locator:
        :param timeout:
        :return:
        """
        try:
            wait = WebDriverWait(self.browser, timeout, poll_frequency=1)
            element = wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            raise TimeoutException("Element is not clickable with locator" + locator.__str__())

    def wait_till_element_visible(self, locator, timeout=40):
        """
        Checks for visibility of element in screen
        :param locator:
        :param timeout:
        :return:
        """
        wait = WebDriverWait(self.browser, timeout, poll_frequency=1)
        element = wait.until(EC.visibility_of_element_located(locator))
        return element

    def wait_till_element_invisible(self, locator, timeout=40):
        """
        Checks for invisibility of the element, precondition is element has to be present prior to calling this method
        :param locator:
        :param timeout:
        :return:
        """
        wait = WebDriverWait(self.browser, timeout, poll_frequency=1)
        element = wait.until(EC.invisibility_of_element_located(locator))
        return element

    # scroll the current page to top
    def scroll_to_top(self):
        """
        Scrolls to top of the page independent of height
        :return:
        """
        self.browser.execute_script("window.scrollTo(0,0);")
        self.sleep(1)
        # scroll the current page to top

    def scroll_to_bottom(self):
        """
        Scrolls to top of the page independent of height
        :return:
        """
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        self.sleep(1)
        # scroll the current page to top

    def scroll_to_location(self, element, by='id'):
        """
        Scrolls to top of the page independent of height
        :return:
        """
        if by == 'class':
            self.browser.execute_script("document.getElementsByClassName('{}')[0].scrollIntoView()".format(element))
        else:
            self.browser.execute_script("document.getElementById('{}')[0].scrollIntoView()".format(element))
        self.browser.execute_script("window.scrollBy(0, -100);")

    def scroll_to_middle_of_page(self):
        self.browser.execute_script("window.scrollTo(500,500);")

    def scroll_into_view(self, element):
        """
        Scrolls till the element gets visible in the screen area
        :param element:
        :return:
        """
        self.browser.execute_script("return arguments[0].scrollIntoView();", element)

    def refresh_browser(self):
        self.browser.refresh()
        self.wait_for_page_to_load()

    def browser_back(self):
        self.browser.back()
        self.wait_for_page_to_load()

    @staticmethod
    def get_visible_element_from_list(element_list):
        """
        Returns only the visible elements from an element list
        :param element_list: Pass the actual web element list not the locators
        :return:
        """
        visible_items = list()
        for item in element_list:
            if item.is_displayed():
                visible_items.append(item)
        return visible_items

    def hover_on_element(self, locator):
        element = self.find_element(locator)
        ActionChains(self.browser).move_to_element(element).click(element).perform()

    @property
    def page_title(self):
        return self.browser.title

    @property
    def get_current_url(self):
        return self.browser.current_url

    @property
    def page_current_url(self):
        return self.browser.current_url

    def hit_escape_key(self):
        actions = ActionChains(self.browser)
        actions.send_keys(Keys.ESCAPE).perform()

    def hit_tab_key(self):
        actions = ActionChains(self.browser)
        actions.send_keys(Keys.TAB).perform()

    def open_new_tab(self):
        self.browser.execute_script("window.open('" + self.base_url + "', 'new_window')")
        self.browser.switch_to.window(self.browser.window_handles[-1])

    def close_tab(self):
        actions = ActionChains(self.browser)
        actions.send_keys(Keys.CONTROL + 'w').perform()

    def accept_alert_if_present(self, timeout):
        try:
            wait = WebDriverWait(self.browser, timeout, poll_frequency=1)
            alert = wait.until(EC.alert_is_present())
            alert.accept()
        except TimeoutException:
            print("No Alert")

    def decline_alert_if_present(self, timeout):
        try:
            wait = WebDriverWait(self.browser, timeout, poll_frequency=1)
            alert = wait.until(EC.alert_is_present())
            alert.dismiss()
        except TimeoutException:
            print("No Alert")
