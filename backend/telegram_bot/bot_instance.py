from telegram.ext import Application
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
app = Application.builder().token(TOKEN).build()