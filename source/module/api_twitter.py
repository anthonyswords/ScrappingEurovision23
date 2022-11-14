
from multiprocessing import JoinableQueue, Queue, Process
import json
import http.client
import urllib.parse
# import matplotlib
from module.commons import *
from datetime import datetime
#matplotlib.use("TkAgg")



def request_tweets_count_from_api(project_path):
    """
    Given the project path, it requests to Twitter API the number of recent tweets posted with "Eurovision" tag, and
    it stores it in a csv allocated in the project path.

    :param project_path: The path where the output file will be generated
    """
    start_time = datetime.now()
    print("Starting job export twitter API...")

    # Creates a connection to Twitter API
    conn = http.client.HTTPSConnection("api.twitter.com")
    payload = ""
    # Using Token of type "Student"
    headers = {
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAHEyjAEAAAAAEsGRzAtWsiWsJBDu5xqtneL0c9s%3DoQsn121Wdx1BZ2sz50fyQVpSjNR4UQOQvoibPkhTEKojlPPXdC',
        'Cookie': 'guest_id=v1%3A166784631654754332'
    }
    # Get data filtering by "Eurovision" hashtag
    encoded_url = "https://api.twitter.com/2/tweets/counts/recent?query=%23Eurovision"
    conn.request("GET", encoded_url, payload, headers)
    res = conn.getresponse()
    data = res.read()

    # Convert the response to JSON object
    json_data = json.loads(data.decode("utf-8"))

    end_timestamp_list = []
    start_timestamp_list = []
    tweet_count_list = []
    # Iterates for every record, and storing to lists
    if "data" in json_data.keys() and json_data["data"] is not None:
        for record in json_data["data"]:
            end_timestamp_list+=[record["end"]]
            start_timestamp_list+=[record["start"]]
            tweet_count_list+=[record["tweet_count"]]

    # Create output data_table from lists
    data_table = {
        'end_timestamp': end_timestamp_list,
        'start_timestamp': start_timestamp_list,
        'tweet_count': tweet_count_list,
    }

    # Export to file
    generate_csv(project_path, data_table, 'Tweets_Count.csv')

    print("Job finished: Export Twitter API. Elapsed time: ", (datetime.now() - start_time).total_seconds(),
          "seconds")