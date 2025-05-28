import asyncio
from botops.monitor import check_system_health, auto_remediate

async def monitor_system(bot, chat_id):
    while True:
        health = check_system_health()
        alerts = []

        if health["cpu"] > 90:
            alerts.append(f"🔥 High CPU Usage: {health['cpu']}%")
        if health["memory"] > 90:
            alerts.append(f"🧠 High Memory Usage: {health['memory']}%")
        if health["disk"] > 95:
            alerts.append(f"💾 High Disk Usage: {health['disk']}%")

        if alerts:
            msg = "*⚠️ System Alert:*\n" + "\n".join(alerts)
            await bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")

            # Auto-remediation attempt
            actions = auto_remediate(health)
            if actions:
                action_msg = "*🛠️ Auto-Remediation:*\n" + "\n".join(actions)
                await bot.send_message(chat_id=chat_id, text=action_msg, parse_mode="Markdown")

        await asyncio.sleep(60)  # Check every 60 seconds
