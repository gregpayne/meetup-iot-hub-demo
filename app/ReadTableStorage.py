from azure.data.tables import TableClient
import os
import pandas as pd

TABLE_CONNECTION_STRING = os.environ["TABLE_CONNECTION_STRING"]

def convertTime(datetime):
    return datetime.replace("T", " ").replace("Z", "")

if __name__ == "__main__":
    dateFormatter = '%Y-%m-%dT%H:%M:%S.%fZ'
    service = TableClient.from_connection_string(conn_str=TABLE_CONNECTION_STRING, table_name='greenhouseenvironment')
    filter = "PartitionKey eq '1'"
    entries = service.query_entities(query_filter=filter, headers={'Accept': 'application/json;odata=nometadata'})
    data = []
    for entry in entries:
        # print(entry)
        record = {"dateTime": convertTime(entry['EventEnqueuedUtcTime']), 'temperature': entry['temperature'], 'humidity': entry['humidity']}
        data.append(record)
    # print(data)
    df = pd.DataFrame(data)
    print(df)
    