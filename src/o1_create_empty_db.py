import sqlite3
import os

path = '../data/youtube_comments.db'
import os
if os.path.exists(path):
  os.remove(path)
else:
  print("The file does not exist")

# Connect to SQLite database (this will create the database file if it doesn't exist)
conn = sqlite3.connect(path)
cursor = conn.cursor()
sql = '''CREATE TABLE youtube_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            comment TEXT NOT NULL
        )'''
cursor.execute(sql)

# Commit your changes in the database
conn.commit()
conn.close()

print("Table created successfully")
