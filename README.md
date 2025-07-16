# Library Management API
A basic REST API to manage books, members, and borrowing in a library. This project is built with Flask and uses SQLite as a file-based database.<br>
Language: Python <br>
Framework: Flask <br>
Database: SQLite <br>

## Setup instructions
1. Created a folder simple-library-api for the project. Inside it, createed two files app.py and requirements.txt <br>
2. Set Up the virtual environment using the code : python3 -m venv venv <br>
3. Installed the dependencies using the code: pip install -r requirements.txt <br>
4. Run the Application using the code: python app.py <br>

## API Documentation

## Sample curl Requests 
1. Add Books: <br>
curl -X POST -H "Content-Type: application/json" -d '{"title": "1984", "author": "George Orwell", "category": "classic", "total_copies": 7}' http://127.0.0.1:5001/books <br>
2. Register Members: <br>
curl -X POST -H "Content-Type: application/json" -d '{"name": "Aleena", "email": "aleena123@gmail.com"}' http://127.0.0.1:5001/members <br>
3. List Books and Members: <br>
curl http://127.0.0.1:5001/books
curl http://127.0.0.1:5001/members

   


