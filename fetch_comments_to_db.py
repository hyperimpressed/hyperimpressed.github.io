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
        maxResults=100,  # Adjust based on your needs
        textFormat='plainText'
    ).execute()

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        if search_string.lower() in comment.lower():
            comments.append(comment)
            if len(comments) == 3:
                break

    return comments

def insert_comments_into_db(video_id, comments):
    for comment in comments:
            sql = "INSERT INTO `youtube_comments` (`video_id`, `comment`) VALUES (?, ?)"
            cursor.execute(sql, (video_id, comment))
    conn.commit()

video_ids = ['HQKwgk6XkIA', 'qGyp0Y5ewBI']  # Your video IDs
search_string = '2'  # String to search in comments

for video_id in video_ids:
    comments = fetch_comments(video_id, search_string)
    if comments:
        insert_comments_into_db(video_id, comments)

conn.close()
