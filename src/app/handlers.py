import asyncio

from application import socketio
from logging_config import logger
from okx_handlers import okx_handler
from binance_handlers import binance_handler


handlers = ["okx", "binance"]
current_handler = 0  


async def connect_to_handler():
    global current_handler 

    while True:
        try:
            if handlers[current_handler] == "okx":
                await okx_handler(socketio)
            elif handlers[current_handler] == "binance":
                await binance_handler(socketio)

        except Exception as e:
            logger.error(f"Error connecting to {handlers[current_handler]}: {e}")

            if handlers[current_handler] == "okx":
                current_handler = (current_handler + 1) % len(handlers)

        await asyncio.sleep(5)


