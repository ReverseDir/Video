#Так, тут не обычная ситуация, так как с какой стороны я не посмотрел, лучшее звонить в exe файл
#Почему будем звонить в exe файл? А что если пользователь захочет перегестрировать пользователя,
#Вроде можно здесь оставить код, но тогда как узнать когда пользователь захочет поменять пользователя?
#Можно куча выходов найти, но по мне оставить exe более чем элегатный ход, ведь его может и пользователь открыть и наткнутся на html doc

#Тут у нас будет лишь читание файла, от регестрации и контроль над открытием этого exe регестрации
#Я буду делать полу-самстоятельные .py файлы, надеюсь так будет норм...

import json
import time
import os
import io
from datetime import datetime, timezone

#Эту штуку можно переместить кстати ЭТОТ БЛОК НУЖЕН ЧТОБЫ ПЕРЕМЕСТИТЬ ВСЕ ФАЙЛЫ В КЭШ

#Всё это нужно чтобы сделать свою большую базу даных, после чего не нужно звонить ютубу и спрашивать у него про теги...
#Что в принцепи осталось сделать? На деле вся система почти сделана, осталось лишь сделать регестрацию и засунуть информацию в json файл,
#Ну и написать туториал текстом, на деле всё просто:
#Нужно зарегать себя как developer и получить youtubeApi ключ,
#Потом нужно себя зарегать как обычный чел (типы что ты не частное лицо и не компания) на Oauth там регестрация
#Зарегать свою почту туда и прекрипить тестого пользоватя всё это в анкете регестрации..
#Потом после регестрации Oauth, там вам доётся secret_client.json и ключ ещё один,
#После регестрации запускаете приложение это и оно автоматически находит по Api тебя и говорит над каким аккаунтом нужно загружать видео
#После трёх кругов ада (хотя всё очень просто, оно на первых парах кажется сложным), вся информация сохроняется в кэш
#Ну и после регестрироватся снова не придётся заполнять информацию, 
#Вся информация не удалится с гугла, поэтому один раз нужно пройти три круга ада...

#По идеи сейчас я смотрю с той стороны, как бы стать меньшем зависимым от Youtube Api я трачу много квот на получение тегов...
#Так и вдруг будут воспринимать как спам... 

def __make_name_file(name_file, individum_name = True):
    if(individum_name == True):
        num_file = 0
        while True:
            num_file += 1
            save_file = os.path.splitext(name_file)[0]+str(num_file)+".txt"
            if(os.path.isfile(save_file) == False):
                return save_file
    else:
        return name_file


def saveInformation(read_data, save_list_folder = "", save_all_folder = "data/", save_list=True, save_all=True, individual_name_list = False, individual_name_all = True):
    all_description_text = read_data.get("all_description")
    all_tags_text = read_data.get("all_tags")
    all_title_text = read_data.get("all_title")
    all_channel_title_text = read_data.get("all_channel_title")
    list_description_text = read_data.get("list_description")
    list_tags_text = read_data.get("list_tags")
    list_title_text = read_data.get("list_title")

    if(save_list_folder != ""):
        save_list_folder += "/"
    if(save_all_folder != ""):
        save_all_folder += "/"

    if(save_all==True):
        #Save all_description.txt
        with io.open(__make_name_file(save_all_folder+"all_description.txt", individual_name_all), 'w', encoding="utf-8") as file:
            file.write(all_description_text)
            file.close()

        #Save all_tags.txt
        with io.open(__make_name_file(save_all_folder+"all_tags.txt", individual_name_all), 'w', encoding="utf-8") as file:
            file.write(all_tags_text)
            file.close()

        #Save all_title.txt
        with io.open(__make_name_file(save_all_folder+"all_title.txt", individual_name_all), 'w', encoding="utf-8") as file:
            file.write(all_title_text)
            file.close()

        #Save all_channel_title.txt
        with io.open(__make_name_file(save_all_folder+"all_channel_title.txt", individual_name_all), 'w', encoding="utf-8") as file:
            file.write(all_channel_title_text)
            file.close()

    if(save_list==True):
        #Save list_tags.txt
        with io.open(__make_name_file(save_list_folder+"list_tags.txt", individual_name_list), 'w', encoding="utf-8") as file:
            file.write(list_tags_text)
            file.close()

        #Save list_description.txt
        with io.open(__make_name_file(save_list_folder+"list_description.txt", individual_name_list), 'w', encoding="utf-8") as file:
            file.write(list_description_text)
            file.close()

        #Save list_title.txt
        with io.open(__make_name_file(save_list_folder+"list_title.txt", individual_name_list), 'w', encoding="utf-8") as file:
            file.write(list_title_text)
            file.close()






def __get_file_by_extension(path, file_endswith, recursive = False):
    array_file = []
    if(recursive == True):
        for root, _, files in os.walk(path):
            for file in files:
                if(file.endswith(file_endswith) == True):
                    array_file.append(root+"/"+file)
    if(recursive == False):
        for file in os.listdir(path):
            if(file.endswith(file_endswith) == True):
                array_file.append(path+"/"+file)
    return array_file



def __delete_file(files, day_difference = 3):
    list_delete_file = []
    for file in files:
        now_time = int(datetime.now(timezone.utc).timestamp())
        create_time = int(os.path.getctime(file))
        day_subst_time = round(divmod(now_time - create_time, 3600)[0]/24,2)
        if(day_difference < day_subst_time):
            list_delete_file.append(file)
            os.remove(file)
    return list_delete_file



def DeleteCache(path, day_delete = 8, type_file = ".mp4", recursive_folder = False):
    'Удаляет кэш, который устарел'
    files = __get_file_by_extension(path, ".mp4")
    delete_file = __delete_file(files, day_delete, recursive_folder)
    return delete_file