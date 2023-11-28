import telebot
from telebot import types
from datetime import datetime

from cconstants import API_KEY

bot = telebot.TeleBot(API_KEY, parse_mode=None)

@bot.message_handler(commands=["help"])
def send_help_message(msg):
    help_text = "This is the list of the commands and their purpose:\n\n" \
                "/time: current time\n" \
                "/wastebin: add wastbin weight data\n" \
                "/history: view past data of wastebins\n" \
                "/edit_history: edit past data of wastebins"

    bot.send_message(chat_id=msg.chat.id, text=help_text)

@bot.message_handler(commands=["time"])
def send_time_message(msg):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    bot.send_message(chat_id=msg.chat.id, text=f"The time now is {current_time}")

from telebot import types

user_input = ''
history = []

input_received = False
message_sent = False

@bot.message_handler(commands=["wastebin"])
def request_ocr_image(msg):
    bot.send_message(chat_id=msg.chat.id, text="Please send the image of the OCR")
    bot.register_next_step_handler(msg, manual_input)

def manual_input(msg):
    bot.send_message(chat_id=msg.chat.id, text="Thank you for the image!")

    global user_input, message_sent, input_received 
    user_input = ''
    message_sent = False
    input_received = False
    markup = types.InlineKeyboardMarkup(row_width=3)

    btns = [types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 10)]
    btns.append(types.InlineKeyboardButton("0", callback_data="0"))
    btns.append(types.InlineKeyboardButton(".", callback_data="."))
    btns.append(types.InlineKeyboardButton("Delete", callback_data="Delete")) 
    btns.append(types.InlineKeyboardButton("Done", callback_data="Done")) 

    for i in range(0, len(btns), 3):
        markup.add(*btns[i:i+3])

    bot.send_message(chat_id=msg.chat.id, text="Please input wastebin(s) weight", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global user_input, history, input_received 

    if call.data == "Done" and user_input.count(".") > 1:
        user_input = ''
        bot.send_message(chat_id=call.message.chat.id, text=f"Weight is invalid, try again")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                            text="Please input wastebin(s) weight", reply_markup=call.message.reply_markup)

    elif call.data == "Done" and user_input.endswith("."):
        bot.send_message(chat_id=call.message.chat.id, text=f"Weight is invalid")
        

    elif call.data == "Done" and user_input.startswith('0'):
        user_input = ''
        bot.send_message(chat_id=call.message.chat.id, text=f"Weight is invalid, try again")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Please input wastebin(s) weight", reply_markup=call.message.reply_markup)

    elif call.data == "Done" and input_received and user_input and not user_input.endswith(".") and not user_input.startswith('0'):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        date_time = now.strftime("%d/%m/%y, %H:%M:%S")
        history.append(f"{date_time} : Weight of the wastebin is {user_input}kg.")

        bot.send_message(chat_id=call.message.chat.id, text=f"At {time}, the weight of the wastebin collected is {user_input}kg.")
        user_input = '' 
        message_sent = True
        input_received = False 
        bot.send_message(chat_id=call.message.chat.id, text="Thank you for submitting the wastebin weight. Please choose the location from the options below.")
        
        location_choices(call)

    elif call.data == "Delete":
        user_input = ''  
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Please input wastebin(s) weight", reply_markup=call.message.reply_markup)
        
    else:
        user_input += call.data
        input_received = True
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Weight: {user_input}kg", reply_markup=call.message.reply_markup)

def location_choices(call):
    global user_input, message_sent, input_received 
    user_input = ''
    message_sent = False
    input_received = False
    markup = types.InlineKeyboardMarkup(row_width=1)

    locs = [
        types.InlineKeyboardButton("University Cultural Centre(UCC)", callback_data="University Cultural Centre(UCC)"),
        types.InlineKeyboardButton("Yong Siew Toh Conservatory of Music(YSTCM)", callback_data="Yong Siew Toh Conservatory of Music(YSTCM)"),
        types.InlineKeyboardButton("Lee Kong Chian Natural History Museum(LKCNHM)", callback_data="Lee Kong Chian Natural History Museum(LKCNHM)"),
        types.InlineKeyboardButton("NUS Staff Club", callback_data="NUS Staff Club"),
        types.InlineKeyboardButton("Department of Mathematics", callback_data="Department of Mathematics"),
        types.InlineKeyboardButton("Centre for Life Sciences(CELS)", callback_data="Centre for Life Sciences(CELS)"),
        types.InlineKeyboardButton("MD11, Yong Loo Lon School of Medicine", callback_data="MD11, Yong Loo Lon School of Medicine"),
        types.InlineKeyboardButton("Faculty of Dentistry", callback_data="Faculty of Dentistry"),
        types.InlineKeyboardButton("Frontier Canteen", callback_data="Frontier Canteen"),
        types.InlineKeyboardButton("MD1, Tahir Foundation Building", callback_data="MD1, Tahir Foundation Building"),
        types.InlineKeyboardButton("S9, Wet Science Building", callback_data="S9, Wet Science Building"),
        types.InlineKeyboardButton("Near Block S4A", callback_data="Near Block S4A"),
        types.InlineKeyboardButton("Yusof Ishak House(YIH)", callback_data="Yusof Ishak House(YIH)"),
        types.InlineKeyboardButton("Central Library", callback_data="Central Library"),
        types.InlineKeyboardButton("Technoedge Canteen", callback_data="Technoedge Canteen"),
        types.InlineKeyboardButton("Ventus building", callback_data="Ventus building"),
        types.InlineKeyboardButton("Mochtar Riady Building", callback_data="Mochtar Riady Building"),
        types.InlineKeyboardButton("Terrace Canteen", callback_data="Terrace Canteen"),
        types.InlineKeyboardButton("13(I-Cube)Building", callback_data="13(I-Cube)Building"),
        types.InlineKeyboardButton("Office of Campus Security", callback_data="Office of Campus Security"),
        types.InlineKeyboardButton("1 Kent Ridge Road", callback_data="1 Kent Ridge Road"),
        types.InlineKeyboardButton("5 Kent Ridge Road", callback_data="5 Kent Ridge Road"),
        types.InlineKeyboardButton("2 Prince George's Park", callback_data="2 Prince George's Park"),
        types.InlineKeyboardButton("3 Prince George's Park", callback_data="3 Prince George's Park"),
        types.InlineKeyboardButton("5 Prince George's Park", callback_data="5 Prince George's Park"),
        types.InlineKeyboardButton("AS8 building", callback_data="AS8 building"),
        types.InlineKeyboardButton("Tropical Marine Science Institude (TSMI)", callback_data="Tropical Marine Science Institude (TSMI)"),
        types.InlineKeyboardButton("University Sports Centre", callback_data="University Sports Centre"),
        types.InlineKeyboardButton("14.0 building", callback_data="14.0 building"),
        types.InlineKeyboardButton("Technology Centre for Offshore and Marine Singapore", callback_data="Technology Centre for Offshore and Marine Singapore"),
        types.InlineKeyboardButton("Institute of Systems Science (ISS)", callback_data="Institute of Systems Science (ISS)"),
        types.InlineKeyboardButton("Shaw Foundation Alumni House (SFAH)", callback_data="Shaw Foundation Alumni House (SFAH)"),
        types.InlineKeyboardButton("Eusoff Hall", callback_data="Eusoff Hall"),
        types.InlineKeyboardButton("Kent Ridge Hall", callback_data="Kent Ridge Hall"),
        types.InlineKeyboardButton("King Edward VII Hall", callback_data="King Edward VII Hall"),
        types.InlineKeyboardButton("Raffles Hall", callback_data="Raffles Hall"),
        types.InlineKeyboardButton("Sheares Hall", callback_data="Sheares Hall"),
        types.InlineKeyboardButton("Temasek Hall", callback_data="Temasek Hall"),
        types.InlineKeyboardButton("Ridge View Residential College, Block G", callback_data="Ridge View Residential College, Block G")
    ]

    for loc in locs:
        markup.add(loc)

    bot.send_message(chat_id=call.message.chat.id, text="Please choose the location", reply_markup=markup)

@bot.message_handler(commands=["history"])
def send_history_message(msg):
    global history  
    if history:
        bot.send_message(chat_id=msg.chat.id, text="\n".join(history))
    else:
        bot.send_message(chat_id=msg.chat.id, text="No history yet.")

@bot.message_handler(commands=["edit_history"])
def send_edit_message(msg):
    global history  
    if history:
        bot.send_message(chat_id=msg.chat.id, text="\n".join(history))
    else:
        bot.send_message(chat_id=msg.chat.id, text="No history yet.")

@bot.message_handler(commands=["exit"])
def send_buttons_message(msg):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id=msg.chat.id, text="Welcome, type /start to use the bot",reply_markup=markup)


@bot.message_handler(commands=["start"])
def send_buttons_message(msg):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    btn1 = types.KeyboardButton("/help")
    btn2 = types.KeyboardButton("/time")
    btn3 = types.KeyboardButton("/wastebin")
    btn4 = types.KeyboardButton("/history")
    btn5 = types.KeyboardButton("/edit_history")
    btn6 = types.KeyboardButton("/exit")
    markup.add(btn1,btn2,btn3,btn4,btn5,btn6)
    bot.send_message(chat_id=msg.chat.id, text="Hello! Welcome to OCRBot, how can I help?",reply_markup=markup)

bot.polling()
