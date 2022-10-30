import pandas as pd
import requests
from bs4 import BeautifulSoup


url = 'https://eurovisionworld.com/odds/eurovision'

header = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

r = requests.get(url, headers=header)
status_code = r.status_code

if status_code == 200:

    # We pass the HTML content of the web to a BeautifulSoup() object
    html = BeautifulSoup(r.text, "html.parser")
    dfs = pd.read_html(r.text)

    # We get all the divs where the inputs are
    entradas = html.find_all('div', {'class': 'poll_inner'})

else:
    print("Status Code %d" % status_code)
    
df = dfs[2]
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df.to_csv('OddsRatioEurovision2023')
