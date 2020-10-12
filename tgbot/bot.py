import telebot
import config
import psycopg2

from telebot import *

con = psycopg2.connect(
    database="vfzuiagd",
    user="vfzuiagd",
    password="J24sY4O6hd61gwZandkRrLXK4B9hN6xe",
    host="kandula.db.elephantsql.com",
    port="5432"
)

cur = con.cursor()

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    regions = types.KeyboardButton("Показати райони")
    nearest = types.KeyboardButton("Показати найближчі мозаїки")

    markup.add(regions, nearest)

    bot.send_message(message.chat.id, "Привіт, {0.first_name}!"
                                      "\nТут Ви зможете переглянути коротку інформацію про історичні мозаїки Львова.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)
    print(message.from_user)


@bot.message_handler(content_types=['text', 'location'])
def lala(message):
    if message.chat.type == 'private':
        markup = types.InlineKeyboardMarkup(row_width=2)
        othermarkup = types.InlineKeyboardMarkup(row_width=2)
        moreinfo = types.InlineKeyboardButton("Дізнатися більше", callback_data='author')
        showonmap = types.InlineKeyboardButton("🗺 Показати на мапі", callback_data='map')
        prev = types.InlineKeyboardButton("⬅ Назад", callback_data='prev')
        next = types.InlineKeyboardButton("➡ Далі", callback_data='next')

        markup.add(showonmap, moreinfo)
        othermarkup.add(showonmap, moreinfo, prev, next)
        kmarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        if message.content_type == 'location':
            print(message.location)
            user_latitude = message.location.latitude
            user_longitude = message.location.longitude
            cur.execute("select * from mozaik")
            rows = cur.fetchall()
            for row in rows:
                loc = row[11].split(' ')
                latitude = loc[0]
                longitude = loc[1]
                if -0.02 <= (float(user_latitude) - float(latitude)) <= 0.02:
                    if -0.02 <= (float(user_longitude) - float(longitude)) <= 0.02:
                        path = row[10]
                        bot.send_photo(message.chat.id, open(path, "rb"))
                        bot.send_message(message.chat.id,
                                         'Тип муралу - ' + row[5] + '\nЛокація, у якій розташовано мурал - ' + row[
                                             6] + '\n' + row[1] + ' ' + row[2] + ' ' + row[3].format(message.from_user,
                                                                                                     bot.get_me()),
                                         parse_mode='html', reply_markup=markup)

        if message.text == "Показати райони":
            item1 = types.KeyboardButton("Галицький район")
            item2 = types.KeyboardButton("Франківський район")
            item3 = types.KeyboardButton("Шевченківський район")
            item4 = types.KeyboardButton("Личаківський район")
            item5 = types.KeyboardButton("Залізничний район")
            item6 = types.KeyboardButton("Сихівський район")
            back = types.KeyboardButton("Назад 🔙")
            kmarkup.add(item1, item2, item3, item4, item5, item6, back)
            bot.send_message(message.chat.id, "Виберіть район, у якому хочете побачити мозаїки",
                                              parse_mode='html', reply_markup=kmarkup)
        if message.text == "Назад 🔙":
            regions = types.KeyboardButton("Показати райони")
            nearest = types.KeyboardButton("Показати найближчі мозаїки")
            kmarkup.add(regions, nearest)
            bot.send_message(message.chat.id, "Повертаємось назад...",
                             parse_mode='html', reply_markup=kmarkup)

        if message.text == "Показати найближчі мозаїки":
            loc = types.KeyboardButton("Поділитися локацією", request_location=True)
            back = types.KeyboardButton("Назад 🔙")
            kmarkup.add(loc, back)
            bot.send_message(message.chat.id, "Для того, щоб продовжити, мені потрібна Ваша локація", reply_markup=kmarkup)

        if message.text == 'Галицький район':
            cur.execute("SELECT * from mozaik where district = 'Галицький'")
            rows = cur.fetchall()
            print(len(rows))
            for row in rows:
                path = row[10]
                bot.send_photo(message.chat.id, open(path, "rb"))
                bot.send_message(message.chat.id, 'Тип муралу - '+row[5]+'\nЛокація, у якій розташовано мурал - '+row[6]+'\n'+row[1]+' '+row[2]+' '+row[3].format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

        elif message.text == 'Франківський район':
            cur.execute("SELECT * from mozaik where district = 'Франківський'")
            rows = cur.fetchall()
            print(len(rows))
            for row in rows:
                path = row[10]
                bot.send_photo(message.chat.id, open(path, "rb"))
                bot.send_message(message.chat.id, 'Тип муралу - '+row[5]+'\nЛокація, у якій розташовано мурал - '+row[6]+'\n'+row[1]+' '+row[2]+' '+row[3].format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

        elif message.text == 'Личаківський район':
            cur.execute("SELECT * from mozaik where district = 'Личаківський'")
            rows = cur.fetchall()
            print(len(rows))
            for row in rows:
                path = row[10]
                bot.send_photo(message.chat.id, open(path, "rb"))
                bot.send_message(message.chat.id, 'Тип муралу - '+row[5]+'\nЛокація, у якій розташовано мурал - '+row[6]+'\n'+row[1]+' '+row[2]+' '+row[3].format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

        elif message.text == 'Залізничний район':
            cur.execute("SELECT * from mozaik where district = 'Залізничний'")
            rows = cur.fetchall()
            print(len(rows))
            for row in rows:
                path = row[10]
                bot.send_photo(message.chat.id, open(path, "rb"))
                bot.send_message(message.chat.id, 'Тип муралу - '+row[5]+'\nЛокація, у якій розташовано мурал - '+row[6]+'\n'+row[1]+' '+row[2]+' '+row[3].format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

        elif message.text == 'Шевченківський район':
            cur.execute("SELECT * from mozaik where district = 'Шевченківський'")
            rows = cur.fetchall()
            print(len(rows))
            for row in rows:
                path = row[10]
                bot.send_photo(message.chat.id, open(path, "rb"))
                bot.send_message(message.chat.id, 'Тип муралу - '+row[5]+'\nЛокація, у якій розташовано мурал - '+row[6]+'\n'+row[1]+' '+row[2]+' '+row[3].format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

        elif message.text == 'Сихівський район':
            cur.execute("SELECT * from mozaik where district = 'Сихівський'")
            rows = cur.fetchall()
            print(len(rows))
            for row in rows:
                path = row[10]
                bot.send_photo(message.chat.id, open(path, "rb"))
                bot.send_message(message.chat.id, 'Тип муралу - '+row[5]+'\nЛокація, у якій розташовано мурал - '+row[6]+'\n'+row[1]+' '+row[2]+' '+row[3].format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'author':
                text = call.message.text.split('\n')
                location = text[2].split()
                if len(location) == 3:
                    cur.execute("SELECT author,creation_period,mozaic_individual_number "
                                "from mozaik where address_type = '"
                                + location[0]+"'AND address_name = '"+location[1]+"'AND housenumber ='"+location[2]+"'")
                    author = cur.fetchall()
                    bot.send_message(call.message.chat.id, call.message.text+'\n\nАвтор муралу - '+author[0][0]+'\nДата створення муралу - '+author[0][1]+'\nОсобистий id муралу - '+author[0][2])
                elif len(location) >= 4:
                    cur.execute(
                        "SELECT author,creation_period,mozaic_individual_number from mozaik where address_type = '" +
                        location[0] + "'AND address_name = '" + location[1] + " " + location[
                            2] + "'AND housenumber ='" + location[3] + "'")
                    author = cur.fetchall()
                    bot.send_message(call.message.chat.id, call.message.text + '\n\nАвтор муралу - ' + author[0][
                        0] + '\nДата створення муралу - ' + author[0][1] + '\nОсобистий id муралу - ' + author[0][2])
            elif call.data == 'map':
                text = call.message.text.split('\n')
                location = text[2].split()
                if len(location) == 3:
                    cur.execute(
                        "SELECT geolocation from mozaik where address_type ='" + location[0] + "'AND address_name = '" +
                        location[1] + "'AND housenumber ='" + location[2] + "'")
                elif len(location) >= 4:
                    cur.execute(
                        "SELECT geolocation from mozaik where address_type = '" +
                        location[0] + "'AND address_name = '" + location[1] + " " + location[
                            2] + "'AND housenumber ='" + location[3] + "'")
                rows = cur.fetchall()
                geo = rows[0][0].split(' ')
                bot.send_message(call.message.chat.id, call.message.text)
                bot.send_location(call.message.chat.id, geo[0], geo[1])
    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
