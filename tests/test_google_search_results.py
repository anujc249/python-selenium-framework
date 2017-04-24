from pages.google_home import GoogleHome
from tests.base_test import BaseTest


class TestGoogleSearch(BaseTest):
    def setup_method(self, method):
        self.get_driver(method)
        self.google_home = GoogleHome(self.driver)
        self.google_home.visit()

    def teardown_method(self, _):
        self.quit_driver()

    def test_search_results(self):
        self.google_home.search_on_google('India')
        self.google_home.wait_for_search_result()
        all_results = self.google_home.get_all_search_results()
        assert len(all_results) != 0, 'Search result not appear'
