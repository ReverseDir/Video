#Так, тут не обычная ситуация, так как с какой стороны я не посмотрел, лучшее звонить в exe файл
#Почему будем звонить в exe файл? А что если пользователь захочет перегестрировать пользователя,
#Вроде можно здесь оставить код, но тогда как узнать когда пользователь захочет поменять пользователя?
#Можно куча выходов найти, но по мне оставить exe более чем элегатный ход, ведь его может и пользователь открыть и наткнутся на html doc

#Тут лишь проверка пользователя

import json
import os
import sys
import httplib2

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

#Хер знает что это такое, оно было в коде, вдруг влияет на что-то...
httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

def __file_extension(path, file_endswith = ".mp4"):
    'Если есть хоть один файл, определённого пути, то функция возврощает 1'
    path_file = ""
    for root, _, files in os.walk(path):
        for file in files:
            if(file.endswith(file_endswith) == True):
                return 1 
    return 0

def __find_file(path, search_file, file_endswith = ".exe"):
    'Ищет файл с определёным именим и расширением в определёном пути'
    path_file = ""
    for root, _, files in os.walk(path):
        for file in files:
            if(file.endswith(file_endswith) == True):
                if(file == search_file):
                    path_file = os.path.join(root, file).replace("\\","/")    
    return path_file

def __find_file_global(search_file = "ffmpeg.exe"):
    'Ищет на уровень ниже определёный файл, более глобальный поиск'
    path_execute_prog = os.path.abspath(os.getcwd())
    path_file = __find_file(path_execute_prog, search_file)
    if(path_file == ""):
        path_execute_prog = os.path.abspath(os.path.dirname('../'))
        path_file = __find_file(path_execute_prog, search_file) #Ищем отчайно на уровень выше это может потребовать больше времени
    return path_file




def CheckVideo(path_video, file_endswith = ".mp4"):
    'Возврощает True, если в папки есть хоть один видео файл'
    return __file_extension(path_video)

def CheckSound(path_video, file_endswith = ".mp3"):
    'Возврощает True, если в папки есть хоть один звукувой файл'
    return __file_extension(path_video)

def CheckFfmpegFfprobe():
    'Возврощает True, если в папке есть ffmpeg.exe и ffprobe.exe'
    path_ffmpeg = __find_file_global("ffmpeg.exe")
    path_ffprobe = __find_file_global("ffprobe.exe")
    if(path_ffmpeg == ""):
        return 0
    if(path_ffprobe == ""):
        return 0
    return 1

def TestConnectionGoogleApi(CLIENT_SECRETS_FILE, YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload", test_google = True):
    'Возврощает True, если пользователь зарегестрирован на Google Api'
    if(test_google == False):
        return -1
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE)
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        return 0
    return 1

def CheckFolderStruct(ifNotCreate=False):
    'Проверяет структуру папок, может их создать либо выдать ошибку, при завершение в хорошем случае выдаёт True'
    path_data = "data"
    path_cache = "data/cache"
    path_temp = "data/cache/Temp"
    path_output = "output"
    path_video = "data/video"
    if(os.path.exists(path_data) == False):
        if(ifNotCreate == True): os.mkdir(path_data)
        else: return 0
    if(os.path.exists(path_cache) == False):
        if(ifNotCreate == True): os.mkdir(path_cache)
        else: return 0
    if(os.path.exists(path_temp) == False):
        if(ifNotCreate == True): os.mkdir(path_temp)
        else: return 0
    if(os.path.exists(path_output) == False):
        if(ifNotCreate == True): os.mkdir(path_output)
        else: return 0
    if(os.path.exists(path_video) == False):
        if(ifNotCreate == True): os.mkdir(path_video)
        else: return 0
    return 1
    
#Опасно проверять ключ, а тратить квоты для проверки, мне кажется не разумным, поэтому оставим на совести пользоваетля
def CheckConnectionYoutubeApi(DEVELOPER_KEY, gadalka_mode = False):
    'Возврощает True, если есть подключение к Youtube Api. \nКрайне не желательная функция так как тратит квоту для проверки.\nТакже есть режим гадалка, который догадывается ключ это или нет'
    if(gadalka_mode == False):
        youtube = build("youtube", "v3", developerKey = DEVELOPER_KEY)
        request = youtube.videos().list(
            part="contentDetails",
            id="jNQXAC9IVRw"
        )
        error = 1
        try:
            response_video = request.execute()
        except:
             error = 0
        return error
    if(gadalka_mode == True):
        error = 1
        if(len(DEVELOPER_KEY) <= 10): #Проверяем длину обычно ключ длиный...
            error = 0
        return error

def CheckJsonFile(check_client_secrets = True, check_video_data = True, check_youtube_data = True):
    'Возврощает True, если json файлы существуют'
    error = 1
    if(check_client_secrets == True):
        error *= os.path.isfile("data/client_secrets.json")
    if(check_video_data == True):  
        error *= os.path.isfile("data/video_data.json")
    if(check_youtube_data == True):
        error *= os.path.isfile("data/youtube_data.json")
    return error


def CheckAllPrintText(check_google = True, youtubeApi_gadalka=False, youtube_api_key = "", path_client_secrets="", path_sound="", type_sound_format=".mp3", path_video="", type_video_format=".mp4"):
    'Безопасная функция, проверяет все пункты для рендера, возрощает массив\n Где первый элемент, это строки для вывода в консоль, второй элемент массива это словарь с \n\n(1) - успешным подключением\n(0) - не успешным подключением\n(-1) - не удавшемся проверка чаще всего по вине программиста'
    text_output = ""
    array_check_list = {}
    return_array_all = []
    #Интернет проверки
    check_youtube_api = 0
    check_google_api = 0
    #Обычные проверки
    check_video_file = 0
    check_sound_file = 0
    check_folder_struct = 0
    check_ffmpeg_file = 0
    check_json_file = 0
    try:
        check_folder_struct = CheckFolderStruct(True)
    except:
        check_folder_struct = -1
    try:
        check_ffmpeg_file = CheckFfmpegFfprobe()
    except:
        check_ffmpeg_file = -1
    try:
        check_sound_file = CheckSound(path_sound, type_sound_format)
    except:
        check_sound_file = -1
    try:
        check_video_file = CheckVideo(path_video, type_video_format)
    except:
        check_video_file = -1
    try:
        check_json_file = CheckJsonFile()
    except:
        check_json_file = -1
    try:
        check_youtube_api = CheckConnectionYoutubeApi(youtube_api_key, youtubeApi_gadalka)
    except:
        check_youtube_api = -1
    try:
        check_google_api = TestConnectionGoogleApi(path_client_secrets, "https://www.googleapis.com/auth/youtube.upload", check_google)
    except:
        check_google_api = -1


    if(check_youtube_api == 1):
        text_output += "✓ - Подключение к youtube успешное\n"
    elif(check_youtube_api == -1):
        text_output += "? - Подключение к youtube не известно\n"
    else:
        text_output += "✖ - Не удалось подключится к youtube успешно\n"

    if(check_google_api == 1):
        text_output += "✓ - Подключение к google успешное\n"
    elif(check_google_api == -1):
        text_output += "? - Подключение к google не известно\n"
    else:
        text_output += "✖ - Не удалось подключится к google успешно\n"

    #Проверяем обязательную информацию
    if(check_folder_struct == 1):
        text_output += "✓ - Структура папок правильная\n"
    elif(check_folder_struct == -1):
        text_output += "? - Структура папок не известно\n"
    else:
        text_output += "✖ - Структура папок не правильная\n"

    if(check_ffmpeg_file == 1):
        text_output += "✓ - файлы ffmpeg.exe и ffprobe.exe существуют\n"
    elif(check_ffmpeg_file == -1):
            text_output += "? - файлы ffmpeg.exe и ffprobe.exe не известно\n"
    else:
        text_output += "✖ - файлы ffmpeg.exe и ffprobe.exe не существует\n"

    if(check_sound_file == 1):
        text_output += "✓ - файлы звука существуют\n"
    elif(check_sound_file == -1):
        text_output += "? - файлы звука не известны\n"
    else:
        text_output += "✖ - файлы звука не существуют\n"

    if(check_video_file == 1):
        text_output += "✓ - файлы видео существуют\n"
    elif(check_video_file == -1):
        text_output += "? - файлы видео не известны\n"
    else:
        text_output += "✖ - файлы видео не существуют\n"

    if(check_json_file == 1):
        text_output += "✓ - файлы json существуют\n"
    elif(check_json_file == -1):
        text_output += "? - файлы json не известны\n"
    else:
        text_output += "✖ - файлы json не существуют\n"


    array_check_list = {
        "video": check_video_file,
        "sound": check_sound_file,
        "struct_folder": check_folder_struct,
        "ffmpeg_ffprobe": check_ffmpeg_file,
        "json": check_json_file,
        "youtube_api": check_youtube_api,
        "google_api": check_google_api
    }
    return_array_all.append(text_output)
    return_array_all.append(array_check_list)
    return return_array_all

    

    


#здесь я напишу код, условия соглашения, если код выполнился успешно
from tkinter import *
from tkinter import scrolledtext  
def checkda():
    text_use = """Вы соглашаетесь с правилами использование этой программы, а именно:
1. Сразу после регестрации и первого успешного выпуска видео на канал, программа не выдаст вам не единного уведомления, даже если в программе произодёт критический сбой она не выдаст никакого сигнала. Такова политика великого создателя Влад икей dalV, то-есть for_example, готов фитом с моргерштерном, в любом случае вы можете просто проверять папки на добавление файлов в программе и делать, то что вы хотите\n
2. Программа имеет права распорежатся ресурсами компа, каждый день, по несколько часов в день (примерное использование ресурсов 1 часовой ролик - 1-2 час рендера 35% - CPU, 700MB - RAM\n
3. В принцепи из-за чего всё это право, то писал, я не несу отвестности, за то что эта программа нанесёт вред - пользователю, организации, компании, учебному заведению и тд... Эту программу можно использовать как так называемый - "Майнер" и использовать в злых намерниях, автор не одобряет такого поведение и если вы провохранительные органы, то не ищите меня, пожалуйста, а если найдете, то возьмите меня работать как того хакера, Славика\n
4. Программа не пересылает не куда данные кроме как в Google и обращение к Youtube, данные работает у вас локально, я не имею никакого контакта к вам, вы лишь доверяете политики Google и YouTube\n

@All rights dalV 
"""


    backround_color = "F0F0F0"
    bg_text = "6B8FD4"
    fg_text = "000000"
    bg_button = "6B8FD4"
    fg_button = "FFE573"

    root = Tk()
    root.geometry("700x400")
    root["bg"] = "#"+backround_color
    text = scrolledtext.ScrolledText(width=100, height=11, bg="#"+bg_text, fg="#"+fg_text)
    text.insert('1.0', text_use)
    text['state'] = 'disabled'
    text.place(relx=0, relwidth=1, y=0)
    


    button = Button(root, text="Я согласен", font=("Arial Bold", 30), bg="#"+bg_button, fg="#"+fg_button)
    button.place(relx=0.5, y=300, anchor="c", bordermode=OUTSIDE)
    root.mainloop()