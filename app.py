from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Создаем экземпляр приложения Flask
app = Flask(__name__)

# Настройки базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем расширение SQLAlchemy
db = SQLAlchemy(app)

# Модель для заметок
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Note {self.title}>'

# Маршруты для создания и получения заметок
@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([{'id': note.id, 'title': note.title, 'content': note.content} for note in notes])

@app.route('/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    new_note = Note(title=data['title'], content=data['content'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'id': new_note.id, 'title': new_note.title, 'content': new_note.content}), 201

if __name__ == '__main__':
    # Создаем таблицы базы данных, если их нет
    db.create_all()
    # Запускаем сервер Flask
    app.run(host='0.0.0.0', port=5000)
