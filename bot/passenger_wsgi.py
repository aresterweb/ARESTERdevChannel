import os
import sys
import threading
import logging
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.chdir(BASE_DIR)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("ARESTERdev.Passenger")

_bot_started = False
_bot_lock = threading.Lock()


def _start_bot():
    global _bot_started

    try:
        from main import run_bot
        logger.info("Starting ARESTERdev Admin Bot thread...")
        run_bot()
    except Exception:
        logger.exception("ARESTERdev Admin Bot crashed.")
        traceback.print_exc()
    finally:
        _bot_started = False


def application(environ, start_response):
    global _bot_started

    with _bot_lock:
        if not _bot_started:
            _bot_started = True

            thread = threading.Thread(
                target=_start_bot,
                name="ARESTERdevBot",
                daemon=True,
            )
            thread.start()

    body = b"ARESTERdev Admin Bot is running."

    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )

    return [body]
