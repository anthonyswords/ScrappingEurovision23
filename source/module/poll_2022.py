from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
import re
from typing import List

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=options)
driver.get(url)
k = driver.find_element_by_class_name('poll_inner').text

text = re.sub(r',', '.', k[44:]) # extracting all text from 1st row until the end
text = re.sub(r'[\r\n]+', ',', text) # replacing any spaces by coma
list_text = text.split(',') # splitting each own word delimited by the coma
split = list_text[-1].split(':') # we need to divided into two pieces to match the df's length
list_text = list_text[:-1]

# adding the 'closed poll', 'xxx votes' distinctly
for i in split: 
    list_text.append(i)

# summing up to Eurovision polls 2022 dataframe's
country= []
wr= []

for i in range(len(list_text)):
    if i%2 == 0:
        wr.append(list_text[i])
    else:
        country.append(list_text[i])

poll = {
    'country' : country,
    'winrate' : wr
}

df_poll_2022 = pd.DataFrame(poll)
df_poll_2022.to_csv('Who_should_win_Eurovision_2022?')
