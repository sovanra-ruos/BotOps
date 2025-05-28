import os
import asyncio
from dotenv import load_dotenv

from botops.scheduler import daily_report
from botops.telegrambot.handlers import setup_bot
from botops.monitoring_task import monitor_system

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID"))


async def run():
    app = setup_bot(TOKEN)

    # Start background monitoring
    asyncio.create_task(monitor_system(app.bot, ALLOWED_USER_ID))
    asyncio.create_task(daily_report(app.bot, ALLOWED_USER_ID, 10, 6))
    # Proper way to start the bot step-by-step
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    print("🚀 Bot is running... Press Ctrl+C to stop.")

    # Use asyncio.Event() to keep it alive
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except RuntimeError as e:
        import nest_asyncio
        import asyncio

        nest_asyncio.apply()
        asyncio.get_event_loop().run_until_complete(run())
