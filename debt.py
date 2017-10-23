import sqlite3
import telebot

bot = telebot.TeleBot('YourTokenHERE')

def send_log(message):
	bot.send_message(118462155,"**New Query**\nUsername : "+message.from_user.username+"\nName : "+message.from_user.first_name+"\nID : "+str(message.from_user.id)+"\nText : "+message.text)


def print_debt(message,name):
	bot.send_chat_action(message.chat.id, 'typing')
	bot.send_message(message.chat.id,"Index = Name = Cost = Location")
	conn = sqlite3.connect('debt.sqlite')		
	c=conn.cursor()
	c.execute('SELECT * FROM '+str(name))
	rows=c.fetchone()
	
	while rows is not None:
		text=[str(rows[0]),str(rows[1]),str(rows[2]),str(rows[3])]
		x='='.join(text)
		bot.send_message(message.chat.id,x)
		rows = c.fetchone()
	c.execute('SELECT SUM(COST) FROM '+str(name))
	rows=c.fetchone()
	rows=str(rows).replace(")","")
	rows=rows.replace(",","")
	rows=rows.replace("(","")
	rows="Total debt is "+rows+" Hezar Toman"
	bot.send_message(message.chat.id,rows)
	conn.close()
	send_log(message)

@bot.message_handler(commands=['behnam'])
def behnam_debt(message):
	print_debt(message,"behnam")

@bot.message_handler(commands=['reza'])
def reza_debt(message):
	print_debt(message,"reza")

@bot.message_handler(commands=['saeid'])
def saeid_debt(message):
	print_debt(message,"saeid")

@bot.message_handler(commands=['soheil'])
def soheil_debt(message):
	print_debt(message,"soheil")

@bot.message_handler(commands=['card'])
def soheil_debt(message):
	bot.send_chat_action(message.chat.id, 'typing')
	bot.send_message(message.chat.id,"My card number is : ")
	bot.send_message(message.chat.id,"****-****-****-****")
	bot.send_message(message.chat.id,"Please notify me on checking out @support")
	send_log(message)

	
# help page
@bot.message_handler(commands=['help','start'])
def command_help(message):
	commands = {  # command description used in the "help" command
              'behnam': 'Behnam\'s list of debts',
              'saeid': 'Saeid\'s list of debts',
              'reza': 'Reza\'s list of debts',
              'soheil': 'Soheil\'s list of debts'
}
	help_text = "The following commands are available: \n"
	for key in commands:  # generate help text out of the commands dictionary defined at the top
		help_text += "/" + key + ": "
		help_text += commands[key] + "\n"
	bot.send_message(message.chat.id, help_text)  # send the generated help page
	send_log(message)
	
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(message):
	bot.send_message(message.chat.id, "I don't understand \"" + message.text + "\"\nMaybe try the help page at /help")
	send_log(message)

bot.polling()
