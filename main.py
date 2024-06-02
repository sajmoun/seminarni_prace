import sqlite3
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.middleware.sessions import SessionMiddleware
from starlette.status import HTTP_303_SEE_OTHER
from fastapi.staticfiles import StaticFiles
from sql_commands import *

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='your-secret-key')
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

# Vytvoření databáze a tabulek
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(CREATE_USERS_TABLE)
    cursor.execute(CREATE_BOOKS_TABLE)
    conn.commit()
    conn.close()

init_db()

# Funkce pro získání knihy z databáze
def get_book_by_id(book_id: int, user_id: int):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(SELECT_BOOK_BY_ID_AND_USER, (book_id, user_id))
    book = cursor.fetchone()
    conn.close()
    return book

# Endpointy
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute(INSERT_USER, (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return templates.TemplateResponse("index.html", {"request": request, "error": "User already exists"})
    conn.close()
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(SELECT_USER_BY_CREDENTIALS, (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        request.session['user_id'] = user[0]
        return RedirectResponse("/welcome", status_code=HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid username or password"})

@app.get("/welcome", response_class=HTMLResponse)
async def welcome(request: Request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("welcome.html", {"request": request})

@app.post("/add_book")
async def add_book(request: Request, title: str = Form(...), author: str = Form(...), year: str = Form(...), genre: str = Form(...), content: str = Form(...), notes: str = Form(...)):
    user_id = request.session.get('user_id')
    if user_id is None:
        return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(INSERT_BOOK, (user_id, title, author, year, genre, content, notes))
    conn.commit()
    conn.close()
    return RedirectResponse("/welcome", status_code=HTTP_303_SEE_OTHER)

@app.get("/book/{book_id}", response_class=HTMLResponse)
async def book_detail(request: Request, book_id: int):
    user_id = request.session.get('user_id')
    book = get_book_by_id(book_id, user_id)
    if book is None:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Knihu nelze nalézt"})
    return templates.TemplateResponse("detail.html", {"request": request, "book": book})

@app.post("/logout")
async def logout(request: Request):
    request.session.pop('user_id', None)
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)

@app.post("/delete_account")
async def delete_account(request: Request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(DELETE_USER_BY_ID, (user_id,))
        cursor.execute(DELETE_BOOKS_BY_USER_ID, (user_id,))
        conn.commit()
        conn.close()
        request.session.pop('user_id', None)
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)

@app.get("/books", response_class=HTMLResponse)
async def list_books(request: Request, author: str = None):
    user_id = request.session.get('user_id')
    if user_id is None:
        return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    if author:
        cursor.execute(SELECT_BOOKS_BY_AUTHOR_AND_USER, (user_id, author))
        books = cursor.fetchall()
        return templates.TemplateResponse("book_list.html", {"request": request, "books": books, "filter_active": True, "filter_author": author})
    else:
        cursor.execute(SELECT_BOOKS_BY_USER, (user_id,))
        books = cursor.fetchall()
        return templates.TemplateResponse("book_list.html", {"request": request, "books": books, "filter_active": False})
    conn.close()

@app.post("/delete_book/{book_id}")
async def delete_book(request: Request, book_id: int):
    user_id = request.session.get('user_id')
    if user_id is None:
        return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(DELETE_BOOK_BY_ID_AND_USER, (book_id, user_id))
    conn.commit()
    conn.close()
    return RedirectResponse("/books", status_code=HTTP_303_SEE_OTHER)
