from flask import Flask, request, Response,jsonify
from datetime import datetime
from flask_cors import CORS
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from qiskit import *
from functions import Circuit
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
intialState = {'wires': 3, 'init': ['0', '0','0'], 'rows': [[], [],[]]}
c=Circuit()
c.createCircuit(intialState)
def graphDrawing(fig):
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
@app.route('/')
def main():
    return "server is on fire"

@app.route('/elementaryGates',methods=['GET','POST'])
def elementaryGates():
    if request.method=='POST':
        recievedDic=request.get_json()
        returnedDictionary=c.elementaryGates(recievedDic["rows"])
        #print("retrived data from qiskit : ",c.returnedDictionary)
    else:
        returnedDictionary={}
    return  jsonify(returnedDictionary) 
@app.route('/isUnitary',methods=['GET','POST'])
def isUnitary():
    if request.method=='POST':
        jsonObj=request.get_json()
        matrix=jsonObj["matrix"]
        from qiskit.quantum_info.operators.predicates import is_unitary_matrix
        #print(matrix,is_unitary_matrix(matrix),jsonify({"isUnitary":is_unitary_matrix(matrix)}))
        return jsonify({"isUnitary":is_unitary_matrix(matrix)})
# sanity check route
@app.route('/data',methods=['GET','POST'])
def run():
    if request.method=='POST':
        recievedDic=request.get_json()
        #print("recieved data from Vue : ",recievedDic[0])
        #print(recievedDic)
        if "qasm" in recievedDic:
            try:
                c.qasm(recievedDic)
            except Exception as e:
                return jsonify({"qasmError":str(e)});
        else:
            c.createCircuit(recievedDic)
        #print("retrived data from qiskit : ",c.returnedDictionary)
    else:
        c.returnedDictionary={}
    c.returnedDictionary["qasmError"]="";
    return  jsonify(c.returnedDictionary) 
@app.route('/blochsphere.png',methods=['GET','POST'])
def blochSphere():
    return graphDrawing(c.blochSphereGraph)
@app.route('/chart.png',methods=['GET','POST'])
def chart():
    return graphDrawing(c.histoGramGraph)

@app.route('/circuit.png',methods=['GET','POST'])
def circuitDraw():
    return  graphDrawing(c.circutDrawing)
@app.route('/reset',methods=['GET','POST'])
def reset():
    if request.method=='POST':
        recievedDic=request.get_json()
        c.createCircuit(recievedDic[0])
        #print(c.returnedDictionary['diracNotation'])
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
