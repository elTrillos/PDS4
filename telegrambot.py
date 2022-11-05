from config import *
import telebot
import random

bot = telebot.TeleBot(TELEGRAM_TOKEN)
number_start = False
trivia_start = False
max_number = 0
numero_seleccionado = 0

@bot.message_handler(commands=['start', 'help', 'number', 'trivia','extra', 'stop'])
def send_welcome(message):
    global trivia_start
    global number_start
    global max_number
    rom = "from"
    global numero_seleccionado
    if(message.text.startswith("/number")):
        bot.send_message(message.chat.id,"empezando el juego number ...")
        bot.send_message(message.chat.id,"escriba el numero maximo, a elegir")
        number_start = True
        numero_seleccionado = random.randint(0,10)
    elif(message.text.startswith("/trivia")):
        bot.send_message(message.chat.id,"empezando el juego trivia ...")
        trivia_start = True
    elif(message.text.startswith("/help")):
        bot.reply_to(message,"comandos disponibles:")
        bot.send_message(message.chat.id,"/number")
        bot.send_message(message.chat.id,"/trivia")
        bot.send_message(message.chat.id,"/extra")
        bot.send_message(message.chat.id,"el chat id {}".format(message.chat.id))
    elif(message.text.startswith("/stop")):
        bot.send_message(message.chat.id,"juego terminado")
        number_start = False
        trivia_start = False
        max_number = 0
    else:
	    bot.reply_to(message, "COMANDO INVALIDO")

@bot.message_handler(content_types=["text"])
def bot_send_text(message):
    global number_start
    global numero_seleccionado
    global max_number
    if(message.text.startswith("/")):
        bot.send_message(message.chat.id,"ejemplito")
    else:
        if(number_start == True and max_number == 0):
            try:
                max_number = int(message.text)
                numero_seleccionado = random.randint(0,max_number)
                bot.send_message(message.chat.id,"numero elegido")
            except:
                bot.send_message(message.chat.id,"no es un numero")
        elif(number_start == True and max_number != 0):
            bot.send_message(message.chat.id,"el numero escrito es...")
            try:
                if(int(message.text) == numero_seleccionado):
                    bot.send_message(message.chat.id,"... igual ganaste")
                    number_start = False
                    max_number = 0
                elif(int(message.text) > numero_seleccionado):
                    bot.send_message(message.chat.id,"... mayor, por tanto, el numero seleccionado es MENOR")
                elif(int(message.text) < numero_seleccionado):
                    bot.send_message(message.chat.id,"... menor, por tanto, el numero seleccionado es MAYOR")
                else:
                    bot.send_message(message.chat.id,"no es un numero {}".format(numero_seleccionado))
            except:
                 bot.send_message(message.chat.id,"no es un numero {}".format(numero_seleccionado))
        else:
            bot.send_message(message.chat.id,"se agradece el comando {}".format(number_start))
if __name__ == '__main__':
    print("iniciando el maravillos bot")
    bot.infinity_polling()