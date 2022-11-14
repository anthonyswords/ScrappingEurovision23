SELENIUM_IMPLICIT_WAIT = 10
from selenium import webdriver
from datetime import datetime

def driver_init(url):
    #print("\t\tInitializing chrome driver...")
    #time_start = datetime.now()

    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized");
        chrome_options.add_argument("--disable-extensions")          # no chrome extensions needed
        chrome_options.add_argument("--disable-infobars")            # no info bar "an automation is running chrome"
        chrome_options.add_argument("--disable-gpu")                 # Docker is not very happy with GPU
        chrome_options.add_argument("--disable-dev-shm-usage")       # Disable memory warnings
        chrome_options.add_argument("--no-sandbox")                  # Disable sandbox protection, for Docker compatibility
        chrome_options.add_argument("--headless")                    # Headless mode, required to run in Docker
        #chrome_options.add_argument("--window-size=1920,1080")       # resolution of 1080, ensure all elements are displayed
        #driver = webdriver.Chrome(options=chrome_options)            # Initialize ChromeDriver with the given options
        driver = webdriver.Chrome("C:\\Users\\PCE6\\Desktop\\chromedriver\\chromedriver.exe",options=chrome_options)#"chromedriver\\chromedriver.exe",options=chrome_options)
        driver.implicitly_wait(SELENIUM_IMPLICIT_WAIT)               # Set the implicit wait to locate elements
        driver.get(url)                            # Load the page
        print(driver.execute_script("return navigator.userAgent"))         # Check if the User Agent is ok
    except Exception as e:
        x = e
    #print("\t\tFinished: ", (datetime.now() - time_start).total_seconds(), "seconds")

    return driver
