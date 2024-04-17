from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# Функция для подключения к базе данных PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            host="postgres-myapp",
            database="myapp",
            user="postgres",
            password="postgres"
        )
        return conn
    except psycopg2.Error as e:
        print("Ошибка при подключении к базе данных PostgreSQL:", e)
        return None

# Функция для получения списка всех заметок из базы данных
def get_notes():
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT id, title, content, created_at FROM notes")
        notes = [{'id': row[0], 'title': row[1], 'content': row[2], 'created_at': row[3]} for row in cur.fetchall()]
        conn.close()
        return notes
    else:
        return []

# Функция для добавления новой заметки в базу данных
def add_note(title, content):
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        cur.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()
        conn.close()

# Функция для удаления заметок из базы данных по их идентификаторам
def delete_notes(id):
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        for id in id:
            cur.execute("DELETE FROM notes WHERE id = %s", (id,))
        conn.commit()
        conn.close()

def delete_all_notes():
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        cur.execute("DELETE FROM notes")
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes', methods=['GET', 'POST', 'DELETE'])
def notes():
    if request.method == 'GET':
        notes = get_notes()
        return jsonify(notes)
    elif request.method == 'POST':
        data = request.json
        title = data.get('title', '')
        content = data.get('content', '')
        if title and content:
            add_note(title, content)
            return jsonify({'message': 'Note created successfully.'}), 201
        else:
            return jsonify({'error': 'Title and content are required.'}), 400
    elif request.method == 'DELETE':
        data = request.json
        note_ids = data.get('ids', [])
        delete_notes(ids)
        return jsonify({'message': 'Notes deleted successfully.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
