

from module.commons import *
from datetime import datetime

def export_countries(project_path):
    start_time = datetime.now()
    print("Starting job export countires ...")
    # Get countries list to export
    (countries_url, countries_codes) = get_countries()
    # Create output data_table

    data_table = {
        'country_code': list(countries_codes.keys()),
        'country_name': list(countries_codes.values())
    }

    # Export to file
    generate_csv(project_path, data_table, 'Countries.csv')

    print("Job finished: Export countries. Elapsed time: ", (datetime.now() - start_time).total_seconds(),
          "seconds")