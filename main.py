import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables from .env file
load_dotenv()

# Get bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Store tasks in memory
tasks = []

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the user starts the bot."""
    await update.message.reply_text(
        "Hello! I am your simple task bot.\n"
        "Use /task your_task to add a task.\n"
        "Use /list to see your tasks."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show available bot commands."""
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show help message\n"
        "/task your_task - Add a new task\n"
        "/list - Show all tasks\n"
        "/clear - Clear all tasks"
    )


async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add a new task to the task list."""
    if not context.args:
        await update.message.reply_text("Please write a task after /task.")
        return

    task_text = " ".join(context.args)
    tasks.append(task_text)

    await update.message.reply_text(f"Task added: {task_text}")


async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all saved tasks."""
    if not tasks:
        await update.message.reply_text("Your task list is empty.")
        return

    task_list = "\n".join(
        [f"{index + 1}. {task}" for index, task in enumerate(tasks)]
    )

    await update.message.reply_text(f"Your tasks:\n{task_list}")


async def clear_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear all saved tasks."""
    tasks.clear()
    await update.message.reply_text("All tasks have been cleared.")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)


def main():
    """Start the Telegram bot."""
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing. Please add it to the .env file.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("task", add_task))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(CommandHandler("clear", clear_tasks))

    app.add_error_handler(error_handler)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
