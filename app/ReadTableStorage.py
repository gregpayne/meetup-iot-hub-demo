from azure.data.tables import TableClient
import os

TABLE_CONNECTION_STRING = os.environ["TABLE_CONNECTION_STRING"]

if __name__ == "__main__":
    service = TableClient.from_connection_string(conn_str=TABLE_CONNECTION_STRING, table_name='greenhouseenvironment')
    filter = "PartitionKey eq '1'"
    entries = service.query_entities(query_filter=filter)
    for entry in entries:
        record = {"EventEnqueuedUtcTime": entry["EventEnqueuedUtcTime"], "Temperature": entry["temperature"]}
        print(record)

