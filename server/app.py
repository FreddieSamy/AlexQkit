#from datetime import datetime

from flask import Flask, request,jsonify
from flask_cors import CORS

from circuit import Circuit
from results import Results
from features import Features
from booleanExpression import BooleanFunction

#from qiskit import *
from qiskit.quantum_info.operators.predicates import is_unitary_matrix

from scipy.linalg import fractional_matrix_power
from math import log2
import numpy as np

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
    #print(c.customGates)
    if request.method=='POST':
        receivedDictionary=request.get_json()
        c.setter(receivedDictionary)
        circuit=c.createDraggableCircuit()
        if type(circuit)==type(""):
            return jsonify({"cloopError":circuit})
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
            #c.shots=receivedDictionary["shots"]
            #c.API_TOKEN=receivedDictionary["API_TOKEN"]
            circuit=c.createQasmCircuit(receivedDictionary["qasm"])
            r.setter(receivedDictionary["shots"],receivedDictionary["API_TOKEN"],receivedDictionary["device"],circuit)
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
        matrix=r.matrixRepresentation(decimals=4)
        matrix=c.reversedMatrix(matrix,c.num_qubits)
        returnedDictionary={"matrixRepresentation":matrix}
    else:
        returnedDictionary={}
    return  jsonify(returnedDictionary) 

###############################################################################################################################
    
@app.route('/addCustomGates',methods=['GET','POST'])
def addCustomGates():
    receivedDictionary=request.get_json()
    matrix=receivedDictionary["matrix"]
    matrix=f.strToComplex(matrix)
    isUnitary=is_unitary_matrix(matrix)
    if isUnitary:
        matrix=c.reversedMatrix(matrix,int(log2(len(matrix))))
        c.customGates[receivedDictionary["gateName"]]=matrix
        #print(c.customGates)
    return jsonify({"isUnitary":isUnitary})

###############################################################################################################################
    
@app.route('/subCircuitCustomGate',methods=['GET','POST'])
def subCircuitCustomGate():
    if request.method=='POST':
        #print(c.customGates)
        receivedDictionary=request.get_json()
        c2=Circuit()
        c2.customGates=c.customGates
        c2.subCircuitSetter(receivedDictionary)
        circuit=c2.createDraggableCircuit()
        r=Results(circuit)
        matrix=r.matrixRepresentation()
        complexMatrix=f.strToComplex(matrix)
        isUnitary=is_unitary_matrix(complexMatrix,1e-4,1e-4)
        if isUnitary:
            c.customGates[receivedDictionary["gateName"]]=complexMatrix
            matrix=c.reversedMatrix(matrix,int(log2(len(matrix))))
            return  jsonify({"isUnitary":isUnitary,"matrix":f.complexToStr(matrix)}) 
        else:
            return  jsonify({"isUnitary":isUnitary})
    return  jsonify({})

###############################################################################################################################
    
@app.route('/nthRoot',methods=['GET','POST'])
def nthRoot():
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
        isUnitary=is_unitary_matrix(matrix,1e-4,1e-4)
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
    if request.method=='POST':
        receivedDictionary=request.get_json()
        rows,newGates=f.elementaryGates(receivedDictionary["rows"],c)
        gates={}
        for (name,matrix) in newGates.items():
            gates[name]=c.reversedMatrix(matrix,int(log2(len(matrix))))
            gates[name]=f.complexToStr(matrix)
        returnedDictionary={"rows":rows,"custom":gates}
        
    else:
        returnedDictionary={}
    return  jsonify(returnedDictionary) 

###############################################################################################################################
    
@app.route('/booleanExpression',methods=['GET','POST'])
def booleanExpress():
    if request.method=='POST':
        recievedData = request.get_json()
        #print(recievedData)
        booleanCircut = BooleanFunction.buildBooleanCircuit(recievedData["vars"],recievedData['fn'])
    return jsonify(booleanCircut)

###############################################################################################################################
    
if __name__ == "__main__":
    app.run(debug=True)

#print(datetime.now() - startTime)