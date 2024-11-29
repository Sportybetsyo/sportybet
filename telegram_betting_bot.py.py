
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Replace with your actual bot token from BotFather
API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Simple in-memory data for users (for production, use a database)
users = {}

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {'points': 100}
    bot.send_message(
        message.chat.id,
        f"Welcome, {message.from_user.first_name}! 🎉\nYou have {users[user_id]['points']} points. Use /bet to place bets and /leaderboard to see rankings!"
    )

# Betting command
@bot.message_handler(commands=['bet'])
def bet(message):
    user_id = message.from_user.id
    if user_id not in users:
        bot.send_message(message.chat.id, "You need to register first using /start.")
        return
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(KeyboardButton("Team A"), KeyboardButton("Team B"))
    bot.send_message(message.chat.id, "Place your bet on Team A or Team B:", reply_markup=markup)

# Handle bets
@bot.message_handler(func=lambda message: message.text in ["Team A", "Team B"])
def handle_bet(message):
    user_id = message.from_user.id
    if user_id not in users:
        bot.send_message(message.chat.id, "You need to register first using /start.")
        return
    users[user_id]['points'] -= 10  # Deduct points for betting
    bot.send_message(
        message.chat.id,
        f"You bet on {message.text}. Good luck! 🍀\nRemaining points: {users[user_id]['points']}."
    )

# Leaderboard command
@bot.message_handler(commands=['leaderboard'])
def leaderboard(message):
    if not users:
        bot.send_message(message.chat.id, "No users yet!")
        return
    leaderboard_text = "🏆 Leaderboard 🏆\n" + "\n".join(
        [f"{i+1}. {bot.get_chat(uid).first_name}: {data['points']} points"
         for i, (uid, data) in enumerate(sorted(users.items(), key=lambda item: item[1]['points'], reverse=True))]
    )
    bot.send_message(message.chat.id, leaderboard_text)

# Run the bot
print("Bot is running...")
bot.polling()
