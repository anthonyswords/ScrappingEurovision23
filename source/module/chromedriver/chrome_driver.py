SELENIUM_IMPLICIT_WAIT = 100

from selenium import webdriver
import os

def driver_init(url):
    """
    Initialize chromedriver instance and request content from url

    :param url: url to request content
    :return: chromedriver object
    """

    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"')
        chrome_options.add_argument("--start-maximized");
        chrome_options.add_argument("--disable-extensions")          # no chrome extensions needed
        chrome_options.add_argument("--disable-infobars")            # no info bar "an automation is running chrome"
        chrome_options.add_argument("--disable-gpu")                 # Docker is not very happy with GPU
        chrome_options.add_argument("--disable-dev-shm-usage")       # Disable memory warnings
        chrome_options.add_argument("--no-sandbox")                  # Disable sandbox protection, for Docker compatibility
        chrome_options.add_argument("--headless")                    # Headless mode, required to run in Docker
        #chrome_options.add_argument("--window-size=1920,1080")       # resolution of 1080, ensure all elements are displayed
        #driver = webdriver.Chrome(options=chrome_options)            # Initialize ChromeDriver with the given options
        chromedriver_path = os.path.dirname(os.path.abspath(__file__)) + "\\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_path, options=chrome_options)
        driver.implicitly_wait(SELENIUM_IMPLICIT_WAIT)               # Set the implicit wait to locate elements
        driver.get(url)                            # Load the page
        #print(driver.execute_script("return navigator.userAgent"))         # Check if the User Agent is ok
    except Exception as e:
        print("Error with chromedriver: " + str(e))
        return None

    return driver
