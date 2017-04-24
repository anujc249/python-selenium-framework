def pytest_addoption(parser):
    parser.addoption("--driver", action="store", default="chrome", help="my option: firefox or chrome")
    parser.addoption("--base_url", action="store", default="https://www.google.com", help="Enter base url")

