
import re
from typing import List
from module.commons import generate_csv, os, date
from module.bet_house_2023 import *
from module.chromedriver.chrome_driver import *
from selenium.webdriver.common.by import By

def export_poll_2022(project_path):
    start_time = datetime.now()
    print("Starting job export Polled Eurovision 2023 table...")
    polled = WebScrapperPolled22()#WebScrapperBetHouse23)
    data_table = polled.get_df_polled22()
    # Export to file
    generate_csv(project_path, data_table, 'Polled_Eurovision_2022.csv')

    print("Job finished: Export countries. Elapsed time: ", (datetime.now() - start_time).total_seconds(),
          "seconds")



class WebScrapperPolled22():
    def __init__(self):
        self.url = "https://eurovisionworld.com/odds/eurovision"
        self.driver = driver_init(self.url)

        
    def get_raw_list_polled(self) -> List:
        """
        Returns a raw list to be transformed subsequently of the 
        names of the countries and their percentages of the 2022's survey.
        Returns:
            List
        """
        parent_div = self.driver.find_element(By.ID, "poll_50939")

        parent_div.click() # click parent to make table visible
        raw = parent_div.find_element(By.CLASS_NAME, "poll_r").text # get content from table

        text = re.sub(r',', '.', raw[:]) # extracting all text from 1st row until the end
        text = re.sub(r'[\r\n]+', ',', text) # replacing any spaces by coma
        list_text = text.split(',') # splitting each own word delimited by the coma
        split = list_text[-1].split(':') # we need to divided into two pieces to match the df's length
        list_text = list_text[:-1]

        # adding the 'closed poll', 'xxx votes' distinctly
        for i in split:
            list_text.append(i)
        return list_text
    
    def get_list_country_wr(self) -> List:
        """
        Returns a double list. On hand, all the countries ordered according the votes.
        On the other hands, the winrates (%) according to the votes.
        Returns:
            Two list separately (country, winrates).
        """
        list_text = self.get_raw_list_polled()
        country = []
        wr = []
        for i in range(len(list_text)):
            if i%2 == 0:
                wr.append(list_text[i])
            else:
                country.append(list_text[i])
        return country, wr
    
    def get_list_polled_vots(self, country: list) -> List:
        """
        Returns a list of total number of voters in each country.
        Country is not included. Orderered desc by default according to the web
        Args:
            country (list): each country ordered by votes according to the web
        Returns:
            List
        """
        total = []
        # click parent to make table visible
        parent_div = self.driver.find_element(By.ID, "poll_50939")
        parent_div.click()

        # click poll to toggle from percent to total votes
        poll = parent_div.find_element(By.CLASS_NAME, "poll_inner")
        poll.click()

        # find votes value and add to total list
        for i in range(1, len(country) + 1):
            total.append(int(re.findall(r'"(\d+,{0,1}\d+)"', 
                                        self.driver.find_element(By.XPATH, f'//*[@id="poll_50939"]/div/div[1]/div[{i}]').get_attribute("innerHTML") )[0].replace(',','')))

        return total
        
    def get_df_polled22(self) -> pd.DataFrame:
        country, wr = self.get_list_country_wr()
        total = self.get_list_polled_vots(country)
        poll = {
        'country' : country,
        'winrate' : wr,
        'n_votes' : total
        }
        df_poll_2022 = pd.DataFrame(poll)
        df_poll_2022.head()
        return df_poll_2022
