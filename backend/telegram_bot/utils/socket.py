import websockets
import json
import base64
import os
import logging
import base64

logger = logging.getLogger(__name__)

BOT_WS_URL = os.environ.get("BOT_WS_URL", "ws://localhost:8080/ws/bot_connection/")


async def listen_to_django(future):
    
    try:
        async with websockets.connect(BOT_WS_URL) as websocket:
            logger.info(f"Connected to Django WebSocket: {BOT_WS_URL}")
            
            while True:
                message = await websocket.recv()
                try :
                    
                    data = json.loads(message)
                    
                except json.JSONDecodeError:
                    logger.warning("Received non-JSON message from WebSocket, skipping.")
                    continue
                
                if "image" in data:
                    
                    image_bytes = base64.b64decode(data["image"])
                    
                    logger.info("Image received from ESP32.")
                    
                    if not future.done():
                        future.set_result(image_bytes)
                    break
                
                else:
                    logger.info(f"Received text: {data}")

                if data.get("message") == "close":
                    logger.info("Server requested close.")
                    break

                logger.debug(f"Non-image message received: {data}")

    except websockets.exceptions.ConnectionClosedError as e:
        logger.error(f"WebSocket connection closed unexpectedly: {e}")
        if not future.done():
            future.set_exception(e)
            
    except OSError as e:
        logger.error(f"Could not connect to WebSocket: {e}")
        if not future.done():
            future.set_exception(e)
            
    except Exception as e:
        logger.exception("Unexpected error in listen_to_django")
        if not future.done():
            future.set_exception(e)