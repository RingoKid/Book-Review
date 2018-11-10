import os
import requests
import bcrypt

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

    error = None
    if not username:
        error = "Username is required."
    elif not password:
        error = "Password is required."

    name = db.execute("SELECT password FROM users WHERE username = '{}';".format(username)).fetchone()

    if name['password']:
        print(name['password'])


    return render_template('index.html', error=error)

@app.route("/signup", methods=['POST'])
def signup():

    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

    pword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    check_name = db.execute("SELECT COUNT(*) FROM users WHERE username='{}'".format(username)).fetchone()

    if check_name[0] != 0:
        error = "{} taken.".format(username)

    if error == None:
        db.execute("INSERT INTO users (name, username, email, password) VALUES ('{}', '{}', '{}', '{}');".format(name, username, email, pword.decode()))
        db.commit()

    return render_template("signup.html")

@app.route("/home", methods=["POST"])
def home():
    return render_template("home.html", username=username, error=error)


@app.route("/books")
def books():
    # book = db.execute("SELECT * FROM books ORDER BY isbn FETCH FIRST 10 ROWS ONLY")
    book = db.execute("SELECT * FROM books ORDER BY id LIMIT 15")
    activate=1

    return render_template("books.html", books=book, activate=activate,p=[1,2,3,4,5])

@app.route("/books/<int:num>")
def book_details(num):
    #Database
    book = db.execute("SELECT * FROM books WHERE id = :id",{"id": num}).fetchone()
    isbn = book['isbn']
    #Google API
    req = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:{}".format(isbn))

    if req.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    res = req.json()

    #GoodReads API
    KEY  = "rzRtpIoujeKZ5rD5q8qA"
    read = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn})
    read = read.json()
    print(read)
    read['books'][0]['percent_rating'] = (float(read['books'][0]['average_rating'])/5)*100

    return render_template("book_details.html", books=book, res=res, read=read)

@app.route("/books/pages/<int:page>")
def book_pages(page):
    book = db.execute("SELECT * FROM books ORDER by id OFFSET :page LIMIT 15",{"page": (page-1)*15})
    if 332 >= page >= 4 :
        initial = [page-2, page-1, page, page+1, page+2]
    elif page >= 332:
        initial = [330,331,332,333,334]
    else:
        initial = [1,2,3,4,5]

    return render_template("books.html", books=book, activate=page, p=initial)
    # return render_template("books.html", books=book, activate=page)

@app.route("/about")
def about():
    return render_template("about.html")

def isyear(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

@app.route("/search", methods=['POST'])
def search():
    book = request.form.get("note")
    # result.append(db.execute("SELECT * FROM books WHERE title LIKE '%{}%'".format(book.title())))

    if len(str(book))==4 and isyear(book):
        result = db.execute("SELECT * FROM books WHERE year = {} LIMIT 15".format(int(book)))
    else:
        result = (db.execute("SELECT * FROM books WHERE title LIKE '%{}%' UNION SELECT * FROM books WHERE author LIKE '%{}%' UNION SELECT * FROM books WHERE isbn = '{}' LIMIT 15".format(book.title(), book.title(), book)))
    return render_template("search.html", result=result)
