from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
import re
from typing import List
from module.commons import generate_csv, os, date
from module.bet_house_2023 import *

def export_poll_2022(project_path):
    start_time = datetime.now()
    print("Starting job export Polled Eurovision 2023 table...")
    
    data_table = WebScrapperPolled22(WebScrapperBetHouse23).get_df_polled22(self)
    # Export to file
    generate_csv(project_path, data_table, 'Polled_Eurovision_2022.csv')

    print("Job finished: Export countries. Elapsed time: ", (datetime.now() - start_time).total_seconds(),
          "seconds")



class WebScrapperPolled22(WebScrapperBetHouse23):
    def __init__(self):
        WebScrapperBetHouse23.__init__(self)
        
    def get_raw_list_polled(self) -> List:
        """
        Returns a raw list to be transformed subsequently of the 
        names of the countries and their percentages of the 2022's survey.
        Returns:
            List
        """
        raw = self.driver.find_element_by_class_name('poll_inner').text
        text = re.sub(r',', '.', raw[44:]) # extracting all text from 1st row until the end
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
        for i in range(1, len(country)):
            total.append(int(re.findall(r'"(\d+,{0,1}\d+)"', 
                                        self.driver.find_element_by_xpath(f'//*[@id="poll_92064"]/div/div[1]/div[{i}]').get_attribute("innerHTML") )[0].replace(',','')))
        total.append(sum(total))
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
