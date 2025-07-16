from flask import Flask, request, jsonify # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Models ---

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    total_copies = db.Column(db.Integer, nullable=False)
    available_copies = db.Column(db.Integer, nullable=False)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class BorrowedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)

    book = db.relationship('Book')
    member = db.relationship('Member')

with app.app_context():
    db.create_all()

# --- Book Management ---

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        category=data['category'],
        total_copies=data['total_copies'],
        available_copies=data['total_copies']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'New book added!'}), 201

@app.route('/books', methods=['GET'])
def list_books():
    all_books = Book.query.all()
    output = []
    for book in all_books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'available_copies': book.available_copies
        }
        output.append(book_data)
    return jsonify({'books': output})

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    book_data = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'category': book.category,
        'total_copies': book.total_copies,
        'available_copies': book.available_copies
    }
    return jsonify(book_data)

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted.'})

# --- Member Management ---

@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    new_member = Member(name=data['name'], email=data['email'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'New member added!'}), 201

@app.route('/members', methods=['GET'])
def list_members():
    members = Member.query.all()
    output = []
    for member in members:
        member_data = {'id': member.id, 'name': member.name, 'email': member.email}
        output.append(member_data)
    return jsonify({'members': output})

# --- Borrow / Return Flow ---

@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()
    book_id = data['book_id']
    member_id = data['member_id']

    book = Book.query.get(book_id)
    member = Member.query.get(member_id)

    if not book or not member:
        return jsonify({'error': 'Book or Member not found'}), 404

    if book.available_copies < 1:
        return jsonify({'error': 'No copies available to borrow'}), 400

    new_borrow = BorrowedBook(book_id=book.id, member_id=member.id)
    book.available_copies = book.available_copies - 1
    
    db.session.add(new_borrow)
    db.session.commit()
    return jsonify({'message': 'Book borrowed successfully.'})

@app.route('/return', methods=['POST'])
def return_book():
    data = request.get_json()
    book_id = data['book_id']
    member_id = data['member_id']
    
    borrow_record = BorrowedBook.query.filter_by(
        book_id=book_id,
        member_id=member_id,
        return_date=None
    ).first()

    if not borrow_record:
        return jsonify({'error': 'Borrow record not found'}), 404

    book = Book.query.get(book_id)
    book.available_copies = book.available_copies + 1
    borrow_record.return_date = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Book returned successfully.'})

# --- Reports ---

@app.route('/books/borrowed', methods=['GET'])
def list_borrowed_books():
    borrowed_records = BorrowedBook.query.filter(BorrowedBook.return_date.is_(None)).all()
    
    output = []
    for record in borrowed_records:
        record_data = {
            'book_title': record.book.title,
            'member_name': record.member.name,
            'borrow_date': record.borrow_date.strftime('%Y-%m-%d')
        }
        output.append(record_data)
        
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True, port=5001)