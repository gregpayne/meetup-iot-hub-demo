import os
import sys
import socket
import asyncio
from app import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':
   # Run from the same directory as this script
   this_files_dir = os.path.dirname(os.path.abspath(__file__))
   os.chdir(this_files_dir)

   # host = socket.gethostbyname(socket.gethostname()) # by getting the IP address of the host, this can be run on multiple PC's without changing the address
   # port = 8003
   # print('Running on http://{0}:{1}'.format(host, port), file=sys.stderr)

   socketio.run(app, port=5000, host='127.0.0.1')


