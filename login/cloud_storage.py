"""
REFERENCES:
Title: ChatGPT
Prompt: how to store media file in another database without changing setting
"""
from storages.backends.gcloud import GoogleCloudStorage

class GoogleCloudMediaStorage(GoogleCloudStorage):
    location = 'media'  
    file_overwrite = False  