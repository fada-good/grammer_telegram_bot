import telebot
import openai
import json
from telebot import types

# Set up your Telegram bot token
bot_token = '6369951441:AAFA1j_1JlHJ-BsUWwAJm_s91cW8D8Prql0'

# Set up your OpenAI API credentials
openai.api_key = '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'

bot = telebot.TeleBot(bot_token)

CALLBACK_MAIN_MENU = 'callback_main_menu'
CALLBACK_VOCABULARY = 'callback_vocabulary'


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    send_main_menu(user_id)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.message.chat.id
    callback_data = call.data

    if callback_data == CALLBACK_MAIN_MENU:
        send_main_menu(user_id)

    elif callback_data == CALLBACK_VOCABULARY:
        bot.send_message(
            user_id, "Please enter the text for vocabulary generation:")
        bot.register_next_step_handler(call.message, generate_vocabulary)


def send_main_menu(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    # Update the button type to "default" after it is clicked
    vocabulary_button = types.InlineKeyboardButton(
        'Vocabulary Generation', callback_data=CALLBACK_VOCABULARY)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(vocabulary_button)
    bot.send_message(
        user_id, "🎉 Welcome to this vocabulary generation bot 🚀 ", reply_markup=keyboard)


def generate_vocabulary(message):
    mes_id = bot.send_message(
        message.chat.id, "We are generating vocabulary... Please wait... ⏳").message_id
    text = "Give me the 10 words related to " + message.text
    print(text)
    messages = [
        {"role": "system", "content": "You are an intelligent assistant."},
        {"role": "user", "content": text}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    vocabulary = response.choices[0].message.content.split("\n")
    bot.delete_message(message.chat.id, mes_id)
    reply = "Generated vocabulary:\n\n" + "\n".join(vocabulary)
    bot.send_message(message.chat.id, reply)


# Start the bot
bot.polling()
