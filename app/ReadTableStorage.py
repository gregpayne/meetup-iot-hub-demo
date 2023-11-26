from azure.data.tables import TableClient
import os
import pandas as pd
import matplotlib.pyplot as plt

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
    df = pd.DataFrame(data)
    df.sort_values(by=['dateTime'], inplace=True)

    fig, ax1 = plt.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax2 = ax1.twinx()
    ax1.plot(df['dateTime'], df['temperature'], 'g-')
    ax2.plot(df['dateTime'], df['humidity'], 'b-')
    ax1.set_xlabel('Time')
    ax1.set_xticklabels(df['dateTime'], rotation=45)
    ax1.set_ylabel('Temperature (C)', color='g')
    ax2.set_ylabel('Humidity (%)', color='b')
    plt.title('Temperature and Humidity')
    plt.show()
