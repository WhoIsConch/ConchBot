from bot.bot import ConchBot


class bot:
    def __init__(self):
        self.bot = ConchBot()
        self.bot.run()


if __name__ == "__main__":
    bot()