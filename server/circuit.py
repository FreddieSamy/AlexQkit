class Circuit():
    
    def __init__(self):
        from qiskit import QuantumCircuit
        
        self.radian = False
        self.exeCount = 0
        self.num_qubits =2
        self.circuit = QuantumCircuit(self.num_qubits, self.num_qubits)
        self.init=["0","0"]
        self.cols = [[],[]]
        self.customGates={}
        self.swapMatrix=[[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]
        self.nonControlledGates=["s","t","sdg","tdg"]

###############################################################################################################################

    def setter(self,receivedDictionary):
        from qiskit import QuantumCircuit
        import numpy as np
        
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
        from qiskit import QuantumCircuit
        import numpy as np
        
        self.radian = receivedDictionary["radian"]
        self.num_qubits = int(receivedDictionary["wires"])
        self.circuit = QuantumCircuit(self.num_qubits, self.num_qubits)
        self.init=[]
        self.cols = np.transpose(receivedDictionary["rows"]).tolist()
        self.exeCount = len(self.cols)
        
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
        
    # this function applies a matrix (custom gate) to a circuit in reverse order of positions
    # positions must be list with numbers
    # we must check unitary before storing it
    # to check unitary use  "is_unitary_matrix(data)"

    # important note .. "according to Qiskit’s convention, first qubit is on the right-hand side"
    # ex: |01⟩  .. 1st qubit is 1 and 2nd qubit is 0
    # keep in mind that the matrix entered in correct order (left to right qubits)
    # so to correct the qiskit order we need to shift the custom matrix to the end (newPos=numOfQubits-pos-1 )
    # you can check that here - https://qiskit-staging.mybluemix.net/documentation/terra/summary_of_quantum_operations.html

    def addCustomGate(self, gateMatrix, positions):#,reversedWires=False):
        """if reversedWires:
            for i in range(len(positions)):
                positions[i]=self.num_qubits-positions[i]-1"""
        from qiskit.quantum_info.operators import Operator
        customGate = Operator(gateMatrix)
        self.circuit.unitary(customGate, positions)
    
###############################################################################################################################

    # inverse the arrange of gates in tensor product

    # important note .. "according to Qiskit’s convention, first qubit is on the right-hand side"
    # ex: |01⟩  .. 1st qubit is 1 and 2nd qubit is 0
    # we corrected that by passing using reversedMatrix() function

    def reversedMatrix(self,matrix,wires):
        import copy
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

    # constructs a matrix to represent controlled gates 
    
    def controlledGate(self,unitary, numOfControls=1):#,reversedWires=True):
        from math import log2
    
        old = len(unitary)
        wires=int(log2(old)+numOfControls)
        new = 2**wires
        controlledGate = []
    
        for i in range(new):
            controlledGate.append([])
            for j in range(new):
                if (i >= new-old) and (j >= new-old):
                    controlledGate[i].append(unitary[i-new+old][j-new+old])
                elif i == j:
                    controlledGate[i].append(1)
                else:
                    controlledGate[i].append(0)
    
        #if reversedWires:
        controlledGate=self.reversedMatrix(controlledGate,wires)
        return controlledGate

############################################################################################################################### 

    # this function takes name of a gate (str)
    # and returns the matrix of the gate

    def gateToMatrix(self,gate):
        from qiskit import QuantumCircuit
        from qiskit import Aer
        from qiskit import execute
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
        
    # this function returns the positions of the multi-Qubit custom gates
    # remove the other gates to prevent applying the gate multiple times
    
    def multiQubitCustomGate(self,column,firstAppear):
        #from math import log2
        pointPos=column[firstAppear].find(".")
        index=int(column[firstAppear][pointPos+1:])
        gateName=column[firstAppear][7:pointPos]
        #size = log2(len(self.customGates[gateName]))
        #pos = [None]*int(size)
        pos=[]
        pos.insert(index,firstAppear)
        #print(pos,size,index)
        for i in range(firstAppear+1, len(column)):
            if "custom_"+gateName == column[i][:pointPos]:
                index=int(column[i][pointPos+1:])
                pos.insert(index,i)
                #print(pos,size,index)
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
                    self.addCustomGate(self.customGates[gateName], [i])
                    continue
                else:
                    column, pos = self.multiQubitCustomGate(column, i)
                    self.addCustomGate(self.customGates[gateName], pos)
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
                self.addCustomGate(self.controlledGate(self.customGates[gateName], numOfControls), pos)
                continue
            if str(column[i]) == "swap":
                p1 = i
                for j in range(i+1, len(column)):
                    if str(column[j]) == "swap":
                        p2 = j
                        column[j] = "i"
                        break
                if numOfControls==1:
                    self.circuit.cswap(c[0],p1, p2)
                    continue
                pos = c+[p1]+[p2]
                self.addCustomGate(self.controlledGate(self.swapMatrix,numOfControls),pos)
                continue
            if numOfControls==1 and str(column[i]) not in self.nonControlledGates:
                if "(" in str(column[i]):
                    angle = column[i][:-1]
                    if not self.radian:
                        angle = column[i][0:3] + str((float(column[i][3:-1])*3.14)/180)
                    pythonLine = "self.circuit.c"+angle+","+str(c[0])+","+str(i)+")"
                    exec(pythonLine)
                    continue
                pythonLine = "self.circuit.c"+str(column[i])+"("+str(c[0])+","+str(i)+")"
                exec(pythonLine)
                continue
            if numOfControls==2 and str(column[i])=="x":
                self.circuit.ccx(c[0],c[1],i)
                continue
            pos = c+[i]
            self.addCustomGate(self.controlledGate(self.gateToMatrix(column[i]), numOfControls), pos)

        for i in oc:                                     # open control
            self.circuit.x(i)

###############################################################################################################################

    def createDraggableCircuit(self):

        self.initState()

        for i in range(self.exeCount):
            if "reset" in self.cols[i]:
                self.resetExist = True
            if "●" in self.cols[i] or "○" in self.cols[i]:
                self.controlledColumns(self.cols[i])
            else:
                self.nonControlledColumns(self.cols[i])
        
        return self.circuit
    
###############################################################################################################################
    
    def createQasmCircuit(self,qasmText):
        from qiskit import QuantumCircuit
        tempCircuit = QuantumCircuit(1)
        self.circuit = tempCircuit.from_qasm_str(qasmText)
        
        return self.circuit
    
############################################################################################################################### 
    # kotta
    def repettion(self, circuitList, listOfPositions, listOfNumberOfRepetition):
        import numpy as np
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
        import numpy as np
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