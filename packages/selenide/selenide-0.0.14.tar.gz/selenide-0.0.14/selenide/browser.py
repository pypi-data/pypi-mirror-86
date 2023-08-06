from enum import Enum, unique

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager


@unique
class Browser(Enum):
    CHROME = ChromeDriverManager().install()
    FIREFOX = GeckoDriverManager().install()
    IE = IEDriverManager().install()


def driver(name=Browser.CHROME, grid_url=None, options=None):
    if name not in Browser:
        raise WebDriverException(f"Un support driver name: {name.name}")
    elif name == Browser.CHROME:
        if grid_url:
            return webdriver.Remote(grid_url,
                                    DesiredCapabilities.CHROME.copy(),
                                    options=options)
        return webdriver.Chrome(name, options=options)
    elif name == Browser.FIREFOX:
        if grid_url:
            return webdriver.Remote(grid_url,
                                    DesiredCapabilities.FIREFOX.copy(),
                                    options=options)
        return webdriver.Firefox(name, options=options)
    elif name == Browser.IE:
        if grid_url:
            return webdriver.Remote(grid_url,
                                    DesiredCapabilities.INTERNETEXPLORER.copy(),
                                    options=options)
        return webdriver.Ie(name, options=options)
