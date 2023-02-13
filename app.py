import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Добро пожаловать в валютный бот!\nОн создан для конвертации валют. \
\nКраткая инструкция для начала работы /help"
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате: <имя валюты> \
<в какую валюту перевести>  \
<количество переводимой валюты>\nПример ввода команды: доллар рубль 100 \
\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException("Неверный формат. Пример ввода команды /help")

        quote, base, amount = values
        result = CurrencyConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду.\n{e}")
    else:
        text = f"Цена за {amount} {quote} в {base} - {result}"
        bot.send_message(message.chat.id, text)


bot.polling()
