import asyncio
import datetime
from botops.monitor import check_system_health

async def daily_report(bot, chat_id, hour=9, minute=0):
    while True:
        now = datetime.datetime.now()
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if now >= target:
            target += datetime.timedelta(days=1)

        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        health = check_system_health()
        message = (
            "📅 *Daily System Health Report*\n"
            f"🔹 CPU Usage: {health['cpu']}%\n"
            f"🔹 Memory Usage: {health['memory']}%\n"
            f"🔹 Disk Usage: {health['disk']}%\n"
        )
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
