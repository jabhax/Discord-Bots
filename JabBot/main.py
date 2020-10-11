import os

from discord.ext import commands
from settings import PREFIX, DISCORD_BOT_TOKEN


def main():
    INIT_FILES = ['__init__.py', 'utils.py']
    # Setup
    bot = commands.Bot(command_prefix=PREFIX)
    for filename in os.listdir('./cogs'):
        # Find all .py files != __init__.py and load them as cogs.
        if filename.endswith('.py') and filename not in INIT_FILES:
            bot.load_extension(f'cogs.{filename[:-3]}')
    # Run
    print(f'Running JabBot Main!')
    bot.run(DISCORD_BOT_TOKEN)

if __name__ == '__main__':
    main()
