import os
import sys
import threading
import runpy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.chdir(BASE_DIR)

_bot_started = False
_bot_lock = threading.Lock()


def _start_bot():
    global _bot_started

    with _bot_lock:
        if _bot_started:
            return

        _bot_started = True

    try:
        runpy.run_path("main.py", run_name="__main__")
    except Exception:
        _bot_started = False
        raise


def application(environ, start_response):
    global _bot_started

    if not _bot_started:
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
