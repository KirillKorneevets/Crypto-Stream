import asyncio
import threading
from flask import render_template

from handlers import connect_to_handler
from application import app, socketio

@app.route('/courses')
def index():
    return render_template('index.html')


@app.route('/btcusdt')
def btcusdt():
    return render_template('render_btcusdt.html')


@app.route('/ethusdt')
def ethusdt():
    return render_template('render_ethusdt.html')

@app.route('/xrpusdt')
def xrpusdt():
    return render_template('render_xrpusdt.html')


new_loop = asyncio.new_event_loop()

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == "__main__":
    threading.Thread(target=start_loop, args=(new_loop,)).start()
    asyncio.run_coroutine_threadsafe(connect_to_handler(), new_loop)
    socketio.run(app)