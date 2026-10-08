import os
import asyncio
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest


BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID_RAW = os.getenv("OWNER_ID")


if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN belum diatur di HostDDNS Environment Variables")


if not OWNER_ID_RAW:
    raise RuntimeError("OWNER_ID belum diatur di HostDDNS Environment Variables")


try:
    OWNER_ID = int(OWNER_ID_RAW)
except ValueError:
    raise RuntimeError("OWNER_ID harus berupa angka Telegram user ID")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("ARESTERdev")


def is_owner(update: Update) -> bool:
    user = update.effective_user
    return bool(user and user.id == OWNER_ID)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not user or not update.message:
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
    if not update.message:
        return

    if not is_owner(update):
        await update.message.reply_text("⛔ Akses ditolak.")
        return

    await update.message.reply_text(
        "👑 ARESTERdev Admin Panel\n\n"
        "Status: 🟢 Online\n"
        "Role: Owner\n\n"
        "Fitur admin akan ditambahkan bertahap."
    )


def build_application():
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

    return app


async def run_bot_async():
    app = build_application()

    try:
        logger.info("Initializing ARESTERdev Admin Bot...")
        await app.initialize()

        logger.info("Starting ARESTERdev Admin Bot...")
        await app.start()

        if app.updater is None:
            raise RuntimeError("Telegram updater tidak tersedia")

        logger.info("Starting Telegram polling...")
        await app.updater.start_polling(
            drop_pending_updates=True
        )

        logger.info("ARESTERdev Admin Bot is ONLINE.")

        # Menjaga coroutine tetap hidup tanpa menggunakan
        # run_polling(), sehingga Passenger tidak mengalami
        # masalah signal handler di background thread.
        await asyncio.Event().wait()

    finally:
        logger.info("Stopping ARESTERdev Admin Bot...")

        if app.updater is not None:
            try:
                await app.updater.stop()
            except Exception:
                logger.exception("Error while stopping updater")

        try:
            await app.stop()
        except Exception:
            logger.exception("Error while stopping application")

        try:
            await app.shutdown()
        except Exception:
            logger.exception("Error while shutting down application")


def run_bot():
    asyncio.run(run_bot_async())


if __name__ == "__main__":
    run_bot()
