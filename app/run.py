import asyncio
import logging
from aiogram import Dispatcher, Bot

from app.config import settings
from app.common.cmd_list import private

from app.database.init import create_db, drop_db, session_maker
from app.handlers.user_private import user_private_router
from app.handlers.get_recipe import get_recipe_router
from app.handlers.get_recipe_by_ings import get_recipe_by_ings_router
from app.handlers.get_random_recipe import get_random_recipe_router
from app.handlers.admin_private import admin_router
from app.handlers.commands import cmd_router
from app.middlewares.db import DataBaseSession

#########################################################
#----------------------run.py---------------------------#


# Initialize Bot and Dispatcher
bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()



# Include Routers
dp.include_router(cmd_router)
dp.include_router(admin_router)
dp.include_router(get_recipe_router)
dp.include_router(get_recipe_by_ings_router)
dp.include_router(get_random_recipe_router)
dp.include_router(user_private_router)





# startup and shutdown handlers
async def on_startup(bot):
    logging.info("Starting bot")
    
    is_dropped = False
    if is_dropped:
        await drop_db()
        
    await create_db()


async def on_shutdown(bot):
    logging.info("Shutting down bot")


# main function
async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot.set_my_commands(private)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    # Start the bot
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("error")