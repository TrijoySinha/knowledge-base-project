from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('db/knowledge_base.db')
    c = conn.cursor()
    # Table for manual notes
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table for saved articles
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            title TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table for future embeddings (optional for now)
    c.execute('''
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_type TEXT, -- 'note' or 'article'
            source_id INTEGER,
            embedding BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_note', methods=['POST'])
def add_note():
    if request.method == 'POST':
        content = request.form['content']
        conn = sqlite3.connect('db/knowledge_base.db')
        c = conn.cursor()
        c.execute("INSERT INTO notes (content) VALUES (?)", (content,))
        conn.commit()
        conn.close()
        return render_template('index.html', message="Note added successfully!")

@app.route('/add_article', methods=['POST'])
def add_article():
    if request.method == 'POST':
        url = request.form['url']
        title = request.form.get('title')
        content = request.form.get('content')
        conn = sqlite3.connect('db/knowledge_base.db')
        c = conn.cursor()
        c.execute("INSERT INTO articles (url, title, content) VALUES (?, ?, ?)", (url, title, content))
        conn.commit()
        conn.close()
        return render_template('index.html', message="Article added successfully!")

@app.route('/view_notes') 
def view_notes():
    conn = sqlite3.connect('db/knowledge_base.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes ORDER BY created_at DESC")
    notes = c.fetchall()
    conn.close()
    return render_template('view_notes.html', notes=notes)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
