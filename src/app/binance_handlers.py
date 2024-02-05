import json
import asyncio
import datetime
import websockets
from flask_socketio import SocketIO
from flask import Flask

from logging_config import logger

app = Flask(__name__)
socketio = SocketIO(app)


async def binance_handler(socketio):
    url = 'wss://stream.binance.com:9443/stream?streams='
    try:
        async with websockets.connect(url) as websocket:
            subscribe_request = {
                "method": "SUBSCRIBE",
                "params": ['btcusdt@kline_1m', 'ethusdt@kline_1m', 'xrpusdt@kline_1m'],
                "id": 1
            }

            await websocket.send(json.dumps(subscribe_request))

            response = json.loads(await websocket.recv())
            logger.info('Connected to Binance ' + datetime.datetime.now().isoformat())
            logger.debug(response)

            while True:
                pair_count = 0
                async for message in websocket:
                    data = json.loads(message)
                    symbol = data['data']['s']
                    price = data['data']['k']['c']

                    timestamp = datetime.datetime.now().isoformat()
                    logger.info(f'{timestamp} {symbol} = {price}')

                    socketio.emit('update_data', {'symbol': symbol, 'price': price})

                    pair_count += 1
                    if pair_count == 3:
                        pair_count = 0
                        await asyncio.sleep(5)
    
    except websockets.ConnectionClosed as e:
        logger.error(f'Connection to Binance closed: {e}')

    except Exception as e:
        logger.error(f'Error in Binance handler: {e}')
            



