from bot_instance import app
from telegram.ext import CommandHandler , MessageHandler , filters
from telegram import BotCommand
import logging
import handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

COMMANDS = {
    "start": ("start the bot", handlers.start_command),
    "take_picture": ("take a picture with flash off", handlers.take_picture_command),
    "take_picture_flash": ("take a picture with flash on", handlers.take_picture_flash_command),
    "board_led_on": ("turn on board LED", handlers.board_led_on_command),
    "board_led_off": ("turn off board LED", handlers.board_led_off_command),
    "led_1_on": ("turn on LED 1", handlers.led_1_on_command),
    "led_1_off": ("turn off LED 1", handlers.led_1_off_command),
    "led_2_on": ("turn on LED 2", handlers.led_2_on_command),
    "led_2_off": ("turn off LED 2", handlers.led_2_off_command),
    "led_3_on": ("turn on LED 3", handlers.led_3_on_command),
    "led_3_off": ("turn off LED 3", handlers.led_3_off_command),
    "help": ("usage guide", handlers.help_command),
}

async def set_commands(application):
    bot_commands = [BotCommand(cmd, desc) for cmd, (desc, _) in COMMANDS.items()]
    await application.bot.set_my_commands(bot_commands)
    
def main():
    
    # system commands
    for command, (_, handler) in COMMANDS.items():
        app.add_handler(CommandHandler(command, handler))

    # text handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_text))
    
    # voice handler
    app.add_handler(MessageHandler(filters.VOICE, handlers.handle_voice))
    
    # picture handler
    app.add_handler(MessageHandler(filters.PHOTO, handlers.handle_photo))
    
    app.job_queue.run_once(lambda c: set_commands(app), 1)
    
    app.run_polling()

if __name__ == "__main__":
    main()