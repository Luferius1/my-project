document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;

    function toggleTheme() {
        body.classList.toggle('dark-theme');
        body.classList.toggle('light-theme');
    }

    // Привязываем функцию к кнопке
    document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

    // Функции для работы с заметками
    function addNote() {
        const currentNoteInput = document.getElementById('note-title');
        const currentNoteContent = document.getElementById('note-content');
        const newNoteTitle = currentNoteInput.value;
        const newNoteContent = currentNoteContent.value;

        if (newNoteTitle.trim() !== '' && newNoteContent.trim() !== '') {
            // Отправляем данные на сервер
            fetch('/notes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    title: newNoteTitle,
                    content: newNoteContent
                })
            })
            .then(response => {
                if (response.ok) {
                    // Обновляем отображение заметок на странице
                    loadNotes();
                    // Очищаем поля ввода
                    currentNoteInput.value = '';
                    currentNoteContent.value = '';
                } else {
                    console.error('Ошибка при добавлении заметки:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Ошибка при отправке запроса:', error);
            });
        }
    }

    function deleteNote() {
        const checkedCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
        const noteIds = Array.from(checkedCheckboxes).map(checkbox => parseInt(checkbox.id.split('-')[1]));

        // Отправляем данные на сервер
        fetch('/notes', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ids: noteIds
            })
        })
        .then(response => {
            if (response.ok) {
                // Обновляем отображение заметок на странице
                loadNotes();
            } else {
                console.error('Ошибка при удалении заметок:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Ошибка при отправке запроса:', error);
        });
    }

    function deleteAllNotes() {
        // Отправляем запрос на сервер для удаления всех заметок
        fetch('/notes', {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                // Обновляем отображение заметок на странице
                loadNotes();
            } else {
                console.error('Ошибка при удалении всех заметок:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Ошибка при отправке запроса:', error);
        });
    }

    function loadNotes() {
        // Отправляем запрос на сервер для получения списка заметок
        fetch('/notes')
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Ошибка при получении списка заметок:', response.statusText);
            }
        })
        .then(notes => {
            const notesContainer = document.getElementById('notes-list');
            notesContainer.innerHTML = '';

            // Отображаем заметки на странице
            notes.forEach(note => {
                const newNoteItem = document.createElement('li');
                newNoteItem.innerHTML = `
                    <input type="checkbox" id="note-${note.note_id}" name="note-${note.note_id}">
                    <label for="note-${note.note_id}">
                        <strong>${note.title}</strong><br>
                        <span>${note.content}</span><br>
                        <small>${note.created_at}</small>
                    </label>`;
                notesContainer.appendChild(newNoteItem);
            });
        })
        .catch(error => {
            console.error('Ошибка при обработке ответа:', error);
        });
    }

    // Привязываем функции к соответствующим кнопкам
    document.getElementById('add-note').addEventListener('click', addNote);
    document.getElementById('delete-note').addEventListener('click', deleteNote);
    document.getElementById('delete-all-notes').addEventListener('click', deleteAllNotes);

    // Загружаем существующие заметки при загрузке страницы
    loadNotes();
});
