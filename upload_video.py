import os

import sys

import pytube

from google.oauth2.credentials import Credentials

from googleapiclient.discovery import build

from googleapiclient.errors import HttpError

def download_video(video_link):

    # Download the video using pytube

    video = pytube.YouTube(video_link)

    stream = video.streams.get_highest_resolution()

    video_path = stream.download()

    return video_path

def upload_video(video_path):

    # Authenticate with the YouTube API using your API key

    api_key = os.environ.get('YOUTUBE_API_KEY')

    credentials = Credentials.from_authorized_user_info(info=None)

    youtube = build('youtube', 'v3', developerKey=api_key, credentials=credentials)

    # Create the video metadata

    request_body = {

        'snippet': {

            'title': 'My Uploaded Video',

            'description': 'This is a video uploaded using Cirrus CI',

            'tags': ['cirrus-ci', 'automation', 'python']

        },

        'status': {

            'privacyStatus': 'private'

        }

    }

    # Upload the video to YouTube

    try:

        response = youtube.videos().insert(

            part='snippet,status',

            body=request_body,

            media_body=video_path

        ).execute()

        print(f"Video uploaded: https://www.youtube.com/watch?v={response['id']}")

    except HttpError as e:

        print(f"An error occurred: {e}")

        sys.exit(1)

if __name__ == '__main__':

    video_link = sys

