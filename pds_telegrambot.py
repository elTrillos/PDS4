# from telegram.ext.updater import Updater
# from telegram.update import Update
# from telegram.ext.callbackcontext import CallbackContext
# from telegram.ext.commandhandler import CommandHandler
# from telegram.ext.messagehandler import MessageHandler
# from telegram.ext.filters import Filters

# updater = Updater("5409552546:AAGjb2tDJNYt4X66ymQV4oKzsm3pC2pecYk",
# 				use_context=True)


# def start(update: Update, context: CallbackContext):
# 	update.message.reply_text(
# 		"Hello sir, Welcome to the Bot.Please write\
# 		/help to see the commands available.")

# def stats(update: Update, context: CallbackContext):
#     	update.message.reply_text("aqui va el estado")

# def help(update: Update, context: CallbackContext):
# 	update.message.reply_text("""Available Commands :-
# 	/number - 
# 	/trivia -
# 	/extra - 
#     /stats - """)



# def number_game(update: Update, context: CallbackContext):
# 	update.message.reply_text(
# 		context.message)


# def unknown(update: Update, context: CallbackContext):
# 	update.message.reply_text(
# 		"Sorry '%s' is not a valid command" % update.message.text)


# def unknown_text(update: Update, context: CallbackContext):
# 	update.message.reply_text(
# 		"Sorry I can't recognize you , you said '%s'" % update.message.text)


# updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CommandHandler('stat', stats))
# updater.dispatcher.add_handler(CommandHandler('help', help))
# updater.dispatcher.add_handler(CommandHandler('number', number_game))
# updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
# updater.dispatcher.add_handler(MessageHandler(
# 	Filters.command, unknown)) # Filters out unknown commands

# # Filters out unknown messages.
# updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

# updater.start_polling()
