# ARESTERdev Admin Bot

Telegram admin bot untuk ekosistem ARESTERdev.

## Runtime

Target:
- Python 3.11.9
- HostDDNS / Passenger

Startup:
- passenger_wsgi.py

Entry point:
- application

## Environment Variables

Wajib disediakan melalui HostDDNS Environment Variables:

BOT_TOKEN
OWNER_ID

Tidak menggunakan file .env pada deployment.

## Commands

/start
/admin

## Passenger Compatibility

Bot tidak menggunakan Application.run_polling() karena Passenger
menjalankan WSGI application dan bot pada background thread.

Telegram polling dijalankan secara manual:

initialize()
start()
updater.start_polling()

Kemudian event loop dijaga tetap hidup dengan asyncio.Event().

Hal ini menghindari error:

RuntimeError:
set_wakeup_fd only works in main thread of the main interpreter
