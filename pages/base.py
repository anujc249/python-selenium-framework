
import pytest
from pages.page import Page


class Base(Page):
    """
    Base class for global project specific functions
    """

    def __init__(self, browser):
        _url = pytest.config.getoption('base_url')
        if not _url:
            raise pytest.UsageError("Provide base_url in confest.py")

        self.base_url = _url
        super(Base, self).__init__(browser)

    def visit(self):
        self.browser.get(self.base_url)
        self.wait_for_page_to_load()
