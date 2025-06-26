from flask import Flask, jsonify, request
from flask_cors import CORS  # Optional: for cross-origin requests (frontend)

app = Flask(__name__)
CORS(app)  # Optional: remove if not needed

# 🧠 In-memory "database"
books = [
    {'id': 1, 'title': 'Book 1', 'author': 'Author 1'},
    {'id': 2, 'title': 'Book 2', 'author': 'Author 2'},
    {'id': 3, 'title': 'Book 3', 'author': 'Author 3'}
]

# 🟢 Home Route
@app.route('/')
def home():
    return "<h2>Flask Book API</h2><p>Try GET /books</p>"

# 🔍 READ ALL
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

# 🔍 READ ONE
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({'error': 'Book not found'}), 404

# 📝 CREATE
@app.route('/books', methods=['POST'])
def create_book():
    if not request.json or 'title' not in request.json or 'author' not in request.json:
        return jsonify({'error': 'Bad Request'}), 400
    
    new_id = max(b['id'] for b in books) + 1 if books else 1
    new_book = {
        'id': new_id,
        'title': request.json['title'],
        'author': request.json['author']
    }
    books.append(new_book)
    return jsonify(new_book), 201

# 🛠️ UPDATE
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    book['title'] = request.json.get('title', book['title'])
    book['author'] = request.json.get('author', book['author'])
    return jsonify(book), 200

# 🗑️ DELETE
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    books.remove(book)
    return jsonify({'message': 'Book deleted'}), 200

# 🚀 Run Server
if __name__ == '__main__':
    app.run(debug=True)
