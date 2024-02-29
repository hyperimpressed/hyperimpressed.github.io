from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

path = '../data/youtube_comments.db'

def get_comments():
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT video_id, comment FROM youtube_comments")
    comments = cursor.fetchall()
    conn.close()
    return comments

@app.route('/')
def show_comments():
    comments = get_comments()
    return render_template('comments.html', comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
