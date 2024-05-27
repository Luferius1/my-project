from flask import request, jsonify, current_app as app
from .models import db, Note

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
