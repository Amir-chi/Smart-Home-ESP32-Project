from telegram import Update
from telegram.ext import ContextTypes
import httpx
import io
import asyncio
import logging
import os

from utils.socket import listen_to_django

END_POINT = os.environ.get("DJANGO_ENDPOINT", "http://localhost:8000/api/receive_message/")


logger = logging.getLogger(__name__)


async def _post(payload: dict = None, files: dict = None, data: dict = None) -> dict | None:
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if files:
                response = await client.post(END_POINT, files=files, data=data)
            else:
                response = await client.post(END_POINT, json=payload)
                
        response.raise_for_status()
        return response.json()
    
    except httpx.HTTPError as e:
        logger.error(f"HTTP error contacting Django: {e}")
        return None
    
    except Exception as e:
        logger.exception(f"Unexpected error in _post: {e}")
        return None


async def _send_led_command(update: Update, action: str, success_msg: str):
    payload = {"type": "command", "action": action}
    result = await _post(payload)

    if result and result.get("result") == "success":
        await update.message.reply_text(success_msg)
    else:
        await update.message.reply_text("Something went wrong, try again.")
        

async def _take_picture(update: Update, flash: str):
    payload = {
        "type": "command",
        "action": "capture",
        "quality": 10,
        "brightness": 0,
        "contrast": 0,
        "flash": flash,
    }

    loop = asyncio.get_running_loop()
    image_future = loop.create_future()
    asyncio.create_task(listen_to_django(image_future))

    result = await _post(payload)
    
    if result is None:
        await update.message.reply_text("Could not contact server.")
        return

    try:
        
        image_bytes = await asyncio.wait_for(image_future, timeout=20.0)
        await update.message.reply_photo(photo=image_bytes, caption="ESP32 picture")
        
    except asyncio.TimeoutError:
        await update.message.reply_text("Took too long to get picture. Try again.")
        
    except Exception as e:
        logger.exception("Socket error while waiting for image")

# ── system commands ──────────────────────────────────────

# start command of bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Wellcome to Smart Home Bot")
    
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/take_picture — take a photo\n"
        "/take_picture_flash — take a photo with flash\n"
        "/board_led_on | /board_led_off\n"
        "/led_1_on | /led_1_off\n"
        "/led_2_on | /led_2_off\n"
        "/led_3_on | /led_3_off"
    )
    

async def take_picture_flash_command(update : Update , context : ContextTypes.DEFAULT_TYPE):
    await _take_picture(update , flash="off")
    
    
async def take_picture_command(update : Update , context : ContextTypes.DEFAULT_TYPE):
    await _take_picture(update , flash="on")
    

async def board_led_off_command(update : Update , context : ContextTypes.DEFAULT_TYPE):
    await _send_led_command(update , "flash_off" , "board LED turned off")
    
    
async def board_led_on_command(update : Update , context : ContextTypes.DEFAULT_TYPE):
    await _send_led_command(update , "flash_on" , "board LED turned on")
    
    
async def led_1_on_command(update : Update , context : ContextTypes.DEFAULT_TYPE):
    await _send_led_command(update , "flash1_on" , "LED 1 turned on")
    
    
async def led_1_off_command(update : Update , context : ContextTypes.DEFAULT_TYPE):
    await _send_led_command(update , "flash1_off" , "LED 1 turned off")
    
    
async def led_2_on_command(update : Update , context : ContextTypes.DEFAULT_TYPE):
    await _send_led_command(update , "flash2_on" , "LED 2 turned on")
    
    
async def led_2_off_command(update : Update , context : ContextTypes.DEFAULT_TYPE): 
    await _send_led_command(update , "flash2_off" , "LED 2 turned off")
    
    
async def led_3_on_command(update : Update , context : ContextTypes.DEFAULT_TYPE):
    await _send_led_command(update , "flash3_on" , "LED 3 turned on")
    

async def led_3_off_command(update : Update , context : ContextTypes.DEFAULT_TYPE): 
    await _send_led_command(update , "flash3_off" , "LED 3 turned off")
    
    
# text message handler ------------------------

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    payload = {"type" : "text" , "data": update.message.text}
    
    await _post(payload)
    
    await update.message.reply_text("extracting commands from your message...")
    
    
# voice message handler ------------------------
    
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text("downloading your voice message...")

    voice_stream = io.BytesIO()
    
    new_file = await context.bot.get_file(update.message.voice.file_id)

    await new_file.download_to_memory(out=voice_stream)   
    

    files = {'voice': ('recording.ogg', voice_stream.getvalue(), 'audio/ogg')}
    result = await _post(files=files , data = {"type" : "voice"})

    if result:
        await update.message.reply_text("Voice message processed")
    else:
        await update.message.reply_text("Failed to process voice message.")
    
# picture handler ------------------------
    
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text("downloading your photo...")
    
    image_stream = io.BytesIO()
    
    photo_file = update.message.photo[-1]

    new_file = await context.bot.get_file(photo_file.file_id)
    
    await new_file.download_to_memory(out=image_stream)

    
    files = {'photo': ('user_photo.jpg', image_stream.getvalue(), 'image/jpeg')}
    result = await _post(files=files, data={"type" : "picture"})

    if result:
        await update.message.reply_text("Photo processed successfully")
    else:
        await update.message.reply_text("Failed to process photo.")
        