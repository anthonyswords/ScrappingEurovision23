from module.chromedriver.chrome_driver import *
from module.commons import *
from multiprocessing import JoinableQueue, Queue, Process
from selenium.webdriver.common.by import By
from datetime import datetime

def process_export_country(countries_to_process, results_q):
    """
    Function executed in every parallel process. It will be reading pending countries from queue "countries_to_process"
    and storing the result in queue "resuslts_q"
    :param countries_to_process: Queue with countries to export
    :param results_q: Queue in which result will be stored
    :return:
    """

    country = countries_to_process.get()

    # while there are tasks to process
    while country:
        (project_path, country_name, country_link) = country
        hc = historic_country(project_path, country_name, country_link)
        data_table = hc.export()

        # save the result in the queue
        results_q.put(data_table)

        # Mark the task as done
        countries_to_process.task_done()

        # get the next task to porcess
        country = countries_to_process.get()

    # Mark the last task as done, it was None.
    countries_to_process.task_done()


def export_historic_countries(project_path, processes_number = 8):
    """
    Given a processes number, generates the historic Eurovision participation of every country. The result will be saved
    in csv file allocated in project_path
    :param project_path: Path where the data will be stored
    :param processes_number: Number of parallel processes that will be used
    :return:
    """
    start_time = datetime.now()
    print("Starting job export countries...")

    # Get countries list to export
    (countries_url, countries_codes) = get_countries()

    # Initialize results queue
    results_q = Queue()

    # Initialize Tasks queue
    countries_to_process = JoinableQueue()

    # Add to queue the tasks to do
    for country_name in countries_url.keys():
        countries_to_process.put((project_path, country_name, countries_url[country_name]))

    # Add to queue one None for each process
    for _ in range(processes_number):
        countries_to_process.put(None)

    # Create and start the processes
    for i in range(processes_number):
        process = Process(
            target=process_export_country, args=(countries_to_process, results_q)
        )
        process.start()

    # Wait until all tasks have finished
    countries_to_process.join()

    # Read results from results queue
    data_table_list = []
    while not results_q.empty():
        val = results_q.get()
        data_table_list += val

    # Create output data_table
    data_table = {
        'country':[x[0] for x in data_table_list],
        'years': [x[1] for x in data_table_list],
        'songs': [x[2] for x in data_table_list],
        'artists': [x[3] for x in data_table_list],
        'places': [x[4] for x in data_table_list],
        'points': [x[5] for x in data_table_list],
        'qualification': [x[6] for x in data_table_list],
    }

    # Export to file
    generate_csv(project_path, data_table, 'Countries_Editions_Songs.csv')

    print("Job finished: Export countries. Elapsed time: ", (datetime.now() - start_time).total_seconds(),
          "seconds")

class historic_country():
    project_path = ""
    country_name = ""
    driver = ""
    url = ""
    start_time = ""
    def __init__(self, project_path, country_name, country_link):
        self.start_time = datetime.now()
        self.project_path = project_path
        self.country_name = country_name
        self.url = "https://eurovisionworld.com/eurovision/" + country_link
        self.driver = driver_init(self.url)


    def export(self):
        """
        Generate the historic Eurovision participation from one country and returns data table
        :return: data table with historic Eurovision participation from country
        """
        data_table = []
        try:
            rows = self.driver.find_elements(By.XPATH,
                                                    "//*[@class='v_table table_sort table_first table_last table_sort_added']/tbody/tr")

            # for every year participation
            for row in rows:
                columns = row.find_elements(By.XPATH, './/td')
                year = columns[0].text
                song_content = columns[1].text
                song_split = song_content.split('\n')
                if len(song_split) == 2:
                    song = song_split[0].strip()
                    artist = song_split[1].strip()
                else:
                    song = song_content.strip()
                    artist = ""
                place = columns[2].text
                points = columns[3].text
                qualification = columns[4].text

                # Add result to data table
                data_table += [[self.country_name, year, song, artist, place, points, qualification]]

        except Exception as e:
            print("Error while exporting historic country "+self.country_name+": " + str(e))


        print("\t\tExport " + self.country_name+" finished: ", (datetime.now() - self.start_time).total_seconds(), "seconds")

        return data_table