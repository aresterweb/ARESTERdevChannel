import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID_RAW = os.getenv("OWNER_ID")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN belum diatur di environment/.env")

if not OWNER_ID_RAW:
    raise RuntimeError("OWNER_ID belum diatur di environment/.env")

try:
    OWNER_ID = int(OWNER_ID_RAW)
except ValueError:
    raise RuntimeError("OWNER_ID harus berupa angka Telegram user ID")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def is_owner(update: Update) -> bool:
    user = update.effective_user

    if not user:
        return False

    return user.id == OWNER_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not user:
        return

    if not is_owner(update):
        await update.message.reply_text(
            "⛔ Akses ditolak.\n"
            "Bot ini hanya dapat digunakan oleh owner."
        )
        return

    await update.message.reply_text(
        f"👋 Halo {user.first_name or 'Owner'}!\n\n"
        "🤖 ARESTERdev Admin Bot\n"
        "Status: 🟢 Online\n"
        "Role: 👑 Owner\n\n"
        "Panel admin akan dikembangkan bertahap."
    )


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.message.reply_text(
            "⛔ Akses ditolak."
        )
        return

    await update.message.reply_text(
        "👑 ARESTERdev Admin Panel\n\n"
        "Status: 🟢 Online\n"
        "Role: Owner\n\n"
        "Fitur admin akan ditambahkan bertahap."
    )


def main():
    request = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0,
        pool_timeout=30.0,
    )

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .request(request)
        .get_updates_request(request)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))

    logger.info("ARESTERdev Admin Bot starting...")
    app.run_polling(bootstrap_retries=-1)


if __name__ == "__main__":
    main()
