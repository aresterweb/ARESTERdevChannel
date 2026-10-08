# ARESTERdev Admin Bot

Telegram admin bot for the ARESTERdev ecosystem.

## Runtime

Target runtime:

- HostDDNS
- Python 3.11.9
- Passenger / WSGI
- `passenger_wsgi.py`
- Telegram polling in a background thread

## Environment Variables

Set these in HostDDNS Environment Variables:

- `BOT_TOKEN`
- `OWNER_ID`

Do not put either value in GitHub, ZIP files, source code, or `.env`.

## Important architecture

The bot does not use `Application.run_polling()`.

Passenger runs the WSGI application in its own environment/thread, so the bot manually controls:

1. `initialize()`
2. `start()`
3. `updater.start_polling()`
4. async wait
5. `updater.stop()`
6. `stop()`
7. `shutdown()`

This avoids the `set_wakeup_fd only works in main thread` problem.

## Deployment

Upload the generated:

`deploy/ARESTERdev-bot-hostddns.zip`

to HostDDNS and extract it into the Python application root.

The deployment package contains the bot source and offline wheelhouse when available.

Do not upload secrets.

## Admin panel

Current commands:

- `/start`
- `/admin`

Current owner-only panel buttons:

- Dashboard
- Bot Manager
- Website
- Channel
- Tools
- Settings

The individual modules are placeholders and will be developed stage-by-stage.
