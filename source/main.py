import time

from module.scoreboard import *
from module.historic_country import *
from pathlib import Path
from module.commons import *
from module.api_twitter import *
if __name__ == "__main__":
    project_path = str(Path(__file__).parent.resolve()) + "\\"
    try:
        #request_tweets_count_from_api(project_path)

        #export_historic_countries(project_path, processes_number=8)
        export_scoreboard(project_path, processes_number=8)


    except Exception as e:
        print(e)
    print("End of program")