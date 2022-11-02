
import requests # todo add requirements
from bs4 import BeautifulSoup
from selenium import webdriver
SELENIUM_IMPLICIT_WAIT = 10
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
from datetime import datetime
import lxml.html
import string
from module.chromedriver.chrome_driver import *

class WebScrapperScoreBord():

    driver = ""
    url = ""
    project_path = ""
    exp_lst_countries = []
    exp_lst_votes = []
    edition_year = ""
    load_votes = True
    def __init__(self, project_path, edition_year):
        self.project_path = project_path
        self.url = "https://eurovisionworld.com/eurovision/" + str(edition_year)
        self.edition_year = str(edition_year)
        self.driver = driver_init(self.url)

    def get_from_table(self, classname, row, column):
        path = "//*[@class='"+classname+"']/tbody/tr[" + str(row) + "]/td["+str(column)+"]"
        text_content = self.driver.find_element(By.XPATH, path).text
        return text_content

    def load_countries(self):

        def load_country(name, classname ):
            print("\t\tStart loading ",name," countries...")
            time_start = datetime.now()

            rows_number = len(self.driver.find_elements(By.XPATH,
                                                        "//*[@class='"+classname+"']/tbody/tr"))

            for row in range(1, (rows_number + 1)):
                path = "//*[@class='"+classname+"']/tbody/tr[" + str(
                    row) + "]/td[1]/i"
                cell_content = self.driver.find_element(By.XPATH, path)

                icon_class_name = cell_content.get_attribute("class")
                icon_class_name_spl = icon_class_name.split()
                country_code = icon_class_name_spl[-1].replace("fl_", "")
                country_name = self.get_from_table(
                    classname, row, 2)
                self.exp_lst_countries += [[country_code, country_name]]
            print("\t\tFinished: ", (datetime.now() - time_start).total_seconds(), "seconds")

        def edition_has_nonqualified_countries():




            countries_div = self.driver.find_element(By.XPATH, "//*[@class='voting_year']")
            countries_div_html = str(countries_div.get_attribute("innerHTML"))

            return "NON QUALIFIED COUNTRIES" in countries_div_html.upper()

        load_country("qualified", 'v_table v_table_main table_sort table_first table_last table_sort_added')
        if edition_has_nonqualified_countries():
            load_country("nonqualified", 'v_table v_table_out table_sort table_first table_last table_sort_added')

    def get_countries_header_dict(self):
        dict_countries_position = {}
        columns_number = len(self.driver.find_elements(By.XPATH, "//*[@class='scoreboard_table']/thead/tr[1]/td"))
        for column in range(2, (columns_number)):
            path = "//*[@class='scoreboard_table']/thead/tr[1]/td["+str(column)+"]/i"
            cell_content = self.driver.find_element(By.XPATH, path)
            icon_class_name = cell_content.get_attribute("class")
            icon_class_name_spl = icon_class_name.split()
            country_code = icon_class_name_spl[-1].replace("fl_", "")
            dict_countries_position[column - 1] = country_code
        return dict_countries_position

    def load_votes(self):
        def load_votes_table(vote_type):

            print("\t\tStart loading votes per country of type",vote_type,"...")
            time_start = datetime.now()
            try:
                # Obtain relation between column number and the header country
                dt_header_countries = self.get_countries_header_dict()
                edition_year = self.edition_year

                if vote_type != "Total":

                    try:
                        path = "//button[@class='button' and text()='"+vote_type+"']"
                        tele_button = self.driver.find_element(By.XPATH, path)
                        tele_button.click()
                    except Exception as e:
                        print("\t\t", vote_type, "Button not detected for year", self.edition_year , ". We will consider only Total data.")
                        vote_type = "Total"

                root = lxml.html.fromstring(self.driver.page_source)

                column_values_per_row = [[y for y in x.xpath('.//td/text()')] for x in root.xpath("//*[@class='scoreboard_table']/tbody/tr") ]

                for row_number in range(len(column_values_per_row)):


                    path = "//*[@class='scoreboard_table']/tbody/tr[" + str(row_number + 1) + "]/td[2]/i"
                    cell_content = self.driver.find_element(By.XPATH, path)
                    icon_class_name = cell_content.get_attribute("class")
                    icon_class_name_spl = icon_class_name.split()
                    country_code_row = icon_class_name_spl[-1].replace("fl_", "")


                    columns = column_values_per_row[row_number]
                    for column_number in range(len(columns)):

                        if column_number > 3:
                            text_content = columns[column_number]
                            if (column_number - 3) in dt_header_countries:
                                country_code_column = dt_header_countries[column_number - 3]
                                self.exp_lst_votes.append([edition_year, country_code_column, text_content, country_code_row, vote_type])
                print("\t\tFinished: ", (datetime.now() - time_start).total_seconds(), "seconds")


            except Exception as e:
                x = e

        def edition_has_only_totals():
            votes_div = self.driver.find_element(By.XPATH, "//*[@id='scoreboard']")
            votes_div_html = str(votes_div.get_attribute("innerHTML"))

            return "scoreboard_button_div" not in votes_div_html.lower()


        if edition_has_only_totals():
            load_votes_table("Total")
        else:
            load_votes_table("Tele")
            load_votes_table("Jury")


    def export_files(self):
        print("\t\tStart exporting csv files...")
        time_start = datetime.now()
        datasets_directory = self.project_path + "..\dataset\\"


        today = date.today()
        today_date = today.strftime("%Y%m%d")
        today_folder = datasets_directory + today_date + "\\"
        if not os.path.exists(today_folder):
            os.mkdir(today_folder)


        if len(self.exp_lst_countries) > 0:
            f_open = open(today_folder + self.edition_year + "_countries.csv", "w")
            for country in self.exp_lst_countries:
                output_string = ";".join(country) + "\n"
                f_open.write(output_string)
            f_open.close()
        if len(self.exp_lst_votes) > 0:
            f_open = open(today_folder + self.edition_year + "_votes.csv", "w")
            for vote in self.exp_lst_votes:
                output_string = ";".join(vote) + "\n"
                f_open.write(output_string)
            f_open.close()
        print("\t\tFinished: ", (datetime.now() - time_start).total_seconds(), "seconds")