#from scoreboard import *

from module.chromedriver.chrome_driver import *
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import date
import os

from multiprocessing import JoinableQueue, Queue, Process
import string


def get_links_per_country():
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
        #country_name = ''.join(x for x in country_name if x in string.printable).strip()
        # Add the result to the result dict
        countries[country_name] = country_link

    print("\t\tFinished: ", (datetime.now() - time_start).total_seconds(), "seconds")
    return countries


def export_country(countries_to_process, results_q):
    country = countries_to_process.get()



    # Apliquem la logica mentre hi hagi tasques
    while country:
        (project_path, country_name, country_link) = country
        hc = historic_country(project_path, country_name, country_link)
        hc.export()

        # Guardem la llista a la cua de resultats si aquesta no està buida
        results_q.put(True)

        # Marquem la tasca com executada
        countries_to_process.task_done()
        # Obtenim la següent tasca a realitzar
        country = countries_to_process.get()

    # Marquem la ultima tasca com a feta, era None.
    countries_to_process.task_done()


def export_historic_countries(project_path):
    countries = get_links_per_country()
    processes_number = 1
    # Inicialitzem la cua de resultats
    results_q = Queue()
    # Inicialitzem la cua de tasques
    countries_to_process = JoinableQueue()

    # Afegim les tasques a la cua
    for country_name in countries.keys():
        countries_to_process.put((project_path, country_name, countries[country_name]))

    # Afegim a la cua tants None com processes_number
    for _ in range(processes_number):
        countries_to_process.put(None)

    # Creem els processos per sol·licitar les dades de la cua
    for i in range(processes_number):
        process = Process(
            target=export_country, args=(countries_to_process, results_q)
        )
        process.start()

    # Esperem que s'hagin completat totes les tasques
    countries_to_process.join()


    for country_name in countries.keys():
        hc = historic_country(project_path, country_name, countries[country_name])
        hc.export()


class historic_country():
    project_path = ""
    country_name = ""
    driver = ""
    url = ""
    def __init__(self, project_path, country_name, country_link):
        self.project_path = project_path
        self.country_name = country_name
        self.url = "https://eurovisionworld.com/eurovision/" + country_link
        self.driver = driver_init(self.url)


    def export(self):
        print("\t\tStart loading country", self.country_name, "...")
        time_start = datetime.now()
        try:
            rows = self.driver.find_elements(By.XPATH,
                                                    "//*[@class='v_table table_sort table_first table_last table_sort_added']/tbody/tr")

            data_table = []
            years = []
            songs = []
            artists = []
            places = []
            points = []
            qualification = []
            for row in rows:
                columns = row.find_elements(By.XPATH, './/td')
                years += [columns[0].text]
                song_content = columns[1].text
                song_split = song_content.split('\n')
                if len(song_split) == 2:
                    song = song_split[0].strip()
                    artist = song_split[1].strip()
                else:
                    song = song_content.strip()
                    artist = ""
                songs += [song]
                artists += [artist]
                places += [columns[2].text]
                points += [columns[3].text]
                qualification += [columns[4].text]

            datasets_directory = self.project_path + "..\dataset\\"
            today = date.today()
            today_date = today.strftime("%Y%m%d")
            today_folder = datasets_directory + today_date + "\\"
            if not os.path.exists(today_folder):
                os.mkdir(today_folder)


            data_table = {
                'years': years,
                'songs': songs,
                'artists': artists,
                'places': places,
                'points': points,
                'qualification': qualification,
            }
            df_historic_country = pd.DataFrame(data_table)
            df_historic_country.to_csv(today_folder + self.country_name + '_historic_country')
        except Exception as e:
            x =  e


        print("\t\tFinished: ", (datetime.now() - time_start).total_seconds(), "seconds")