import requests
import pandas as pd
import os
import logging 
import sys

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def make_query_url(ip, port, action):
    return 'http://' + ip + ':' + port + '/' + action

if __name__ == "__main__":
    test_data = pd.read_csv('data/csgo_test.csv').drop('round_winner', axis = 1)
    test_data_features = test_data.columns.to_list()
    test_data = test_data.to_numpy().tolist()
    test_data_types = [type(el).__name__ for el in test_data[0]]

    ip = os.getenv("WORLD_IP", "0.0.0.0")
    port = os.getenv("WORLD_IP", "8080")

    health_response = requests.get(make_query_url(ip, port, 'health'))
    health_server = health_response.status_code == 200
    if health_server:
        logger.info(f"Server is healthy")
        
        predict_query_url = make_query_url(ip, port, 'predict')
        logger.info(f"Start execute POST predict query {predict_query_url}")

        response = requests.post(predict_query_url,
                                json = {'data' : test_data,
                                        'data_types' : test_data_types,
                                        'features' : test_data_features})
        logger.info(f"Predict POST query was executed with status code: {response.status_code}")
    else:
        logger.info(f"Server is not healthy. Rerun build_and_run.sh script and check ports.")
