import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# sorts out the chromedriver path so selenium can find it
driver_path = ChromeDriverManager().install()
os.environ["PATH"] = os.path.dirname(driver_path) + os.pathsep + os.environ["PATH"]
