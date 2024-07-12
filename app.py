from flask import Flask,jsonify,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:admin@localhost/BookInventory"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
CORS(app)

class Author(db.Model):
    __tablename__ = 'Author'
    author_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(50), nullable=False)
    author_email = db.Column(db.String(50), nullable=False)
    author_age = db.Column(db.Integer, nullable=False)



class Genre(db.Model):
    __tablename__ = 'Genre'
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(50), nullable=False)



class Editorial(db.Model):
    __tablename__ = 'Editorial'
    editorial_id = db.Column(db.Integer, primary_key=True)
    editorial_name = db.Column(db.String(50), nullable=False)
    editorial_location = db.Column(db.String(50), nullable=False)
    editorial_phone = db.Column(db.String(50), nullable=False)



class Book(db.Model):
    __tablename__ = 'Book'
    ISBN = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), nullable=False)
    editorial_id = db.Column(db.Integer, db.ForeignKey('editorial.editorial_id'), nullable=False)



@app.route('/')
def home():
    return '<h1>Home</h1>'

@app.route("/author")
def getAuthors():
    authors=Author.query.all()
    authors_list=[]
    for author in authors:
        authors_list.append(
            {
                "id": author.author_id,
                "name": author.author_name,
                "email": author.author_email,
                "age": author.author_age
            }
        )
    return jsonify(authors_list),200



@app.route("/genre")
def getGenres():
    genres=Genre.query.all()
    genres_list=[]
    for genre in genres:
        genres_list.append(
            {
                "id": genre.genre_id,
                "name": genre.genre_name
            }
        )
    return jsonify(genres_list),200

@app.route("/editorial")
def getEditorials():
    editorials=Editorial.query.all()
    editorials_list=[]
    for editorial in editorials:
        editorials_list.append(
            {
                "id": editorial.editorial_id,
                "name": editorial.editorial_name,
                "location": editorial.editorial_location,
                "phone": editorial.editorial_phone
            }
        )
    return jsonify(editorials_list),200

@app.route("/book")
def getBooks():
    books=Book.query.all()
    author=Author.query.filter_by(author_id=Book.author_id).first()
    editorial=Editorial.query.filter_by(editorial_id=Book.editorial_id).first()
    genre=Genre.query.filter_by(genre_id=Book.genre_id).first()
    books_list=[]
    for book in books:
        books_list.append(
            {
                "id": book.ISBN,
                "title": book.title,
                "price": book.price,
                "author": {
                    "id": author.author_id,
                    "name": author.author_name
                },
                "genre": {
                    "id": genre.genre_id,
                    "name": genre.genre_name
                },
                "editorial": {
                    "id": editorial.editorial_id,
                    "name": editorial.editorial_name,
                    "location": editorial.editorial_location,
                    "phone": editorial.editorial_phone
                
                }
            }
        )
    return jsonify(books_list),200


@app.route("/book/<int:ISBN>")
def getBook(ISBN):
    book=Book.query.filter_by(ISBN=ISBN).first()
    if book is None:
        return jsonify({"message": "Book not found"}),404
    
    author=Author.query.filter_by(author_id=book.author_id).first()
    editorial=Editorial.query.filter_by(editorial_id=book.editorial_id).first()
    genre=Genre.query.filter_by(genre_id=book.genre_id).first()
    return jsonify({
        "id": book.ISBN,
        "title": book.title,
        "price": book.price,
        "author": {
            "id": author.author_id,
            "name": author.author_name
        },
        "genre": {
            "id": genre.genre_id,
            "name": genre.genre_name
        },
        "editorial": {
            "id": editorial.editorial_id,
            "name": editorial.editorial_name,
            "location": editorial.editorial_location,
            "phone": editorial.editorial_phone
        }
    }),200

@app.route("/book",methods=["POST"])
def createBook():
    try:
        data=request.get_json()
        book=Book()
        book.ISBN=data['ISBN']
        book.title=data['title']
        book.price=data['price']
        book.quantity=data['quantity']
        book.author_id=data['author_id']
        book.genre_id=data['genre_id']
        book.editorial_id=data['editorial_id']
        db.session.add(book)
        db.session.commit()
        return jsonify({"message": "Book created"}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}),500

@app.route("/book/<int:ISBN>",methods=["DELETE"])
def deleteBook(ISBN):
    book=Book.query.filter_by(ISBN=ISBN).first()
    if book is None:
        return jsonify({"message": "Book not found"}),404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}),200



if __name__ == '__main__':
    app.run()
