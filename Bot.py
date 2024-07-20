import telebot
from config import  keys, TOKEN
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    text = f"Приветствую, {message.chat.username}!\nЯ Боб. И я помогу перевести ваши деньги в необходимую валюту.\nЧтобы узнать как перевести воспользуйтесь командой:/help\nЧтобы узнать какие валюты я могу перевести воспользуйтесь командой:/values\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help(message):
    text = 'Чтобы перевести деньги из одной валюты в другую, отправте сообщение в следующем виде: <валюта,из которой надо перевести> <валюта, в которую надо перевести> <количество валюты>.'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types= ['text'])
def convert(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Неправильная форма сообщения')
        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка ввода. {e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка в работе бота. Повторите попытку')
    else:
        text = f'Стоимость {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()