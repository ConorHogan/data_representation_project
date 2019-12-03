#!flask/bin/python
from flask import Flask, jsonify, request, abort
from bookDAO import bookDAO # file where the functions to interact with the database are stored

app = Flask(__name__,static_url_path='',static_folder='.')

# @app.route('/')
# def index():
#   return "Hello, world"

@app.route('/books')
def getAll():
  results = bookDAO.getAll()
  return jsonify(results)
# C:\Users\Conor>curl "http://127.0.0.1:5000/books"

@app.route('/books/<int:id>')
def findByID(id):
  foundBook = bookDAO.findByID(id)
  return jsonify(foundBook)
# C:\Users\Conor>curl "http://127.0.0.1:5000/books/3"


@app.route('/books', methods=['POST'])
def create():
  if not request.json:
    abort(400)
  # other checking e.g properly formated
  book = {
    "id":nextID,
    "Title":request.json['Title'],
    "Author":request.json['Author'],
    "Price":request.json['Price']
  }
  values = (book['Title'],book['Author'], book['Price'])
  newID = bookDAO.create(values)
  book['id'] = newID
  return jsonify(book)
# curl -i -H "Content-Type:application/json" -X POST -d "{\"Title\":\"hello\",\"Author\":\"someone\",\"Price\":123}" http://127.0.0.1:5000/books


@app.route('/books/<int:id>', methods=['PUT'])
def update(id):
  foundBook = bookDAO.findByID(id)
  if not foundBook:
    abort(404)
  if not request.json:
    abort(400)
  reqJson = request.json
  if 'Price' in reqJson and type(reqJson['Price']) is not int:
    abort(400)
  if 'Title' in reqJson:
    foundBook['Title'] = reqJson['Title']
  if 'Author' in reqJson:
    foundBook['Author'] = reqJson['Author']
  if 'Price' in reqJson:
    foundBook['Price'] = reqJson['Price']
  values = (foundBook['Title'],foundBook['Author'], foundBook['Price'], foundBook['id'])
  bookDAO.update(values)
  return jsonify(foundBook)
# C:\Users\Conor>curl -i -H "Content-Type:application/json" -X PUT -d "{\"Author\":\"Jimmy\"}" http://127.0.0.1:5000/books/1

@app.route('/books/<int:id>', methods=['DELETE'])
def delete(id):
  bookDAO.delete(id)
  return jsonify({"done":True})
# C:\Users\Conor>curl -X DELETE "http://127.0.0.1:5000/books/1"
# {"done":true}

if __name__=='__main__':
  app.run(debug=True)