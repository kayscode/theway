import requests
from googleapiclient.discovery import build
from django.conf import settings


class YoutubeService:

    def __int__(self):
        self.youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

    def search(self, url):
        return self.youtube.search().list(
            part="snippet",
            forMine=True,
            maxResults=25,
            q="fun",
            type="video"
        ).execute()
