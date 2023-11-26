from flask import Blueprint, render_template, request, current_app
from datetime import datetime
import websockets
import json
import asyncio
import sys
from . import socketio

bp = Blueprint('main', __name__)

async def send_message(payload):
    socketio.emit('message', data=payload)
    # async with websockets.connect('ws://127.0.0.1:5000') as websocket:
    #     try:
    #         await websocket.send(json.dumps(payload))
    #     except Exception as e:
    #         print(f'Error: {e}', file=sys.stderr)

@bp.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')

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