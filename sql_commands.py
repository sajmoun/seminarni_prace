CREATE_USERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
'''

CREATE_BOOKS_TABLE = '''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        author TEXT,
        year INTEGER,
        genre TEXT,
        content TEXT,
        notes TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
'''

INSERT_USER = 'INSERT INTO users (username, password) VALUES (?, ?)'

SELECT_USER_BY_CREDENTIALS = 'SELECT * FROM users WHERE username = ? AND password = ?'

INSERT_BOOK = 'INSERT INTO books (user_id, title, author, year, genre, content, notes) VALUES (?, ?, ?, ?, ?, ?, ?)'

SELECT_BOOK_BY_ID_AND_USER = 'SELECT * FROM books WHERE id = ? AND user_id = ?'

DELETE_USER_BY_ID = 'DELETE FROM users WHERE id = ?'
DELETE_BOOKS_BY_USER_ID = 'DELETE FROM books WHERE user_id = ?'

SELECT_BOOKS_BY_AUTHOR_AND_USER = 'SELECT id, title FROM books WHERE user_id = ? AND author = ?'
SELECT_BOOKS_BY_USER = 'SELECT id, title FROM books WHERE user_id = ?'

DELETE_BOOK_BY_ID_AND_USER = 'DELETE FROM books WHERE id = ? AND user_id = ?'
