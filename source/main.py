import time

from module.scoreboard import *
from module.historic_country import *
from module.bet_house_2023 import *
from module.poll_2022 import *
from pathlib import Path
from module.commons import *
from module.api_twitter import *
if __name__ == "__main__":
    project_path = str(Path(__file__).parent.resolve()) + "\\"

    export_historic_countries(project_path)
    bet_house_2023(project_path)
    poll_2022(project_path)



    if False:

        years = list(range(1957, 2023))
        #years = [2022]
        try:

        #export_historic_countries(project_path, processes_number=8)
        export_scoreboard(project_path, processes_number=8)

                    print("Export finished ", edition_year,":",  (datetime.now() - time_start).total_seconds(), "seconds")

        except Exception as e:
            print(e)
