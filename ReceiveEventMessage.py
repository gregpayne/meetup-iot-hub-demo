#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
An example to show receiving events from an Event Hub asynchronously.
"""

import asyncio
import os
import sys
import json
from flask_socketio import SocketIO
from azure.eventhub.aio import EventHubConsumerClient
import websockets


# The Service Event Hub compatible endpoint from Azure portal Built-in endpoint section of theIoT Hub
CONNECTION_STR = os.environ["EVENT_HUB_CONN_STR"]
EVENTHUB_NAME = os.environ['EVENT_HUB_NAME']

sio = None

def convert(data):
    if isinstance(data, bytes):  return data.decode('ascii')
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    return data

async def send_message(payload):
    async with websockets.connect('ws://127.0.0.1:5000') as websocket:
        try:
            await websocket.send(json.dumps(payload))
        except Exception as e:
            print(f'Error: {e}', file=sys.stderr)

async def on_event(partition_context, event):
    # Put your code here.
    # If the operation is i/o intensive, async will have better performance.
    print("Received event from partition: {}.".format(partition_context.partition_id))
    print(f'Event Data: {event.body_as_str(encoding="UTF-8")}', file=sys.stderr)
    # the properties is a dictionary where the keys are decoded to bytes
    # this needs to be converted to a string before reading the values
    properties = { key.decode(): convert(val) for key, val in event.system_properties.items()}
    payload = {
        "IotData": event.body_as_str(encoding="UTF-8"),
        "MessageDate": event.enqueued_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
        "DeviceId": properties['iothub-connection-device-id']
    }
    print(f'Payload: {payload}', file=sys.stderr)
    await send_message(payload)
    await partition_context.update_checkpoint(event)


async def on_partition_initialize(partition_context):
    # Put your code here.
    print("Partition: {} has been initialized.".format(partition_context.partition_id))


async def on_partition_close(partition_context, reason):
    # Put your code here.
    print("Partition: {} has been closed, reason for closing: {}.".format(
        partition_context.partition_id,
        reason
    ))


async def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


async def main():
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group="dashboard-cg",
        eventhub_name=EVENTHUB_NAME
    )

    async with client:
        await client.receive(
            on_event=on_event,
            on_error=on_error,
            on_partition_close=on_partition_close,
            on_partition_initialize=on_partition_initialize,
            starting_position="-1",  # "-1" is from the beginning of the partition.
        )


if __name__ == '__main__':
    asyncio.run(main())