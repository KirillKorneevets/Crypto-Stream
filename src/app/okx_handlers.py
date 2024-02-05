import json
import asyncio
import datetime
import websockets
from flask import Flask
from flask_socketio import SocketIO

from logging_config import logger
from utils import *

app = Flask(__name__)
socketio = SocketIO(app)



async def okx_handler(socketio):
    url = 'wss://ws.okx.com:8443/ws/v5/public'
    try:
        async with websockets.connect(url, ping_interval=30, ping_timeout=90) as websocket:
            logger.info('Connected to OKX' + datetime.datetime.now().isoformat())

            await subscribe_to_channels(websocket)

            pair_count = 0

            while True:
                message = await websocket.recv()
                message = json.loads(message)
                await handle_message(message, socketio)

                pair_count += 1
                if pair_count == 3:
                    pair_count = 0
                    await asyncio.sleep(5)
    
    except websockets.ConnectionClosed as e:
        logger.error(f'Connection to OKX closed: {e}')

    except Exception as e:
        logger.error(f'Error in OKX handler: {e}')
