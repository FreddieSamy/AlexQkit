from flask import Flask, request, Response,jsonify
from datetime import datetime
from flask_cors import CORS
import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from qiskit import *
from functions import Circuit
import time 
startTime = datetime.now()
# configuration
DEBUG = True

# intiate the app
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
c=Circuit()
@app.route('/')
def main():
    return "server is on fire"
# sanity check route
@app.route('/data',methods=['GET','POST'])
def run():
    if request.method=='POST':
        recievedDic=request.get_json()
        print("recieved data from Vue : ",recievedDic[0])
        #c=Circuit()
        c.createCircuit(recievedDic[0])
        print("retrived data from qiskit : ",c.returnedDictionary)
        print(c.returnedDictionary['blochSphere'])
    else:
        c.returnedDictionary=[]
    return  str(c.returnedDictionary) #jsonify(returnedDic) #str(returnedDic)

def graphDrawing(image):
    fig = image
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
@app.route('/blochsphere.png',methods=['GET','POST'])
def blochSphere():
    return graphDrawing(c.returnedDictionary['blochSphere'])
@app.route('/chart.png',methods=['GET','POST'])
def chart():
    return graphDrawing(c.returnedDictionary['graph'])
@app.route('/circuit.png')
def circuitDraw():
    return  graphDrawing(c.returnedDictionary['draw'])
@app.route('/reset',methods=['GET','POST'])
def reset():
    if request.method=='POST':
        recievedDic=request.get_json()
        c.createCircuit(recievedDic[0])
        print(c.returnedDictionary['diracNotation'])
    return "success"
if __name__ == "__main__":
    app.run(debug=True)

#print(c.returnedDictionary)   
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

print(datetime.now() - startTime)
