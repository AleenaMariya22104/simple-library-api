# Library Management API
A basic REST API to manage books, members, and borrowing in a library. This project is built with Flask and uses SQLite as a file-based database.<br>
Language: Python <br>
Framework: Flask <br>
Database: SQLite <br>

## Setup instructions
1. Created a folder simple-library-api, for the project. Inside it, created two files: app.py and requirements.txt <br>
2. Set up the virtual environment using the code: python3 -m venv venv <br>
3. Installed the dependencies using the code: pip install -r requirements.txt <br>
4. Run the Application using the code: python app.py <br>

## API Documentation
The base URL is http://127.0.0.1:5001 <br>
1. Books: <br>
POST /books - Add a new book. <br>
GET /books - List all books. <br>
GET /books/<id> - Get a single book. <br>
DELETE /books/<id> - Delete a book. <br>

2. Members: <br>
POST /members - Add a new member. <br>
GET /members - List all members. <br>

3. Actions: <br>
POST /borrow - Borrow a book. <br>
POST /return - Return a book. <br>
GET /books/borrowed - See all currently borrowed books. <br>

## Sample curl Requests 
1. Add Books: <br>
curl -X POST -H "Content-Type: application/json" -d '{"title": "1984", "author": "George Orwell", "category": "classic", "total_copies": 7}' http://127.0.0.1:5001/books <br>
2. Register Members: <br>
curl -X POST -H "Content-Type: application/json" -d '{"name": "Aleena", "email": "aleena123@gmail.com"}' http://127.0.0.1:5001/members <br>
3. List Books and Members: <br>
curl http://127.0.0.1:5001/books <br>
curl http://127.0.0.1:5001/members <br>
4. Borrow a Book: <br>
curl -X POST -H "Content-Type: application/json" -d '{"book_id": 1, "member_id": 1}' http://127.0.0.1:5001/borrow <br>
5. Get details of a book: <br>
curl http://127.0.0.1:5001/books/1 <br>
6. Get details of currently borrowed books: <br>
curl http://127.0.0.1:5001/books/borrowed <br>
7. Return a Book <br>
curl -X POST -H "Content-Type: application/json" -d '{"book_id": 1, "member_id": 1}' http://127.0.0.1:5001/return <br>
8. Delete a Book with id 2 <br>
curl -X DELETE http://127.0.0.1:5001/books/2 <br>



   


