from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from functions import *
import pydrive
start=time.time()
gauth = GoogleAuth()
gauth.LoadCredentialsFile("json/credentials.txt")
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile("json/credentials.txt")

drive = GoogleDrive(gauth)


def upload_file(folder_id, file_name):
    file = drive.CreateFile({'parents': [{'id': folder_id}]})
    file.SetContentFile(file_name)
    file.Upload()


def download_file(file_name, file_id):
    try:
        downloaded = drive.CreateFile({'id': file_id})  # '13fl0of7dFzJOLsuP8_MjGzhkFFqFsh1x'
        downloaded.GetContentFile('data/'+file_name)  # 'export_id_repository.csv'
        data = get_mapping_contents('data/' + file_name)
        return data
    except pydrive.files.FileNotDownloadableError:
        print(file_name, file_id)


def find_file(des_list, root_id):
    if len(des_list) == 1:
        file_list = drive.ListFile({'q': "'" + root_id + "' in parents and trashed = false"}).GetList()
        for i in file_list:
            if des_list[0] == i['title']:
                return i['title'], i['id']
    else:
        file_list = drive.ListFile(
            {'q': "mimeType='application/vnd.google-apps.folder' and parents in '" + root_id +
                  "' and trashed = false"}).GetList()
        for i in file_list:
            if des_list[0] == i['title']:
                del des_list[0]
                return find_file(des_list, i['id'])


if __name__ == '__main__':
    path = 'main folder/sub folder/file'
    path_l = path.split('/')
    find_file(path_l, 'folder_id')