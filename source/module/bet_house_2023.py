import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
from module.commons import *
from module.chromedriver.chrome_driver import *

def export_odds_2023_df(project_path):
    start_time = datetime.now()
    print("Starting job export Odds Rate Eurovision 2023 table...")
    betHouse = WebScrapperBetHouse23()
    data_table = betHouse.get_df_BetHouse23()
    # Export to file
    generate_csv(project_path, data_table, 'Odds_Rate_Table_2023.csv')

    print("Job finished: Export odds. Elapsed time: ", (datetime.now() - start_time).total_seconds(),
          "seconds")

class WebScrapperBetHouse23():

    def __init__(self):
        self.start_time = datetime.now()
        self.url = "https://eurovisionworld.com/odds/eurovision"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
          "X-Requested-With": "XMLHttpRequest"
        }

    
    def get_df_BetHouse23(self, pos: int=2) -> pd.DataFrame:
        """
        Returns a DataFrame according to the main table about 
        odds/winrates from url.
        Args:
            pos (int, optional): pos-ition 2 by default
        Return:
            Dataframe
        """

        r = requests.get(self.url, headers=self.header)
        status_code = r.status_code

        if status_code == 200:
            # We pass the HTML content of the web to a BeautifulSoup() object
            #html = BeautifulSoup(r.text, "html.parser")
            try:
                df = pd.read_html(r.text)[pos]
                df.drop(['Unnamed: 0'], axis=1, inplace=True)
                df.rename(columns={'Unnamed: 1': 'country', 
                                   'winningchance': 'winrate'},
                          inplace=True)
                df.loc[:,'scrapped_day'] = datetime.now()
                df.head()
                return df
            except Exception as e:
                print(e)       
        else:
            print("Status Code %d" % status_code)
