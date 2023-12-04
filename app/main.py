from flask import Blueprint, render_template, request, current_app
from datetime import datetime
import websockets
import json
import asyncio
import sys
from . import socketio
from azure.data.tables import TableClient
import pandas as pd
import matplotlib.pyplot as plt

bp = Blueprint('main', __name__)

async def send_message(payload):
    socketio.emit('message', data=payload)
    # async with websockets.connect('ws://127.0.0.1:5000') as websocket:
    #     try:
    #         await websocket.send(json.dumps(payload))
    #     except Exception as e:
    #         print(f'Error: {e}', file=sys.stderr)

def convertTime(datetime):
    return datetime.replace("T", " ").replace("Z", "")

@bp.route('/', methods=['GET', 'POST'])
def main():
    print(request.args, file=sys.stderr)
    if request.args.get('selectDate', ''):
        date_from = '{0}T00:00:00.0Z'.format(request.args.get('from', '').strip()) # '2014-05-27 11:50:12'
        date_to = '{0}T23:59:59.9Z'.format(request.args.get('to', '').strip()) # '2018-09-13 13:21:39'
        service = TableClient.from_connection_string(conn_str=current_app.config['TABLE_CONNECTION_STRING'], table_name='greenhouseenvironment')
        filter = f"PartitionKey eq '1' and EventEnqueuedUtcTime gt datetime'{date_from}' and EventEnqueuedUtcTime lt datetime'{date_to}'" # https://learn.microsoft.com/en-us/rest/api/storageservices/querying-tables-and-entities
        entries = service.query_entities(query_filter=filter, headers={'Accept': 'application/json;odata=nometadata'})
        data = []
        for entry in entries:
            record = {"dateTime": convertTime(entry['EventEnqueuedUtcTime']), 'temperature': entry['temperature'], 'humidity': entry['humidity']}
            data.append(record)
        df = pd.DataFrame(data)
        df.sort_values(by=['dateTime'], inplace=True)
        times = df['dateTime'].tolist()
        temperature = df['temperature'].tolist()
        humidity = df['humidity'].tolist()
        plot = {}
        plot['data'] = {
            'labels': times,
            'datasets': [{
                'label': 'Temperature',
                'data': temperature,
                'backgroundColor': '#01a4e0',
                'borderColor': '#01a4e0',
                'type': 'line',
                'yAxisID': 'y-temperature'
            },{
                'label': 'Humidity',
                'data': humidity,
                'backgroundColor': '#feca45',
                'borderColor': '#feca45',
                'type': 'line',
                'yAxisID': 'y-rh'
            }]
        }
        plot['options'] = {
            'plugins': {
                'title': {'display': True, 'text': f'Temperature and Humidity', 'font': { 'size': 21 }},
                'zoom': {
                    'pan': {'enabled': True, 'mode': 'xy', 'threshold': 5},
                    'zoom': {'wheel': {'enabled': True}, 'pinch': {'enabled': True}, 'mode': 'xy'}
                },
            },
            'responsive': True,
            'scales': {
                'y-temperature': {
                    'type': 'linear',
                    'display': True,
                    'position': 'left',
                    'title': {'display': True, 'text': 'Temperature', 'font': { 'size': 12 }}
                },
                'y-rh': {
                    'type': 'linear',
                    'display': True,
                    'position': 'right',
                    'title': {'display': True, 'text': 'Humidity', 'font': { 'size': 12 }},
                    'grid': {'drawOnChartArea': False}
                },
            }
        }
        return render_template('index.html', display=True, plot=plot)
    else:
        return render_template('index.html', display=False)

@bp.route('/iot', methods=['GET', 'POST'])
def iot():
    payload = {
        "IotData": {"temperature": 22, "humidity": 80},
        "MessageDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "DeviceId": "testDevice"
    }
    print(payload, file=sys.stderr)
    asyncio.run(send_message(payload=payload))
    return render_template('index.html')