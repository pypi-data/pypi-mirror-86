import csv
import shutil
from tempfile import NamedTemporaryFile

import click
import googleapiclient.discovery
import youtube_transcript_api as yta


def get_captions(api_key, playlist_id, uploads_path):
    """Download captions for a YouTube `playlist_id` and save them in csv format at `uploads_path`.

    Args:
        api_key: A YouTube API key.
        playlist_id: A YouTube Playlist ID.
        uploads_path: Path at which to store caption data.
    """

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey=api_key
    )

    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50,
        fields='nextPageToken,items(contentDetails(videoId,videoPublishedAt))',
    )
    print('Getting unseen uploads...')
    while request is not None:
        synced = False
        response = request.execute()

        with open(uploads_path, 'a+') as uploads_file:
            uploads_reader = csv.reader(uploads_file)
            known_ids = [upload[0] for upload in uploads_reader]
            for video in response['items']:
                if video['contentDetails']['videoId'] in known_ids:
                    synced = True
                else:
                    print('Found new video id', video['contentDetails']['videoId'])
                    with open(uploads_path, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            video['contentDetails']['videoId'],
                            video['contentDetails']['videoPublishedAt'],
                            ''  # Empty field for the captions
                        ])
        if synced is True:
            print('Caught up on uploads.')
            request = None
        else:
            request = youtube.playlistItems().list_next(request, response)

    print('Downloading missing captions...')
    tempfile = NamedTemporaryFile(mode='w', delete=False, newline='')
    with open(uploads_path) as uploads_file, tempfile:
        uploads_reader = csv.reader(uploads_file)
        uploads_writer = csv.writer(tempfile)
        with click.progressbar(list(uploads_reader)) as bar:
            for upload in bar:
                if not upload[2]:
                    row = upload
                    try:
                        row[2] = ' '.join(
                            [caption['text'] for caption in yta.YouTubeTranscriptApi.get_transcript(upload[0])])
                    except (yta._errors.TranscriptsDisabled,
                            yta._errors.NoTranscriptFound):
                        row[2] = '*'
                    uploads_writer.writerow(row)
                else:
                    row = upload
                    uploads_writer.writerow(row)

    shutil.move(tempfile.name, uploads_path)
    print('Finished.')
