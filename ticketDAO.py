"""database interaction for CS tickets"""

import mysql.connector
import appconfig as cfg # import a config file "dbconfig.py"
class TicketDAO:
  db = ""

  def __init__(self):
    self.db = mysql.connector.connect(
    host=cfg.mysql['host'],
    user=cfg.mysql['username'],
    password=cfg.mysql['password'],
    database=cfg.mysql['database']
    )

  def create(self, values):
    cursor = self.db.cursor()
    sql = "insert into tickets (company, description, priority, ownerid) values (%s, %s, %s, rand()*(5-1)+1)" # assign ticket to one of 5 onwers at random
    cursor.execute(sql, values)

    self.db.commit() # send to database
    return cursor.lastrowid

  def getAll(self):
    cursor = self.db.cursor()
    sql = "select tickets.id, tickets.company, tickets.description, tickets.priority, concat(owners.firstname,' ', owners.lastname) as owner from tickets left join owners on tickets.ownerid=owners.owner_id"
    cursor.execute(sql)
    results = cursor.fetchall() # get from database
    returnArray = []
    for result in results:
      returnArray.append(self.convertToDictionary(result))
    return returnArray

  def findByID(self, id):
    cursor = self.db.cursor()
    sql = "select tickets.id, tickets.company, tickets.description, tickets.priority, concat(owners.firstname, ' ', owners.lastname) as owner  from tickets left join owners on tickets.ownerid=owners.owner_id where id = %s"
    values = (id,) # values must be a tuple, hence the comma

    cursor.execute(sql,values)
    result = cursor.fetchone()
    return self.convertToDictionary(result) #######

  def update(self, values):
    cursor = self.db.cursor()
    sql="update tickets set company = %s, description=%s, priority=%s where id = %s"
    cursor.execute(sql,values)
    self.db.commit()

  def delete(self, id):
    cursor = self.db.cursor()
    sql="delete from tickets where id = %s"
    values = (id,)
    cursor.execute(sql, values)
    self.db.commit()
    print("delete done")

  def getCount(self): # get the count of ticket by priority for pie chart
    cursor = self.db.cursor()
    sql = "select count(id) as count, Priority from tickets group by Priority"
    cursor.execute(sql)
    results = cursor.fetchall() # get from database
    returnArray = []
    for result in results:
      returnArray.append(self.countsToDict(result))
    return returnArray

  def getCountPerOwner(self): # get the count of ticket by priority for pie chart
    cursor = self.db.cursor()
    sql = "select owners.owner_id, owners.firstname, count(tickets.id) as counts from owners inner join tickets on owners.owner_id=tickets.ownerid group by owners.firstname"
    cursor.execute(sql)
    results = cursor.fetchall() # get from database
    returnArray = []
    for result in results:
      returnArray.append(self.ownercountsToDict(result))
    return returnArray

  def convertToDictionary(self, result):
    colnames=['id','Company','Description', 'Priority', 'Owner']
    item = {}

    if result:
      for i, colName in enumerate(colnames):
        value = result[i]
        item[colName] = value
    return item

  def countsToDict(self, result):
    colnames=['count', 'Priority']
    item = {}
    if result:
      for i, colName in enumerate(colnames):
        value = result[i]
        item[colName] = value
    return item

  def ownercountsToDict(self, result):
    colnames=['id','firstname', 'counts']
    item = {}
    if result:
      for i, colName in enumerate(colnames):
        value = result[i]
        item[colName] = value
    return item

ticketDAO = TicketDAO()
