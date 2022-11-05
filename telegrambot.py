from config import *
import telebot
import random

bot = telebot.TeleBot(TELEGRAM_TOKEN)
user_in_game = []
user_first_game = []
trys_list = []
loser_list = []
number_start = False
trivia_start = False
stop_iterator = False
trys = 0
max_number = 0
numero_seleccionado = 0

@bot.message_handler(commands=['start', 'help', 'number', 'trivia','extra', 'stop'])
def send_welcome(message):
    global trivia_start
    global number_start
    global max_number
    global numero_seleccionado
    global user_in_game
    global user_first_game
    global loser_list
    global trys_list
    if(message.text.startswith("/number")):
        bot.send_message(message.chat.id,"empezando el juego number ...")
        bot.send_message(message.chat.id,"ingrese los jugadores (cada jugador debe escribir YO)")
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
        bot.send_message(message.chat.id,"el json {}".format(message.json))
        bot.send_message(message.chat.id,"el otra cosa {}".format((message.json)['from']['id'])) #el identificador individual de cada usuario.
    elif(message.text.startswith("/stop")):
        bot.send_message(message.chat.id,"juego terminado")
        number_start = False
        trivia_start = False
        user_in_game = []
        user_first_game = []
        loser_list = []
        trys_list = []
        max_number = 0
    else:
	    bot.reply_to(message, "COMANDO INVALIDO")

@bot.message_handler(content_types=["text"])
def bot_send_text(message):
    global number_start
    global user_in_game
    global user_first_game
    global trys_list
    global trys
    global numero_seleccionado
    global max_number
    global stop_iterator
    global loser_list
    val_try = 0
    if(message.text.startswith("/")):
        bot.send_message(message.chat.id,"ejemplito")
    else:
        if(number_start == True and max_number == 0):
            if(stop_iterator != True):
                if(message.text == 'stop'):
                    stop_iterator = True
                    bot.send_message(message.chat.id,"se termino de añadir a los usuarios/jugadores | jugadores actuales: ")
                    for i in user_first_game:
                        bot.send_message(message.chat.id,"{}".format(i))
                    bot.send_message(message.chat.id,"escriba la cantidad de intentos")
                else:
                    if((message.json)['from']['first_name'] in user_first_game):
                        bot.send_message(message.chat.id,"este usuario ya se añadio")
                    else:
                        user_in_game.append((message.json)['from']['id'])
                        user_first_game.append((message.json)['from']['first_name'])
                        bot.send_message(message.chat.id,"se añadio a {}".format((message.json)['from']['first_name']))
                        bot.send_message(message.chat.id,"escriba stop para parar de añadir jugadores")
  
            elif(trys != 0):
                try:
                    max_number = int(message.text)
                    numero_seleccionado = random.randint(0,max_number)
                    bot.send_message(message.chat.id,"numero maximo elegido {}".format(max_number))
                    bot.send_message(message.chat.id,"escribe un numero :)")
                except:
                    bot.send_message(message.chat.id,"no es un numero ERROR")
            else:
                try:
                    trys = int(message.text)
                    for i in user_first_game:
                        trys_list.append([i,trys])
                    bot.send_message(message.chat.id,"numero de intentos {}".format(trys))
                    bot.send_message(message.chat.id,"lista {}".format(trys_list))
                    bot.send_message(message.chat.id,"escriba el numero maximo")
                except:
                    bot.send_message(message.chat.id,"no es un numero AQUI {}".format(trys_list))
        elif(number_start == True and max_number != 0):
            bot.send_message(message.chat.id,"el numero escrito por {} es...".format((message.json)['from']['first_name']))
            try:
                for i in range(len(trys_list)):
                    if(trys_list[i][0] == (message.json)['from']['first_name']):
                        val_try = trys_list[i][1]  
                        print(val_try)
                        trys_list.remove([(message.json)['from']['first_name'],val_try])
                        val_try = val_try-1
                        trys_list.append([(message.json)['from']['first_name'],val_try])
                        print(trys_list,"oasdkskds")
                        val_try = 0
                        if(trys_list[i][1] < 0 ):
                            loser_list.append(trys_list[i][0])
                            print(loser_list)
                if(int(message.text) == numero_seleccionado and (message.json)['from']['first_name'] not in loser_list):
                    bot.send_message(message.chat.id,"... igual ganaste {}".format((message.json)['from']['first_name']))
                    user_in_game = []
                    user_first_game = []
                    trys_list = []
                    loser_list = []
                    number_start = False
                    stop_iterator = False
                    trys = 0
                    max_number = 0
                    numero_seleccionado = 0
                elif(int(message.text) > numero_seleccionado and (message.json)['from']['first_name'] not in loser_list):
                    bot.send_message(message.chat.id,"... mayor, por tanto, el numero seleccionado es MENOR {}".format(numero_seleccionado))
                elif(int(message.text) < numero_seleccionado and (message.json)['from']['first_name'] not in loser_list):
                    bot.send_message(message.chat.id,"... menor, por tanto, el numero seleccionado es MAYOR")
                elif((message.json)['from']['first_name'] in loser_list):
                    bot.send_message(message.chat.id,"jugador {} no le quedan intentos :(".format((message.json)['from']['first_name']))
                else:
                    bot.send_message(message.chat.id,"no es un numero {}".format(numero_seleccionado))
            except:
                 bot.send_message(message.chat.id,"no es un numero {}".format(numero_seleccionado))
        else:
            bot.send_message(message.chat.id,"se agradece el comando {}".format(number_start))
if __name__ == '__main__':
    print("iniciando el maravillos bot")
    bot.infinity_polling()