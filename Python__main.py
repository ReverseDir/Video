
import Python_make_video 
import Python_get_youtube_video_info 
import Python_upload_video
import Python_file_manipulate
import Python_check_data
import json
import os




#1. Узнаёт где видео, параметр важный, на него не похер
video_path_data = json.load(open("data/video_data.json"))
path_video_mp4 = os.path.normpath(os.path.abspath(video_path_data.get("video")).replace("\\", "/"))
path_sound_mp3 = os.path.normpath(os.path.abspath(video_path_data.get("sound")).replace("\\", "/"))



#2. Клиент сикрет и юутб json, если нет файла, то похер
client_secrets = "data/client_secrets.json"
youtube_api_data = ""
try:
    data_youtube_api_file = json.load(open("data/youtube_data.json"))
    youtube_api_data = data_youtube_api_file.get("youtube_api")
except:
    pass


#3. Проверка папок, файлов, Api, на всё это похуй и на ответы от программы насрать мне и пользователю
check_all_info = Python_check_data.CheckAllPrintText(False, True, youtube_api_data, client_secrets, path_sound_mp3, ".mp3", path_video_mp4, ".mp4")
check_youtube_api       = check_all_info[1].get("google_api")
check_google_api       = check_all_info[1].get("youtube_api")
check_folder_struct  = check_all_info[1].get("struct_folder")
check_ffmpeg_file   = check_all_info[1].get("ffmpeg_ffprobe")
check_sound_file   = check_all_info[1].get("sound")
check_video_file  = check_all_info[1].get("video")
check_json_file  = check_all_info[1].get("json")
print(check_all_info[0])



#4. Берём теги, описание, название, если нет подключение к гугла или ютубу, то похуй
data = {}
try:
    data = Python_get_youtube_video_info.GetTagsByTxt()
    Python_file_manipulate.saveInformation(data, "output", "data/cache", True, False)
except:
    playlist_video_id = 'PL5DAB733F1999178F'
    data = Python_get_youtube_video_info.GetTagsByYoutubePlaylist(youtube_api_data, playlist_video_id)
    Python_file_manipulate.saveInformation(data, "output", "data/cache", True, True)


#5. Нахождение папки cache, Temp, output, на которые похуй
path_execute_prog = os.getcwd()
output_video = (path_execute_prog+"/output").replace("\\", "/")
cache_video = (path_execute_prog+"/data/cache/Temp").replace("\\", "/")





#6. Делаем видео, на это откровенно не похуй, но всем окружающим похуй
path_video_output = Python_make_video.makeVideoByFfmpeg(path_video_mp4, path_sound_mp3, output_video, cache_video)







#7. Получаем теги, название, описание, на которые не похуй:
list_title_text = data.get("list_title")
list_tags_text = list((data.get("list_tags")).split(", "))
list_description_text =  data.get("list_description")



#8. Загружаем видео на которое всем похуй, но на пункт не похуй
#path_video_output = "C:/Users/user/source/repos/Python auto-make video/Python auto-make video/output/myfile_final2.mp4"
final_output = Python_upload_video.UploadVideoOnYoutube(youtube_api_data, client_secrets, path_video_output, list_title_text, list_tags_text, list_description_text)
print(final_output)


#9. Удаление кэша, на который все похуй
Python_file_manipulate.DeleteCache("data/cache/Temp", 4, ".mp4")
Python_file_manipulate.DeleteCache("data/cache/Temp", 4, ".mp3")
Python_file_manipulate.DeleteCache("output", 6, ".mp4")


