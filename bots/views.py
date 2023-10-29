from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.http import require_POST, require_GET
import telebot
import logging
import json, sys, os, time  
from config.settings import BOT_TOKEN, ADMIN_CHAT_ID, STATIC_DIR

from .models import Chat, Bot


bot = telebot.TeleBot(BOT_TOKEN, parse_mode = 'HTML')
chat_arr = [ADMIN_CHAT_ID]

logging.basicConfig(
    level = logging.DEBUG, 
    filename = f'{STATIC_DIR}/text.log', 
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", 
    datefmt = '%H:%M:%S',
)

logger = logging.getLogger(__name__)

def write_json(data, filename=None):
        filename = f'{STATIC_DIR}/data.json' if filename is None else filename
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filename=None):
    filename = f'{STATIC_DIR}/data.json' if filename is None else filename
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
    return {}

def main_view(request):    
    response = JsonResponse({'ok':True, 'result':True, 'method':request.method, 'v':'0.0.3'})
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

@require_POST
def api_bots(request: HttpRequest, token):    
    method = request.method  
    data_unicode = request.body.decode('utf-8')

    if data_unicode is None:
        return JsonResponse({'error':True, 'method':method})

    update = telebot.types.Update.de_json(data_unicode)
    bot.process_new_updates([update])

    return main_view(request)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    name = f'{message.from_user.first_name}' if message.from_user.last_name is None else f'{message.from_user.first_name} {message.from_user.last_name}'
    bot.send_message(message.chat.id, f'Приветствуем Вас! {name}\n'
                                      f'Мы бот, который будет наравлять беседу\n\n'
                                      f'Чтобы узнать больше команд, напишите /help', reply_markup=markup_inline())

@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    name = f'{message.from_user.first_name}' if message.from_user.last_name is None else f'{message.from_user.first_name} {message.from_user.last_name}'
    bot.send_message(message.chat.id, f'Приветствуем Вас! {name}\n'
                                      f'/start - включить бота\n'
                                      f'/help - справочник\n'
                                      f'/getchatid - возвращает ваш id или id чата\n', reply_markup=markup_inline())

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

@bot.message_handler(commands=['getuser'])
def getuser(message: telebot.types.Message):
    try:
        fid = message.from_user.id
        bot.send_message(message.chat.id, '\n'.join([f'fid: {fid}',
                                                     f'first_name: {message.from_user.first_name}',
                                                     f'username: {message.from_user.username}', 
                                                     f'last_name: {message.from_user.last_name}',
                                                     f'language_code: {message.from_user.language_code}']))  
    except Exception as e:
        logger.error(sys.exc_info()[1])

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    is_admin = message.chat.id in chat_arr

    # logger.debug(message)
    # write_json(message.json)

    if is_admin is True:
        if message.reply_to_message is not None:
            rm_arr = (message.reply_to_message.text).split('\n')
            old_chat_id = rm_arr[0].replace('cid:','',1).strip()      
            bot.send_message(old_chat_id, message.text)

    if is_admin is False:
        markup = telebot.types.ForceReply(selective=False)        
        for cid in chat_arr:
            bot.send_message(cid, f'cid: {message.chat.id}\n'
                                  f'@{message.from_user.username} / {message.from_user.first_name} / {message.from_user.last_name} / {message.from_user.language_code}\n\n'
                                  f'{message.text}', reply_markup=markup)