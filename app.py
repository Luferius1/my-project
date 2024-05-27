from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Создаем подключение к базе данных
# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@postgres-service/mydb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для заметок
class Note(db.Model):
    __tablename__ = 'notes'
    note_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Note {self.title}>'

# Создание таблицы, если она не существует
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    notes_list = [{'title': note.title} for note in notes]
    return jsonify(notes_list)

@app.route('/notes/<note_title>', methods=['GET'])
def get_note_content(note_title):
    note = Note.query.filter_by(title=note_title).first()
    if note:
        return jsonify({"content": note.content})
    return jsonify({"error": "Note not found"}), 404

@app.route('/notes', methods=['POST'])
def save_note():
    note_title = request.json.get('title')
    note_content = request.json.get('content')
    note = Note.query.filter_by(title=note_title).first()
    if note:
        note.content = note_content
    else:
        note = Note(title=note_title, content=note_content)
        db.session.add(note)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/notes/<note_title>', methods=['DELETE'])
def delete_note(note_title):
    note = Note.query.filter_by(title=note_title).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"error": "Note not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
