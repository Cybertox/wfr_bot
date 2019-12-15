from config import TOKEN, URL, PORT
import logging
import re
from RatioGen import ratioGenerator, dataGenerator
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
data_patern = re.compile(r'^[0-9]+/[0-9]+/[0-9]+/[0-9]+$', re.MULTILINE)

def start_command(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo="https://github.com/Cybertox/wfr_bot/blob/master/wf_profile.png?raw=true", caption="Please, copy your stats from https://wayfarer.nianticlabs.com/profile \n and paste here. Or use inline mode")

def ratio_gen(update, context):
    try:
        data = dataGenerator(update.message.text.split())  # парсимо повідомлення, витягуєм з нього цифри
        ratiodata = ratioGenerator((data[0]), data[1], data[2], data[3])  # отримуємо додаткові дані стати
        message_text_pattern = ""  # для онікса і не_онікса різні шаблони повідомлення
        username_message_pattern = ""  # в групах та супергрупах у вихлопі буде відображатись нікнейм
        if update.effective_chat.type != "private":
            username_message_pattern = "<b>" + message.from_user.username + "</b>:\n"
        if ratiodata[3] == 'Onyx':
            message_text_pattern = username_message_pattern + "👀{0:,} 👍🏻{1:,} 👎🏻{2:,} 👯‍♂{3:,}\nRatio: <b>{4:.2%}</b>\nLimbo: <b>{5:,}</b>\nBadge: <b>{6}</b> (<i>{7:,} agreements</i>)".format(
               data[0], data[1], data[2], data[3], ratiodata[1], ratiodata[2], ratiodata[3], ratiodata[0])
        else:
            message_text_pattern = username_message_pattern + "👀{0:,} 👍🏻{1:,} 👎🏻{2:,} 👯‍♂{3:,}\nRatio: <b>{4:.2%}</b>\nLimbo: <b>{5:,}</b>\nBadge: <b>{6}</b> (<i>{7:,} agreements</i>)\nNext: <b>{8:,} to {9}</b>".format(
            data[0], data[1], data[2], data[3], ratiodata[1], ratiodata[2], ratiodata[3], ratiodata[0],
                ratiodata[4], ratiodata[5])
        context.bot.send_message(chat_id=update.effective_chat.id, text=message_text_pattern, parse_mode='HTML')

    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))

#def query_opr_empty(update, context):

def query_opr(update, context):
    try:
        query = update.inline_query.query
        if not query:
            r_data = InlineQueryResultArticle(
                id='1',
                title="Enter your data",
                description="Reviewed/Accepted/Rejected/Duplicated",
                thumb_url="https://raw.githubusercontent.com/Cybertox/decypher_bot/master/wfr_logo.png",
                input_message_content=InputTextMessageContent(
                    message_text="You didn't enter anything. Try again"
                )
            )
            context.bot.answer_inline_query(update.inline_query.id, [r_data])
            return
        matches = re.match(data_patern, query)
        data = matches.group().split(r'/')
        for i in range(len(data)):
            data[i] = int(data[i])
        ratiodata = ratioGenerator(data[0], data[1], data[2], data[3])
        message_text_pattern = ""
        if ratiodata[3] == 'Onyx':
            message_text_pattern = "👀{0:,} 👍🏻{1:,} 👎🏻{2:,} 👯‍♂{3:,}\nRatio: <b>{4:.2%}</b>\nLimbo: <b>{5:,}</b>\nBadge: <b>{6}</b> (<i>{7:,} agreements</i>)".format(
                data[0], data[1], data[2], data[3], ratiodata[1], ratiodata[2], ratiodata[3], ratiodata[0])
        else:
            message_text_pattern = "👀{0:,} 👍🏻{1:,} 👎🏻{2:,} 👯‍♂{3:,}\nRatio: <b>{4:.2%}</b>\nLimbo: <b>{5:,}</b>\nBadge: <b>{6}</b> (<i>{7:,} agreements</i>)\nNext: <b>{8:,} to {9}</b>".format(
                data[0], data[1], data[2], data[3], ratiodata[1], ratiodata[2], ratiodata[3], ratiodata[0], ratiodata[4],
                ratiodata[5])
        try:
            r_data = InlineQueryResultArticle(
                id='1', title="👀{0:,} 👍🏻{1:,} 👎🏻{2:,} 👯‍♂{3:,}".format(data[0], data[1], data[2], data[3]),
                description="Ratio: {0:.2%} | Limbo: {1:,}\nBadge: {2} ({3:,} agreements)".format(
                    ratiodata[1], ratiodata[2], ratiodata[3], ratiodata[0]),
                input_message_content=InputTextMessageContent(message_text=message_text_pattern, parse_mode='HTML'),
                thumb_url=ratiodata[6]
            )
            context.bot.answer_inline_query(update.inline_query.id, [r_data])
            print(update.inline_query.from_user.username + " used inline function")
        except Exception as e:
            print("{!s}\n{!s}".format(type(e), str(e)))
    except AttributeError as e:
        return


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.text, ratio_gen))
    dp.add_handler(InlineQueryHandler(query_opr))

    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook(URL + TOKEN)
    #updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()