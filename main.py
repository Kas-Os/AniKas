import requests
import telebot
from telebot import types
import qbittorrentapi
from time import *

i = 0

url = "https://api.anilibria.tv/v3/"

random = "https://api.anilibria.tv/v3/title/random?filter=id,names[ru],names[en],season[year],season[string],genres,type[episodes],type[length],torrents,status[string]"

search = "title/search?search="

filters = "title/search?search=&genres="

all_genres = "genres"

image = "https://api.jikan.moe/v4/anime?q="

years = "years"

TOKEN = "7793252647:AAHiEwR2WsdvAKVLmQeCpPYmn-BnqDDctvs"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Рандомное Аниме")
    item2=types.KeyboardButton("Поиск Аниме")

    markup.add(item1)
    markup.add(item2)

    start = bot.send_message(message.chat.id, "Добро пожаловть в Мир Аниме!",reply_markup=markup)

    bot.delete_message(message.chat.id, start.message_id-1)


@bot.message_handler(content_types='text')
def random_anime(message):

    global ida, download_r, sizer

    if message.text=="Рандомное Аниме":

        r = requests.get(url+random).json()

        r_img = requests.get(image+r["names"]["en"]).json()

        button_exit = types.InlineKeyboardButton('Выйти', callback_data='exit')
        button_download = types.InlineKeyboardButton('Скачать', callback_data="download")

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_exit)
        keyboard.add(button_download)

        pictor_anime = bot.send_photo(message.chat.id, r_img["data"][0]["images"]["jpg"]["image_url"])

        random_anime = bot.send_message(message.chat.id,f"{r["names"]["ru"]}/\n{r["names"]["en"]}", reply_markup=keyboard)

        bot.delete_message(message.chat.id, random_anime.message_id-2)

        ida = random_anime.message_id

        lis_dw = len(r["torrents"]["list"])

        size = 0

        list_dw = []

        try:

            for i in range(lis_dw):

                dow_sizer = r["torrents"]["list"][i]["size_string"]

                i =+ 1

                list_dw.append(dow_sizer)
        
                if list_dw[0] <  list_dw[1]:

                    sizer = 0

                else: 

                    sizer = 1
        except:
            sizer = 0

        download_r = r["torrents"]["list"]
    
    if message.text=="Поиск Аниме":

        send_sh = bot.send_message(message.chat.id, "Введите Аниме")

        bot.register_next_step_handler(send_sh, sh)

def sh(message):

    global ani, lis

    ani = message.text

    bot.delete_message(message.chat.id, message.message_id-2)
    bot.delete_message(message.chat.id, message.message_id-1)

    wait = bot.send_message(message.chat.id, "Идет поиск Аниме...")

    r = requests.get(url+search+ani).json()

    sleep(1)

    bot.delete_message(message.chat.id, wait.message_id)

    naideno = bot.send_message(message.chat.id, "Аниме Найдено")

    sleep(1)

    bot.delete_message(message.chat.id, naideno.message_id)

    sleep(0.5)

    bot.delete_message(message.chat.id, message.message_id)

    sleep(0.5)

    lis = len(r["list"])

    try:

        for i in range(lis):

            bot.send_message(message.chat.id,f"{i+1}) {r["list"][i]["names"]["ru"]}")

            print(i)

            i =+ 1

        sel = bot.send_message(message.chat.id, "Выберите Аниме: ")

        bot.register_next_step_handler(sel, sel_anime)

    except:

        bot.send_message(message.chat.id,r["list"][0]["names"]["ru"])

def sel_anime(message):

    global idal, download_sh, size

    list_dw = []

    i = 1

    print(ani, lis)
    
    sel = message.text

    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id-1)
    
    button_exit = types.InlineKeyboardButton('Выйти', callback_data='exit2')
    button_download = types.InlineKeyboardButton('Скачать', callback_data='download2')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_exit)
    keyboard.add(button_download)

    for i in range(lis):
        
        print(i)

        bot.delete_message(message.chat.id, message.message_id-i-2)

        i =+ 1

    r = requests.get(url+search+ani).json()

    r_img = requests.get(image+r["list"][int(sel)-1]["names"]["en"]).json()

    bot.send_photo(message.chat.id, r_img["data"][0]["images"]["jpg"]["image_url"])

    send = bot.send_message(message.chat.id, r["list"][int(sel)-1]["names"]["ru"],reply_markup=keyboard)
    
    idal = send.message_id

    lis_dw = len(r["list"][int(sel)-1]["torrents"]["list"])

    i = 0

    size = 0

    try:

        list_dw = []

        for i in range(lis_dw):

            dow_size = r["list"][int(sel)-1]["torrents"]["list"][i]["size_string"]

            i =+ 1

            list_dw.append(dow_size)

        print(list_dw)

        if list_dw[0] <  list_dw[1]:

            size = 1

        else: 

            size = 0

    except:

        size = 0

    print(size)

    download_sh = r["list"][int(sel)-1]["torrents"]["list"]

@bot.callback_query_handler(func=lambda call:True)
def exit(call):
    if call.message:

        if call.data == "exit2":


            bot.delete_message(call.message.chat.id, idal)
            bot.delete_message(call.message.chat.id, idal-1)

        if call.data == "exit":
            bot.delete_message(call.message.chat.id, ida)
            bot.delete_message(call.message.chat.id, ida-1)

        if call.data == "download":

            conn_info = dict(
                host="localhost",
                port=8080,
                username="admin",
                password="adminadmin",
            )
            qbt_client = qbittorrentapi.Client(**conn_info)

            try:
                qbt_client.auth_log_in()
            except qbittorrentapi.LoginFailed as e:
                print(e)

            qbt_client.auth_log_out()

            with qbittorrentapi.Client(**conn_info) as qbt_client:
                if qbt_client.torrents_add(urls=download_r[sizer]["magnet"]) != "Ok.":
                    print("Failed to add torrent.")

        if call.data == "download2":
            conn_info = dict(
                host="localhost",
                port=8080,
                username="admin",
                password="adminadmin",
            )
            qbt_client = qbittorrentapi.Client(**conn_info)

            try:
                qbt_client.auth_log_in()
            except qbittorrentapi.LoginFailed as e:
                print(e)

            qbt_client.auth_log_out()

            

            with qbittorrentapi.Client(**conn_info) as qbt_client:
                if qbt_client.torrents_add(urls=download_sh[size]["magnet"]) != "Ok.":
                    print("Failed to add torrent.")

bot.infinity_polling()