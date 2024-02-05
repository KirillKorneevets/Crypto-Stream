import datetime
import json
from flask import Flask
from flask_socketio import SocketIO

from logging_config import logger

app = Flask(__name__)
socketio = SocketIO(app)

data_map = {}


async def subscribe_to_channels(ws):
    channels = [
        {'channel': 'mark-price', 'instId': 'BTC-USDT'},
        {'channel': 'mark-price', 'instId': 'ETH-USDT'},
        {'channel': 'mark-price', 'instId': 'XRP-USDT'}
    ]
    subs = {'op': 'subscribe', 'args': channels}
    await ws.send(json.dumps(subs))


def process_data(data, socketio):
    symbol = data.get('instId')
    price = float(data.get('markPx', '0.0'))

    timestamp = datetime.datetime.now().isoformat()
    logger.info(f'{timestamp} {symbol} = {price}')

    data_map[symbol] = price

    socketio.emit('update_data', {'timestamp': timestamp, 'symbol': symbol, 'price': price})


async def handle_message(msg, socketio):
    ev = msg.get('event')
    data = msg.get('data')

    if ev:
        logger.info(f'******** event {ev} ********')
    elif data and len(data) > 0:
        process_data(data[0], socketio)
