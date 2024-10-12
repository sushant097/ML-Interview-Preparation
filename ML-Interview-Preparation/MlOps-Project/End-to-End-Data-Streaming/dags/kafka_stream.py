from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2023, 9, 3, 10, 00),
}

def get_data():
    import requests

    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res["results"][0]
    return res

def format_data(res):
    # extract and format the data
    data = {}
    location = res['location']
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']} "\
                      f"{location['city']} {location['state']} {location['country']}"
    data['postcode'] = location['postcode']
    data['email'] = res['email']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data

def stream_data():
    import json
    from kafka import KafkaProducer
    import time
    import logging


    producer = KafkaProducer(bootstrap_servers='broker:29092', max_block_ms=5000)
    curr_time = time.time()
    while True:
        if time.time() > curr_time + 60: # 1 minute
            break
        try:
            res = get_data()
            res = format_data(res)

            # publish and push to the queue
            producer.send("users_created", json.dumps(res).encode("utf-8"))
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            continue # even loop if error occurred




with DAG('user_automation',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:
    streaming_task = PythonOperator(
        task_id='streaming_data_from_api',
        python_callable=stream_data,
    )

# stream_data()