from flask import Flask, request,jsonify
from flask_cors import CORS

from circuit import Circuit
from results import Results
from features import Features
from booleanExpression import BooleanFunction

from qiskit.quantum_info.operators.predicates import is_unitary_matrix

from math import log2

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
        try:
            circuit=c.createDraggableCircuit()
            r.setter(receivedDictionary["shots"],receivedDictionary["API_TOKEN"],receivedDictionary["device"],circuit)
            return  jsonify(r.draggableCircuitResults()) 
        except Exception as e:
            return jsonify({"conditionalLoopError":str(e)})
        
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

###############################################################################################################################

@app.route('/matrixRepresentation',methods=['GET','POST'])
def matrixRepresentation():
    if request.method=='POST':
        r=Results(c.circuit)
        try:
            matrix=r.matrixRepresentation(decimals=4)
            matrix=c.reversedMatrix(matrix,c.num_qubits)
            return  jsonify({"error":False,"matrixRepresentation":matrix})
        except Exception:
            return  jsonify({"error":True})

###############################################################################################################################
    
@app.route('/addCustomGates',methods=['GET','POST'])
def addCustomGates():
    receivedDictionary=request.get_json()
    matrix=receivedDictionary["matrix"]
    matrix=f.strToComplex(matrix)
    isUnitary=is_unitary_matrix(matrix)
    if isUnitary:
        matrix=c.reversedMatrix(matrix,int(log2(len(matrix))))
        c.gatesObjects[receivedDictionary["gateName"]]=f.matrixToGateObject(matrix,receivedDictionary["gateName"])
    return jsonify({"isUnitary":isUnitary})

###############################################################################################################################
    
@app.route('/subCircuitCustomGate',methods=['GET','POST'])
def subCircuitCustomGate():
    if request.method=='POST':
        receivedDictionary=request.get_json()
        c2=Circuit()
        c2.gatesObjects=c.gatesObjects
        c2.subCircuitSetter(receivedDictionary)
        try:
            circuit=c2.createDraggableCircuit()
        except Exception as e:
            return jsonify({"conditionalLoopError":str(e)})
        r=Results(circuit)
        matrix=r.matrixRepresentation()
        complexMatrix=f.strToComplex(matrix)
        isUnitary=is_unitary_matrix(complexMatrix)
        if isUnitary:
            c.gatesObjects[receivedDictionary["gateName"]]=f.matrixToGateObject(complexMatrix,receivedDictionary["gateName"])
        return  jsonify({"isUnitary":isUnitary})

###############################################################################################################################
    
@app.route('/nthRoot',methods=['GET','POST'])
def nthRoot():
    if request.method=='POST':
        receivedDictionary=request.get_json()
        root=receivedDictionary["root"]
        gateName=receivedDictionary["gateName"]
        gate=c.gatesObjects[gateName]
        try:
            unitaryGate=gate.power(1/int(root))
        except Exception:
            return jsonify({"isUnitary":False})
        gateName=receivedDictionary["newGateName"]
        if receivedDictionary["adjoint"]:
            unitaryGate=unitaryGate.adjoint()
        c.gatesObjects[gateName]=f.matrixToGateObject(unitaryGate.to_matrix(),gateName)
        return  jsonify({"isUnitary":True}) 

###############################################################################################################################
    
@app.route('/elementaryGates',methods=['GET','POST'])
def elementaryGates():
    if request.method=='POST':
        receivedDictionary=request.get_json()
        rows,newGates=f.elementaryGates(receivedDictionary["rows"],c)
        """gates={}
        for (name,matrix) in newGates.items():
            gates[name]=c.reversedMatrix(matrix,int(log2(len(matrix))))
            gates[name]=f.complexToStr(matrix)"""
        return  jsonify({"rows":rows,"custom":newGates}) 

###############################################################################################################################
    
@app.route('/booleanExpression',methods=['GET','POST'])
def booleanExpress():
    if request.method=='POST':
        recievedData = request.get_json()
        if recievedData['indices'] != [''] :
            booleanCircut = BooleanFunction.buildBooleanCircuit_indecies(recievedData["vars"],recievedData['fn'],recievedData['indices'])
        else  :
            booleanCircut = BooleanFunction.buildBooleanCircuit(recievedData["vars"],recievedData['fn'])
    return jsonify(booleanCircut)

###############################################################################################################################
    
if __name__ == "__main__":
    app.run(debug=True)