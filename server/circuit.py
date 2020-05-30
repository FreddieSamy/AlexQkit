from stateVectorNormalization import Normalization
from results import Results

from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator
import qiskit.circuit.library.standard_gates as gates

import copy
import numpy as np
    

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
    #############################
    """
    freddy should put some comments and clarifications 3shan 5atrr rbna yakrmna
    """
    def gateToMatrix(self,gate):
        if gate == "swap":
            tempCircuit = QuantumCircuit(2)
            tempCircuit.swap(0, 1)
        elif "(" in gate:
            tempCircuit = QuantumCircuit(1)
            angle = gate[:-1]
            if not self.radian:
                angle = gate[0:3]+str((float(gate[3:-1])*3.14)/180)
            pythonLine = "tempCircuit."+angle+",0)"
            exec(pythonLine)
        else:
            tempCircuit = QuantumCircuit(1)
            exec("tempCircuit."+gate+"(0)")
        simulator = Aer.get_backend('unitary_simulator')
        result = execute(tempCircuit, backend=simulator).result()
        return result.get_unitary()
###############################################################################################################################
       
    def subCircuitSetter(self,receivedDictionary):
        self.radian = receivedDictionary["radian"]
        self.num_qubits = int(receivedDictionary["wires"])
        self.circuit = QuantumCircuit(self.num_qubits, self.num_qubits)
        self.init=[]
        self.cols = np.transpose(receivedDictionary["rows"]).tolist()
        self.exeCount = len(self.cols)
        
###############################################################################################################################

    def initState(self):
        """
        applies equivalent gates of the initialization list
        
        qiskit always start with |0⟩ state
        |1⟩ state equivalent to X|0⟩
        |+⟩ state equivalent to H|0⟩
        |-⟩ state equivalent to H|1⟩ = HX|0⟩
        |i⟩ = |↻⟩ state equivalent to S|+⟩ = SH|0⟩
        |-i⟩ = |↺⟩ state equivalent to S|-⟩ = SH|1⟩ = SHX|0⟩
        
        """
        stateList=self.init
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

    def reversedMatrix(self,matrix,wires):
        """
        convert a matrix to another for the reversed order of wires
        to inverse qiskit order of wires
        
        important note .. "according to Qiskit’s convention, first qubit is on the right-hand side"
        ex: |01⟩  .. 1st qubit is 1 and 2nd qubit is 0
        """
        #this function swaps every pos by its inverse for all columns an rows
        #ex.. circuit with 3 wires
        #row 1 = "001" will swap with "100"= row 4  
        matrixCopy=copy.deepcopy(matrix)
        reversedMatrix=[]
        for i in range(len(matrixCopy)):
            reversedMatrix.append([])
            #the next line finds the inverse position in decimal ex.. 3 -> 011 -> 110 -> 6
            pos=int(''.join(reversed(str(("{0:0"+str(wires).replace('.0000','')+"b}").format(i)))),2)
            tempList=matrixCopy[pos]
            for j in range(len(tempList)):
                pos=int(''.join(reversed(str(("{0:0"+str(wires).replace('.0000','')+"b}").format(j)))),2)
                reversedMatrix[i].append(tempList[pos])
        return reversedMatrix

###############################################################################################################################       
    
    def customGateInfo(self,column,firstAppear):
        """
        returns the position(s) of a custom gate and its name
        and removes the other gates from the column to prevent applying the gate multiple times
        
        custom gates represented as ..  custom_<name>.<index>
        
        ex.. col=["i","custom_not.1","i","custom_not.0"] -> name=not, pos=[3,1] 
        means that not is a 2 qubit gate should apply to the 2nd and the 4th wire
        the first input for this gate is the 4th wire and the second input is th 2nd wire 
        
        indices give us the arrangement of the input wires to the gate
        indices must start with 0 and end with n-1  ex.. 3 qubit gate indices are 0,1,2 in any order
        
        naming a custom gate..
        don't accept "." in any position
        """
        pointPos = column[firstAppear].find(".")
        if pointPos == -1:
            pointPos = len(column[firstAppear])
        gateName = str(column[firstAppear])[7:pointPos]
        if len(self.customGates[gateName]) == 2: #one wire
            pos=[firstAppear]
        else:
            index=int(column[firstAppear][pointPos+1:])
            pos=[]
            pos.insert(index,firstAppear)
            for i in range(firstAppear+1, len(column)):
                if "custom_"+gateName == column[i][:pointPos]:
                    index=int(column[i][pointPos+1:])
                    pos.insert(index,i)
                    column[i] = "i"
        return column,pos,gateName
    
###############################################################################################################################          
    
    def swapPos(self,column,firstAppear):
        """
        returns the two positions of a swap gate 
        and remove the second one to prevent applying it multiple times
        """
        pos = [firstAppear]
        for j in range(firstAppear+1, len(column)):
            if str(column[j]) == "swap":
                pos.append(j)
                column[j] = "i"
                break
        return column,pos
    
###############################################################################################################################

    def nonControlledColumns(self,column):
        """
        applies noncontrolled gates on the circuit
        
        ex.. column=["i","x","swap","i","swap"]
        means x on the 2nd wire and swap between the 3rd and the 5th wires
        """
    
        for i in range(len(column)):
            #empty
            if str(column[i]) == "i": 
                continue
            #measurement
            if str(column[i]) == "m": 
                self.circuit.measure(i, i)
                continue
            #custom gates
            if str(column[i])[:7] == "custom_": 
                column, pos, gateName = self.customGateInfo(column, i)
                self.addCustomGate(self.customGates[gateName], pos,gateName)
                continue
            #swap
            if str(column[i]) == "swap":
                column,pos=self.swapPos(column,i)
                self.circuit.swap(pos)
                continue
            #gates with angles rx,ry,rz
            if "(" in str(column[i]):  
                gate = column[i][:-1]
                #degree to radian
                if not self.radian:    
                    gate = column[i][0:3] + str((float(column[i][3:-1])*3.14)/180)
                pythonLine = "self.circuit."+gate+","+str(i)+")"
                exec(pythonLine)
                continue
            #any other gate
            pythonLine = "self.circuit."+column[i]+"("+str(i)+")"
            exec(pythonLine)

############################################################################################################################### 
            
    def controlsPos(self,column):
        """
        returns the controls positions in a column
        """
        
        c = []   #all controls positions
        oc = []  #open controls positions
        for i in range(len(column)):
            if str(column[i]) == "●":
                c.append(i)
                column[i] = "i"

            elif str(column[i]) == "○":
                self.circuit.x(i)  #applying x gate before and after a closed control to convert it to an open control
                oc.append(i)
                c.append(i)
                column[i] = "i"
        return c,oc

############################################################################################################################### 
            
    def controlledColumns(self,column):
        """
        applies controlled gates on the circuit
        
        ex.. column=["c","i","c","i","x"]
        means ccx(0,2,4)
        
        column=["c","i","c","y","x"] -> ccy(0,2,3) , ccx(0,2,4)
        """
        c,oc=self.controlsPos(column)
        numOfControls = len(c)
        for i in range(len(column)):
            #empty
            if str(column[i]) == "i":
                continue
            #controlled swap
            if str(column[i]) == "swap":
                column,pos=self.swapPos(column,i)
                pos = c+pos
                gate=gates.SwapGate().control(numOfControls)
                self.circuit.append(gate,pos)
                continue
            pos = c+[i]
            #gates with angles rx,ry,rz
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
            #controlled custom gates
            gateName=column[i]
            if gateName[:7] == "custom_":
                column, pos, gateName = self.customGateInfo(column, i)
                pos = c+pos
            #controlled custom gates and any other controlled gate
            gate=self.gatesObjects[gateName].control(numOfControls)
            self.circuit.append(gate,pos)

        for i in oc:   #applying x gate before and after a closed control to convert it to an open control
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
