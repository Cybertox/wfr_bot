import telebot
import RatioGen
import re
from telebot import types
import os
from flask import Flask, request
from config import TOKEN, PORT, URL

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

data_patern = re.compile(r'^[0-9]+/[0-9]+/[0-9]+/[0-9]+$', re.MULTILINE)

@bot.message_handler(commands=['start'])
def start_command(message):
    print(message.from_user.username + " pressed <<start>>")
    bot.send_photo(message.chat.id,  photo="https://github.com/Cybertox/wfr_bot/blob/master/wf_profile.png?raw=true",
                   caption="Please, copy your stats from https://wayfarer.nianticlabs.com/profile \n and paste here. Or use inline mode")

@bot.message_handler(content_types=['text'])
def ratio_gen(message):
    try:
        data = RatioGen.dataGenerator(message.text.split())  # парсимо повідомлення, витягуєм з нього цифри
        ratiodata = RatioGen.ratioGenerator((data[0]), data[1], data[2], data[3])  # отримуємо додаткові дані стати
        message_text_pattern = ""  # для онікса і не_онікса різні шаблони повідомлення
        username_message_pattern = ""  # в групах та супергрупах у вихлопі буде відображатись нікнейм
        if message.chat.type != "private":
            username_message_pattern = "<b>" + message.from_user.username + "</b>:\n"
        if ratiodata[3] == 'Onyx':
            message_text_pattern = username_message_pattern + "👀{0:,} 👍🏻{1:,} 👎🏻{2:,} 👯‍♂{3:,}\nRatio: <b>{4:.2%}</b>\nLimbo: <b>{5:,}</b>\nBadge: <b>{6}</b> (<i>{7:,} agreements</i>)".format(
                data[0], data[1], data[2], data[3], ratiodata[1], ratiodata[2], ratiodata[3], ratiodata[0])
        else:
            message_text_pattern = username_message_pattern + "👀{0:,} 👍🏻{1:,} 👎🏻{2:,} 👯‍♂{3:,}\nRatio: <b>{4:.2%}</b>\nLimbo: <b>{5:,}</b>\nBadge: <b>{6}</b> (<i>{7:,} agreements</i>)\nNext: <b>{8:,} to {9}</b>".format(
                data[0], data[1], data[2], data[3], ratiodata[1], ratiodata[2], ratiodata[3], ratiodata[0],
                ratiodata[4], ratiodata[5])

        bot.send_message(message.chat.id, message_text_pattern, parse_mode='HTML')
        print(message.from_user.username + " used stats-parser function")
        if message.chat.type != "private":
            bot.delete_message(message.chat.id, message.message_id)

    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))

@bot.inline_handler(func=lambda query: len(query.query) is 0)
def query_opr_empty(query):
    try:
        r_data = types.InlineQueryResultArticle(
            id='1',
            title="Enter your data",
            description="Reviewed/Accepted/Rejected/Duplicated",
            thumb_url="https://raw.githubusercontent.com/Cybertox/decypher_bot/master/wfr_logo.png",
            input_message_content=types.InputTextMessageContent(
                message_text="You didn't enter anything. Try again"
            )
        )
        bot.answer_inline_query(query.id, [r_data])
    except Exception as e:
        print(e)

@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_opr(query):
    try:
        matches = re.match(data_patern, query.query)
        data = matches.group().split(r'/')
        for i in range(len(data)):
            data[i] = int(data[i])
        ratiodata = RatioGen.ratioGenerator(data[0], data[1], data[2], data[3])
        message_text_pattern = ""
        if ratiodata[3] == 'Onyx':
            message_text_pattern = "👀{0:,} 👍🏻{1:,} 👎🏻{2:,} 👯‍♂{3:,}\nRatio: <b>{4:.2%}</b>\nLimbo: <b>{5:,}</b>\nBadge: <b>{6}</b> (<i>{7:,} agreements</i>)".format(
                   data[0], data[1], data[2], data[3], ratiodata[1], ratiodata[2], ratiodata[3], ratiodata[0])
        else:
            message_text_pattern = "👀{0:,} 👍🏻{1:,} 👎🏻{2:,} 👯‍♂{3:,}\nRatio: <b>{4:.2%}</b>\nLimbo: <b>{5:,}</b>\nBadge: <b>{6}</b> (<i>{7:,} agreements</i>)\nNext: <b>{8:,} to {9}</b>".format(
                   data[0], data[1], data[2], data[3], ratiodata[1], ratiodata[2], ratiodata[3], ratiodata[0], ratiodata[4], ratiodata[5])
        try:
            r_data = types.InlineQueryResultArticle(
                id='1', title="👀{0:,} 👍🏻{1:,} 👎🏻{2:,} 👯‍♂{3:,}".format(data[0], data[1], data[2], data[3]),
                description="Ratio: {0:.2%} | Limbo: {1:,}\nBadge: {2} ({3:,} agreements)".format(
                ratiodata[1], ratiodata[2], ratiodata[3], ratiodata[0]),
                input_message_content= types.InputTextMessageContent(
                   message_text=message_text_pattern, parse_mode='HTML'
                ),
                thumb_url=ratiodata[6]
            )
            bot.answer_inline_query(query.id, [r_data])
            print(message.from_user.username + " used inline function")
        except Exception as e:
            print("{!s}\n{!s}".format(type(e), str(e)))
    except AttributeError as e:
        return

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://wfr-bot.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

#bot.polling(none_stop=True)
