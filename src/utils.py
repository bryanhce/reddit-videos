import os

def clean_up():
    '''
    Delete mp3 files in audio
    '''
    folder_path = "../audio"
    for file in os.listdir(folder_path):
        if file.endswith(".mp3"):
            os.remove(os.path.join(folder_path, file))