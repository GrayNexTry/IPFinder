import configparser
import telebot
import requests
import socket

parser = configparser.ConfigParser()
parser.read('config.ini')


def main():
    bot = telebot.TeleBot(pars('token'))

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, f"Привет, {message.from_user.username}! \nКак пользоваться ботом? \nЛегко, пишешь /find (IP) или (Домен) и все!")

    @bot.message_handler(commands=['find'])
    def find(message):
        arg = message.text.split()[1]
        ip = socket.gethostbyname(arg)
        responce = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        try:
            answer = bot.send_message(message.chat.id, "Запрос обрабатывается...")
            bot.edit_message_text(f"Страна: {responce.get('country')} \nРегион: {responce.get('regionName')} \nГород: {responce.get('city')} \nПочтовый индекс: {responce.get('zip')} \nЧасовой пояс: {responce.get('timezone')} \nПровайдер: {responce.get('isp')}", chat_id=message.chat.id, message_id=answer.id)
            bot.send_location(message.chat.id, latitude=responce.get('lat'), longitude=responce.get('lon'))
        except socket.error:
            bot.send_message(message.chat.id, "Не правильный домен или IP")

    bot.polling(none_stop=True)


def pars(arg: str):
    try:
        result = parser['APITelegram'][arg]
        return result
    except NameError:
        return 0


if __name__ == '__main__':
    main()
