import telebot
import time
from flask import Flask, request
from messages import *
from config import IS_DEPLOYED, TOKEN, WEBHOOK_URL, WEBHOOK_SECRET, OPENCAGE_KEY
from sql_worker import SQL
from parking_coords import ParkingCoords
from opencage.geocoder import OpenCageGeocode


bot = telebot.TeleBot(TOKEN, threaded=False)
geocoder = OpenCageGeocode(OPENCAGE_KEY)

@bot.message_handler(commands=['start'])
def welcome(msg):
  bot.send_message(msg.chat.id, HELLO)


@bot.message_handler(content_types=["location"])
def send_parking_by_geo(msg):
  try:
    send_parkings_button(msg.chat.id, msg.location.latitude, msg.location.longitude)
  except Exception as e:
    print(e)


@bot.message_handler(content_types=["text"])
def send_parking_by_address(msg):
  try:
    result = geocoder.geocode(f'{msg.text}, Lviv', no_annotations=1, language='ua')
    lat = result[0]['geometry']['lat']
    lon = result[0]['geometry']['lng']

    send_parkings_button(msg.chat.id, lat, lon)
  except Exception as e:
    print(e)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
  try:
    if call.message:
      markup = telebot.types.InlineKeyboardMarkup()

      data_type, id = call.data.split('_')
      
      if data_type == 'subscribe' or data_type == 'unsubscribe':
        markup.add(
          telebot.types.InlineKeyboardButton(
            'Відмінити' if data_type == 'subscribe' else 'Повідомити, якщо зайнято',
            callback_data=f'unsubscribe_{id}' if data_type == 'subscribe' else f'subscribe_{id}'
          )
        )

        bot.edit_message_reply_markup(
          chat_id=call.message.chat.id,
          message_id=call.message.message_id,
          reply_markup=markup
        )

        database = SQL()

        if (data_type == 'subscribe'):
          database.add_subscription(call.message.chat.id, id)
        else:
          database.delete_subscription(call.message.chat.id, id)
      elif data_type == 'parking':
        send_parking(call.message.chat.id, id)

      bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Готово")
  except Exception as e:
    print(e)


def send_parkings_button(chat_id, lat, lon):
  try:
    parkingCoords = ParkingCoords()
    parkings = parkingCoords.get_5_closest_parking(lat, lon)

    markup = telebot.types.InlineKeyboardMarkup()

    for parking in parkings:
      if (parking['camera_url']):
        markup.add(
          telebot.types.InlineKeyboardButton(
            f"{parking['street']}, вільні місця: {parking['spaces_amount']}",
            callback_data=f"parking_{parking['id']}"
          )
        )
      else:
        markup.add(
          telebot.types.InlineKeyboardButton(
            f"{parking['street']}, немає камери",
            callback_data=f"parking_{parking['id']}"
          )
        )

    bot.send_message(chat_id, 'Найближчі парковки:', reply_markup=markup)
  except Exception as e:
    print(e)


def send_parking(chat_id, id):
  database = SQL()
  parking = database.get_parking(id)
  parking = {
    'id': parking[0],
    'street': parking[1],
    'spaces_amount': parking[2],
    'lat': float(parking[3]),
    'lon': float(parking[4]),
    'camera_url': parking[5]
  }

  if (parking['camera_url']):
    photo = open(f"recognition/images/{parking['street']}.jpg", 'rb')

    bot.send_message(
      chat_id,
      f"""
      Парковка: _{parking['street']}_
      \nВільні місця: *{parking['spaces_amount']}*
      """,
      parse_mode="Markdown"
    )
    bot.send_photo(chat_id, photo)
  else:
    bot.send_message(
      chat_id,
      f"""
      Парковка: _{parking['street']}_
      \n*На даній парковці поки немає камери*
      """,
      parse_mode='Markdown'
    )

  markup = telebot.types.InlineKeyboardMarkup()
  
  if (parking['camera_url']):
    markup.add(
      telebot.types.InlineKeyboardButton(
        'Повідомити, якщо зайнято',
        callback_data=f"subscribe_{parking['id']}"
      )
    )

  bot.send_location(chat_id, parking['lat'], parking['lon'], reply_markup=markup)


if __name__ == '__main__':
  if IS_DEPLOYED:
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=WEBHOOK_URL + WEBHOOK_SECRET)

    app = Flask(__name__)

    @app.route('/' + WEBHOOK_SECRET, methods=['POST'])
    def webhook():
      bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
      return 'ok', 200
      
    app.run()
  else:
    bot.remove_webhook()
    bot.polling(none_stop=True)