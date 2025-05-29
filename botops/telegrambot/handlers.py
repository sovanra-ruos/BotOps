import subprocess
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

from botops.core.commands.allowport import allow_port
from botops.core.commands.deploy import deploy_container
from botops.core.commands.logcontainer import get_container_logs
from botops.docker_utils import list_running_docker_containers
from botops.monitor import check_system_health

# Set up logging
logging.basicConfig(filename='botops.log', level=logging.INFO, format='%(asctime)s - %(message)s')

ALLOWED_USER_ID = str(os.getenv("ALLOWED_USER_ID", "816611680"))

# Helper to check if the user is authorized
def is_authorized(update: Update) -> bool:
    return str(update.effective_user.id) == ALLOWED_USER_ID

async def unauthorized(update: Update):
    await update.message.reply_text("⛔ Unauthorized access.")

def run_command(cmd: list[str]) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Command: /start
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return await unauthorized(update)
    await update.message.reply_text("👋 Hello! I'm your DevOps assistant bot. Type /help to see what I can do.")

# Command: /help
async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return await unauthorized(update)
    await update.message.reply_text(
        """🛠 *PythonBotOps Help*
/status - Check CPU, memory, and disk usage
/ping <host> - Ping a server or IP
/restart <service> - Restart a system service
/log <service> - Show last 20 lines of system logs""",
        parse_mode='Markdown'
    )

# Command: /status
async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return await unauthorized(update)
    cmd = ["sh", "-c", "top -bn1 | head -5; df -h | grep '^/'"]
    output = run_command(cmd)
    await update.message.reply_text(f"📊 *System Status:*\n```{output}```", parse_mode='Markdown')

# Command: /ping <host>
async def ping_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return await unauthorized(update)
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /ping <host>")
    host = context.args[0]
    output = run_command(["ping", "-c", "4", host])
    await update.message.reply_text(f"📶 *Ping Result for* `{host}`:\n```{output}```", parse_mode='Markdown')

# Command: /restart <name>
async def restart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return await unauthorized(update)
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /restart <service>")
    service = context.args[0]
    output = run_command(["sudo", "systemctl", "restart", service])
    await update.message.reply_text(f"♻️ *Restarting* `{service}`:\n```{output or '✅ Done.'}```", parse_mode='Markdown')

# Command: /log <name>
async def log_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return await unauthorized(update)
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /log <service>")
    service = context.args[0]
    output = run_command(["journalctl", "-u", service, "--no-pager", "-n", "20"])
    await update.message.reply_text(f"📄 *Logs for* `{service}`:\n```{output}```", parse_mode='Markdown')

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    allowed_id = int(os.getenv("ALLOWED_USER_ID"))

    if user_id != allowed_id:
        await update.message.reply_text("🚫 You are not authorized.")
        return

    health = check_system_health()
    message = (
        "🖥️ *System Health Report*\n"
        f"🔹 CPU Usage: {health['cpu']}%\n"
        f"🔹 Memory Usage: {health['memory']}%\n"
        f"🔹 Disk Usage: {health['disk']}%\n"
    )

    await update.message.reply_text(message, parse_mode='Markdown')

async def docker_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    containers = list_running_docker_containers()
    if containers:
        message = "🚢 *Running Docker Containers:*\n" + "\n".join(f"- {c}" for c in containers)
    else:
        message = "No running Docker containers found."
    await update.message.reply_text(message, parse_mode="Markdown")

async def deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "⚠️ Usage: /deploy <image_name> <container_name> [<host_port:container_port>]"
        )
        return

    image_name = args[0]
    container_name = args[1]
    ports = args[2] if len(args) >= 3 else "80:80"

    result = deploy_container(image_name, container_name, ports)
    await update.message.reply_text(result)

async def allowport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("⚠️ Usage: /allowport <port_number>")
        return

    port = args[0]
    if not port.isdigit():
        await update.message.reply_text("❌ Invalid port number. Must be numeric.")
        return

    result = allow_port(port)
    await update.message.reply_text(result, parse_mode="Markdown")

async def log_container(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("⚠️ Usage: /logcontainer <container_name> [tail_lines]")
        return

    container_name = args[0]
    tail = int(args[1]) if len(args) > 1 and args[1].isdigit() else 50

    result = get_container_logs(container_name, tail)
    await update.message.reply_text(result, parse_mode="Markdown")

# Setup the Telegram bot
def setup_bot(token: str):
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("ping", ping_handler))
    app.add_handler(CommandHandler("restart", restart_handler))
    app.add_handler(CommandHandler("log", log_container))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("services", docker_command))
    app.add_handler(CommandHandler("deploy", deploy))
    app.add_handler(CommandHandler("allow_port", allowport))
    print("🚀 Bot is running...")
    return app
