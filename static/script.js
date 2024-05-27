document.addEventListener('DOMContentLoaded', () => {
    loadNotes();
});

function loadNotes() {
    fetch('/notes')
        .then(response => response.json())
        .then(data => {
            const notesList = document.getElementById('notes');
            notesList.innerHTML = '';
            data.forEach(note => {
                const li = document.createElement('li');
                li.textContent = note;
                li.classList.add('list-group-item');
                li.onclick = () => loadNoteContent(note);
                notesList.appendChild(li);
            });
        });
}

function newNote() {
    document.getElementById('note-name').value = '';
    document.getElementById('note-content').value = '';
}

function loadNoteContent(noteName) {
    fetch(`/notes/${noteName}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('note-name').value = noteName;
                document.getElementById('note-content').value = data.content;
            }
        });
}

function saveNote() {
    const noteName = document.getElementById('note-name').value;
    const noteContent = document.getElementById('note-content').value;

    fetch('/notes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: noteName, content: noteContent })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadNotes();
            alert('Note saved successfully');
        } else {
            alert('Error saving note');
        }
    });
}

function deleteNote() {
    const noteName = document.getElementById('note-name').value;

    fetch(`/notes/${noteName}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadNotes();
            newNote();
            alert('Note deleted successfully');
        } else {
            alert(data.error);
        }
    });
}
