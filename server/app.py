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


@app.route('/subCircuitCustomGate',methods=['GET','POST'])
def subCircuitCustomGate():
    from qiskit.quantum_info.operators.predicates import is_unitary_matrix
    if request.method=='POST':
        recievedDic=request.get_json()
        c.createCircuit(recievedDic)
        matrix=c.returnedDictionary["matrixRepresentation"]
    else:
        c.returnedDictionary={}
    return  jsonify({"isUnitary":is_unitary_matrix(c.strToComplex(matrix)),"matrix":c.complexToStr(matrix)}) 

@app.route('/nthRoot',methods=['GET','POST'])
def nthRoot():
    import numpy as np
    from qiskit.quantum_info.operators.predicates import is_unitary_matrix
    from scipy.linalg import fractional_matrix_power
    if request.method=='POST':
        jsonObj=request.get_json()
        gate=jsonObj["gate"]
        root=jsonObj["root"]
        if gate in jsonObj["custom"]:
            customGtes=jsonObj["custom"]
            a=np.matrix(c.strToComplex(customGtes[gate]))
        else:
            a=np.matrix(c.gateToMatrix(gate))
        matrix=fractional_matrix_power(a,1/int(root)).tolist()
        #print(is_unitary_matrix(matrix),matrix)
        #print(matrix,is_unitary_matrix(matrix),jsonify({"isUnitary":is_unitary_matrix(matrix)}))
        return jsonify({"isUnitary":is_unitary_matrix(matrix),"matrix":c.complexToStr(matrix)})

@app.route('/elementaryGates',methods=['GET','POST'])
def elementaryGates():
    if request.method=='POST':
        recievedDic=request.get_json()
        returnedDictionary=c.elementaryGates(recievedDic["rows"],recievedDic["custom"])
        #print("retrived data from qiskit : ",c.returnedDictionary)
    else:
        returnedDictionary={}
    return  jsonify(returnedDictionary) 

@app.route('/isUnitary',methods=['GET','POST'])
def isUnitary():
    if request.method=='POST':
        jsonObj=request.get_json()
        matrix=jsonObj["matrix"]
        c.strToComplex(matrix)
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

print(datetime.now() - startTime)
