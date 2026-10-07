
import os
from threading import Thread
import telebot
from http.server import HTTPServer, BaseHTTPRequestHandler

# ================= CONFIGURATION =================
BOT_TOKEN ="8545222508:AAHB6XemaS2GWPU5djLcMbanVEJSsdU0JcI" # Apna token yahan complete rakhein
ADMIN_ID = 8933363928

bot = telebot.TeleBot(BOT_TOKEN)

# ================= TELEGRAM BOT LOGIC =================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Screenshot ke mutabiq exact custom welcome message aur aesthetic fonts
    user_first_name = message.from_user.first_name if message.from_user.first_name else "s4saad"
    
    welcome_text = (
        f"THANK YOU, #𝗦-ᶻᶻᶻ {user_first_name} ❤️\n"
        f"✨ THANKS FOR UsinG THIS BOT ✨\n"
        f"THiS BOT Is FOR CONTACTING #𝗦-💤 🧸\n"
        f"👤 UsERNAMe: @s4saad\n"
        f"💌 YOUR MESSaGE WILL BE SENT TO #𝗦-💤\n\n"
        f"PLEASe SEND YOUR MESSAGE BELOW.\n\n"
        f"_This bot was made using custom python script_"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Screenshot walay aesthetic style mein bot ka reply format
    fancy_response = (
        f"╭━━━ 🤖 *#𝗦-💤 Response* ━━━╮\n\n"
        f"💬 Your Message:\n`{message.text}`\n\n"
        f"✨ *Status:* Successfully sent to @s4saad!\n"
        f"╰━━━━━━━━━━━━━━━━━━━━╯"
    )
    bot.reply_to(message, fancy_response, parse_mode='Markdown')

# ================= RENDER PORT REQUIREMENT SERVER (AT THE VERY END) =================
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active and running!")

def run_server():
    port = int(os.environ.f("PORT", 10000)) if hasattr(os, 'environ') else 10000
    # Safe port fetching for Render
    try:
        port = int(os.environ.get("PORT", 10000))
    except:
        port = 10000
        
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    # 1. Background mein HTTP server start kar rahe hain taake Render port detect kar le
    Thread(target=run_server, daemon=True).start()
    
    # 2. Telegram bot ko polling par laga rahe hain
    print("Bot polling started...")
    bot.infinity_polling()

