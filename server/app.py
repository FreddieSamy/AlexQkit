from flask import Flask, request,jsonify
#from datetime import datetime
from flask_cors import CORS
from qiskit import *
from circuit import Circuit
from results import Results
from features import Features
from booleanExpression import Booleanfunction

#startTime = datetime.now()

# configuration
DEBUG = True

# intiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
CORS_DEBUG=1


c=Circuit()
f=Features()
r=Results(c.circuit)

###############################################################################################################################

@app.route('/')
def main():
    return "server is on fire"

###############################################################################################################################
    
@app.route('/draggableCircuit',methods=['GET','POST'])
def draggableCircuit():
    if request.method=='POST':
        receivedDictionary=request.get_json()
        c.setter(receivedDictionary)
        circuit=c.createDraggableCircuit()
        r.setter(receivedDictionary["shots"],receivedDictionary["API_TOKEN"],receivedDictionary["device"],circuit)
        returnedDictionary=r.draggableCircuitResults()
    else:
        returnedDictionary={}
    return  jsonify(returnedDictionary) 

###############################################################################################################################
    
@app.route('/qasm',methods=['GET','POST'])
def qasm():
    if request.method=='POST':
        receivedDictionary=request.get_json()
        try:
            c.shots=receivedDictionary["shots"]
            circuit=c.createQasmCircuit(receivedDictionary["qasm"])
            r.setCircuit(circuit)
            returnedDictionary=r.qasmCircuitResults()
        except Exception as e:
            return jsonify({"qasmError":str(e)})
    else:
        returnedDictionary={}
    returnedDictionary["qasmError"]=""
    return  jsonify(returnedDictionary) 
###############################################################################################################################
@app.route('/circuit.png',methods=['GET','POST'])
def circuitDraw():
    return  r.circutDrawing

@app.route('/blochsphere.png',methods=['GET','POST'])
def defaultBlochSphere():
    return  r.defaultBlochSphere

@app.route('/blochsphere.png/<i>',methods=['GET','POST'])
def blochSphere(i):
    return r.blochSpheres[int(i)-1]
"""
@app.route('/chart.png',methods=['GET','POST'])
def chart():
    return graphDrawing(c.histoGramGraph)

"""
###############################################################################################################################

@app.route('/matrixRepresentation',methods=['GET','POST'])
def matrixRepresentation():
    if request.method=='POST':
        r=Results(c.circuit)
        matrix=r.matrixRepresentation()
        matrix=c.reversedMatrix(matrix,c.num_qubits)
        returnedDictionary={"matrixRepresentation":matrix}
    else:
        returnedDictionary={}
    return  jsonify(returnedDictionary) 

###############################################################################################################################
    
@app.route('/addCustomGates',methods=['GET','POST'])
def addCustomGates():
    from qiskit.quantum_info.operators.predicates import is_unitary_matrix
    from math import log2
    receivedDictionary=request.get_json()
    matrix=receivedDictionary["matrix"]
    matrix=f.strToComplex(matrix)
    isUnitary=is_unitary_matrix(matrix)
    if isUnitary:
        matrix=c.reversedMatrix(matrix,int(log2(len(matrix))))
        c.customGates[receivedDictionary["gateName"]]=matrix
    return jsonify({"isUnitary":isUnitary})

###############################################################################################################################
    
@app.route('/subCircuitCustomGate',methods=['GET','POST'])
def subCircuitCustomGate():
    from qiskit.quantum_info.operators.predicates import is_unitary_matrix
    from math import log2
    if request.method=='POST':
        receivedDictionary=request.get_json()
        c2=Circuit()
        c2.subCircuitSetter(receivedDictionary)
        circuit=c2.createDraggableCircuit()
        r=Results(circuit)
        matrix=r.matrixRepresentation()
        isUnitary=is_unitary_matrix(f.strToComplex(matrix))
        if isUnitary:
            c.customGates[receivedDictionary["gateName"]]=matrix
            matrix=c.reversedMatrix(matrix,int(log2(len(matrix))))
            return  jsonify({"isUnitary":isUnitary,"matrix":f.complexToStr(matrix)}) 
        else:
            return  jsonify({"isUnitary":isUnitary})
    return  jsonify({})

###############################################################################################################################
    
@app.route('/nthRoot',methods=['GET','POST'])
def nthRoot():
    import numpy as np
    from qiskit.quantum_info.operators.predicates import is_unitary_matrix
    from scipy.linalg import fractional_matrix_power
    from math import log2
    if request.method=='POST':
        receivedDictionary=request.get_json()
        root=receivedDictionary["root"]
        gate=receivedDictionary["gateName"]
        if gate in c.customGates:
            a=np.matrix(c.customGates[gate])
        else:
            a=np.matrix(c.gateToMatrix(gate.lower()))
            gate=gate.upper()
        matrix=fractional_matrix_power(a,1/int(root)).tolist()
        isUnitary=is_unitary_matrix(matrix)
        if isUnitary:
            c.customGates[gate+"^(1/"+root+")"]=matrix
            matrix=c.reversedMatrix(matrix,int(log2(len(matrix))))
            return  jsonify({"isUnitary":isUnitary,"matrix":f.complexToStr(matrix)}) 
        else:
            return  jsonify({"isUnitary":isUnitary})
    return  jsonify({})

###############################################################################################################################
    
@app.route('/elementaryGates',methods=['GET','POST'])
def elementaryGates():
    from math import log2
    if request.method=='POST':
        receivedDictionary=request.get_json()
        rows,newGates=f.elementaryGates(receivedDictionary["rows"],c)
        gates={}
        for (name,matrix) in newGates.items():
            gates[name]=c.reversedMatrix(matrix.copy(),int(log2(len(matrix))))
            gates[name]=f.complexToStr(matrix.copy())
        returnedDictionary={"rows":rows,"custom":gates}
        
    else:
        returnedDictionary={}
    return  jsonify(returnedDictionary) 

###############################################################################################################################
    
@app.route('/booleanExpression',methods=['GET','POST'])
def booleanExpress():
    if request.method=='POST':
        recievedData = request.get_json()
        print(recievedData)
        booleanCircut = Booleanfunction.buildBooleanCircuit(recievedData["vars"],recievedData['fn'])
    return jsonify(booleanCircut)

###############################################################################################################################
    
if __name__ == "__main__":
    app.run(debug=True)

#print(datetime.now() - startTime)