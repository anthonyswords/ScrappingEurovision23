
from module.chromedriver.chrome_driver import *
from selenium.webdriver.common.by import By
from datetime import date
import os
import pandas as pd
import string

def get_countries():
    """
    Returns a dictionary with the relation between every country and his url-name used in the site.

    :return: Dictionary. Key: Country Name; Value: Country URL Name
    """
    countries = dict()
    # start Chrome Driver
    countries_driver = driver_init(url="https://eurovisionworld.com/national")
    print("\t\tStart loading countries to export...")
    time_start = datetime.now()
    # Obtain the first column of data table
    column_with_countries = countries_driver.find_elements(By.XPATH,
                                          "//*[@class='national_fp_table']/tbody/tr[1]/td")[0]
    # Get and iterate every row
    rows = column_with_countries.find_elements(By.XPATH, './/a')
    for row in rows:
        country_name = row.text
        country_link = row.get_attribute('href').split("/")[-1]
        country_name = ''.join(x for x in country_name if x in string.printable).strip()
        # Add the result to the result dict
        countries[country_name] = country_link

    print("\t\tFinished: ", (datetime.now() - time_start).total_seconds(), "seconds")
    return countries

def generate_csv(project_path, data_table, filename):
    datasets_directory = project_path + "..\dataset\\"
    today = date.today()
    today_date = today.strftime("%Y%m%d")
    today_folder = datasets_directory + today_date + "\\"
    if not os.path.exists(today_folder):
        os.mkdir(today_folder)
    df_historic_country = pd.DataFrame(data_table)
    df_historic_country.to_csv(today_folder + filename, index=False)