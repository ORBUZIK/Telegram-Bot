import telebot
from config import *
from extensions import *


bot = telebot.TeleBot(TOKEN)





@bot.message_handler(commands=['start', 'help'])
def start_func(message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты цену нужно узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты> \nСписок всех доступных валют -> /values'
    bot.send_message(message.chat.id, text)



@bot.message_handler(commands=['values'])
def available_currencies(message):
    text = 'Доступные валюты:\n'

    for key in available_dict.keys():
        text =  '\n- '.join((text, key))
    
    bot.send_message(message.chat.id, text)



@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        parameters = message.text.split(' ')
        
        # проверяем достаточно ли элементов получили
        if len(parameters) != 3:
            raise APIException('Неверное кол-во параметров')
        
        base, quote, amount = parameters
        total_base = CurrencyConverter(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, 'Ошибка пользователя\n {e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} -> {total_base.get_price(base, quote, amount)}'
        bot.send_message(message.chat.id, text)





bot.polling(non_stop=True)