from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = Flask(__name__)

# Создаем подключение к базе данных
engine = create_engine('postgresql://myuser:mypassword@postgres-service/mydb')
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Определяем модель для таблицы заметок
class Note(Base):
    __tablename__ = 'notes'

    note_id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Создаем таблицу, если она еще не существует
Base.metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes', methods=['GET', 'POST', 'DELETE'])
def notes():
    if request.method == 'GET':
        session = Session()
        notes = session.query(Note).all()
        session.close()
        return jsonify([{'note_id': note.note_id, 'title': note.title, 'content': note.content, 'created_at': note.created_at} for note in notes])
    elif request.method == 'POST':
        data = request.json
        title = data.get('title', '')
        content = data.get('content', '')
        if title and content:
            session = Session()
            new_note = Note(title=title, content=content)
            session.add(new_note)
            session.commit()
            session.close()
            return jsonify({'message': 'Note created successfully.'}), 201
        else:
            return jsonify({'error': 'Title and content are required.'}), 400
    elif request.method == 'DELETE':
        data = request.json
        note_ids = data.get('ids', [])
        session = Session()
        for note_id in note_ids:
            note = session.query(Note).filter_by(note_id=note_id).first()
            if note:
                session.delete(note)
        session.commit()
        session.close()
        return jsonify({'message': 'Notes deleted successfully.'})

if __name__ == '__main__':
    app.run(debug=True)