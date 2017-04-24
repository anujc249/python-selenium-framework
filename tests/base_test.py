
import os

import pytest
from selenium import webdriver


class BaseTest(object):
    """A base test class that can be extended by other tests to include utility
     methods."""

    home_dir = os.path.join(os.path.dirname(__file__), '..')

    def get_driver(self, caller):
        driver_type = pytest.config.getoption('driver')
        os.environ['driver'] = driver_type.lower()
        self.display = None

        if driver_type is None:
            raise pytest.UsageError('--driver must be specified')
        if 'firefox' == driver_type.lower():
            self.driver = webdriver.Firefox()
        elif 'chrome' == driver_type.lower():
            self.driver = webdriver.Chrome()
        else:
            raise pytest.UsageError('Invalid driver specified')
        self.driver.maximize_window()
        return self.driver

    def quit_driver(self):
        self.driver.quit()
