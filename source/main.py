
from module.scoreboard import *
from module.historic_country import *
from module.bet_house_2023 import *
form module.poll_2022 import *
from pathlib import Path
if __name__ == "__main__":
    project_path = str(Path(__file__).parent.resolve()) + "\\"

    export_historic_countries(project_path)    
    bet_house_2023(project_path)
    poll_2022(project_path)



    if False:

        years = list(range(1957, 2023))
        #years = [2022]
        try:

            for edition_year in years:
                if edition_year != 2020:
                    print("Start exporting", edition_year)
                    time_start = datetime.now()
                    scoreboard = WebScrapperScoreBord(project_path,edition_year)
                    scoreboard.load_countries()
                    scoreboard.load_votes()
                    scoreboard.export_files()

                    print("Export finished ", edition_year,":",  (datetime.now() - time_start).total_seconds(), "seconds")

        except Exception as e:
            print(e)
