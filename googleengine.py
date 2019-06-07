from google.cloud import monitoring_v3
import time
import csv
import numpy as np
from google.cloud import storage

print("Code is running....")

glob_bucket = {}
instances = []


def implicit():
    # Function for setting up credentials to google cloud compute engine
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
    print("Credentials accepted")

    print(storage_client)

    print("Project name: ", storage_client.project)

    print("Project email: ", storage_client.get_service_account_email())
    print("scope", storage_client.SCOPE)
    project_id = storage_client.project

    # Collecting metrics for the past 30 mins with 10 sec aggregation
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(project_id)
    interval = monitoring_v3.types.TimeInterval()
    now = time.time()
    interval.end_time.seconds = int(now)
    interval.end_time.nanos = int((now - interval.end_time.seconds))
    interval.start_time.seconds = int(now - 1800)
    interval.start_time.nanos = interval.end_time.nanos
    aggregation = monitoring_v3.types.Aggregation()
    aggregation.alignment_period.seconds = 10  # 10 seconds
    aggregation.per_series_aligner = (monitoring_v3.enums.Aggregation.Aligner.ALIGN_MEAN)

    results = client.list_time_series(
        project_name,
        'metric.type = "compute.googleapis.com/instance/cpu/utilization"',
        interval,
        monitoring_v3.enums.ListTimeSeriesRequest.TimeSeriesView.FULL, aggregation)

    # Reading Metrics and Writing to file
    log = open("test.txt", "w")
    for result in results:
        print(result)
        print(result, file=log)
    log.close()


def get_data(file_name):
    # Parsing text file
    input_file = open(file_name, "r").read().splitlines()

    data = [[None for i in range(3)] for j in range(1000)]
    current_row = 55
    for i in range(len(input_file)):
        line = input_file[i]
        if 'key: "instance_name"' in line:
            data[current_row][0] = input_file[i + 1][12:22]
            instance_name = input_file[i + 1][12:22]
        elif 'seconds:' in line:
            data[current_row][1] = input_file[i][16:]
            data[current_row][0] = instance_name
        elif 'double_value:' in line:
            data[current_row][2] = input_file[i].split(": ")[1]
            current_row -= 1

    print(data)
    return data


def data_csv(data):
    with open('mycsv.csv', 'w', newline='') as out_f:
        w = csv.writer(out_f, delimiter=',')
        w.writerows(data)





# calling the functions
implicit()
columns = ["instance", "time", "value"]
data = get_data("test.txt")
np_data = np.array(data)
np_data = np.insert(np_data, 0, np.array(columns), 0)
data_csv(np_data)
