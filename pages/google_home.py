from selenium.webdriver.common.by import By
from pages.base import Base


class GoogleHome(Base):

    IN_SEARCH = (By.ID, 'lst-ib')
    BTN_GOOGLE_SEARCH = (By.XPATH, "//button[@value='Search']")
    LNK_SEARCH_RESULTS_HEADING = (By.CSS_SELECTOR, 'div.g h3>a')
    TXT_STATS = (By.ID, 'resultStats')

    def search_on_google(self, search_keyword):
        self.find_element(self.IN_SEARCH).send_keys(search_keyword)
        self.find_element(self.BTN_GOOGLE_SEARCH).click()

    def wait_for_search_result(self):
        self.is_visible(self.TXT_STATS)

    def get_all_search_results(self):
        return [i.text for i in self.find_elements(self.LNK_SEARCH_RESULTS_HEADING)]
