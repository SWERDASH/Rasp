import telebot, urllib3
from telebot import types
import datetime
import re
from pdf2image import convert_from_bytes
pathP = r".\poppler-24.08.0\Library\bin"
tempPath = r".\temp"
usecount = 65
def current(i, add, textr):
    if textr == 0:
        date = []
        t = datetime.datetime.now()
        tt = t + datetime.timedelta(days=add)
        weekd = tt.strftime('%a')
        if weekd == "Sat":
            tt += datetime.timedelta(days=2)
            month = tt.strftime('%b')
            day = tt.strftime('%d')
        elif weekd == "Sun":
            tt += datetime.timedelta(days=1)
            month = tt.strftime('%b')
            day = tt.strftime('%d')
        elif weekd == "Fri" and add == 1:
            tt += datetime.timedelta(days=3)
            month = tt.strftime('%b')
            day = tt.strftime('%d')
        else:
            month = tt.strftime('%b')
            day = tt.strftime('%d')
    else:
        date = []
        case = datetime.date(int(textr[0]), int(textr[1]), int(textr[2]))
        month = case.strftime('%b')
        day = case.strftime('%d')
        weekd = case.strftime('%a')

    date.append(str(day))

    if weekd == "Mon":
        date.append("ponedelnik")
    if weekd == "Tue":
        date.append("vtornik")
    if weekd == "Wed":
        date.append("sreda")
    if weekd == "Thu":
        date.append("chetverg")
    if weekd == "Fri":
        date.append("piatnitsa")
    if weekd == "Sat":
        date.append("ponedelnik")
    if weekd == "Sun":
        date.append("ponedelnik")

    if month == "Jan":
        date.append("ianvaria")
    if month == "Feb":
        date.append("fevralia")
    if month == "Mar":
        date.append("marta")
    if month == "Apr":
        date.append("aprelia")
    if month == "May":
        date.append("maia")
    if month == "Sep":
        date.append("sentiabria")
    if month == "Okt":
        date.append("oktiabria")
    if month == "Nov":
        date.append("noiabria")
    if month == "Dec":
        date.append("dekabria")

    return date[i]

bot = telebot.TeleBot('7584280846:AAGobSGdGjOjsxCYT5AVn3xXbzHEF1lbd-w')

@bot.message_handler(commands=["start"])
def start(start):
    button = types.InlineKeyboardMarkup()
    button.add(types.InlineKeyboardButton("Начать", callback_data="info"))
    bot.send_photo(start.chat.id, open(r"./temp/waiting.gif", "rb"), caption="Бот, отправляющий расписание", reply_markup=button)

@bot.callback_query_handler(func=lambda info: info.data == "info")
def main(info):
    bot.delete_message(info.message.chat.id, info.message.message_id)
    button = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('Сегодня', callback_data="send_today")
    bt2 = types.InlineKeyboardButton('Определённый день', callback_data="send_exact")
    button.row(bt1, bt2)
    button.add(types.InlineKeyboardButton('Следующий день', callback_data="send_tomorrow"))
    bot.send_photo(info.message.chat.id, open(r'./temp/images.jpeg','rb'), caption="Расписание на", reply_markup=button)

@bot.callback_query_handler(func=lambda callback: callback.data == 'send_today' or callback.data == 'send_tomorrow')
def send_template(callback):
    global usecount
    if callback.data == 'send_tomorrow':
        add = 1
        imgGet(add, callback)
        imgDel(add)
    else:
        add = 0
        imgGet(add, callback)
        imgDel(add)
    usecount += 1

@bot.callback_query_handler(func=lambda callback: callback.data == 'send_exact')
def send_exact(callback):
    bot.send_message(callback.message.chat.id, "Отправь дату в формате: <blockquote>2025 01 01</blockquote> <blockquote>(Год) (Месяц) (День) ←(это пояснение, не нужно так писать)</blockquote>", parse_mode='html')
    @bot.message_handler(content_types=["text"])
    def rec(message):
        global usecount
        text = re.sub(r'\D', " ", str(message.text.lower()))
        rex = re.compile(r"[0-9]")
        textr = text.split()
        if rex.match(text) and (formatcheck(textr)):
            imgExactGet(textr, callback)
            imgExactDel(textr)
            usecount+=1
        else:
            bot.send_message(message.chat.id, "Неверный формат")

def exists(url):
    if url.status >= 200 and url.status < 400:
        return True
    else:
        return False

def formatcheck(textr):
    if len(textr) == 3 and 0 < int(textr[1]) <= 12 and  0 < int(textr[2]) <= 31:
        return True

import os

def imgExactGet(textr, callback):
    add = 0
    url = urllib3.request("GET", f'https://gimn25.eduface.ru/uploads/62400/62391/section/2192375/{current(0, 0, textr)}_{current(2, 0, textr)}_2025_goda__{current(1, 0, textr)}_.pdf')
    if exists(url):
        img = convert_from_bytes(url.data, poppler_path=pathP)
        img_name=f"img-{current(0, add, textr)}-{current(2, 0, textr)}-{current(1, 0, textr)}.jpeg"
        img[1].save(os.path.join(tempPath, img_name), "JPEG")
        button = types.InlineKeyboardMarkup()
        button.add(types.InlineKeyboardButton("Назад", callback_data="info"))
        bot.send_photo(callback.message.chat.id, open(f"./temp/{img_name}", "rb"), caption=f"Расписание на {datetime.date(int(textr[0]), int(textr[1]), int(textr[2])).strftime("%Y-%m-%d")}", reply_markup=button)
    else:
        bot.send_animation(callback.message.chat.id, open(r'./temp/crying-emoji-meme.gif', 'rb'), caption="Расписания не существует или ссылку сломали")

def imgExactDel(textr):
    add = 0
    url = urllib3.request("GET", f'https://gimn25.eduface.ru/uploads/62400/62391/section/2192375/{current(0, 0, textr)}_{current(2, 0, textr)}_2025_goda__{current(1, 0, textr)}_.pdf')
    if exists(url):
        img = convert_from_bytes(url.data, poppler_path=pathP)
        img_name=f"img-{current(0, add, textr)}-{current(2, 0, textr)}-{current(1, 0, textr)}.jpeg"
        os.remove(f"./temp/{img_name}")

def imgGet(add, callback):
    url = urllib3.request("GET", f'https://gimn25.eduface.ru/uploads/62400/62391/section/2192375/{current(0, add, 0)}_{current(2, add, 0)}_2025_goda__{current(1, add, 0)}_.pdf')
    if exists(url):
        t = datetime.datetime.now()
        tt = t + datetime.timedelta(days=add)
        img = convert_from_bytes(url.data, poppler_path=pathP)
        img_name=f"img-{current(0, add, 0)}-{current(2, add, 0)}-{current(1, add, 0)}.jpeg"
        img[1].save(os.path.join(tempPath, img_name), "JPEG")
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        button = types.InlineKeyboardMarkup()
        button.add(types.InlineKeyboardButton("Назад", callback_data="info"))
        bot.send_photo(callback.message.chat.id, open(f"./temp/{img_name}", 'rb'), caption=f"Расписание на {tt.strftime("%Y-%m-")}{current(0, add, 0)}", reply_markup=button)
    else:
        bot.send_animation(callback.message.chat.id, open(r'./temp/crying-emoji-meme.gif', 'rb'), caption="Расписания не существует или ссылку сломали")


def imgDel(add):
    url = urllib3.request("GET", f'https://gimn25.eduface.ru/uploads/62400/62391/section/2192375/{current(0, add, 0)}_{current(2, add, 0)}_2025_goda__{current(1, add, 0)}_.pdf')
    if exists(url):
        img = convert_from_bytes(url.data, poppler_path=pathP)
        img_name=f"img-{current(0, add, 0)}-{current(2, add, 0)}-{current(1, add, 0)}.jpeg"
        os.remove(f"./temp/{img_name}")

@bot.message_handler(commands=["info"])
def usage(message):
    d = int(str(usecount)[-1])
    if  1 < d < 5:
        p = "а"
    else:
        p = ""
    bot.send_message(message.chat.id, f"Ботом воспользовались: {usecount} раз{p}")

bot.infinity_polling(timeout=10, long_polling_timeout = 5)