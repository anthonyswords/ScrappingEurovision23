

import os
from selenium.webdriver.common.by import By
from datetime import date
from datetime import datetime
import lxml.html
from module.chromedriver.chrome_driver import *
from module.commons import *
from multiprocessing import JoinableQueue, Queue, Process
import threading
import time


lock = threading.Lock()

def process_export_country(years_to_process, temp_path, thread_number):


    f_open = open(temp_path + str(thread_number) + "_votes.csv", "w")

    with lock:
        year = years_to_process.get()

    # while there are tasks to process
    while year:
        (edition_year, countries_codes) = year

        scoreboard = Scoreboard(edition_year, countries_codes)
        data_table = scoreboard.export()

        # write result to temp file
        for vote in data_table:
            output_string = ",".join(vote) + "\n"
            f_open.write(output_string)

        with lock:
            # Mark the task as done
            years_to_process.task_done()

            # get the next task to porcess
            year = years_to_process.get()

    with lock:
        # Mark the last task as done, it was None.
        years_to_process.task_done()

    f_open.close()
def export_scoreboard(project_path, processes_number=8):
    start_time = datetime.now()
    print("Starting job export scoreboard...")

    # Generate outfile
    datasets_directory = project_path + "..\dataset\\"
    today = date.today()
    today_date = today.strftime("%Y%m%d")
    today_folder = datasets_directory + today_date + "\\"
    tmp_folder = today_folder + "tmp\\"
    if not os.path.exists(today_folder):
        os.mkdir(datasets_directory + today_date)
    if not os.path.exists(tmp_folder):
        os.mkdir(tmp_folder)
    # Get the countries to include in the export
    (countries_url, countries_codes) = get_countries()

    # Get all year editions to export
    years_all = get_edition_years()

    # exclude 2023 (not celebrated yet) and 2020 (suspended due to covid)
    years = [year for year in years_all if year not in ('2023', '2020', '1956')]

    # Initialize Tasks queue
    years_to_process = JoinableQueue()

    # Add to queue the tasks to do
    for edition_year in years:
        years_to_process.put((edition_year, countries_codes))

    # Add to queue one None for each process
    for _ in range(processes_number):
        years_to_process.put(None)

    # Create and start the processes
    for i in range(processes_number):
        process = Process(
            target=process_export_country, args=(years_to_process,  tmp_folder, i)
        )
        process.start()

    # Wait until all tasks have finished
    years_to_process.join()

    # open file where data will be merged
    f_open_merged = open(today_folder + "Votes_From_Scoreboard.csv", "w")

    # Add headers to file
    file_headers = ['edition_year', 'country_code_column', 'value', 'country_code_row', 'vote_type']
    file_headers_string = ",".join(file_headers) + "\n"
    f_open_merged.write(file_headers_string)

    # for each temp file
    for file in os.listdir(tmp_folder):
        f_open_tmp = open(tmp_folder + "//" + file, 'r')
        lines = f_open_tmp.readlines()
        for line in lines:
            # Write every line to output file
            f_open_merged.write(line)
        f_open_tmp.close()
        # remove temp file
        os.remove(tmp_folder + "//" + file)

    f_open_merged.close()
    # remove temp folder
    os.rmdir(tmp_folder)
    print("Job finished: Export editions scoreboard. Elapsed time: ", (datetime.now() - start_time).total_seconds(),
          "seconds")


class Scoreboard():

    driver = ""
    url = ""
    exp_lst_countries = []
    edition_year = ""
    load_votes = True
    countries_codes = dict()
    def __init__(self, edition_year, countries_codes):
        self.start_time = datetime.now()
        self.url = "https://eurovisionworld.com/eurovision/" + str(edition_year)
        self.edition_year = str(edition_year)
        self.driver = driver_init(self.url)
        self.countries_codes = countries_codes

    def get_from_table(self, classname, row, column):
        """
        Given a classname, row number and column number, it will read the content from table cell and return it.
        :param classname: Classname of the table to read
        :param row: Row number to read
        :param column: Column to read
        :return: Cell content from the concrete cell
        """
        path = "//*[@class='"+classname+"']/tbody/tr[" + str(row) + "]/td["+str(column)+"]"
        text_content = self.driver.find_element(By.XPATH, path).text
        return text_content

    def get_countries_header_dict(self):
        """
        Returns a dictionary with the relation between column number and the country that represents.
        :return: A dictionary where the key is the column number and the value the country code.
        """
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

    def export(self):
        """
        Generate a datatable with all content from one scoreboard
        :return:A datatable with scoreboard information
        """
        def load_votes_table(vote_type):
            data_table = []
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
                                data_table += [[edition_year, country_code_column, text_content, country_code_row, vote_type]]


            except Exception as e:
                print("Error while reading scoreboard: " + e)
            return data_table

        def edition_has_only_totals():
            """
            Return True if the edition has only total information. False if it has Tele and Jury information
            :return: Boolean that indicates if edition has only total information or not.
            """
            votes_div = self.driver.find_element(By.XPATH, "//*[@id='scoreboard']")
            votes_div_html = str(votes_div.get_attribute("innerHTML"))

            return "scoreboard_button_div" not in votes_div_html.lower()

        # Main code from export funcion
        exp_lst_votes = []

        # Check if scoreboard has Total information or Tele and Jury
        if edition_has_only_totals():
            data_table = load_votes_table("Total")
            exp_lst_votes += data_table
        else:
            data_table = load_votes_table("Tele")
            exp_lst_votes += data_table
            data_table = load_votes_table("Jury")
            exp_lst_votes += data_table
        print("\t\tExport " + self.edition_year + " finished: ", (datetime.now() - self.start_time).total_seconds(),
              "seconds")
        return exp_lst_votes

