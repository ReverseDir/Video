
import os
import random
import subprocess
import time
import tkinter #Могут быть проблемы тут, ну главное скачать tkinter если надо. У меня он преустановлен
from copy import copy, deepcopy
from msvcrt import getch
from tkinter import filedialog
from tqdm import tqdm
import numpy

#Супер форсможёрный путь как исправить пути к ffmpeg, это радикальные меры
#AudioSegment.converter = "C:\\ffmpeg\\ffmpeg\\bin\\ffmpeg.exe"
#AudioSegment.ffmpeg = "C:\\ffmpeg\\ffmpeg\\bin\\ffmpeg.exe"
#AudioSegment.ffprobe ="C:\\ffmpeg\\ffmpeg\\bin\\ffprobe.exe"


def find_file(path, search_file):
    "Он ищет указаный файл"
    path_file = ""
    for root, _, files in os.walk(path):
        for file in files:
            if(file.endswith(".exe") == True):
                if(file == search_file):
                    path_file = os.path.join(root, file).replace("\\","/")    
    return path_file

def find_file_global(search_file = "ffmpeg.exe"):
    "Он ищет отчайно указаный файл"
    path_execute_prog = os.path.abspath(os.getcwd())
    path_file = find_file(path_execute_prog, search_file)
    if(path_file == ""):
        path_execute_prog = os.path.abspath(os.path.dirname('../'))
        path_file = find_file(path_execute_prog, search_file) #Ищем отчайно на уровень выше это может потребовать больше времени
    return path_file


#find fuken FFMPEG and FFPROBE
path_ffmpeg = find_file_global("ffmpeg.exe")
if(path_ffmpeg == ""):
    print("ffmpeg not find! Please download or put inside folder ffmpeg\n")
    path_ffmpeg = "ffmpeg" 
path_ffprobe = find_file_global("ffprobe.exe")
if(path_ffprobe == ""):
    print("ffprobe not find! Please download or put inside folder ffprobe\n")
    path_ffprobe = "ffprobe"


global_path = os.path.split(path_ffmpeg)[0]
os.environ["PATH"] += os.pathsep + global_path #Есть такая грёбаная возможность, что умник перетащит файл ffprobe.exe хрен пойми куда


#Я думаю нельзя завершать код ошибкой, даже если файл не нашёлся, это не значит что его нет,
#Возможно он в глобальной переменой, я постарался сделать всё чтобы файл нашёлся и не выдало ошибку...
import pydub
from pydub import AudioSegment





def get_length_video(filename):
    'Узнать длину видео'
    path_ffprobe = find_file_global("ffprobe.exe")
    duration_in_ms = subprocess.run([path_ffprobe, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if(duration_in_ms == None): return 0
    return int(float(duration_in_ms.stdout)*1000)

def get_height_width(filename, width = True, height = False):
    'Узнать высоту и ширину видео'
    path_ffprobe = find_file_global("ffprobe.exe")
    result = ""
    if(width):
        result = subprocess.run([path_ffprobe, '-v', 'error', '-show_entries', 'stream=width', '-of', 'default=noprint_wrappers=1:nokey=1', filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = str(result.stdout)
        resolution = int(''.join(i for i in result if i.isdigit()))
        return resolution
    if(height):
        result = subprocess.run([path_ffprobe, '-v', 'error', '-show_entries', 'stream=height', '-of', 'default=noprint_wrappers=1:nokey=1', filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = str(result.stdout)
        resolution = int(''.join(i for i in result if i.isdigit()))
        return resolution

def get_file_in_folder(path = "E:/Video", type = ""):
    'Получить файлы из папок и подпапок'
    files = []
    for root, _, _files in os.walk(path):
        for file in _files:
            if(file.endswith(type) == True or type == ""):
                path = os.path.join(root, file).replace("\\","/")
                files.append(path)
    return files

def delete_procent_array(array, procent_delete = 50):
    'Удаляет из массива процент элементов'
    length = int(float(len(array))*(procent_delete/100))
    for index in range(length):
        array.pop()

def small_size_delete(video_array, minimum_width = 1920, minimum_height = 1080):
    'Удалить видео с маленьким размером из массива'
    index = 0
    for _ in range(len(video_array)):
        if(get_height_width(video_array[index],1,0) < minimum_width or get_height_width(video_array[index],0,1) < minimum_height):
            del video_array[index]
            continue
        index+=1

def time_calculate_array(array, video = True):
    'Получить полное время, всех видео или музыки'
    sum_time = 0
    for index in range(len(array)):
        sum_time += get_length_video(array[index])
    return sum_time

def unpack_cmd_array(cmd):
    "Распаковка двойных массивов в один целый массиве"
    _cmd = []
    for index in range(len(cmd)):
        if(isinstance(cmd[index], list)):
            for jndex in range(len(cmd[index])):
                _cmd.append(cmd[index][jndex])
        else:
            _cmd.append(cmd[index])
    return _cmd

def time_calculate(double_array, video = True):
    'Посчитать время для двойного массива'
    sum_time = 0
    for index in range(len(double_array[0])):
        if(video == True):  sum_time += double_array[11][index]
        if(video == False): sum_time += double_array[6][index]
    return sum_time





#Там идут функции, которые уже не скопировать и они не имеют связи с будующеми проектами...





#Мы сделаем такой же массив как для видео, но будет он для музыки
def create_empty_parms_sound(sound_array):
    #Сегодня 3 сентября я опять рандомно оставляю записки в коде...
    double_sound_array = []
    for i in range(7):
        double_sound_array.append([0] * len(sound_array))
    for index in range(len(sound_array)):
        audiofile = AudioSegment.from_file(sound_array[index], 'mp3')
        chunks = pydub.utils.make_chunks(audiofile,250) #Нарезать каждую четверти секунды...
        average_dBFS = 0
        max_dBFS = 0
        for _, chunk in enumerate(chunks):
            if(chunk.dBFS != float('-inf')):
                dBFS = chunk.dBFS #Уровень дцебел в эту секунду в этот миг...
                average_dBFS += dBFS
                if(dBFS < max_dBFS):
                    max_dBFS = dBFS
        max_dBFS = round(max_dBFS,1)
        average_dBFS = round(average_dBFS / len(chunks),1)
        max_allow = audiofile.max #Максимальная громкость которая была достигнута

        double_sound_array[0][index] = sound_array[index]
        double_sound_array[1][index] = max_dBFS     #max dBFS
        double_sound_array[2][index] = average_dBFS #average dBFS
        double_sound_array[3][index] = max_allow    #max allow там большие числа от 29000 до 32000 я примерно понимаю что это не не напишу...
        double_sound_array[4][index] = 0 #mult где 1 - 100%    1.5 - 150%
        double_sound_array[5][index] = 0 #add dBSF
        double_sound_array[6][index] = get_length_video(sound_array[index])/1000 #duration seconds
    return double_sound_array


#Теперь работа со звуком
def create_effect_sound(double_sound_array):
    #7166 - минимальный  E:/Relax new file/Sound/Tides - Windows of Ken.mp3 да оказывается не настолько тихий звук как кажется и его можно повысить ну как минимум только в 4 раза
    #Обычно у нас разделение на три лагеря одни до 18000 другие от 22000 и до 25000 другие совсем мажоры и от 31000 до 33000 - на самом деле эти параметры особо ничего не говорят...
    #Более гланое это средней и максимальный Дцебел, при таком мы точно можем гарантировать, что звук громкий или относительно громкий
    #mp3 = get_file_in_folder("E:/Relax new file/Sound", ".mp3")
    #print("Средний Дц - " + str(average_dBFS) + "\t - Максимальный порог - " + str(max_allow) + " - Минимальный Дц - " + str(max_dBFS) + "\t - name - " + str(mp3[index]))
    #Так что мы имеем уровень ДЦ и мы имеем самые максимальные всплески громкости, возможно мы будем нормализовывать в конце, ну скорее всего не будем...
    #Так в целом всё становится ясно чем больше ДЦ чем гроче так -20 - это тихо довольно, а -8 это очень громко так мы можем с большей увереностью уменьшить громкость
    #Ооо ксттаи я тут пюре с котлеткой ем и сразу песня та вспомнилась, ладно, забили, кстати ещё огурчики тут нарезаные есть, правда есть я их не буду, они горькие.
    #В целом я конечно не против горьких огурцов, просто по моему вкусу всё горькое такое себе... Хотя скорее всего не вкусные огурцы в целом и есть натуральные...
    #Хотя я не имею права судить так как не являюсь экспертом в области ботаники и рзделять на чёрное-белое точно нельзя...
    #На самом деле мои алгоритм довольно не универсальны Дцебел не важны как может показатся, их может слышать комп, но ты можешь не услышать, 
    #лёгкий пример если сделать звук со 500 сэмплами (это очень мало), то самый громкий скачёк звука нашему уху даже слышен не будет из-за малой частоты
    #Поэтому по хорошему я должен больше упиратся на частоту и резкие спады и подъёмы... Ноооо, идёт это всё нахер, я хер знаю как это сделать, потом как-нибудь, к тому же это не супер важная часть... И это и так рабоатет норм...
    #По поводу максимально частоты, самое ужасное если она равна около -65, да если там в -50, был кстати звук с минимум -39 - это прям в общее очень громко в любом случае, то всё очень плохо. Самая примемлема от -78 до -93 - это довольно тихая и средня громкость
    #Теперь я опишу норму отклонения тоже опишу

        #       |   Название   |    Норма       |  Критическая не норма  |     Не норма     |
        #       |   max_allow  | 28000 до 32000 |          -             |  15000 до 28000  |
        #       | average_dBFS | -16 до -21     |       0 до -10         |   -10  до -16    |
        #       |   max_dBFS   | -78 до -93     |       -20 до -50       |   -50 до -78     |
    
    sound_array = double_sound_array[0]
    for index in range(len(sound_array)):
        mult = 1.0
        add_dBFS = 0
        max_dBFS = int(double_sound_array[1][index])
        average_dBFS = int(double_sound_array[2][index])
        max_allow = double_sound_array[3][index]
        ignore_average = False
        ignore_max     = False

        #Работа с average значениями
        if(average_dBFS > -11): #Это критическая не норма
            mult -= 0.6
            ignore_average = True
        if(average_dBFS <= -11 and average_dBFS > -17 and (ignore_average==False) ): #Это не норма
            mult -= 0.3
            ignore_average = True
        if(average_dBFS <= -17 and average_dBFS > -20 and (ignore_average==False) ): #Это сойдёт
            mult -= 0.225
            ignore_average = True
        if(average_dBFS <= -20 and average_dBFS > -24 and (ignore_average==False) ): #Это сойдёт
            mult -= 0.15
            ignore_average = True
        #Работа с max значениями
        if(max_dBFS > -40): #Это критическая не норма Тут есть шанс что звук слишком мелкий, в будущющех версиях я рассматрию такой вариант
            mult -= 0.25
            ignore_average = True
        if(max_dBFS <= -40 and average_dBFS > -60 and (ignore_max==False) ): #Это не норма
            mult -= 0.1
            ignore_average = True
        if(max_dBFS <= -60 and average_dBFS > -80 and (ignore_max==False) ): #Это не норма
            mult -= 0.04
            ignore_average = True
        #Игнор по тому был ли применён эффект тихого звука
        if(ignore_average == True):
            mult -= 0.1
        if(ignore_max == True):
            mult -= 0.03
        #Странные ситуации
        if(average_dBFS <= -28): #Это критически тихий звук, но оказывается при игре дольше 8 минут звук сам по себе опускается к такой цифорке
            mult += 0.1
        if(mult < 0.1): #В каком-то смысле это самая странная ситуация при которой звук реально громкий, но компенсировать ущерб определёный нужно
            mult += 0.1 
        #Такой вид игнора... Я просто боюсь забыть поэтому сам от себя сделал защиту
        if(mult == 1):
            mult = 0
        else:
            mult -= 0.2 #Звуки в целом громкие довольно...
        double_sound_array[4][index] = round(mult,4)
        #В итоги мы получаем очень условную таблицу значений с разным мультиплаером амплитуды...
        #НООО, ЕСТЬ ОГРОМНОЕ НО, наша музыка длится слишком мало... Ну и это так себе, моя идея создать функцию которая именно будет маятся такой хернёй как тайминги...

#Применить эффекты
def apply_effect_sound(double_array_settings):
    #И так тут будет весело, так как мне нужно придумать такой алгориитм, который будет аккуратно делать видео без звука и хорошо паралелится на видеокарте...
    #Ну начнём с простого импорт mp3 на язык ffmpegа...
    len_double_arr = len(double_array_settings[0])
    string_effect = ""
    for index in range(len_double_arr):
        string_effect += "["+str(index)+":a]"
        lenght_str = len(string_effect)
        if(index == 0):
            string_effect += "afade=t=in:st=0:d=2"+","
        if(index == len_double_arr-1):
            length_video = int(get_length_video(double_array_settings[0][index])/1000)-7
            string_effect += "afade=t=out:st="+str(length_video)+":d=7"+","
        if(double_array_settings[4][index] != 0):
            volume = double_array_settings[4][index]
            string_effect += "volume=" + str(volume) + ","
        if(double_array_settings[5][index] != 0):
            volume_dBST = double_array_settings[5][index]
            string_effect += "volume=" + str(volume_dBST) + "dB" + ","
        #DEBUG if not change effect
        if(lenght_str == len(string_effect)):
            string_effect += "volume=0.97" + ","
        string_effect = string_effect[:-1]
        string_effect += "[a" + str(index) + "]; "
    for index in range(len_double_arr):
        string_effect += "[a" + str(index) + "]"
    string_effect += "concat=n=" + str(len_double_arr) + ":v=0:a=1" + "[Merged]"
    return string_effect

#Эта функция довольно важная и её суть довольно простая он просто добовляет файлы до определённого достигнутоно времени
def create_by_duration(array = [], duration_minute = 180, use_copy_file = False, append_random_file = True, folder = "E:/Video/", type_file = ".mp4"):
    #Так в чём заключается алгоритм... Начнём с самой простой ситуации, видео не 3 часа как надо, а 6 часов в таком случае надо не добовлять, а лишь удалить файлы
    lenght_array = len(array)
    time_ = time_calculate_array(array)/1000/60 # Допустим 6 часов тутачки...
    delete_time = time_-duration_minute #Мы получим 180, что значит время привышено на 180 минут
    #Нужно получить 3 часа в итоги
    if(delete_time > 0):
        while(True):
            lenght_array = len(array)
            rand_num = random.randint(0, abs(lenght_array-1))
            subst_minute = get_length_video(array[rand_num])/1000/60
            del array[rand_num]
            delete_time -= subst_minute
            if(delete_time < 0):
                break
    ##В итоги при самом плохом случаем мы получим довольно маленькие числа и допустим мы получим на выходе 1 час видео, но опять же мы конперсируем потерю следующеми иттерациями, но мы не можем гарантировать полностью не потерю материала
    ##Поэтому придётся в каждом компиляторе указывать clip самого материала из-за тупого пользователя, будь ты проклит кто 2 часовые видео суёт в мой компилятор, всё что могу сказать таким людям, это попробуй меня трахнуть, я тебя сам трахну, ублюдок, онанист чертов, будь ты проклят, иди идиот, трахать тебя и всю семью, говно собачье, жлоб вонючий, дерьмо, падла, иди сюда, мерзавец, негодяй, гад, ты — говно, жопа...
    ##Ладно, возможно мне станет лень, поэтому я просто подрежу звук под видео, а не наооборот...
    ##В лучшем случаем мы удалили 5 минут примерно, что в общее не страшно это в случае со звуком, в случае с видео 1 минуту...
    #Я предлагаю два метода... А именно копировать из исходного массива или взять из папки новые видео
    #Так вот нужно добавлять файлы из папки...
    if(append_random_file == True):
        time_ = time_calculate_array(array)/1000/60 #Допустим тут 2:20:00 нужно добавить 40 минут
        delete_time = time_-duration_minute #Тут мы получим уже -40 минут, то-есть не хватка 40 минут
        new_files = get_file_in_folder(folder, type_file)
        new_lenght_array = len(new_files)
        random.shuffle(new_files)
        while(True):
            new_lenght_array = len(new_files)
            rand_num = random.randint(0, new_lenght_array-1)
            add_minute = get_length_video(new_files[rand_num])/1000/60
            delete_time += add_minute
            array.append(new_files[rand_num])
            if(delete_time > 0):
                break
    if(use_copy_file == True):
        time_ = time_calculate_array(array)/1000/60 #Допустим тут 2:20:00 нужно добавить 40 минут
        delete_time = time_-duration_minute #Тут мы получим уже -40 минут, то-есть не хватка 40 минут
        while(True):
            new_lenght_array = len(array)
            rand_num = random.randint(0, abs(new_lenght_array-1))
            add_minute = get_length_video(array[rand_num])/1000/60
            delete_time += add_minute
            array.append(array[rand_num])
            if(delete_time > 0):
                break
    #Может что-то тут не так я не так сильно думал когда писал это буквально скопировал у самого себя...
    #Ну по идеи в худшем случае мы дадим пользователю плюс бесконечность к времени... Нууууу похеееерр, просто насрать, я не виноват, виноват пользователь...
    #В лучшем случае со звуком мы дадим плюс 5 минут
    #И с видеом 3 минуты... Кароче, сегодня у меня 2 сентября писать код не охото, поэтому делаю всё на отеъбись как и все здесь...

    #Ооо точняк вместо проверки работоспобости этого участка кода, опишу свой день, кароче сёдня в колледже было скучно, но зато весело после него...
    #Пошёл я значит из колледжа в Ашан, через все эти тратуары Шиномонтажки, Покупачки, Радежы, Офисмаги и прочи хери... 
    #Дошёл значит, захожу в Ашан через Строительный (РеарлиМерлин), потому что злые охраники не впускают... В общем зашёл, поднялся на третий этаж, в макдак, купил гамбургер себе и хэппи мил Андрею... 
    #Потом пошляся по всему Ашану, ну так бесцельно по-приколу через третий этаж походил по второму и спустился так на первый, дошёл до Ашана, (блин понял что надо было всё время писать Акварель, похер), дошёл до Ашана как магаз
    #Значит купил себе блокнот, блокнот нужен чтобы когда на парах ты сидешь и тебе запретили телефон например, злая такая преподша, то твой едиственый нормальный вариант, открыть блокнот и начать рисовать или как я писать идеи, код, так как рисовать я не умею...
    #В общем купил блокнот стоит он всего 44.99 рублей 120 листов, в общее топовый, я два купил пусть и тупой поступок ну типа вокруг были блокноты по 100-200 рублей и некоторы с меньшим количеством листов или маленьким размером...
    #Ну кароче взял я блокноты и потопал взял водичку минералку за 15.99 и взял виноградный сок, ашановский, ну просто он мне нравится и на него цена прям фиксированя ну кароче топовый сок 37.89 вроде стоил не помню...
    #Ну в целом всё пошёл на кассу спросил про блокнот касирша не поняла собираюсь ли я брать блокнот или просто цену узнать, я сказал "и то и то", на такие аргументы она просто замолчала, ну кароче я как рэпер просто уничтожил её словами...
    #Потом выхожу с кассы и чувствую в портфели чё-то мокрое... Я начинаю думать, что же произошло, потом до меня допёрло ВЫБИГАЮ ПРОСТО ИЗ АШАНА НАХЕР, ищу галазами первую лавочку, вижу лавочку бегу со всех ног, быстро кладу портфель на лавочку, я уже понимал что произошло, произошёл просто пиздец, разлился из хэппи мила СОК, просто представь что произошло, мне дали сок в стаканчики, а не в коробки...
    #Понимая в какой я жопе, просто быстро нахер, выкладываю все тетрадки, и просто охериваю так как я разлил на почти каждую тетрадку в портфели нахер, потом когда я всё выложил, я подумал вытереть весь портфель салфетками, которые в этом же хэппи миле лежали, вытерил весь портфель
    #Заметил что ещё новую футболку я испачкал как-то сзади... Ну кароче просто пиздец... Тетрадки я не планирую менять, расскажу просто историю если преподы будут орать, что повезло только тетрадки по БЖ (это ОБЖ), а тетрадка по матеши и две по информатики просто пиндец, особебенно одной там в общее конце, ну всё равно похер...
    #Да потом всгрустил после такого сок допил конечно, ну всё равно обидно... А и да прийдя ещё домой мне дали игрушку для девочек в хэппи миле... Просто сил не хватает описать моё не довольствие... Но хоть довёз гамбургер и картошку ну и игрушку пусть и для девочки...
    #А ещё смешная херь она мне прям запомнилась, иду из Ашана домой по той длиной дороги и напеваю Eminema Rap God, ну что помню прям вслух ну когда около людей проходил, конечно замолкал и про себя говорил. И кароче вспоминал ещё треки, которые я могу спеть и вспоминл такой трек, который напевается примерно так scrrrrrr pa ka ka ka scibidi pa pa and pureee boom, а дальше я забыл что дальше и тут чисто машина проезжает именно в этот момент и именно с этой песней и как раз я дослушал открывок, а именно - "Скаяя тук тук туктум пум пум", было забавно скомпенсировало мою не удачу с соком...
    #Так ну кароче всё хватит с сегодня историй из жизни возврощаем время всех видео
    time_ = time_calculate_array(array)/1000/60
    return time_







#Дальше идут функции, которые никак не использовать второй раз, если ты сможешь их использовать где-то в коде второй раз при встречи дам 10 рублей...



def create_empty_parms(videos):
    "Создаёт пустые параметры для видео"
    double_video_array = []
    for i in range(14):
        double_video_array.append([0] * len(videos))
    for index in range(len(videos)):
        double_video_array[0][index]  = videos[index]
        double_video_array[1][index]  = get_height_width(videos[index],1,0) #width
        double_video_array[2][index]  = get_height_width(videos[index],0,1) #height
        double_video_array[3][index]  = 0 #scalex
        double_video_array[4][index]  = 0 #scaley
        double_video_array[5][index]  = 0 #cropx
        double_video_array[6][index]  = 0 #cropy
        double_video_array[7][index]  = 0 #hflip
        double_video_array[8][index]  = 0 #vflip
        double_video_array[9][index]  = 0 #gamma
        double_video_array[10][index] = 0 #saturation
        double_video_array[11][index] = get_length_video(videos[index])/1000 #duration seconds
        double_video_array[12][index] = 0 #Эффект рыбий глаз
        double_video_array[13][index] = 0 #curve
    return double_video_array


#Важнее может быть следующие 5 параметров:
#4 - применить куча рандомных эффектов и из малого кол-во роликов сделать больше в 2-3 раза видео
#3 - сделать с меньшим количеством эффектов, но также растянуть хорометраж
#2 - сделать без эффектов, только склейка, но с переходами, без растягивания хорометража
#1 - отключить переходы и оставить только видео (переходы отвечает другая часть кода)
#0 - к каждому из пунктов, можно сказать чтобы было галка сделать видео с другой цвето корекции или сменить ракурс (так как авторские права)

#Создаёт эффекты, у тебя нету контроля особого, ну зато она без твоего спроса будет клипать видео и ничего у тебя не спрашивать
def create_effect_video(double_video_array, width = 1920, height = 1080, effects5 = True, effects4 = True, effects3 = True, effects2 = True, effects1 = True, delete_small_video = True):
    if(delete_small_video == 1):
        small_size_delete(double_video_array[0],1280,720) #Удаляем видео по минимально не красивому разрешению... Если пользователь захочет зайдёт в исходный код разберётся со всем перепишит и может менять разрешение...
    len_double_vid_arr = len(double_video_array[0])
    two_double_video_array = deepcopy(double_video_array)
    three_double_video_array = deepcopy(double_video_array)
    four_double_video_array = deepcopy(double_video_array)
    len_two_double_vid_arr = len(two_double_video_array[0])
    len_three_double_vid_arr = len(three_double_video_array[0])
    len_four_double_vid_arr = len(four_double_video_array[0])
    #effects1
    #effects2
    for index in range(len_double_vid_arr):
        if( double_video_array[1][index] != width):
            double_video_array[3][index] =  width
        if( double_video_array[2][index] != height):    
            double_video_array[4][index] =  height
    #effects3
    for index in range(len_two_double_vid_arr):
        two_double_video_array[7][index] = 1    #hflip
        two_double_video_array[9][index] = 1.3  #gamma
        two_double_video_array[10][index] = 0.7 #saturation
        if(two_double_video_array[1][index] != width):
            sum_width = two_double_video_array[1][index]-width #2560 - 1980 = 580
            if(two_double_video_array[1][index] > width): 
                two_double_video_array[5][index] = width+sum_width/4 #crop half-half
            two_double_video_array[3][index] = width #scale full
            continue
        if(two_double_video_array[2][index] != height):
            sum_height = two_double_video_array[2][index]-height #1440 - 1080 = 360
            if(two_double_video_array[2][index] > height):
                two_double_video_array[6][index] = height+sum_width/4 #crop half-half
            two_double_video_array[4][index] = height #scale full
            continue
        two_double_video_array[5][index] = width-120 #crop half
        two_double_video_array[3][index] = width #scale full
    #effects4
    for index in range(len_double_vid_arr):
        three_double_video_array[12][index] = 1 #random
        if(three_double_video_array[1][index] != width):
            three_double_video_array[3][index] = width   #scale full
        if(three_double_video_array[2][index] != height):
            three_double_video_array[4][index] = height #scale full
    #effects5
    for index in range(len_four_double_vid_arr):
        four_double_video_array[7][index] = 1 #hflip
        if(four_double_video_array[1][index] != width):
            four_double_video_array[13][index] = 1 #random
            four_double_video_array[3][index] = width #scale full
            continue
        if(four_double_video_array[2][index] != height):
            four_double_video_array[13][index] = 1 #random
            four_double_video_array[4][index] = height #scale full
            continue
        #Но если иначе всё то мы делаем такой трюк кропнуть чу-чуть и заскейлить, это не особо заметно
        four_double_video_array[5][index] = width-60 #crop half
        four_double_video_array[3][index] = width #scale full
    #Apply effects
    for index in range(len(two_double_video_array)):
        for jndex in range(len_two_double_vid_arr):
            if(effects1 == True):
                pass #Пока тут ничего нету...
            if(effects2 == True):
                pass #Пока тут ничего нету...
            if(effects3 == True):
                double_video_array[index].append(two_double_video_array[index][jndex])
            if(effects4 == True or effects5 == True):
                rand = random.randint(0,len_two_double_vid_arr-1)
                if(random.randint(0,5) == 1):
                    double_video_array[index].append(three_double_video_array[index][rand]) #Вероятность попадения 1/6 как револьвер перед головой с одним патроном
                else:
                    double_video_array[index].append(four_double_video_array[index][rand])
        #10 + 10 + 10 = 30 minute
        #К сожалению пришлось принять ислам и сказать, что 20 минут тоже норм, но 30 минут можно выбрать...



#Кароче, это херня пытается быть умной и она применяет все эффект и возврощает строку для использование ffmpegom
def apply_effect_video(double_video_array, fade_start = True, fade_end = True, use_transition = True):
    len_double_vid_arr = len(double_video_array[0])
    string_effect = ""
    array_not_use = []
    for index in range(len_double_vid_arr):
        old_lenght_str = len(string_effect)
        string_effect += "["+str(index)+":v]"
        lenght_str = len(string_effect)
        if(index == 0 and fade_start == True):
            string_effect += "fade=in:0:70"+","
        if(index == len_double_vid_arr-1 and fade_end == True):
            length_video = int(get_length_video(double_video_array[0][index])/1000)-5
            string_effect += "fade=type=out:duration=3:start_time="+str(length_video)+","
        if(double_video_array[5][index] != 0):
            if(double_video_array[6][index] != 0):
                x = str(double_video_array[5][index])
                y = str(double_video_array[6][index])
                string_effect += "crop=" + x + ":" + y + ","
        if(double_video_array[3][index] != 0):
            if(double_video_array[4][index] != 0):
                x = str(double_video_array[3][index])
                y = str(double_video_array[4][index])
                string_effect += "scale=" + x + ":" + y + ","
        if(double_video_array[7][index] != 0):
            string_effect += "hflip" + ","
        if(double_video_array[8][index] != 0):
            string_effect += "vflip" + ","
        if(double_video_array[9][index] != 0):
            gamma = float(double_video_array[9][index])
            string_effect += "eq=gamma=" + str(gamma) + ","
        if(double_video_array[10][index] != 0):
            saturation = float(double_video_array[10][index])
            string_effect += "eq=saturation=" + str(saturation) + ","
        if(double_video_array[12][index] != 0):
            w = str(double_video_array[1][index])
            h = str(double_video_array[2][index])
            #Прикольные фильтры:
            # v360=e:fisheye:v_fov=180:h_fov=180:yaw=-90:w=1024:h=1024 #Это прикольный фильтр
            #"v360=e:fisheye:v_fov=180:h_fov=180:yaw=0:w="+w+":h="+h+"" + ","
            #=input=equirect:ih_fov=180:iv_fov=180:output=flat
            if(random.randint(0,6) == 3):
                string_effect += "v360=input=equirect:h_fov=180:iv_fov=180:yaw=0:w="+w+":h="+h+","
            else:
                string_effect += "curves=preset=vintage" + ","
        #DEBUG if not change effect
        if(lenght_str == len(string_effect)): #Допустим первая длина 10 и конечная длина 10 значит, надо завершить цикл и вписать индекс
            string_effect = string_effect[:-(lenght_str-old_lenght_str)]
            array_not_use.append(index+1) #Может это решит мою проблему... ПИЗДЕЦ
            continue
        string_effect = string_effect[:-1]
        string_effect += "[v" + str(index) + "];"
        array_not_use.append(0)
    #[v1]fade=d=1:t=in:alpha=1,setpts = PTS-STARTPTS + 1 / TB[f0];
	#[v2]fade=d=1:t=in:alpha=1,setpts = PTS-STARTPTS + 1 / TB[f1];
	#[v0][f0]overlay[bg1];
	#[bg1][f1]overlay[Merged]
    #TB - 1000 ms
    #Тут для переходов
    ##'v1 - 1:v' 'если он находится в array_not_use'
    #Переходы через contact - только склеивать видео
    string_not_effect = ""
    if(use_transition == False):
        string_not_effect = string_effect
        for index in range(len_double_vid_arr):
            if(array_not_use[index] != 0):
                string_not_effect += "[v" + str(index) + "]"
            else:
                string_not_effect += "[" + str(index) + ":v]"
        string_not_effect += "concat=n=" + str(len_double_vid_arr) + ":v=1:a=0" + "[Merged]"
    #Переходы через overlay - через перекрёстный наплыв
    offset = 0
    xfade_duration = 1
    for index in range(len_double_vid_arr):
        previous_xfade_offset = offset
        xfade_duration = xfade_duration
        if(index == 0): #ПИЗДЕЦ, ВОТ ТУТ Я ДОБАВИЛ IF И ELSE 
            if(array_not_use[index] != 0): #Я это добавил
                string_effect += "[0:v]setpts=PTS-STARTPTS[f0];" #Я это добавил
            else: #Я это добавил
                string_effect += "[v0]setpts=PTS-STARTPTS[f0];" #Я это добавил но это не помогло
            input_duration = int(get_length_video(double_video_array[0][index])/1000)
            offset = input_duration-xfade_duration+previous_xfade_offset
            continue
        if(array_not_use[index] != 0):
            string_effect += "["+str(index)+":v]"
        else:
            string_effect += "[v"+str(index)+"]"
        string_effect += "fade=d=1:t=in:alpha=1,setpts=PTS-STARTPTS+" + str(offset) + "/TB[f"+str(index)+"];"
        input_duration = int(get_length_video(double_video_array[0][index])/1000)
        offset = input_duration-xfade_duration+previous_xfade_offset
    offset = 0
    for index in range(len_double_vid_arr-1):
        previous_xfade_offset = offset
        xfade_duration = xfade_duration
        input_duration = int(get_length_video(double_video_array[0][index])/1000)
        offset = input_duration-xfade_duration+previous_xfade_offset
        overlay_p = "=enable='between(t,"+str(offset-2)+","+str(offset+2)+")'"
        if(index == 0):
            string_effect += "[f0][f1]overlay[o1];"
            continue 
        if(index == len_double_vid_arr-2):
            string_effect += "[o"+str(index)+"][f"+str(index+1)+"]overlay[Merged]"
            continue
        string_effect += "[o"+str(index)+"][f"+str(index+1)+"]overlay[o"+str(index+1)+"];"
        #Чтобы сделать zoom [0:v]zoompan=z='pzoom-0.1':d=1
        #[0:v]setpts=PTS-STARTPTS[v0];
        #[1:v]fade=in:st=0:d=1:alpha=1,setpts=PTS-STARTPTS+(4/TB)[v1];
        #[2:v]fade=in:st=0:d=1:alpha=1,setpts=PTS-STARTPTS+(8/TB)[v2];
        #[3:v]fade=in:st=0:d=1:alpha=1,setpts=PTS-STARTPTS+(12/TB)[v3];
        #[4:v]fade=in:st=0:d=1:alpha=1,setpts=PTS-STARTPTS+(16/TB)[v4];
        #[v0][v1]overlay[v12]; [v12][v2]overlay[v123]; [v123][v3]overlay[v1234]; [v1234][v4]overlay,format=yuv420p[v]
    #Попытка сделать из xfade, но минусы довольно сильные... Поэтому нахер надо
    #offset = 0
    #for index in range(len_double_vid_arr-1):
    #    input_duration = int(get_length_video(double_video_array[0][index])/1000)
    #    previous_xfade_offset = offset
    #    xfade_duration = 1
    #    offset = int(input_duration + previous_xfade_offset - xfade_duration)
    #    if(len_double_vid_arr == 2):
    #        string_effect += "[v"+str(index)+"][v"+str(index+1)+"]xfade=transition=fade:duration="+str(xfade_duration)+":offset="+str(offset)+"[Merged]"
    #        continue
    #    if(index == 0):
    #        string_effect += "[v"+str(index)+"][v"+str(index+1)+"]xfade=transition=fade:duration="+str(xfade_duration)+":offset="+str(offset)+"[vfade"+str(index+1)+"];"
    #        continue
    #    if(index == len_double_vid_arr-2):
    #        string_effect += "[vfade"+str(index)+"][v"+str(index+1)+"]xfade=transition=fade:duration="+str(xfade_duration)+":offset="+str(offset)+"[Merged]"
    #        continue
    #    string_effect += "[vfade"+str(index)+"][v"+str(index+1)+"]xfade=transition=fade:duration="+str(xfade_duration)+":offset="+str(offset)+"[vfade"+str(index+1)+"];"
    #xfade=transition=wiperight:duration=2:offset=0,format=yuv420p[over];
    if(use_transition == False):
        string_effect = string_not_effect
    return string_effect
    


#start_GPU_decoder - сделан для debuga и возможно будет включен по умолачнию, если коротко это галка включает все риски в самом начале просчёта и уменьшает их под конец
def make_string_filename(setting_array, use_nvidea = False, use_amd = False, count_GPU_decoder = 8, start_GPU_decoder = True):
    'При использование разных видеокарт он настраивает им cuvid либо для amd автоматический режим, так как я не имею карт от amd'
    filename_str = []
    #Тут важно сделать так чтобы, cuvid был в конце
    length_array = len(setting_array[0]) #24 - получаем 18
    for index in range(len(setting_array[0])):
        #filename_str.append('-hwaccel_output_format')
        #filename_str.append('cuda') # Это оказывается для быстрого применение эффектов на cuda https://forums.developer.nvidia.com/t/how-to-use-ffmpeg-overlay-cuda-filter-to-create-sbs-video/147495
        if(index >= length_array-count_GPU_decoder and start_GPU_decoder == False or index <= count_GPU_decoder and start_GPU_decoder == True): #Я выжал все возможные соки, которые мог так как cuvid работает не больше 16 раз в поток, а чтобы не лагала я пока выставил меньше, это не создаёт мне проблему и моему компу... Плюс обязательно они должны работать вместе иначе жопа компу...
            if(use_nvidea == True):
                filename_str.append('-hwaccel')
                filename_str.append('auto')
                filename_str.append('-c:v')
                filename_str.append('h264_cuvid')
            if(use_amd == True):
                filename_str.append('-hwaccel')
                filename_str.append('auto')
        filename_str.append("-i")
        filename_str.append(setting_array[0][index])
    return filename_str


































#Ооо боже, как же я уже замучился, да это та самая функция нажми на кнопку и будет тебе видео, а карсивое или нет, то скорее нет, ну ты всё равно схаваешь...
def makeVideoByFfmpeg(folder_video, folder_sound, output_folder = "final-render", cache_folder = "cache_render"):
    directory_video = folder_video
    directory_sound = folder_sound
    if(directory_sound == "" or directory_video == ""):
        print("Видео или звука нету...")
        exit(12)
    video_array = get_file_in_folder(directory_video, ".mp4")
    sound_array = get_file_in_folder(directory_sound, ".mp3")
    random.shuffle(video_array)
    random.shuffle(sound_array)


    #Settings:
    #HD и выше
    nvidea = True #СУПЕР ВАЖНАЯ НАСТРОЙКА
    amd = False
    delete_start_end_fade = False #Отключить начальные переходы если True
    individual_video = random.randint(0, 1) #Пресет видео стноавится более разнобразное при значение True, 
    #но не самое лучшее так как записывает в два раза больше кэша и напрягает больше CPU и RAW, по скорости выходит примерно одно и тоже, лишь разница в результате
    

    #Разрешение конченого видео
    arr_xy = [[1920, 1080], [2560, 1440], [3840, 2160]]
    index_resolution = 0 #1920x1080
    res_x = arr_xy[index_resolution][0]
    res_y = arr_xy[index_resolution][1]

    #Оптимизация
    bitrate = "6.2M"
    bufsize = "1M"
    fps = "30"
    cut_array = 10 #Разрез массива, важный парметр для скорости
    #4K и выше
    if(res_x >= 3840 and res_y >= 2160):
        bitrate = "16.2M"
        bufsize = "2M"
        fps = "24"
        cut_array = 16 #Для 4K мы сделаем больше фрагментов, в два раза, да пусть и переходы будут более стыкованные, но пофиг...

    minutes_duration_minute = 16 #Это стандартное требование 
    Use_not_standart_effect = True #Это параметр говорит использовать ли тонировку или цветокроекцию если True
    if(individual_video == 1):
        minutes_duration_minute = 28 #Это в два раза более индивидуальней...
        Use_not_standart_effect = False
    else:
        minutes_duration_minute = 16 
        Use_not_standart_effect = True


    #Компинсация
    if(minutes_duration_minute > 24):
        if(res_x >= 3840 and res_y >= 2160):
            cut_array *= 1.6
        else:
            cut_array *= 1.2
        cut_array = int(round(cut_array))

    ###########################################################################
    ###################################ERROR###################################
    ###########################################################################
    use_transition = False #ПЕРЕХОДЫ С НИМИ ПРОБЛЕМЫ ОГРОМНЫЕ, ИСПРАВЬ ПРОШУ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #ЕСЛИ use_transition = True , то выдаёт ошибку
    ###########################################################################
    ###################################ERROR###################################
    ###########################################################################


    








    


    if not os.path.exists(output_folder): os.makedirs(output_folder) #Создать если нету YES
    if not os.path.exists(cache_folder): os.makedirs(cache_folder) #Создать если нету YES
    final_output = ""
    if(1 == 1): #Создаю область видемости.. Чтобы index не расспростанился дальше
        index = 0
        while(True):
            index+=1
            if( os.path.exists(output_folder+'/myfile_final'+str(index)+'.mp4') == False):
                final_output = output_folder+'/myfile_final'+str(index)+'.mp4' #Создать с новым следующем индексом YES
                break
    output_sound = cache_folder+'/temp_cache_sound.mp3' #Перезапись или создание YES
    video_list_task = cache_folder+'/temp_cache_video.txt' #Перезапись или создание
    start_time = time.time()
    print("Рендер уже запущен, вот характеристики видео:")
    print("Разрешение: " + str(res_x) + "x" + str(res_y))
    print("Кодирование     - VBR")
    print("Видео битрейт   - " + str(bitrate[:-1]))
    print("Видео кодек     - h264")
    print("Название кодека - libx264")
    print("Аудио битрейт   - 320")
    print("Аудио кодек     - AAC")
    print("Файлов mp4 - " + str(len(video_array)) + "\nФайлов mp3 - " + str(len(sound_array)))
    print("Можете ничего не делать, видео создатся и сразу же окажется у вас в папки с программой, в случае ошибок, рендер завершится, оставив кэш память")
    

    #Алгоритм
    if(1==1):
        #mp4
        duration_video = create_by_duration(video_array, duration_minute = minutes_duration_minute, use_copy_file = True, append_random_file = False, folder = directory_video, type_file = ".mp4") #Всё работает хоть с пустым, хоть с полным, хоть с переполненым массивам норм функция кароче...
        random.shuffle(video_array)
        #duration_video = create_by_duration(video_array, duration_minute = 60, use_copy_file = True, append_random_file = False, folder = directory_video, type_file = ".mp4")
        #print(duration_video) #Мы получаем 60 минутное видео

        #Так вот я придумал гениальный алгоритм распаралеливания, а что если мы будем действовать по алгоритму разделяй и властуй?
        #Это один из самых передовых алгоритмов, он является выйграшным практически со 100 процентным шансом, суть алгоритма такова
        #Буду придерживатся как сортировка merge, разделить куча кусков на элементарные куски и сложить их в единый ролик!
        #Почему это сработает 100%. И мы получим прирост в скорости? Во-первых, cuvid работает только над 16 потоками
        #Дальше его ломает и всё что остаётся переключится на другое, ну другое типа cuda не даст такой производительности поэтому мы теряем -5 фпс
        #Дальше оперативка будет под 80-90% и её почти будет не хватать, а при такой загрузки опреативки ну и в целом, что надо всё это держать даёт ещё -10 фпс
        #По мои наблюдениям видеокарта очень круто стартует набирает скорость, вспомни игры, до пиковой скорости, ничего не остаётся кроме как сбрасывать скорость... -1 фпс
        #Выходит -16 фпс, но на самом деле -24 фпс и остаётся всего 4 фпс, да всё равно круто и так можно жить, но зачем если я могу сохранить на каждом просчёте 24 кадров стабильно?
        
        
        
        double_split_array = numpy.array_split(video_array.copy(), cut_array) #Режим массив на несколько частей...
        #Первое затухание
        first_array_add = numpy.array([video_array[int(len(video_array)-1)], video_array[int(len(video_array)/2)], 
                           video_array[int(len(video_array)/3)], video_array[int(len(video_array)/4)]])
        #Конечное затухание
        second_array_add = numpy.array([video_array[int(len(video_array)/5)], video_array[int(len(video_array)/6)],
                           video_array[int(len(video_array)/7)], video_array[int(len(video_array)/8)]])

        double_split_array.insert(0, first_array_add) #Добавить начало к видео
        double_split_array.append(second_array_add) #Добавить конец к видео
        cut_array+=2
        video_array.clear()
        #Допустим у нас 20 минут довольно всё логично, но нужно дать пользователю указывать в процентах индивидуальность контента...
        print(double_split_array)
        array_temp_name = [] #Тут будут хранится временые файлы которые потом превратятся в видео
        for index in range(int(cut_array)):
            fade_start = (index==0) #Применять затухание в самом начале...
            fade_end = (index==(cut_array-1)) #Применять затухание в конце...
            video_array = double_split_array[index]
            print(video_array)
            double_video_array = create_empty_parms(video_array)
            #У нас 20 минут
            if(fade_start == 0 and fade_end == 0):
                #Чё это за два True такие говнокодные? Да признаю лучшее не придумал массив перемешался и как бы из грязного белья искать чистое не получится
                #Поэтому я просто предложил пользователю убрать тройное копирование... И оставить двойное копирование, сохранив ценность контента, правда и тут есть проблемы...
                #Проблемы которые я решил примерно через недельку)) Да проблем нету теперь я предложу пользователю отключить переходы и отключить двойное копирование видео, если тот так хочет
                create_effect_video(double_video_array, res_x, res_y, False, (Use_not_standart_effect==True), (Use_not_standart_effect==False), False, False) #Создание эффектов к видео
            else:
                create_effect_video(double_video_array, res_x, res_y, False, False, False, True, False) #Создание эффектов к видео без копирования самого себя
            #Так я решил один баг в начале, ура!)
            #У нас 30+30 = 60
            #Перевод в строки
            video_filename_str = make_string_filename(double_video_array) #Имена всех файлов на ffmpegoвском языке...
            #Не особо красиво может потом в функцию заверну
            jndex = 0
            while(True):
                if((os.path.exists(cache_folder+'/myfile' + str(jndex) + '.mp4')) == False):
                    output_video = cache_folder+'/myfile' + str(jndex) + '.mp4' #Здесь надо бы добавить папку одну...
                    break
                jndex+=1
            #Не особо красиво может потом в функцию заверну
            video_effect_str = apply_effect_video(double_video_array, fade_start, fade_end, use_transition = True) #Применение эффектов к видео
            print(time_calculate(double_video_array))
            preset1_4k_NVIDIA = []
            preset2_4k_NVIDIA = []
            preset1_4k_CPU = []
            preset2_4k_CPU = []
            count_decoder = 10 #Нельзя создавать 16 потоков и почему-то именно на 16 потоке ошибка из-за ограничения, поэтому создаём 15, но так как мне религия не позволяет создаём 14 потоков, но в самом начале видео уже использует 4 потока и сразу переключается на второй поток, в итоги получаем что 10 + 4 = 14 и приходится использовать 10 потоков
            if(res_x >= 3840):
                count_decoder = 8 #Вынужденая мера из-за вылетов при 4K
                if(res_y >= 2160):
                    preset1_4k_NVIDIA = ['-preset:v', 'p2'] #-tune -level, но один слишком плох, другой не понятно... -qp - это добавление кубического шума, но в пользу скорости
                    preset2_4k_NVIDIA = ['-spatial_aq:v', '1', '-aq-strength:v', '15']
                    preset1_4k_CPU = ['-preset:v','faster']
                    preset2_4k_CPU = ['-crf:v','26'] #23 - standart #-q чем выше тем хуже
            cmd = ""
            #'-ssim', '1', '-tune', 'ssim',
            if(nvidea == True): #NVIDIA
                video_filename_str = make_string_filename(double_video_array, True, False, count_decoder) #Имена всех файлов на ffmpegoвском языке...
                #cmd = [path_ffmpeg, '-y', '-hide_banner', video_filename_str, '-an', #sound_filename_str,
                #    '-b:v', bitrate, '-bufsize:v', bufsize, '-rc:v', 'cbr', preset1_4k_NVIDIA,
                #    '-filter_complex', video_effect_str, '-map', '[Merged]', '-r', str(fps), preset2_4k_NVIDIA,
                #    output_video]


                cmd = [path_ffmpeg, '-y', '-hide_banner', video_filename_str, '-an', #sound_filename_str,
                    '-c:v', 'libx264', '-b:v', bitrate, '-threads', '1', preset1_4k_CPU,  #'-profile:v', 'main'
                    '-filter_complex', video_effect_str, '-map', '[Merged]', '-r', str(fps), preset2_4k_CPU,
                    output_video]

            if(amd == True): #Amd без рисков сделано, шанс работы 70%, думаю более чем достаточно
                video_filename_str = make_string_filename(double_video_array, False, True, count_decoder) #Имена всех файлов на ffmpegoвском языке...
                cmd = [path_ffmpeg, '-y', '-hide_banner', video_filename_str, '-an', #sound_filename_str,
                    '-c:v', 'h264_amf', '-b:v', bitrate, '-rc:v', 'cbr',
                    '-filter_complex', video_effect_str, '-map', '[Merged]', '-r', str(fps),
                    output_video]
            if(False == amd and nvidea == False): #CPU #'-bufsize', '6M', '-maxrate', '4.5M', 
                video_filename_str = make_string_filename(double_video_array, False, False) #Имена всех файлов на ffmpegoвском языке...
                cmd = [path_ffmpeg,  '-y', '-hide_banner', video_filename_str, '-an', #sound_filename_str,
                    '-c:v', 'libx264', '-b:v', bitrate, '-threads', '1', preset1_4k_CPU,  #'-profile:v', 'main'
                    '-filter_complex', video_effect_str, '-map', '[Merged]', '-r', str(fps), preset2_4k_CPU,
                    output_video] #'-bufsize', '6M', '-maxrate', '4.5M', #эти параметры вроде прикольные, но вроде нет...
            cmd = unpack_cmd_array(cmd)
            print(cmd) #Просто по приколу узнаем, что там хранится
            p = subprocess.Popen(cmd, shell=False)
            time.sleep(0.5)
            p.wait()
            array_temp_name.append(output_video)
        video_filename_str = make_string_filename(array_temp_name)
    #Подсчёт для 3 часового ролика нужно любыми методами сделать час как минимум
    #На 3 минуты = 3 минуты - это почти сто процентов в среднем
    #В итоги мы получаем 4 часа на весь ролик если повезёт, может быть и статистика хуже, типа 5 часов, если эффекты сложные... Это ровно так же как и премьер про и даже хуже с плохим шансом... Но туз в рукове, шах и мат, девочки...
    #А что если мы из часа ролики начнём его дубрировать, то тогда мы получим около - 2 часов (уже 1 час 20 минут), и как в том меме -  чтооооо? Да вот именно премьер про сосёт у меня что? Привильно полную загрузка cuda и GPU у nvidea...
    #Такой алгоритм жертвуя индивидуальности видео может отрендерить и за 10 минут и даже ещё меньше, если я включу полную аксиллирацию... Ну как говорится это уже совсем другая история

    #Теперь остался последний шаг, просто нахер сгенерить допустим 3 часа видео из массива array_temp_name, и создать временый блокнот с записями...

    #5 сентября, я уже почти дописал всё... Конечно код это жесть... Хотя я всё могу контролировать и помню почти всё что тут написанно...
    #Комменты я не удалялю так как хочу понять как я пришёл к такому решению чтобы переписать в будующем, блин конечно я большие надежды возлагаю
    #На эту херь так как я понимаю, что это штука будет прям жесть, можно массово делать мемные видосы, либо делать релакс-видео, либо соединять куча фрагментов для любой цели...
    #Самое печальное, что идею никому не офишировал и писал неделю в полной тишине о проекте, даже при том что это самый крупный проект из того, что я делал (на тот момент)...

    #mp3
    delete_procent_array(sound_array, 60)
    random.shuffle(sound_array)
    duration_sound = create_by_duration(sound_array, duration_minute = 60, use_copy_file = True, append_random_file = False, folder = directory_sound, type_file = ".mp3") #Всё работает хоть с пустым, хоть с полным, хоть с переполненым массивам норм функция кароче...
    #Чтобы предугадать более точнее длину видео со звуком... Можно попробывать расчитать длину от звука:
    #Затем не достающий фрагмен допустим 6 минут добавить по возможности видеом...
    all_time_sounds = 0
    for index in range(len(sound_array)):
        all_time_sounds += get_length_video(sound_array[index])/1000/60 #duration minuts
    all_time_videos = 0
    array_temp_name_len = len(array_temp_name)
    count_array_file = 0
    filename_in_temp_str = ""
    while(True):
        #file 'C:/Users/User/source/repos/Python_ffmpeg_setup_part_2/Python_ffmpeg_setup_part_2/cache-render/myfile0.mp4'
        if(all_time_videos > (all_time_sounds-(get_length_video(array_temp_name[array_temp_name_len-1])/1000)/60) ): #170>180 #Тут ошибка
            filename_in_temp_str += "file '" + array_temp_name[array_temp_name_len-1] + "'\n"
            all_time_videos += (get_length_video(array_temp_name[array_temp_name_len-1])/1000)/60
            break
        if(count_array_file != 0):
            rand = random.randint(1, array_temp_name_len-1)
            filename_in_temp_str += "file '" + array_temp_name[rand] + "'\n"
            all_time_videos += (get_length_video(array_temp_name[rand])/1000)/60
        if(count_array_file == 0):
            filename_in_temp_str += "file '" + array_temp_name[0] + "'\n"
            all_time_videos += (get_length_video(array_temp_name[0])/1000)/60
        count_array_file+=1

    #Так ну уже лучшее самая не удачная ситуация, может быть 17 минут нету музыки... И тут беда прям...
    #all_time_videos
    #all_time_sounds
    #Видео длится 179 , звук на 178 получаем 181 так ну это ещё врде бы повезло... Ну может быть вот такое:
    #Видео длится 189
    #Звук  длится 180 
    video_t = all_time_videos-all_time_sounds #Типа 9 получаем
    #9 минут тишины... Что можно сделать? Я вижу только один выход добавить из той папки со звуком звук который по длине подходит в рандомное место...
    sound_array_again = get_file_in_folder(directory_sound, ".mp3")
    #Проблема осталась где-то туточки...
    for jindex in range(len(sound_array_again)-1):
        sound_t = get_length_video(sound_array_again[jindex])/1000/60
        if(sound_t < video_t):
            sound_tt = sound_array_again[jindex]
            sound_array.insert( random.randint(1, len(sound_array)-3), sound_tt)
            video_t -= sound_t

    #Воооу, теперь мы можем уже получить примерно до 5 минут при самом не удачном моменте, ну как я люблю говорить виноват во всём пользователь... Так как мало звука = плохой результат
    #Так-то если у него полно музыки от 1 минуты, до 18 минут я смогу ему сделать и всё до 2 минут, но так как пользователь даун, могу только к врачу выписку сделать...
    double_sound_array = create_empty_parms_sound(sound_array)
    create_effect_sound(double_sound_array) #Создание эффектов к звуку
    sound_filename_str = make_string_filename(double_sound_array) #Имена всех файлов на ffmpegoвском языке...
    sound_effect_str = apply_effect_sound(double_sound_array) #Применение эффектов к звукам

    cmd = [path_ffmpeg, '-hide_banner', '-y', sound_filename_str, 
        '-filter_complex', sound_effect_str, '-map', '[Merged]', '-b:a', '320k', #'-t', '00:00:03',
        output_sound]
    cmd = unpack_cmd_array(cmd)
    print(cmd) #Просто по приколу узнаем, что там хранится
    p = subprocess.Popen(cmd, shell=False)
    p.wait()
    f = open(video_list_task, 'w')
    f.write(filename_in_temp_str)
    f.close()

    cmd = [path_ffmpeg, '-y', '-safe', '0', '-f', 'concat', '-i', video_list_task, '-i', output_sound, '-c', 'copy', final_output]
    print(cmd) #Просто по приколу узнаем, что там хранится важна инфа только мне...
    p = subprocess.Popen(cmd, shell=False)
    p.wait()

    print("--- %s seconds ---" % (time.time() - start_time)) #Принтит время выполнение программы
    return final_output #Возврощаем путь к отрендереному файлу






#-map 0:v:0 -map 1:a:0  - замена из звука mp4 на mp3...
#'-profile:v','baseline'
#subprocess.call('ffmpeg -hide_banner -hwaccel cuda -i' + name + '-c:a copy -ac 1 -c:v h264_nvenc -preset hq -movflags faststart -qp 30 "E:/Video/4534543.mp4"', shell=True)
#Понять как работает GPU и аппаратное ускорение CUDA - https://superuser.com/questions/1296374/best-settings-for-ffmpeg-with-nvenc
# -level:v 4.1 -rc:v ll_2pass_quality -rc-lookahead:v 32 -temporal-aq:v 1 -weighted_pred:v 1 -coder:v cabac \
#preset -faster
#'-hide_banner','-h'
#[v0][v1]xfade=transition=wiperight:duration=2:offset=0,format=yuv420p[over];
#format=yuv420p
#'-hwaccel', 'nvdec', '-hwaccel_output_format', 'auto'  - Есть прирост к скорости, но примерно глобально на 0.2 в реальности на 0.06 , но пишет ошибку так что забью
#vdpau
#vaapi
#drm
#opencl
#cuvid
#cuda  - 21.8, 21.9, 22.0
#nvdec - 21.8, 22.2, 22.1, 22.1
#auto  - 22.0
#nvenc
#-vcodec
#-codec:v
#-c:v #По идеи он самый норм про другие можно забыть
#-init_hw_device cuda=cuda -filter_hw_device cuda -hwaccel cuvid
#"-an" # удалить аудио дорожку, но есть недостаток он всё равно её просчитывает походу... Можно прям в начале запихнуть и норм будет https://www.linux.org.ru/forum/multimedia/5982257
#'-map 0' # Выбрать все потоки
#'-map -0:a' #Удалить их
#cmd = [path_ffmpeg, '-y' ,"-i", "E:/Video/1920x1080/1135623476.mp4", "-i", "E:/Video/1920x1080/1993439236.mp4", "-filter_complex", "xfade=transition=dissolve:duration=3:offset=3", output]
#cmd = 'ffmpeg -filters'
#По поводу GPU у меня сейчас колеблится от 12 до 25 процентов GPU в среднем можно сказать, что держится около 22 процентах
#Это довольно хороший показатель так как при самом обычном соединение видео я получу максимум 60 процентов загрузки GPU, но надо понимать GPU
#Вычисляет только малую часть, основные просчёт идёт на CPU, но на самом деле прирост в скорости есть и очень даже большой.
#Охх ты бы знал чего мне это всё стоило, да теперь я могу даже на Amd сделать просчёт, так что всё будет на много круче... 
#Дальше поддержка Amd пока, всё что я нарыл это: h264_vaapi 

#Так под конец, хочу всё описать, все потоки сразу опасно, поэтому распаралеленивание даёт + к безопасности
#Потом это с точки зрения скорости лучшее так как cuvid работает только при максимум 16 эффектов, что является огромным минусом... Ведь cuvid - это примерно + 10 фпс, и загрузка на GPU + 10%
#Считать всё сразу реально медленно, да скорее по многим причинам медленно
#Нельзя использовать гипербыстрый рендер при таком и хитрить


#Нужно упростить алгоритмы склеивание видео, чтобы рендер был быстрее... 

#13 fps - max CPU
#18 fps - max CPU + GPU, NVENC
#20 fps - max убрано не много эффектов CPU + GPU, NVENC
#24 fps - max CPU + GPU, CUVID, CUDA, NVENC
#76 fps - max распаралелно на 6 потоков CPU + GPU, CUVID, CUDA, NVENC
#41 fps - max из-за ошибок с nvenc, я отключил его, к сожалению, выдавыла ошибку из-за того что не установлены новые драйверы, что критично если пользователь окажется в такой ситуации
#30 fps - max переход полностью на CPU, да выходит довольно плочебный результат, максимум что могу включить это cuvid, но во-первых, вдруг чёт случится, плюс приходится переключатся с CPU на GPU , а прошлые попытки были заточены практически only GPU, в общем очень печально плакать хочется



#Всё это становится не важным, так как ролики уже создаются в 4K, поэтому у нас тут супер жёсткая ситация с оптимизации
#4K видео 30 fps
#6.2 fps - распаралелно на 6 потоков CPU + GPU, CUVID, CUDA, NVENC
#9.5 fps - распаралелно на 10 потоков CPU + GPU, CUVID, CUDA, NVENC
#3.6 fps - переход только на CPU
#Да мы потеряли фпс в 8 раз, но мы должны понимать из-за чего, а именно повышение размера видео в 2 раза, повышение битрейта в 2 раза, плюс у меня CUVID опять помер и пришлось уменьшить его до 8... Ну и логичней, что я стал оперировать с видео 4K обрабатывать на них эффекты класть, что тоже делает просчёт сложнее
#Рендер был 3 часа, хоть и с 1920 на 1080 всего 1 час...
#В целом идея есть что с этим делать они должны спасти нас довольно сильно


#Чтобы найти возможные не правильно работающие места в коде достаточно нажать Ctrl+F и найти слово "ПИЗДЕЦ"


#Справка по оптимизации:
#Сейчас наш fps упал до маленького числа, что мы можем сделать?
#1. Постаратся cuvid использовать под конец видео и более правильно, потому что в самом начале просчёт смешной и простой... А потом просчёт сложный и всё делает не cuvid, а процессор
#2. Использовать буферизацию и использовать пресет сжатия видео
#3. Разобратся с параметрами вызова
#Что это за параметры '-vsync', 'cfr', '-f'
#-f - мы работаем только с mp4
#-vsync - при переходе из 25 кадров допустим в 60 будет более плавней...
#sp.call(ffmpeg_cmd, stderr=DEVNULL, stdout=DEVNULL)
#subprocess.call(ffmpeg_cmd, stderr=DEVNULL, stdout=DEVNULL)
#child = sp.Popen(ffmpeg_cmd, stderr=sp.PIPE, stdout=sp.PIPE)

#Так нам нужно установить пока что три параметра, потом буферизацию, но так вот:
#1 - -preset veryfast or superfast or faster or fast (medium standart)
#3 - -ssim 1 -tune ssim

#Не знаю я тут по впечатлением от прочитанного на stackoverflow... В общем один безумец стал рассказывать, серкреты человеческого восприятия...
#Щас буду его слова сюда передавать. Ну мысли очень интересные:

#Имейте ввиду, важно учитывать также психовизуальную оптимизацию, 
#которые делают изображения лучше для людей (например -psy-rd=1.0:0.15),
#Psy-rd означает учет человеческого восприятия при оптимизации соотношения скорости и искажения. 
#AQ (адаптивное квантование) - еще одна психическая оптимизация, но такая, что SSIM достаточно сложна, чтобы признать ее полезной, 
#в отличие от более простой метрики качества PSNR .
#Люди склонны воспринимать высокочастотный (пространственный) шум как мелкие детали, даже если он не такой, как на исходном изображении. 
#И нашим глазам нравятся детали, а не размытость. например, артефакты окантовки и звона от квантования = округления коэффициентов 
#DCT могут на самом деле выглядеть лучше, чем просто размытие всего, если они незначительны. 
#То, что выглядит хуже, когда вы ставите на паузу и увеличиваете масштаб, может приятно обмануть ваш глаз, когда вы просто смотрите в обычном режиме.

#Прочитав про этому штуку в 2 часа ночи и осознавая что мне завтра в колледже, я выяснил, что такая корректировка, распределяет битрейт и добовляет шум так что нам кажется видео качественей... Но она это делаете без сильных затрат ресурсов...


#Я довольно долго сидел и размышлял, как сделать рендер реально быстрее, да я смогу выйти с 12 часов на 3 часа и даже с контролем на меньшеее время, с большем кэшем и с куча ухрещений, при том выдавать пользователю качество лучшее
#Но время пришло, сказать честно, то что есть пересложнёные вещи, к примеру, нужно сделать такой режим кто мне сможет экономить весь просчёт, хотя зачем тратить столько сил? Ладно, просто опишу идею, я знаю что она даст плюс к скорости за меньшие ресурсы, но она сложна в релизации

#1. Нужно сделать временый кэш, и делать такое расспаралеленивание, то-есть нужно сделать план на час как обычно, но при этом будет всё происходить не в два этапа, а в три
#2. Каждое видео отдельно заэнкодить и применить эффект и в конце мы получим час видео в виде 10 минутных фрагментов (в несколько раза быстрее)
#3. Каждое видео отрезать начала и конец отдельно с помощью диска и маленьким отрезкам применить overlay (около 3 минут)
#4. соединить всё по 10 минутнам сигментам, удалить куча мелких видео


#Сейчас мы идём больше ногой со временим и тут есть много типов видео, которые можно сделать и все они не будут слишком сложно делатся
#1. Concat видео, без эффектов и дублирования видео и переходов
#2. Видео с эффектами как сейчас есть
#3. Бесконечно катать по одному видео
#4. Заменить звук своими mp3 это для видео номер 2 вопрос

#2 и 3 пункту нужно указывать длину


#Вау 1000 строк (у меня сейчас 1001 строка!), жаль что код уберётся и всё сожмётся до 900 строк наверно, ну так-то я крут... Да я крут, всегда знал... Хотя учитывая, что тут очень много комментариев которые я не удалил, чтобы во время разработки просто банально не запутатся, то да тут скорее строк тогда 500 может...