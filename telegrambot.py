
from config import *
import telebot
from  telebot.types import ForceReply
from flask import Flask, request #crea servidor wewb
from pyngrok import ngrok, conf 
import random
import time

bot = telebot.TeleBot(TELEGRAM_TOKEN)
web_app_server = Flask(__name__)

#variables
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

#decoradores
@web_app_server.route('/',methods=['POST'])
def webhook():
    if request.headers.get("content-type") == "application/json":
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return "OK", 200

@bot.message_handler(commands=['start', 'help', 'number', 'trivia','extra', 'stop', 'stats'])
def send_welcome(message):
    global trivia_start
    global number_start
    global max_number
    global numero_seleccionado
    global user_in_game
    global user_first_game
    global loser_list
    global trys_list
    global stop_iterator
    global trys
    markup = ForceReply()
    if(message.text.startswith("/number")):
        bot.send_message(message.chat.id,"empezando el juego number ...")
        bot.send_message(message.chat.id,"ingrese los jugadores (cada jugador debe escribir YO)")
        number_start = True
        numero_seleccionado = random.randint(0,10)
    elif(message.text.startswith("/trivia")):
        bot.send_message(message.chat.id,"empezando el juego trivia ...")
        trivia_start = True
    elif(message.text.startswith("/help") or message.text.startswith("/start") ):
        bot.reply_to(message,"comandos disponibles:")
        bot.send_message(message.chat.id,"/number")
        bot.send_message(message.chat.id,"/trivia")
        bot.send_message(message.chat.id,"/extra")
        #bot.send_message(message.chat.id,"el json {}".format(message.json))
        #bot.send_message(message.chat.id,"el otra cosa {}".format((message.json)['from']['id'])) #el identificador individual de cada usuario.
    elif(message.text.startswith("/stop")):
        bot.send_message(message.chat.id,"juego terminado")
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
    elif(message.text.startswith("/extra")):
        bot.send_message(message.chat.id,"3°juego En DESARROLLO -_-")
    elif(message.text.startswith("/stats")):
        bot.send_message(message.chat.id,"EN DESARROLLO")
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
    markup = ForceReply()
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
                    bot.send_message(message.chat.id,"escriba la cantidad de intentos",reply_markup=markup)
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
                    bot.send_message(message.chat.id,"escribe un numero :)",reply_markup=markup)
                except:
                    bot.send_message(message.chat.id,"no es un numero ERROR, ingrese el numero maximo")
            else:
                try:
                    trys = int(message.text)
                    for i in user_first_game:
                        trys_list.append([i,trys])
                    bot.send_message(message.chat.id,"numero de intentos {}".format(trys))
                    #bot.send_message(message.chat.id,"lista {}".format(trys_list))
                    bot.send_message(message.chat.id,"escriba el numero maximo",reply_markup=markup)
                except:
                    bot.send_message(message.chat.id,"no es un numero, ingrese el numero de intentos")
        elif(number_start == True and max_number != 0 and (message.json)['from']['first_name'] in user_first_game):
            try:
                for i in range(len(trys_list)):
                    if(trys_list[i][0] == (message.json)['from']['first_name']):
                        bot.send_message(message.chat.id,"intento n°{} de {}. escrito por {} es...".format(trys_list[i][1],trys,trys_list[i][0]))
                        val_try = trys_list[i][1]  
                        print(val_try)
                        trys_list.remove([(message.json)['from']['first_name'],val_try])
                        val_try = val_try-1
                        trys_list.append([(message.json)['from']['first_name'],val_try])
                        print(trys_list,"oasdkskds")
                        print("---------------------------------------------------------------")
                        val_try = 0
                        if(trys_list[i][1] < -1 and trys_list[i][0] not in loser_list):
                            loser_list.append(trys_list[i][0])
                            print(loser_list)
                            break
                        else:
                            break
                if(int(message.text) == numero_seleccionado and (message.json)['from']['first_name'] not in loser_list):
                    bot.send_message(message.chat.id,"... igual ganaste {}".format((message.json)['from']['first_name']))
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
                elif(int(message.text) > numero_seleccionado and (message.json)['from']['first_name'] not in loser_list):
                    bot.send_message(message.chat.id,"... mayor, por tanto, el numero seleccionado es MENOR {}".format(numero_seleccionado))
                elif(int(message.text) < numero_seleccionado and (message.json)['from']['first_name'] not in loser_list):
                    bot.send_message(message.chat.id,"... menor, por tanto, el numero seleccionado es MAYOR")
                elif((message.json)['from']['first_name'] in loser_list):
                    bot.send_message(message.chat.id,"jugador {} no le quedan intentos :(".format((message.json)['from']['first_name']))
                    if(len(loser_list) == len(user_first_game)):
                        bot.send_message(message.chat.id,"ya a nadie le quedan intentos \n se procede a terminar el juego \n la respuesta es {}".format(numero_seleccionado))
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
                else:
                    bot.send_message(message.chat.id,"no es un numero {}".format(numero_seleccionado))
            except:
                 bot.send_message(message.chat.id,"no es un numero")
        else:
            None

if __name__ == '__main__':
    print("iniciando el maravillos bot")
    #bot.infinity_polling()
    #definimos la ruta del archivo de configuracion de ngrok
    conf.get_default().config_path = "./config_ngrok.yml"
    #configuramos la region del servidor de ngrok
    conf.get_default().region = "sa"
    #creamos el archivo de credenciales de la api
    ngrok.set_auth_token(NGROK_TOKEN)
    # creamos un tunel https en el puerto 5000
    ngrok_tunel = ngrok.connect(5001,bind_tls=True)
    #url del tunel https creado
    ngrok_url = ngrok_tunel.public_url
    print("url ngrok: {}".format(ngrok_url))
    #eliminamos el webhook anterior
    bot.remove_webhook()
    #pequeña pausa para eliminar el webhook
    time.sleep(1)
    #definimos el webhook
    bot.set_webhook(url=ngrok_url)
    web_app_server.run(host="0.0.0.0", port=5001)