#!flask/bin/python
from flask import Flask, jsonify, request, abort
from ticketDAO import ticketDAO # file where the functions to interact with the database are stored
app = Flask(__name__,static_url_path='',static_folder='.')


@app.route('/tickets')
def getAll():
  results = ticketDAO.getAll()
  return jsonify(results)
# C:\Users\Conor>curl "http://127.0.0.1:5000/tickets"

@app.route('/tickets/<int:id>')
def findByID(id):
  foundTicket = ticketDAO.findByID(id)
  return jsonify(foundTicket)
# C:\Users\Conor>curl "http://127.0.0.1:5000/tickets/1"

@app.route('/tickets', methods=['POST'])
def create():
  if not request.json:
    abort(400)
  # other checking e.g properly formated
  ticket = {
    "Company":request.json['Company'],
    "Description":request.json['Description'],
    "Priority":request.json['Priority']
  }
  values = (ticket['Company'],ticket['Description'], ticket['Priority'])
  newID = ticketDAO.create(values)
  ticket['id'] = newID
  return jsonify(ticket)
# curl -i -H "Content-Type:application/json" -X POST -d "{\"Company\":\"Google\",\"Description\":\"My tummy hurts\",\"Priority\":\"High\",\"Due Date\":\"2019-10-30\"}" http://127.0.0.1:5000/tickets


@app.route('/tickets/<int:id>', methods=['PUT'])
def update(id):
  foundTicket = ticketDAO.findByID(id)
  if not foundTicket:
    abort(404)
  if not request.json:
    abort(400)
  reqJson = request.json
  # if 'Price' in reqJson and type(reqJson['Price']) is not int:
  #   abort(400)
  if 'Company' in reqJson:
    foundTicket['Company'] = reqJson['Company']
  if 'Description' in reqJson:
    foundTicket['Description'] = reqJson['Description']
  if 'Priority' in reqJson:
    foundTicket['Priority'] = reqJson['Priority']
  values = (foundTicket['Company'],foundTicket['Description'], foundTicket['Priority'],foundTicket['id'])
  ticketDAO.update(values)
  return jsonify(foundTicket)
# C:\Users\Conor>curl -i -H "Content-Type:application/json" -X PUT -d "{\"Due Date\":\"2017-12-05\"}" http://127.0.0.1:5000/tickets/3

@app.route('/tickets/<int:id>', methods=['DELETE'])
def delete(id):
  ticketDAO.delete(id)
  return jsonify({"done":True})
# C:\Users\Conor>curl -X DELETE "http://127.0.0.1:5000/tickets/3"
# {"done":true}

@app.route('/counts') # gives counts of tickets by priority for piechart
def getCounts():
  results = ticketDAO.getCount()
  return jsonify(results)

@app.route('/countsperowner') # gives counts of tickets by owner
def getCountperOwner():
  results = ticketDAO.getCountPerOwner()
  return jsonify(results)

if __name__=='__main__':
  app.run(debug=True)