from flask import Flask, request, abort
import telebot
import hmac
import hashlib
import time

app = Flask(__name__)

BOT_TOKEN = "8304017648:AAG0jHnSATmil0qnkVJ7Bz0nBnhUFMUaXSg"  # Replace with your bot token from BotFather

def check_telegram_auth(data: dict, bot_token: str) -> bool:
    auth_data = data.copy()
    hash_received = auth_data.pop('hash', None)
    if not hash_received:
        return False

    # Sort the data and create data_check_string
    data_check_arr = [f"{k}={v}" for k, v in sorted(auth_data.items())]
    data_check_string = '\n'.join(data_check_arr)

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # Check if hashes match
    if hmac_hash != hash_received:
        return False

    # Check auth date (not older than 1 day)
    auth_date = int(auth_data.get('auth_date', 0))
    if time.time() - auth_date > 86400:
        return False

    return True

@app.route('/auth')
def auth():
    # Get query params sent by Telegram
    data = request.args.to_dict()

    if check_telegram_auth(data, BOT_TOKEN):
        user = data.get('username', 'Unknown')
        return f"Hello, @{user}! You have successfully logged in via Telegram."
    else:
        abort(403)  # Forbidden if verification fails

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
