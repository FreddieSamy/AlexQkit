from flask import Flask, request
from datetime import datetime
from flask_cors import CORS

startTime = datetime.now()

from qiskit import *
from functions import Circuit

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
CORS_DEBUG=1

#testing
"""
c=Circuit()
print(c.createCircuit({"wires":2,"rows": [['h'], ['i'], ['i'], ['i']]}))
"""

# sanity check route
@app.route('/')
def main():
    return "Server is on fire"


@app.route('/data',methods=['GET','POST'])
def run():
    if request.method=='POST':
        recievedDic=request.get_json()
        #print("recieved data in python : ",recievedDic[0])
        c=Circuit()
        returnedDic=c.createCircuit(recievedDic[0])
        #print("recieved data in python : ",returnedDic)
    else:
        returnedDic=[]
    return str(returnedDic) #jsonify(recievedDic[0])

     
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
#print(datetime.now() - startTime)
app.run(debug=True)