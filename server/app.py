from flask import Flask, jsonify, render_template, request
import time
from datetime import datetime
import json

import uuid
from flask_cors import CORS
startTime = datetime.now()

from functions import Circuit

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
CORS_DEBUG=1


BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]


def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/mario')
@app.route('/mario', methods=['POST','GET'] )
def mario():
    import json

    #print(post_data[0])
    #c=Circuit()
    #print(c)
    #dic=c.createCircuit(json.loads(post_data[0]))
    #print(dic)
    #return json.dumps(dic)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        
        post_data = request.get_json()
        print(type(post_data))
        print(post_data[0])
        c=Circuit()
        dic = c.createCircuit(json.loads(post_data[0]))
        print(dic)
        #response_object['message'] = 'succes to reach here'
    else:
        response_object['books'] = "reached but cant get te object"
    return jsonify(response_object)


@app.route('/mario2')
def mario2():
    return "mario"


@app.route('/q', methods=['POST','GET'])
def q():
    post_data = request.get_json()
    return jsonify(post_data)




@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)









@app.route("/")
def main():
    return render_template('main.html', reload = time.time())

@app.route("/api/info")
def api_info():
    info = {
       "ip" : "127.0.0.1",
       "hostname" : "everest",
       "description" : "Main server",
       "load" : [ 3.21, 7, 14 ]
    }
    return jsonify(info)

@app.route("/api/calc")
def add():
    a =json.loads(request.args.get('a', 0))
    #c=Circuit()
    #dic=c.createCircuit(a)
    b=a["data"]
    for i in range(len(b)):
        b[i]=b[i]*2
    return jsonify(b)

     
#dic={"qasm":'OPENQASM 2.0;include "qelib1.inc";qreg q1[2];creg c1[2];x q1[0];cx q1[0],q1[1];measure q1[0] -> c1[0];measure q1[1] -> c1[1];'}



'''{"wires":2,"cols":[["h"],["c","x"]]}


{
     "wires":6,
     "cols":[["h"],
             ["x"],
             ["y"],
             ["z"],
             ["s"],
             ["sdg"],
             ["t"],
             ["tdg"],
             ["barrier"],
             ["","swap","swap"],
             ["","c","x"],
             ["","oc","x"],
             ["barrier"],
             ["","","","c","swap","swap"],
             ["","","","oc","swap","swap"],
             ["","","","c","c","x"],
             ["","","","oc","oc","x"],
             ["barrier"],
             ["","","c","c","swap","swap"],
             ["","","oc","oc","swap","swap"],
             ["","","c","c","c","x"],
             ["","","oc","oc","oc","x"],
             ["barrier"],
             ["","","","","","custom_not"],
             ["","","","custom_I4.0","","custom_I4.1"],
             ["barrier"],
             ["","","","","c","custom_not"],
             ["","","c","custom_I4.0","c","custom_I4.1"],
             ["barrier"],
             ["","","","","oc","custom_not"],
             ["","","oc","custom_I4.0","oc","custom_I4.1"],
             ["barrier"],
             ["m","m","m","m","m","m"]
             ],
     "init":[0,1,"+","-","i","-i"],
     "shots":2048,
     "custom":{
               "not":[[0,1],[1,0]],
               "I4":[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
               }
     }'''

#print(startTime)
print(datetime.now() - startTime)
