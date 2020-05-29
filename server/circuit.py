from stateVectorNormalization import Normalization
from results import Results

from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator
import qiskit.circuit.library.standard_gates as gates

import copy
import numpy as np
from math import log2
    

class Circuit():
    
    def __init__(self):
        self.radian = False
        self.exeCount = 0
        self.num_qubits =2
        self.circuit = QuantumCircuit(self.num_qubits, self.num_qubits)
        self.init=["0","0"]
        self.cols = [[],[]]
        self.customGates={}
        self.gatesObjects={
                "x":gates.XGate(),
                "y":gates.YGate(),
                "z":gates.ZGate(),
                "h":gates.HGate(),
                "s":gates.SGate(),
                "t":gates.TGate(),
                "sdg":gates.SdgGate(),
                "tdg":gates.TdgGate()
                }

###############################################################################################################################

    def setter(self,receivedDictionary):        
        self.radian = receivedDictionary["radian"]
        self.exeCount = receivedDictionary["exeCount"]
        self.num_qubits = int(receivedDictionary["wires"])
        self.circuit = QuantumCircuit(self.num_qubits, self.num_qubits)
        self.init=receivedDictionary["init"]

        if receivedDictionary["repeated"] != {}:
            oldSize=len(receivedDictionary["rows"][0])
            self.cols = self.repettion(receivedDictionary["rows"], receivedDictionary["repeated"]['listOfPos'], receivedDictionary["repeated"]['listOfRep'])
            self.cols = np.transpose(self.cols).tolist()
            newSize=len(self.cols)
            self.exeCount+=(newSize-oldSize)
        else:
            self.cols = np.transpose(receivedDictionary["rows"]).tolist()
            
        #print("cols: ",self.cols)
 
###############################################################################################################################
       
    def subCircuitSetter(self,receivedDictionary):
        self.radian = receivedDictionary["radian"]
        self.num_qubits = int(receivedDictionary["wires"])
        self.circuit = QuantumCircuit(self.num_qubits, self.num_qubits)
        self.init=[]
        self.cols = np.transpose(receivedDictionary["rows"]).tolist()
        self.exeCount = len(self.cols)
        
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
    
    # this function takes list of initial states and apply equivalent gates

    # important note .. "according to Qiskit’s convention, first qubit is on the right-hand side"
    # ex: |01⟩  .. 1st qubit is 1 and 2nd qubit is 0
    # so we corrected that by applying all gates in reverse order by bassing reversedWires=True if needed
    # you can check that here - https://qiskit-staging.mybluemix.net/documentation/terra/summary_of_quantum_operations.html

    # you can intialize your circuit with vector that represent your initialization
    # to initialize two qubits with |1⟩ ( initialize a system of two wires by |11⟩  ) ... circuit.initialize([0,0,0,1],[0,1])

    # qiskit always start with |0⟩ state
    # |1⟩ state equivalent to X|0⟩
    # |+⟩ state equivalent to H|0⟩
    # |-⟩ state equivalent to H|1⟩ = HX|0⟩
    # |i⟩ = |↻⟩ state equivalent to S|+⟩ = SH|0⟩
    # |-i⟩ = |↺⟩ state equivalent to S|-⟩ = SH|1⟩ = SHX|0⟩

    # dirac notation doc - https://docs.microsoft.com/en-us/quantum/concepts/dirac-notation

    def initState(self):#,reversedWires=False):
        stateList=self.init
        #if reversedWires:
        #    stateList=self.init[::-1]
        for i in range(len(stateList)):
            if str(stateList[i]) == "0":
                continue
            elif str(stateList[i]) == "1":
                self.circuit.x(i)
            elif stateList[i] == "+":
                self.circuit.h(i)
            elif stateList[i] == "-":
                self.circuit.x(i)
                self.circuit.h(i)
            elif stateList[i] == "i":
                self.circuit.h(i)
                self.circuit.s(i)
            elif stateList[i] == "-i":
                self.circuit.x(i)
                self.circuit.h(i)
                self.circuit.s(i)
        #circuit.barrier()

###############################################################################################################################       
        
    def addCustomGate(self, gateMatrix, positions,gateName):
        """
        applies a unitary matrix (custom gate) to the circuit
        """
        customGate = Operator(gateMatrix)
        self.circuit.unitary(customGate, positions,label=gateName)
    
###############################################################################################################################

    # inverse the arrange of gates in tensor product

    # important note .. "according to Qiskit’s convention, first qubit is on the right-hand side"
    # ex: |01⟩  .. 1st qubit is 1 and 2nd qubit is 0
    # we corrected that by passing using reversedMatrix() function

    def reversedMatrix(self,matrix,wires):
        matrixCopy=copy.deepcopy(matrix)
        reversedMatrix=[]
        for i in range(len(matrixCopy)):
            reversedMatrix.append([])
            pos=int(''.join(reversed(str(("{0:0"+str(wires).replace('.0000','')+"b}").format(i)))),2)
            tempList=matrixCopy[pos]
            for j in range(len(tempList)):
                pos=int(''.join(reversed(str(("{0:0"+str(wires).replace('.0000','')+"b}").format(j)))),2)
                reversedMatrix[i].append(tempList[pos])
        return reversedMatrix

###############################################################################################################################       
        
    # this function returns the positions of the multi-Qubit custom gates
    # remove the other gates to prevent applying the gate multiple times
    
    def multiQubitCustomGate(self,column,firstAppear):
        pointPos=column[firstAppear].find(".")
        index=int(column[firstAppear][pointPos+1:])
        gateName=column[firstAppear][7:pointPos]
        pos=[]
        pos.insert(index,firstAppear)
        for i in range(firstAppear+1, len(column)):
            if "custom_"+gateName == column[i][:pointPos]:
                index=int(column[i][pointPos+1:])
                pos.insert(index,i)
                column[i] = "i"
        return column, pos
    
###############################################################################################################################

    # this function applies noncontrolled gates on the circuit

    def nonControlledColumns(self,column):
        # naming a custom gate
        # don't accept "." in any position
    
        for i in range(len(column)):
            if str(column[i]) == "i":
                continue
            if str(column[i]) == "m":
                self.circuit.measure(i, i)
                continue
            if str(column[i])[:7] == "custom_":
                end = str(column[i]).find(".")
                if end == -1:
                    end = len(column[i])
                gateName = str(column[i])[7:end]
                if len(self.customGates[gateName]) == 2:
                    self.addCustomGate(self.customGates[gateName], [i],gateName)
                    continue
                else:
                    column, pos = self.multiQubitCustomGate(column, i)
                    self.addCustomGate(self.customGates[gateName], pos,gateName)
                    continue
            if str(column[i]) == "swap":
                p1 = i
                for j in range(i+1, len(column)):
                    if str(column[j]) == "swap":
                        p2 = j
                        column[j] = "i"
                        break
                self.circuit.swap(p1, p2)
                continue
            if "(" in str(column[i]):
                angle = column[i][:-1]
                if not self.radian:
                    angle = column[i][0:3] + str((float(column[i][3:-1])*3.14)/180)
    
                pythonLine = "self.circuit."+angle+","+str(i)+")"
                exec(pythonLine)
                continue
    
            pythonLine = "self.circuit."+column[i]+"("+str(i)+")"
            exec(pythonLine)

############################################################################################################################### 

    # this function applies controlled gates on the circuit
            
    def controlledColumns(self,column):
        c = []
        oc = []
        
        for i in range(len(column)):
            if str(column[i]) == "●":
                c.append(i)
                column[i] = "i"

            elif str(column[i]) == "○":
                self.circuit.x(i)                             #open control
                oc.append(i)
                c.append(i)
                column[i] = "i"

        numOfControls = len(c)
        for i in range(len(column)):
            if str(column[i]) == "i":
                continue
                
            if str(column[i])[:7] == "custom_":
                end = str(column[i]).find(".")
                if end == -1:
                    end = len(column[i])
                gateName = str(column[i])[7:end]
                if len(self.customGates[gateName]) == 2:
                    pos = c+[i]
                else:
                    column, pos = self.multiQubitCustomGate(column, i)
                    pos = c+pos
                gate=self.matrixToGateObject(self.customGates[gateName],gateName).control(numOfControls)
                self.circuit.append(gate,pos)
                continue
            if str(column[i]) == "swap":
                p1 = i
                for j in range(i+1, len(column)):
                    if str(column[j]) == "swap":
                        p2 = j
                        column[j] = "i"
                        break
                pos = c+[p1]+[p2]
                gate=gates.SwapGate().control(numOfControls)
                self.circuit.append(gate,pos)
                continue
            pos = c+[i]
            if "(" in str(column[i]):
                name=column[i][0:2]
                angle = column[i][3:-1]
                if not self.radian:
                    angle = (float(angle)*3.14)/180
                if name=="rx":
                    gate=gates.RXGate(angle).control(numOfControls)
                elif name=="ry":
                    gate=gates.RYGate(angle).control(numOfControls)
                else:
                    gate=gates.RZGate(angle).control(numOfControls)
                self.circuit.append(gate,pos)
                continue
            gate=self.gatesObjects[column[i]].control(numOfControls)
            self.circuit.append(gate,pos)

        for i in oc:                                     # open control
            self.circuit.x(i)

###############################################################################################################################

    def createDraggableCircuit(self):

        self.initState()

        for i in range(self.exeCount):
            if "reset" in self.cols[i]:
                self.resetExist = True
              
            if "cLoop(" in self.cols[i]:
                r=Results(self.circuit)
                newInitialization=Normalization.buildLoopCond(self.num_qubits,self.cols[i],r.stateVector)
                if all(ele == 0 for ele in newInitialization):
                    return "condition at column i will never be satisfied"
                self.circuit=QuantumCircuit(self.num_qubits, self.num_qubits)
                self.circuit.initialize(newInitialization,list(range(self.num_qubits)))
                
            elif "●" in self.cols[i] or "○" in self.cols[i]:
                self.controlledColumns(self.cols[i])
            else:
                self.nonControlledColumns(self.cols[i])
        
        return self.circuit
    
###############################################################################################################################
    
    def createQasmCircuit(self,qasmText):
        tempCircuit = QuantumCircuit(1)
        self.circuit = tempCircuit.from_qasm_str(qasmText)
        
        return self.circuit
    
############################################################################################################################### 
    # kotta
    def repettion(self, circuitList, listOfPositions, listOfNumberOfRepetition):
        dic = self.dicOfBlockAndPosition(
            circuitList, listOfPositions, listOfNumberOfRepetition)
        circuitList = np.array(circuitList)
        for key in dic:
            repetedBlock, insertPostition, numberOfRepetition = dic[key][
                'repetedBlock'], dic[key]['insertPostion'], dic[key]['NumberOfRepetition']
            for repet in range(numberOfRepetition-1):
                circuitList = np.insert(
                    circuitList, insertPostition, repetedBlock, axis=1)
        return circuitList.tolist()
    
###############################################################################################################################

    def blockToRepet(self, circutList, position):
        circutList = np.array(circutList)
        repetBlock = circutList[:, position[0]: position[1] + 1].transpose()
        return repetBlock, position[0], position[1]
    
###############################################################################################################################

    def dicOfBlockAndPosition(self, circutList, listOfPositions, listOfNumberOfRepetition):
        dicOfPos = {}
        for i in range(len(listOfPositions)):
            repetedBlock, insertPosition, endPosition = self.blockToRepet(circutList, listOfPositions[i])
            if i:
                previousInsertPosition = dicOfPos[i]['insertPostion']
                insertPosition = self.positionEquation(previousInsertPosition, listOfNumberOfRepetition[i-1], len(dicOfPos[i]['repetedBlock']), self.factor(insertPosition, endPreviousPos))
            endPreviousPos = endPosition
            dicOfPos[i+1] = {'repetedBlock': repetedBlock, 'insertPostion': insertPosition,'NumberOfRepetition': listOfNumberOfRepetition[i]}
        return dicOfPos
    
###############################################################################################################################

    def positionEquation(self, previousInsertPosition, numberOfRepetition, lengthOfBlock, factor):
        return previousInsertPosition + factor + (numberOfRepetition * lengthOfBlock)
    
###############################################################################################################################

    def factor(self, startNextPosition, endPreviousPosition):
        fac = startNextPosition - endPreviousPosition
        if fac <= 0:
            return 0
        return fac - 1
    
###############################################################################################################################