from module.scoreboard import *
from module.historic_country import *
from module.bet_house_2023 import *
from module.poll_2022 import *
from pathlib import Path
from module.countries import *
from module.api_twitter import *

if __name__ == "__main__":
    start_time = datetime.now()
    print("*** Export started")
    try:
        project_path = str(Path(__file__).parent.resolve()) + "\\"
        export_countries(project_path)
        request_tweets_count_from_api(project_path)
        export_poll_2022(project_path)
        export_odds_2023_df(project_path)
        export_historic_countries(project_path, processes_number=8)
        export_scoreboard(project_path, processes_number=8)

    except Exception as e:
        print(e)


    print("*** Export finished. Total time: ", (datetime.now() - start_time).total_seconds(), "seconds")