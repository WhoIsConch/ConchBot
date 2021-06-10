from bot.bot import ConchBot
from web.main import flask_thread, run
import time

def run_bot():
    bot = ConchBot()
    bot.run()

def run_web():
    run()

if __name__ == "__main__":
    run_bot()