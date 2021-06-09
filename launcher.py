from bot.bot import ConchBot
import asyncio
from web.main import flask_thread, run
import time

def run_bot():
    bot = ConchBot()
    bot.run()

def run_web():
    run()

if __name__ == "__main__":
    flask_thread(func=run)
    print("------")
    time.sleep(1)
    print("------")
    print("Loaded Website")
    print("------")
    run_bot()