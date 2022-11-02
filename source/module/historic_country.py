from module.chromedriver.chrome_driver import *
from module.commons import *
from multiprocessing import JoinableQueue, Queue, Process


def process_export_country(countries_to_process, results_q):

    country = countries_to_process.get()

    # Apliquem la logica mentre hi hagi tasques
    while country:
        (project_path, country_name, country_link) = country
        hc = historic_country(project_path, country_name, country_link)
        data_table = hc.export()

        # Guardem la llista a la cua de resultats si aquesta no està buida
        results_q.put(data_table)

        # Marquem la tasca com executada
        countries_to_process.task_done()
        # Obtenim la següent tasca a realitzar
        country = countries_to_process.get()

    # Marquem la ultima tasca com a feta, era None.
    countries_to_process.task_done()


def export_historic_countries(project_path, processes_number = 8):
    start_time = datetime.now()
    print("Starting job export countries...")

    # Get countries list to export
    countries = get_countries()

    # Initialize results queue
    results_q = Queue()

    # Initialize Tasks queue
    countries_to_process = JoinableQueue()

    # Add to queue the tasks to do
    for country_name in countries.keys():
        countries_to_process.put((project_path, country_name, countries[country_name]))

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
    data_table = []
    while not results_q.empty():
        val = results_q.get()
        data_table += val

    # Create output data_table
    data_table = {
        'country':[x[0] for x in data_table],
        'years': [x[1] for x in data_table],
        'songs': [x[2] for x in data_table],
        'artists': [x[3] for x in data_table],
        'places': [x[4] for x in data_table],
        'points': [x[5] for x in data_table],
        'qualification': [x[6] for x in data_table],
    }

    # Export to file
    generate_csv(project_path, data_table, 'historic_countries.csv')

    print("Job finished: Export countries. Elapsed time: ", (datetime.now() - start_time).total_seconds(),
          "seconds")

class historic_country():
    project_path = "",
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
        data_table = []
        try:
            rows = self.driver.find_elements(By.XPATH,
                                                    "//*[@class='v_table table_sort table_first table_last table_sort_added']/tbody/tr")


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
                data_table += [[self.country_name, year, song, artist, place, points, qualification]]

        except Exception as e:
            x =  e


        print("\t\tExport " + self.country_name+" finished: ", (datetime.now() - self.start_time).total_seconds(), "seconds")
        return data_table