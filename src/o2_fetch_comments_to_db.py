from googleapiclient.discovery import build
import sqlite3

# YouTube API setup
API_KEY = 'AIzaSyAZJRxunHxliV4-xAfvxi6LKEIDjb5ItiM';
youtube = build('youtube', 'v3', developerKey=API_KEY)

path = '../data/youtube_comments.db'

# Database setup
conn = sqlite3.connect(path)
cursor = conn.cursor()

def fetch_comments(video_id, search_string):
    comments = []
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        order='relevance',
        maxResults=1000,
        textFormat='plainText'
    ).execute()

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        if search_string.lower() in comment['textDisplay'].lower():
            comments.append({
                'author': comment['authorDisplayName'],
                'text': comment['textDisplay'],
                'likes': comment['likeCount'],
                'publishedAt': comment['publishedAt']
            })
    sorted_comments = sorted(comments, key=lambda x: x['likes'], reverse=True)
    return sorted_comments[0:3]

def insert_comments_into_db(video_id, comments):
    for comment in comments:
            sql = "INSERT INTO `youtube_comments` (`video_id`, `comment`) VALUES (?, ?)"
            cursor.execute(sql, (comment['author'], comment['text']))
    conn.commit()

video_ids = ['qGyp0Y5ewBI', 'BSXoI9MDvU0']  # Your video IDs
search_string = ''  # String to search in comments

for video_id in video_ids:
    comments = fetch_comments(video_id, search_string)
    if comments:
        insert_comments_into_db(video_id, comments)

conn.close()
