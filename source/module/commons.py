
from module.chromedriver.chrome_driver import *
from selenium.webdriver.common.by import By
from datetime import date
import os
import pandas as pd
import string
from datetime import datetime

def get_countries():
    """
    Returns a dictionary with the relation between every country and his url-name used in the site.

    :return: Dictionary. Key: Country Name; Value: Country URL Name
    """
    countries_url = dict()
    countries_codes = dict()
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
        country_code = row.get_attribute('class').split("_")[-1]
        country_link = row.get_attribute('href').split("/")[-1]
        country_name = ''.join(x for x in country_name if x in string.printable).strip()
        # Add the result to the result dict
        countries_url[country_name] = country_link
        countries_codes[country_code] = country_name
    print("\t\tFinished: ", (datetime.now() - time_start).total_seconds(), "seconds")
    return (countries_url, countries_codes)


def get_edition_years():
    """
    Returns a list with the edition years

    :return: List with edition years
    """
    edition_years = []
    # start Chrome Driver
    countries_driver = driver_init(url="https://eurovisionworld.com/national")
    print("\t\tStart loading years to export...")
    time_start = datetime.now()
    # Obtain the first column of data table
    column_with_countries = countries_driver.find_elements(By.XPATH,
                                          "//*[@class='national_fp_table']/tbody/tr[1]/td")[1]
    # Get and iterate every row
    rows = column_with_countries.find_elements(By.XPATH, './/a')
    for row in rows:
        edition_year = row.text
        edition_years += [edition_year]


    print("\t\tFinished: ", (datetime.now() - time_start).total_seconds(), "seconds")
    return edition_years

def generate_csv(project_path, data_table, filename):
    """
    Create a new file in project_path + filename path with the data_table content

    :param project_path: Path where project is found
    :param data_table: data table to export
    :param filename: name of file to generate
    :return: None
    """
    datasets_directory = project_path + "..\dataset\\"
    today = date.today()
    today_date = today.strftime("%Y%m%d")
    today_folder = datasets_directory + today_date + "\\"
    if not os.path.exists(today_folder):
        os.mkdir(today_folder)
    df_historic_country = pd.DataFrame(data_table)
    df_historic_country.to_csv(today_folder + filename, index=False)