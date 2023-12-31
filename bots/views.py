from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.http import require_POST, require_GET
import telebot
import logging
import json, sys, os, time  
from config.settings import BOT_TOKEN, ADMIN_CHAT_ID, STATIC_DIR

from .models import Chat, Bot


version_relise = '0.0.7'
bot = telebot.TeleBot(BOT_TOKEN, threaded = False,  parse_mode = 'HTML')

logging.basicConfig(
    level = logging.DEBUG, 
    filename = f'{STATIC_DIR}/text.log', 
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", 
    datefmt = '%H:%M:%S',
)

logger = logging.getLogger(__name__)

def main_view(request):
    response = JsonResponse({'ok':True, 'result':True, 'method':request.method, 'v':version_relise})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

    return response

def markup_inline():
    markup_inline_ = telebot.types.InlineKeyboardMarkup()
    item_yes = telebot.types.InlineKeyboardButton(text='Понятно', callback_data='Y')
    item_no = telebot.types.InlineKeyboardButton(text='Непонятно', callback_data='N')
    return markup_inline_.add(item_yes, item_no)

def get_name(message):
    name = f'{message.from_user.first_name}' if message.from_user.last_name is None else f'{message.from_user.first_name} {message.from_user.last_name}'
    return name

@require_POST
def api_bots(request: HttpRequest, token):
    """ main function """
    try:  
        method = request.method  
        data_unicode = request.body.decode('utf-8')

        if data_unicode is None or data_unicode is '':
            return JsonResponse({'error':True, 'method':method})

        data = json.loads(data_unicode)
        update = telebot.types.Update.de_json(data)
        bot.process_new_updates([update])

    except Exception as e:
        logger.error(sys.exc_info()[1])        

    return main_view(request)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    name = get_name(message)
    bot.send_message(message.chat.id, f'Приветствуем Вас! {name}\n'
                                      f'Это бот, который будет направлять беседу\n\n'
                                      f'Чтобы узнать больше команд, напишите /help', reply_markup=markup_inline())

@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    name = get_name(message)
    bot.send_message(message.chat.id, f'Приветствуем Вас! {name}\n'
                                      f'/start - включить бота\n'
                                      f'/help - справочник\n'
                                      f'/info - информация\n'
                                      f'/getchatid - возвращает ваш id или id чата\n', reply_markup=markup_inline())

@bot.message_handler(commands=['info'])
def start(message: telebot.types.Message):
    name = get_name(message)

    keyboard_ = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text="Автор: GC82", url="https://github.com/glasscat82")
    keyboard_.add(url_button)

    bot.send_message(message.chat.id, f'Информация для: {name}\n'
                                      f'Работет на: Django,Webhook,pyTelegramBotAPI\n'
                                      f'Бот: службы технической поддержки\n'
                                      f'(или прокси бот)',
                                      reply_markup = keyboard_)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'Y':
        # bot.send_message(call.message.chat.id, 'Ваш выбор - Принять')
        bot.edit_message_text('Ваш ответ принят, мы рады что вам понятно', call.message.chat.id,call.message.message_id)
    elif call.data == 'N':
        # bot.send_message(call.message.chat.id, 'Ваш выбор - Отказаться')
        bot.edit_message_text('Ваш ответ принят, если вам что-то непонятно попробуйте /help', call.message.chat.id, call.message.message_id)
    elif call.data == 'ANSWER':        
        # bot.edit_message_text(call.message.text, call.message.chat.id, call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup_inline())

@bot.message_handler(commands=['getchatid'])
def getchatid(message: telebot.types.Message):
    cid = message.chat.id
    mid = message.message_id
    fid = message.from_user.id    
    bot.send_message(message.chat.id, '\n'.join([f'cid: {cid}', f'mid: {mid}', f'fid: {fid}']))

@bot.message_handler(content_types=['text','audio','video','image','photo','voice','document'])
def on_message(message):
    is_admin = message.chat.id == int(ADMIN_CHAT_ID)

    if is_admin is True:
        if message.reply_to_message is not None:            
            # logger.debug(message.reply_to_message.forward_from)
            # logger.debug(message.reply_to_message.chat.id)
            cid = message.reply_to_message.forward_from.id
            bot.copy_message(cid, message.chat.id, message.id)
        else:
            bot.forward_message(int(ADMIN_CHAT_ID), message.chat.id, message.id)
    
    if is_admin is False:        
        bot.forward_message(int(ADMIN_CHAT_ID), message.chat.id, message.id)