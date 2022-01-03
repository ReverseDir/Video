from googleapiclient.discovery import build
import random
import time
import json
import io
#Абузить сервера гугла, довольно страшная затея,
#Поэтому идея возможно будет такова, что мы будем обновлять список может раз в неделю...
#В принцепи это редкая операция и нам хватит сполна миллиард тегов и миллиард названий и миллиард

#Мне нужна информация о каждом видео, где-либо а именно нужно -
#дата создание видео 
#длительность видео
#количество просмотров
#лайков
#тэг
#название
#описание
#url
#id
#id_channel


def getVideoInfo(response_with_items):
    "Берёт информацию с видео он аргументы snippet, statistics, contentDetails, если их не указать выдаст ошибку"
    response = response_with_items
    info_video = {}
    info_video.update(response.get("snippet"))
    info_video.update(response.get("statistics"))
    info_video.update(response.get("contentDetails"))
    #get-info
    need_info = {}
    need_info["channelTitle"] = info_video.get("channelTitle")
    need_info["channelId"] = info_video.get("channelId") #Ид создателя видео
    need_info["publishedAt"] = info_video.get("publishedAt") #Дата создания
    need_info["likeCount"] = info_video.get("likeCount") #Количество лайков
    need_info["viewCount"] = info_video.get("viewCount") #Количество просмотров
    need_info["title"] = info_video.get("title") #Название
    need_info["duration"] = info_video.get("duration") #Длина видео
    need_info["description"] = info_video.get("description") #Описание
    need_info["tags"] = info_video.get("tags") #Тэг
    return need_info #Оставляем нужную информацию

def clamp_array(array = [], max_len = 10):
    "Ограничевает массив делая длину менее чем"
    all_len = 0
    for i in range(len(array)):
        if(all_len > max_len):
            array.pop()
            continue
        all_len += len(array[i])
    return array


def delete_line_by_words(text = "", split_symbol = "\\n", list_delete_words = []):
    "Удаляет между указаным символом указаные слова и удаляет полностью всю строчку"
    edit_text = repr(text).split(split_symbol)
    index = 0
    while True:
        if(len(edit_text) <= index):
            break
        for del_index in list_delete_words:
            if del_index in edit_text[index]:
                edit_text.pop(index)
                index -= 1
                break
        index += 1
    edit_text = (split_symbol.join(edit_text))
    return edit_text


















#Некоторые функции хочется отдельно, поэтому разделю код не смотря на риски:

def get_video_info_youtube_api(api_key_youtube, PLAYLIST_VIDEO_ID):
    'Возврощает словарь в котором массивы:\n'
    youtube = build('youtube', 'v3', developerKey=api_key_youtube)

    request_playlist = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=PLAYLIST_VIDEO_ID,
        maxResults = 25
    )
    response_playlist = request_playlist.execute()
    playlist_items = []
    while request_playlist is not None:
        response_playlist = request_playlist.execute()
        playlist_items += response_playlist["items"]
        request_playlist = youtube.playlistItems().list_next(request_playlist, response_playlist)

    #Мы берём информацию о каждом видео в плейлисте
    playlist_items_info = []
    for item in playlist_items:
        id_video = item.get("contentDetails").get("videoId")
        request_video = youtube.videos().list(
            part="snippet, statistics, contentDetails",
            id=id_video
        )
        response = request_video.execute().get("items")
        if(len(response) != 0):
            playlist_items_info.append(getVideoInfo(response[0]))

    #НУЖНО УЗНАТЬ АВТОРОВ И ВЫЧИСЛИТЬ ИХ ПО АЙПИ ШОБЫ УБРАТЬ КОНКУРЕНТОВ
    #playlist_items_info.get("channelId")
    #all_channelId = []
    all_channel_title = []
    all_tags = []
    all_title = []
    all_description = []
    for item in playlist_items_info:
        if(item.get("tags") != None):
            for tag in item.get("tags"):
                all_tags.append(tag)
        if(item.get("title") != None):
            all_title.append(item.get("title"))
        if(item.get("description") != None):
            all_description.append(item.get("description"))
        if(item.get("channelTitle") != None):
            all_channel_title.append(item.get("channelTitle"))
    all_channel_title = list(set(all_channel_title)) #Удаляет копии каналов
    all_data = {
        "all_tags": all_tags,
        "all_title": all_title,
        "all_description": all_description,
        "all_channel_title": all_channel_title
    }
    return all_data


def get_video_info_txt(path_txt_all_tags = "data/cache/all_tags1.txt", path_txt_all_title = "data/cache/all_title1.txt", path_txt_all_description = "data/cache/all_description1.txt", path_txt_all_channel_title="data/cache/all_channel_title1.txt"):
    all_tags = []
    all_title = []
    all_description = []
    all_channel_title = []
    all_tags = (io.open(path_txt_all_tags, mode="r", encoding="utf-8").read()).split(", ")
    all_title = (io.open(path_txt_all_title, mode="r", encoding="utf-8").read()).split(", ")
    all_description = (io.open(path_txt_all_description, mode="r", encoding="utf-8").read()).split("\n\n\n")
    all_channel_title = (io.open(path_txt_all_channel_title, mode="r", encoding="utf-8").read()).split("\n\n")
    all_data = {
        "all_tags": all_tags,
        "all_title": all_title,
        "all_description": all_description,
        "all_channel_title": all_channel_title
    }
    return all_data










#И так тут в принцепи всё прикольно по контролю, нужно лишь параметры добавить и есть неплохой хоть какой-то контроль...
def ReadVideoBy(all_info_video_dict):
    'Выдаёт тэги, описание, название видео и название каналов\n\nПервый параметр может брать данные из заранее записаных кешей при первом успешном запуске программы, либо заранее записаных кешей, которые нужно скинуть в папку'
    #Project ID: youtube-api-336009. It cannot be changed late 
    #https://www.youtube.com/watch?v=XpX_iV3dDaA&list=PL5DAB733F1999178F&ab_channel=MusicaPara

    all_tags = all_info_video_dict.get("all_tags")
    all_title = all_info_video_dict.get("all_title")
    all_description = all_info_video_dict.get("all_description")
    all_channel_title = all_info_video_dict.get("all_channel_title")
    



    #Ну типа мы тут либо записываем всю инфу либо её читаем с файлов, которые сами записали...











    #Так кароче тут вот в чём проблема, мы должны сделать дополнительно чтение просто файла, а не с ютуба

    #Чтобы сгенерировать название я думаю надо взять рандомные слова из рандомного массивов и просто их рандомно вставить
    #Но сделалв так я получил Sex more in the description, что в принцепи не плохо для кликбейта!
    #На деле, весь прикол сейчас в том что ютуб дейстивительно сработате один раз так как надо,
    #Почему? Потому что если у меня всё будет поставлено на рандоме, то когда-то алгоритмы и моё описание, теги, сработают на конец на меня...
    #Что мы делаем?
    #Мы должны сделать четыре текстовика,
    #1 - теги
    #2 - название
    #3 - описание видео
    #4 - по-приколу, потому что я так хочу, статистику по своему каналу...

    #Ну кароче в чём прикол и печаль, Python конечно крут на даный момент, но он медленно обрабатывает циклы и проверяет слова
    #Но, обудмав по хорошему я понял, что перегонять код отуда и обратно будет сложнее) Ну в принцепи, идею оставлю,
    #Ну типа если задача была бы супер огромная, то да проще было бы проще переводить текст в python, а обрабатывать

    #И так у нас есть инфа, о тегах видео, названия видео и о описание,
    #Проблема пока что только в том что навзание, теги и описание могут хранить ссылку, что в принцепи очень плохо.
    #Но пока что-то это не важно, мы хотим из видео взять из списка видео все теги.


    random.shuffle(all_tags)
    all_len_tags_array = len(all_tags)
    list_tags = []
    for tag in range(500):
        if(tag < all_len_tags_array):
            list_tags.append(all_tags[tag])
    list_tags = list(set(list_tags)) #Удаляет копии тэгов

    #Делаем тегов не больше 450 символов...


    max_len_tag_symbol = 200 + random.randint(0,245)
    list_tags = clamp_array(list_tags, max_len_tag_symbol) #Возможно тут ОШИБКА




    list_delete_new_line = ["https://", "spotify","Spotify","P.S.", "(C)", "P.s.","p.s.", "&", "©", "℗", "my music", "……", "-~", "~~~", "---", "===", "###", "....", "___", "***", "All rights", "www", "Emile" , "all rights", "All Right", ":", "B.", "J.", "G.", "k.", "Copyright", "http://", ".com", ".ru", "mp3", "MP3", "Keyboard", "USB", "Drum", "drum"]
    list_delete_comma = ["#", "$", "@", "mail", "soothing", "Soothing", "ITUNES", " by ", "Robert", "ownload","OWNLOAD", "Amazon", "Yellow", "yellow", "Michel"]
    list_delete_point = ["EasySleepMusic", "Easy Sleep Music", "easysleepmusic", "easy sleep music"]
    #Только сейчас понял одну вещь, чтобы защитить себя от того что мы украдём чужое название канал и случайно вставим его
    #То смотри нам просто нужно, взять и добавить всех авторов в особый чёрный список, при совпадение которого удалять строку
    #Узнать навзание 150 каналов и вставить их в list_delete_new_line

    list_delete_words = ["''", "\"'", "\\r", "'\"", "'\\'", "\\\'", "\\\"", "\\", '""', "' ", 'u200b"', '" ', "'", '"' ]
    all_description_array = []
    for index_i in range(len(all_description)-1):
        all_description_piece = delete_line_by_words(all_description[index_i], "\\n", list_delete_new_line)
        all_description_piece = all_description_piece.replace("\\n", "\n")
        all_description_piece = delete_line_by_words(all_description_piece, ",", list_delete_comma)
        all_description_piece = all_description_piece.replace("\\n", "\n")
        all_description_piece = delete_line_by_words(all_description_piece, ",", list_delete_point)
        all_description_piece = all_description_piece.replace("\\n", "\n")
        for i in list_delete_words:
            all_description_piece = all_description_piece.replace(i, "")
        all_description_piece = all_description_piece.replace(" , ", ",")
        all_description_piece = all_description_piece.replace("  ", " ")
        all_description_array.append(all_description_piece)
    all_description = all_description_array
    #Теперь у нас массив из различных описаний видео без ссылок и упоминаний автора.
    #Теперь нам надо пройтись по массивам и разделить их до запятой и сложить рандомно




    #Так теперь у нас есть текст, который не до конца исправлен. Что в нём не так? В принцепи всё)) Ну ладно, не всё
    #Скорее всего я должен юзать Python, чтобы изменять всё, но мы поступим более гениально
    #И так рассматриваем текст по типичных 5 этапов


    #1. Описание, не большое, но главное прикольное (либо нет)
    #2. Контакты, либо по умолчанию, (пока что пропуск)
    #3. Ещё рандомного текста (либо нет)
    #4. Теги (от 10 до 30) (либо нет)
    #5. Хэштеги (3-6 штук) (либо нет)

    #Рассматриваем пункт 4 и 5
    #Чтобы получить теги которые нужно вписывать, нужно взять рандомные теги, плюс наши, которые уже есть и получим 15/15

    #0. Intro - name video, Description, thanks for subscribe other... 500 символов

    #1. Text description
    description_add_text = []
    description_str_text = []
    for index_i in range(len(all_description)-1):
        array_words = repr(all_description[index_i]).split(".")
        for i in array_words:
            if(len(i) > 8):
                description_str_text.append(i+".")
    for i in range(random.randint(4, 18)):
        random.seed(i+time.time())
        random_index_str = random.randint(0, len(description_str_text)-1)
        description_add_text.append(description_str_text[random_index_str])
    max_len_description_add_text = random.randint(200, 660)
    description_add_text = list(set(description_add_text)) #Удаляем повторы
    clamp_array(description_add_text, max_len_description_add_text)
    #Так теперь нужно, ограмничить предложение до 700 символов

    #Генерится текст довольно осмысленый так действительно генерят нейроные сети, что в принцепи довольно круто...
    #У меня получается при нескольких перезапусках осмысленый типичный ботовский текст, причём структура наш мозг сам додумает
    #В итоги как по мне всё классно работает


    #2. About Contact url 1000 символов
    #Тут на деле пропуск, так как это то что вы хотите указать, 
    #в целом я не знаю как это учитывать, но конечно можно придумать не спорю


    #3. Text description
    description_add_text2 = []
    description_str_text2 = []
    random.seed(time.time()+80)
    for index_i in range(len(all_description)-1):
        array_words = repr(all_description[index_i]).split(".")
        for i in array_words:
            if(len(i) > 8):
                description_str_text2.append(i+".")
    for i in range(random.randint(8, 38)):
        random.seed(i+time.time()*4)
        random_index_str = random.randint(0, len(description_str_text2)-1)
        description_add_text2.append(description_str_text2[random_index_str])
    max_len_description_add_text2 = random.randint(400, 1700)
    description_add_text = list(set(description_add_text)) #Удаляем повторы
    clamp_array(description_add_text2, max_len_description_add_text2)
    #Так теперь нужно, ограничить предложение до 1800 символов
    #1800 + 700 + 900 = 3400 - это значит, что нам есть 1600 символов для ещё трёх столбцов, которые захочет пользователь


    #4. Tags description
    description_add_tags = []
    for i in range(random.randint(10, 40)):
        random.seed(i+time.time())
        rand_index_list = random.randint(0, len(list_tags)-1)
        rand_index_all = random.randint(0, len(all_tags)-1)
        if(random.randint(0,80)%2):
            description_add_tags.append(list_tags[rand_index_list])
        else:
            description_add_tags.append(all_tags[rand_index_all])
    description_add_tags = list(set(description_add_tags))
    max_len_tag_symbol_2 = 200 + random.randint(0,380)
    clamp_array(description_add_tags, max_len_tag_symbol_2) #до 580 символов



    #5. Hashtag description
    description_add_hashtags  = []
    for i in range(random.randint(3, 7)):
        random.seed(i-time.time())
        rand_index_add_list = random.randint(0, len(description_add_tags)-1)
        rand_index_all = random.randint(0, len(all_tags)-1)
        if(random.randint(0,80)%3):
            description_add_hashtags.append("#"+all_tags[rand_index_all])
        else:
            description_add_hashtags.append("#"+description_add_tags[rand_index_add_list])
    description_add_hashtags = list(set(description_add_hashtags))
    max_len_tag_symbol_3 = 100 + random.randint(0,110)
    clamp_array(description_add_hashtags, max_len_tag_symbol_3) #до 210 символов

    #до 800 символов

    #6. Ending description 100
    #Thanks for watching и тд...


    #Что у нас в итоги
    #Мы имеим четыре массива и потенциально три массива...
    #Но даже без потенциальных массивов мы можем сделать норм описание
    #У нас есть description_add_hashtags description_add_tags description_add_text description_add_text2
    #В общей сумме выходит до 3800 символов плюс у нас есть 1200 символов для своих нужд

    #Конвертируем всё в текст:
    description_str_text1 = str("".join(description_add_text))
    description_str_text2 = str("".join(description_add_text2))

    ######
    #Я не хочу делать как надо, это оказывается намного рискованей чем кажется, поэтому так проще и меньше рисков сломать систему
    description_str_text1 = description_str_text1.replace("\\n\\n\\n\\n", "\\n\\n")
    description_str_text1 = description_str_text1.replace("\\n\\n\\n", "\\n\\n")
    description_str_text1 = description_str_text1.replace("\\n\\n\\n", "\\n\\n")
    description_str_text1 = description_str_text1.split("\\n")
    #Удаляем в самом начале new line
    while True:
        if(len(description_str_text1[0]) < 8): description_str_text1.pop(0)
        else: break
    if(description_str_text1[0] == " "): description_str_text1 = description_str_text1[1:]
    description_str_text1 = "\\n".join(description_str_text1)

    description_str_text2 = description_str_text2.replace("\\n\\n\\n\\n", "\\n\\n")
    description_str_text2 = description_str_text2.replace("\\n\\n\\n", "\\n\\n")
    description_str_text2 = description_str_text2.replace("\\n\\n\\n", "\\n\\n")
    description_str_text2 = description_str_text2.split("\\n")
    #Удаляем в самом начале new line
    while True:
        if(len(description_str_text2[0]) < 8): description_str_text2.pop(0)
        else: break
    if(description_str_text2[0] == " "): description_str_text2 = description_str_text2[1:]
    description_str_text2 = "\\n".join(description_str_text2)
    #######



    description_str_text1 = description_str_text1.split("\\n")
    description_str_text1_text = description_str_text1
    description_str_text1 = []
    for i in description_str_text1_text:
        if(len(i) < 10 and len(i) >= 1):
            pass
        else:
            description_str_text1.append(i)
    description_str_text1 = "\n".join(description_str_text1)

    description_str_text2 = description_str_text2.split("\\n")
    description_str_text2_text = description_str_text2
    description_str_text2 = []
    for i in description_str_text2_text:
        if(len(i) < 10 and len(i) >= 1):
            pass
        else:
            description_str_text2.append(i)
    description_str_text2 = "\n".join(description_str_text2)

    #Исправляем хэштег убираем пробелы между словами
    random.seed(time.time() + 89678)
    seed_description_add_hashtags = random.randint(0,1)
    for i in description_add_hashtags:
        if(seed_description_add_hashtags == 1):
            i.replace(" ", "")
        else:
            i.replace(" ", "_")
    description_str_hashtags = " ".join(description_add_hashtags)

    #Исправляем теги внизу добавляем запятые между словами
    description_str_tags = ""
    random.seed(time.time() + 92)
    if(random.randint(0,1) == 1):
        description_str_tags = ", ".join(description_add_tags)
    else:
        description_str_tags = " ".join(description_add_tags)

    #Исправляем теги внизу добавляем надпись Tags:
    random.seed(time.time()/32)
    if(random.randint(0,2) != 1):
        description_str_tags = "Tags: " + description_str_tags
    description_str_tags = "\n\n\n\n"+description_str_tags+"\n"

    #Исправляем хэштеги внизу добавляем надпись Hashtags:
    random.seed(time.time()-783)
    if(random.randint(0,3) == 1):
        description_str_hashtags = "Hashtags: " + description_str_hashtags
    description_str_hashtags = "\n"+description_str_hashtags

    #Всё это для добавки рандома в тексте
    #Кстати, при генерации текста случилось забавно, там была рекомендация как надо отдыхать,
    #Причём внутри действительно написан осмысленый текст, что довольно удивительно... Вот что было сгенерировано:
    #СГЕНЕРИРОВАНЫЙ ТЕКСТ:
    #Управлние медитации:
    #Чувствуете усталость или стресс? Устройтесь поудобнее, расслабьтесь и позвольте нежному руководящему голосу погрузить вас в состояние глубокого расслабления. Поделись с друзьями, они тебе за это скажут. Глубокий сон водная релаксация. 
    #Цель этого - предупредить ваш разум, пока ваше тело продолжает спать, что теоретически должно помочь вам войти в состояние осознанного сна.
    #Расслабляющая музыкальная терапия может исцелить, успокоить и успокоить возбужденный ум. Спа-музыка, звуки природы, звуки дождя и наша музыка помогут вам расслабить разум и тело. Наша музыка черпает вдохновение из музыки и песнопений африканской и индийской йоги ». 
    #Наша расслабляющая музыка для сна поможет вам мягко и без беспокойства войти в состояние сна.

    #В каком-то смысле всё это выглядет хоть чу-чуть да осмысленно.. Но в этом и прикол
    #Минусы это, то что есть слова на 8 символов занимающую всё строку...

    list_description_text = description_str_text1+description_str_text2+description_str_tags+description_str_hashtags
    all_description_text = ""
    for i in all_description:
        all_description_text += i







    #Деламе теперь название видео
    title_add_count = []
    title_add_tags = (" ".join(all_channel_title)).split(" ")
    for i in title_add_tags:
        total = 0
        for j in title_add_tags:
            if i in j:
                total += 1
        title_add_count.append(total)

    title_add_tags2 = title_add_tags
    title_add_tags = []
    for i in range(len(title_add_tags2)):
        if(title_add_count[i] > 9):
            title_add_tags.append(title_add_tags2[i])

    title_add_tags = list(set(title_add_tags))
    list_delete_words = ["HD", "4K", "No", "Soothing", "J.", "(", ")"]
    #Если одно слово длинное
    for i in title_add_tags:
        if (len(i) > 60): title_add_tags.remove(i)
    #Если слово в списке не нужных слов
    for i in list_delete_words:
        if i in title_add_tags: title_add_tags.remove(i)

    #Добовляем слова, как раз на случай если их в общее нету
    title_add_tags.append("|")
    title_add_tags.append("||")
    title_add_tags.append("Top")
    title_add_tags.append("Music")
    title_add_tags.append("Chill")
    for i in range(3):
        title_add_tags.append("Playlist")
        title_add_tags.append("Best")
        title_add_tags.append("Amazing")
        title_add_tags.append("•")
        title_add_tags.append("❤️")
        title_add_tags.append("►")
    #Создаём слова
    list_title_text = ""
    list_not_use_first_word = ["(", ")", ".", ":", "|", "&", "y", "||", "Y", "and", "And"]
    for i in range(random.randint(10,25)):
        word_use = True
        index = random.randint(0, len(title_add_tags)-1)
        if(len(title_add_tags[index]) < random.randint(1, 3) and i < 6):
            continue
        for j in list_not_use_first_word:
            if(i<=1 and title_add_tags[index] == j):
                word_use = False
        if(word_use == True):
            list_title_text += title_add_tags[index]+" "

    list_title_text = list_title_text.split(" ")
    title_text = ""
    for i in range(len(list_title_text)-1):
        if((len(list_title_text[i])<=2) and (len(list_title_text[i+1])<=2)):
            continue
        if(list_title_text[i] != list_title_text[i+1]):
            title_text += list_title_text[i] + " "

    if(random.randint(0, 14) == 0):
        title_text = title_text.split(" ")
        while True:
            title_text.pop(0)
            if(len(" ".join(title_text)) < 40):
                title_text = " ".join(title_text)
                break
        title_text = " ".join(title_text)

    if(random.randint(0, 6) == 2):
        title_text = title_text.upper()
        

    #Если слишком длиное описание
    if(len(title_text) > 100):
        title_text = title_text.split(" ")
        while True:
            title_text.pop(0)
            if(len(" ".join(title_text)) < 100):
                title_text = " ".join(title_text)
                break
    list_title = title_text.replace(" :", ":")
    list_title = list_title.replace(" )", ")")
    list_title = list_title.replace("( ", "(")
    list_title = list_title.replace("  ", " ")
    list_title_text = str(list_title)
    
    #Довольно не плохо с названием получилось, могут быть 3 паттерна названия,
    #Сам алгоритм я думал меньше неделю, так как это довольно сложная задача, сделать
    #Без нейроных сетей название причём без упоменание никнеймов и аддекватное название
    #Но всё нормально обдумав, получилось сделать прикольный генератор названий,
    #Кстати делать описание к видео было легче, так как там может быть всякий бред написан,
    #А вот навзание зависит кликнет или нет, тот самый робот...





    all_tags_text = ", ".join(all_tags)
    list_tags_text = ", ".join(list_tags)
    all_title_text = ", ".join(all_title)
    all_channel_title_text = ", ".join(all_channel_title)

    output_data = {
        'all_tags': all_tags_text,
        'all_title': all_title_text,
        'all_description': all_description_text,
        'all_channel_title': all_channel_title_text,
        'list_tags': list_tags_text,
        'list_title': list_title_text,
        'list_description': list_description_text
    }
    return output_data








def GetTagsByYoutubePlaylist(DEVELOPER_KEY = "", PLAYLIST_VIDEO_ID = 'PL5DAB733F1999178F'):
    'Берёт в качестве аргумента только ключ и ID плейлиста и возращает информацию для видео в качестве словаря'
    all_info_video_dict = {}
    all_info_video_dict = get_video_info_youtube_api(DEVELOPER_KEY, PLAYLIST_VIDEO_ID)
    all_info_video_dict = ReadVideoBy(all_info_video_dict)
    return all_info_video_dict


def GetTagsByTxt(path_txt_all_tags = "data/cache/all_tags1.txt", path_txt_all_title = "data/cache/all_title1.txt", path_txt_all_description = "data/cache/all_description1.txt", path_txt_all_channel_title="data/cache/all_channel_title1.txt"):
    'Берёт в качестве аргумента пути к необходимым файлам и возращает информацию для видео в качестве словаря'
    all_info_video_dict = {}
    all_info_video_dict = get_video_info_txt(path_txt_all_tags, path_txt_all_title, path_txt_all_description, path_txt_all_channel_title)
    all_info_video_dict = ReadVideoBy(all_info_video_dict)
    return all_info_video_dict


#Хммм, я так подумал, но ведь нам нужно получать теги от видео и в manual режиме... Типа если я хочу, просто получить включая exe файл... Ну кароче сделаю отдельную версию



