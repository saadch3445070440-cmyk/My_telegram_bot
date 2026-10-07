import os 
from threading 
import Thread

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
BOT_TOKEN = "8545222508:AAEGlKXKBpJKREDBpfXU4p7Mozs5EgbDoGI"
ADMIN_ID = 8933363928

bot = telebot.TeleBot(BOT_TOKEN)

# ------------------------------------------------------------------
# DATABASE SETUP (Permanent Storage for Replies)
# ------------------------------------------------------------------
def init_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reply_mapping (
            admin_msg_id INTEGER PRIMARY KEY,
            user_chat_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def save_mapping(admin_msg_id, user_chat_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO reply_mapping (admin_msg_id, user_chat_id) VALUES (?, ?)', (admin_msg_id, user_chat_id))
    conn.commit()
    conn.close()

def get_user_chat_id(admin_msg_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_chat_id FROM reply_mapping WHERE admin_msg_id = ?', (admin_msg_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# ------------------------------------------------------------------
# BOT HANDLERS
# ------------------------------------------------------------------

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 **Hello / Welcome!**\n\n"
        "You can send your orders or messages here directly.\n"
        "Your message will be forwarded to the admin, and they will reply soon."
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID, content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'sticker'])
def handle_user_messages(message):
    user = message.from_user
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    username = f"@{user.username}" if user.username else "No Username"
    
    user_info = (
        "📩 **New Message / Order Received!**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Name:** {full_name}\n"
        f"🏷️ **Username:** {username}\n"
        f"🆔 **User ID:** `{user.id}`\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "👇 *Reply to this message below to send your answer:*"
    )
    
    try:
        bot.send_message(ADMIN_ID, user_info, parse_mode="Markdown")
        fw_msg = bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        save_mapping(fw_msg.message_id, message.chat.id)
        bot.reply_to(message, "✅ Your message has been sent to the admin. Please wait for a reply.")
    except Exception as e:
        print(f"Error forwarding message: {e}")

@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID and message.reply_to_message is not None)
def handle_admin_reply(message):
    target_msg_id = message.reply_to_message.message_id
    user_chat_id = get_user_chat_id(target_msg_id)
    
    if user_chat_id:
        try:
            bot.copy_message(user_chat_id, ADMIN_ID, message.message_id)
            bot.reply_to(message, "✅ Your reply has been sent to the user!")
        except Exception as e:
            bot.reply_to(message, f"❌ Error sending message: {e}")
    else:
        bot.reply_to(message, "⚠️ Message record not found in the database.")

if __name__ == "__main__":
    print("🤖 Order / PM Forwarder Bot (with SQLite Database) is running...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
  
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    server_address = ('0.0.0.0', 10000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

# Server ko background thread mein chalane ke liye
Thread(target=run_server).start()
        
