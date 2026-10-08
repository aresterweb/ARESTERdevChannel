#!/usr/bin/env python3

import getpass
import json
import os
import re
import urllib.request
import urllib.error
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


def ask_token():
    while True:
        token = getpass.getpass(
            "\n🔐 Masukkan BOT TOKEN Telegram baru:\n"
            "(input tidak akan ditampilkan)\n> "
        ).strip()

        if not token:
            print("❌ Token tidak boleh kosong.")
            continue

        if not re.fullmatch(r"\d+:[A-Za-z0-9_-]+", token):
            print("⚠️ Format token terlihat tidak sesuai.")
            ulang = input("Tetap coba token ini? [y/N]: ").strip().lower()
            if ulang != "y":
                continue

        return token


def check_token(token):
    url = f"https://api.telegram.org/bot{token}/getMe"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        if data.get("ok") is True:
            return data.get("result")

        print("\n❌ Telegram menolak token tersebut.")
        return None

    except urllib.error.HTTPError as exc:
        print(f"\n❌ HTTP error dari Telegram: {exc.code}")
        return None

    except Exception as exc:
        print(f"\n❌ Gagal menghubungi Telegram: {exc}")
        return None


def ask_owner_id():
    while True:
        owner_id = input(
            "\n👑 Masukkan Telegram User ID kamu:\n> "
        ).strip()

        if not owner_id.isdigit():
            print("❌ User ID harus berupa angka.")
            continue

        if int(owner_id) <= 0:
            print("❌ User ID tidak valid.")
            continue

        return owner_id


def save_env(token, owner_id):
    ENV_FILE.write_text(
        f"BOT_TOKEN={token}\n"
        f"OWNER_ID={owner_id}\n",
        encoding="utf-8",
    )

    try:
        os.chmod(ENV_FILE, 0o600)
    except OSError:
        pass


def main():
    print("=" * 60)
    print("   ARESTERdev — BOT CONFIGURATION SETUP")
    print("=" * 60)
    print("\nData akan disimpan hanya di:")
    print(f"  {ENV_FILE}")
    print("\nFile .env tidak boleh di-upload ke GitHub.")

    token = ask_token()

    print("\n🔎 Mengecek BOT TOKEN ke Telegram...")
    bot = check_token(token)

    if not bot:
        print("\nSetup dibatalkan.")
        print("Periksa kembali token bot kamu.")
        return 1

    print("\n✅ BOT TOKEN valid!")
    print(f"🤖 Bot: @{bot.get('username', '-')}")
    print(f"🆔 Bot ID: {bot.get('id', '-')}")

    owner_id = ask_owner_id()

    save_env(token, owner_id)

    print("\n" + "=" * 60)
    print("✅ KONFIGURASI BERHASIL DISIMPAN")
    print("=" * 60)
    print(f"📁 File : {ENV_FILE}")
    print(f"👑 OWNER_ID : {owner_id}")
    print(f"🤖 BOT : @{bot.get('username', '-')}")
    print("\n🔒 BOT TOKEN tidak ditampilkan kembali.")
    print("🔒 .env tidak boleh di-commit ke GitHub.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
