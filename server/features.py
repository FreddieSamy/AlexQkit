import copy
from math import log2

from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

import numpy as np

class Features():
    
    
    def controlsAndGatesPositions(self, column):
        """
        returns controls and gates positions for a column
        used in elementaryGates() function
        """
        controlsPos=[]
        gatesPos=[]
        for i in range(len(column)):
            if column[i] == "i":
                continue
            if column[i] == "●" or column[i] == "○":
                controlsPos.append(i)
            else:
                gatesPos.append(i)
        return controlsPos ,gatesPos
    
###############################################################################################################################
        
    def createNewGates(self,coulmn,gatesPos,circuitObj,allNames,newGates):
        """
        adding new gates to gatesObjects
        updating allNames and NewGates    
        
        used in elementaryGates() function
        """
        for gatePos in gatesPos:
            gate=coulmn[gatePos]
            if gate[:7] == "custom_":
                end = gate.find(".")
                if end == -1:
                    end = len(gate)
                gateName=gate[7:end]
                unitaryGate=circuitObj.gatesObjects[gateName].power(0.5)
            else:
                gateName=gate
                if "(" in gate:
                    unitaryGate=circuitObj.gatesWithAngles(gate).power(0.5)
                else:
                    unitaryGate=circuitObj.gatesObjects[gateName].power(0.5)
        
            newGateName = "√("+gateName+")"
            allNames.append(newGateName)
            
            circuitObj.gatesObjects[newGateName]=self.matrixToGateObject(unitaryGate.to_matrix(),newGateName)
            newGates.append(newGateName)
                    
            newGateName+="†"
            unitaryGate=unitaryGate.adjoint()
            circuitObj.gatesObjects[newGateName]=self.matrixToGateObject(unitaryGate.to_matrix(),newGateName)
            newGates.append(newGateName)
 
###############################################################################################################################    
    
    def updateColumns(self,columns,columnPos,controlsPos,gatesPos,allNames):
        """
        decompose multi-controlled gates to its elementary gates for one column
        https://arxiv.org/pdf/quant-ph/9503016.pdf
        ["c","c","u"] ==> [["c","i","custom_√u"], 
                           ["c","x","i"], 
                           ["i","c","custom_√u†"], 
                           ["c","x","i"], 
                           ["i","c","custom_√u"]]
        
        if there exist more than 2 controls it will operate on the first two controls
        ex.. 
        ["c","c","c","u"] ==> [["c","i","c","custom_√u"],
                               ["c","x","c","i"], 
                               ["i","c","c","custom_√u†"], 
                               ["c","x","c","i"], 
                               ["i","c","c","custom_√u"]]
        
        used in elementaryGates() function
        """
        columnLen=len(columns[columnPos])
        col = ["i"]*columnLen
        col[controlsPos[1]] = columns[columnPos][controlsPos[1]]
        for l in range(len(gatesPos)):
            col[gatesPos[l]] = "custom_"+allNames[l]
        for k in range(len(controlsPos)-2):
            col[controlsPos[k+2]] = columns[columnPos][controlsPos[k+2]]
        columns.insert(columnPos+1, col)

        col = ["i"]*columnLen
        col[controlsPos[0]] = columns[columnPos][controlsPos[0]]
        col[controlsPos[1]] = "x"
        for k in range(len(controlsPos)-2):
            col[controlsPos[k+2]] = columns[columnPos][controlsPos[k+2]]
        columns.insert(columnPos+1, col)

        col = ["i"]*columnLen
        col[controlsPos[1]] = columns[columnPos][controlsPos[1]]
        for l in range(len(gatesPos)):
            col[gatesPos[l]] = "custom_"+allNames[l]+"†"
        for k in range(len(controlsPos)-2):
            col[controlsPos[k+2]] = columns[columnPos][controlsPos[k+2]]
        columns.insert(columnPos+1, col)

        col = ["i"]*columnLen
        col[controlsPos[0]] = columns[columnPos][controlsPos[0]]
        col[controlsPos[1]] = "x"
        for k in range(len(controlsPos)-2):
            col[controlsPos[k+2]] = columns[columnPos][controlsPos[k+2]]
        columns.insert(columnPos+1, col)

        col = ["i"]*columnLen
        col[controlsPos[0]] = columns[columnPos][controlsPos[0]]
        for l in range(len(gatesPos)):
            col[gatesPos[l]] = "custom_"+allNames[l]
        for k in range(len(controlsPos)-2):
            col[controlsPos[k+2]] = columns[columnPos][controlsPos[k+2]]
        columns.insert(columnPos+1, col)
        
        del columns[columnPos]
    
############################################################################################################################### 
        
    def elementaryGates(self, rows, circuitObj):
        """
        decompose multi-controlled gates to single controlled gates 
        according to elementary gates paper 
        https://arxiv.org/pdf/quant-ph/9503016.pdf
        
        ["c","c","u"] ==> [["c","i","custom_√u"], 
                           ["c","x","i"], 
                           ["i","c","custom_√u†"], 
                           ["c","x","i"], 
                           ["i","c","custom_√u"]]
        
        newGates.. to add them in the frontEnd gates
        """
        
        newGates=[]
        columns = np.transpose(rows).tolist() #received from the frontend as rows and we need to operate on columns
        
        i = 0
        while i < len(columns):
            
            controlsPos, gatesPos = self.controlsAndGatesPositions(columns[i])
           
            if len(controlsPos) > 1:
                allNames=[]
                self.createNewGates(columns[i],gatesPos,circuitObj,allNames,newGates)
                self.updateColumns(columns,i,controlsPos,gatesPos,allNames)
            
            if len(controlsPos) == 2: 
                i = i+5 #go to the next old colunmn ... "column i replaced by 5 columns"
            #else decompose the same position
            #["c","c","c","u"] ==> [["c","i","c","√u"], ["c","x","c","i"], ["i","c","c","√u†"], ["c","x","c","i"], ["i","c","c","√u"]]

        return np.transpose(columns).tolist(),newGates

###############################################################################################################################

    def strToComplex(self, matrix):
        """
        converts the received matrices from the frontend with string elements to complex values
        """
        matrixCopy=copy.deepcopy(matrix)
        for i in range(len(matrixCopy)):
            for j in range(len(matrixCopy[i])):
                if(type(matrixCopy[i][j]) == type("")):
                    matrixCopy[i][j] = matrixCopy[i][j].replace("i", "j")
                    matrixCopy[i][j] = complex(matrixCopy[i][j])
        return matrixCopy

###############################################################################################################################
    
    def matrixToGateObject(self,matrix,name):
        """
        returns gate object of a matrix
        """
        num_qubits=int(log2(len(matrix)))
        tempCircuit=QuantumCircuit(num_qubits,name=name)
        customGate = Operator(matrix)
        tempCircuit.unitary(customGate, list(range(num_qubits)))
        return tempCircuit.to_gate()

###############################################################################################################################