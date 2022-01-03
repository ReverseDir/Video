#Что нам нужно, к печальным новостям и к счастливам для себя, загрузка видео требует меньше информации, 
#но требует api информация, почему так? На данный момент, если вы обычный пользователь, то
#от вас требуются просто заходить на ваш аккаунт и смотреть видосики, у вас такая функция, ещё размножатся как репродуктивная функция...
#Но на меня ютуб смотрит не как на пользователя
#А как на developera, очень секусально звучит, но на деле я тот же робот, тока не много выше, самый высокий это ютуб
#Он и поработил эту всю систему... Хотя выше гугл, а ещё выше... Ну в прочем не важно


#Other
import io
import os
import sys
import time
import httplib2
import random

#Google Api
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

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def get_authenticated_service(CLIENT_SECRETS_FILE, YOUTUBE_UPLOAD_SCOPE="https://www.googleapis.com/auth/youtube.upload"):
    'Получает данные о гугл и создаёт build'
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE)
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        if(0==1):
            credentials = run_flow(flow, storage)
    return build("youtube", "v3", http=credentials.authorize(httplib2.Http()))



# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print('Uploading file...')
            status, response = request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print('Video id "%s" was successfully uploaded.' % response['id'])
                else:
                    exit('The upload failed with an unexpected response: %s' % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = 'A retriable error occurred: %s' % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit('No longer attempting to retry.')

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print('Sleeping %f seconds and then retrying...' % sleep_seconds)
            time.sleep(sleep_seconds)




#Тут настройки для upload (загрузки видео)
def initialize_upload(youtube, path_video, body):
    'Иницилизация данных для загрузки, возврощает данные, которые нужно запрустить через комманду .execute()'
    data_request = youtube.videos().insert(
        part="snippet, status",
        body=body,
        media_body=MediaFileUpload(path_video, chunksize=-1, resumable=True)
    )
    resumable_upload(data_request)










  

#Загрузка видео на канал
def UploadVideoOnYoutube(DEVELOPER_KEY, CLIENT_SECRETS_FILE, path_video = "", title_output = "", tags_output = [], description_output = "", privacyStatus = "public", categoryId = "22"):
    'Загружает видео на ютуб\nПроблемотичная функция по все параметрам...\nТо квоты не хватит, то опертивку забирает много, то человек закроет прогу и видео не загрузится'
    body={
        "snippet":{
            "title":title_output,
            "description":description_output,
            "tags":tags_output,
            "categoryId": categoryId
        },
        "status": {
            "privacyStatus": privacyStatus
        }
    }
    path_video = path_video
    youtube = get_authenticated_service(CLIENT_SECRETS_FILE)
    #youtube = build("youtube", "v3", developerKey = DEVELOPER_KEY)
    data_request = initialize_upload(youtube, path_video, body)

    #Самая опасная команда:
    print(data_request)
    #response = data_request.execute()
    #exit(12)
    return data_request
