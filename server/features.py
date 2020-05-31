import copy
import numpy as np
from math import log2

from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

class Features():

    def elementaryGates(self, rows, circuitObj):
        newGates=[]
        columns = np.transpose(rows).tolist()
        i = 0
        while i < len(columns):
            c = []
            gatePositions=[]
            for j in range(len(columns[i])):
                if columns[i][j] == "i":
                    continue
                if columns[i][j] == "●" or columns[i][j] == "○":
                    c.append(j)
                else:
                    gatePositions.append(j)
            if len(c) > 1:
                allNames=[]
                for gatePos in gatePositions:
                    if columns[i][gatePos][:7] == "custom_":
                        end = columns[i][gatePos].find(".")
                        if end == -1:
                            end = len(columns[i][gatePos])
                        gateName=columns[i][gatePos][7:end]
                    else:
                        gateName=columns[i][gatePos]
                    newGateName = "√"+gateName
                    allNames.append(newGateName)

                    unitaryGate=circuitObj.gatesObjects[gateName].power(0.5)
                    circuitObj.gatesObjects[newGateName]=self.matrixToGateObject(unitaryGate.to_matrix(),newGateName)
                    newGates.append(newGateName)
                    
                    newGateName+="†"
                    unitaryGate=unitaryGate.adjoint()
                    circuitObj.gatesObjects[newGateName]=self.matrixToGateObject(unitaryGate.to_matrix(),newGateName)
                    newGates.append(newGateName)

                col = ["i"]*len(columns[i])
                col[c[1]] = columns[i][c[1]]
                for l in range(len(gatePositions)):
                    col[gatePositions[l]] = "custom_"+allNames[l]
                for k in range(len(c)-2):
                    col[c[k+2]] = columns[i][c[k+2]]
                columns.insert(i+1, col)

                col = ["i"]*len(columns[i])
                col[c[0]] = columns[i][c[0]]
                col[c[1]] = "x"
                for k in range(len(c)-2):
                    col[c[k+2]] = columns[i][c[k+2]]
                columns.insert(i+1, col)

                col = ["i"]*len(columns[i])
                col[c[1]] = columns[i][c[1]]
                for l in range(len(gatePositions)):
                    col[gatePositions[l]] = "custom_"+allNames[l]+"†"
                for k in range(len(c)-2):
                    col[c[k+2]] = columns[i][c[k+2]]
                columns.insert(i+1, col)

                col = ["i"]*len(columns[i])
                col[c[0]] = columns[i][c[0]]
                col[c[1]] = "x"
                for k in range(len(c)-2):
                    col[c[k+2]] = columns[i][c[k+2]]
                columns.insert(i+1, col)

                col = ["i"]*len(columns[i])
                col[c[0]] = columns[i][c[0]]
                for l in range(len(gatePositions)):
                    col[gatePositions[l]] = "custom_"+allNames[l]
                for k in range(len(c)-2):
                    col[c[k+2]] = columns[i][c[k+2]]
                columns.insert(i+1, col)

                del columns[i]

            if len(c) == 2:
                i = i+4
            elif len(c) > 2:
                i = i-1
            i = i+1

        return np.transpose(columns).tolist(),newGates

###############################################################################################################################

    def strToComplex(self, matrix):
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