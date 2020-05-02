class Circuit():
    def __init__(self):
        self.circutDrawing = None
        self.returnedDictionary = {}

###############################################################################################################################

    def initState(self,circuit,stateList,reversedWires=False):
        if reversedWires:
            stateList=stateList[::-1]
        for i in range(len(stateList)):
            if str(stateList[i]) == "0":
                continue
            elif str(stateList[i]) == "1":
                circuit.x(i)
            elif stateList[i] == "+":
                circuit.h(i)
            elif stateList[i] == "-":
                circuit.x(i)
                circuit.h(i)
            elif stateList[i] == "i":
                circuit.h(i)
                circuit.s(i)
            elif stateList[i] == "-i":
                circuit.x(i)
                circuit.h(i)
                circuit.s(i)
        #circuit.barrier()
        return circuit

###############################################################################################################################
    
    def stateVector(self,circuit):
        from qiskit import Aer
        from qiskit import execute
    
        simulator=Aer.get_backend('statevector_simulator')
        result=execute(circuit,backend=simulator).result()
        statevector=result.get_statevector(decimals=4)
        return statevector
        
###############################################################################################################################
    
    def reversedStateVector(self,statevector,num_qubits):
        reversedStateVector=[]
        statevector=statevector.tolist()
        for i in range(len(statevector)):
            pos=int(''.join(reversed(str(("{0:0"+str(num_qubits).replace('.0000','')+"b}").format(i)))),2)
            reversedStateVector.append(statevector[pos])
        return reversedStateVector
    
###############################################################################################################################
    
    def numberFormat(self,num,isImag=False):
        string=str(num)
        test=float(string)
        if test!=0:
            if test>0:
                string="+" if test==1 else "+"+string
            else:
                string="-" if test==-1 else string
            return string+"i" if isImag else string
        return ""
    
###############################################################################################################################

    def diracNotation(self,circuit,statevector):
        diracNotation=""
        for i in range(len(statevector)):
            if statevector[i]==0:
                continue
            diracNotation+=self.numberFormat(statevector[i].real)
            diracNotation+=self.numberFormat(statevector[i].imag,True)
            diracNotation+="|"+str(("{0:0"+str(circuit.num_qubits).replace('.0000','')+"b}").format(i))+"⟩ "
        return diracNotation.lstrip("+")

###############################################################################################################################

    def matrixRepresentation(self,circuit):
        from qiskit import Aer
        from qiskit import execute

        temp = circuit.copy()
        temp.remove_final_measurements()

        simulator = Aer.get_backend('unitary_simulator')
        result = execute(temp, backend=simulator).result()
        unitary = result.get_unitary(decimals=4).tolist()
        #print(unitary)
        for i in range(len(unitary)):
            for j in range(len(unitary[i])):
                if unitary[i][j]==0:
                    unitary[i][j]="0"
                else:
                    string=str(unitary[i][j].real).replace(".0","")
                    string="" if float(string)==0 else string
                    string+=self.numberFormat(unitary[i][j].imag,True)
                    unitary[i][j]=string.lstrip("+")
        return unitary

###############################################################################################################################

    def separatedProbabilities(self,circuit,statevector):
        res=[]
        for j in range(circuit.num_qubits):
            #vector=[0,0] 
            val=0
            for i in range(len(statevector)):
                pos=str(("{0:0"+str(circuit.num_qubits).replace('.0000','')+"b}").format(i))
                if pos[j]=='1':
                    #vector[1]+=abs(statevector[i])**2        
                    val+=abs(statevector[i])**2
                #else:
                    #vector[0]+=abs(statevector[i])**2
                    
            """vector[0]=round(vector[0], 4)
            vector[1]=round(vector[1], 4)
            res=[vector]+res"""
            
            val=round(val*100, 2)
            res.insert(0,val)
            #separated state vectors
            """vector[0]=np.around(vector[0]**0.5, 8)
            vector[1]=np.around(vector[1]**0.5, 8)
            res=[vector]+res"""
            #print(res)
        return res
    
###############################################################################################################################
    
    def separatedBlochSpheres(self,circuit,statevector):
        from qiskit.quantum_info import partial_trace
        pos=list(range(circuit.num_qubits))
        res=[]
        for i in range(circuit.num_qubits):
            [[a, b], [c, d]] = partial_trace(statevector, pos[:i]+pos[i+1:]).data
            x = 2*b.real
            y = 2*c.imag
            z = a.real-d.real
            res.append([x,y,z])
        return res

###############################################################################################################################

    def addCustomGate(self,circuit, gateMatrix, positions, reversedWires=False):
        if reversedWires:
            reversedPositions = []
            for i in range(len(positions)):
                reversedPositions.insert(0,circuit.num_qubits-positions[i]-1)
            positions=reversedPositions
            #positions=reversedPositions[::-1]
        from qiskit.quantum_info.operators import Operator
        customGate = Operator(gateMatrix)
        circuit.unitary(customGate, positions)
        return circuit

###############################################################################################################################

    def graph(self,circuit,numberOfShots,statevector):
        from qiskit import Aer
        from qiskit import execute
        
        temp = circuit.copy()
        temp.remove_final_measurements()
        arr = []
        if temp == circuit:
            for i in range(len(statevector)):
                state = str(("{0:0"+str(circuit.num_qubits).replace('.0000', '')+"b}").format(i))
                arr.append([state,round(abs(statevector[i])**2, 4)])
            return arr
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(circuit, backend=simulator,shots=numberOfShots).result()
        counts = result.get_counts(circuit)
        for i in range(2**circuit.num_qubits):
            state = str(("{0:0"+str(circuit.num_qubits).replace('.0000', '')+"b}").format(i))
            if state in counts:
                arr.append([state,counts[state]/numberOfShots])
            else:
                arr.append([state,0.0])
        return arr

###############################################################################################################################

    # drawing of the circuit
    def draw(self, circuit):
        from qiskit import Aer
        from qiskit import execute

        simulator = Aer.get_backend('qasm_simulator')
        execute(circuit, backend=simulator).result()
        # %matplotlib inline
        return circuit.draw(output='mpl')

###############################################################################################################################

    def runOnIBMQ(self, API_TOKEN, circuit, shots, device):
        from qiskit import IBMQ
        from qiskit import execute
        IBMQ.enable_account(API_TOKEN)
        #print(device)
        provider = IBMQ.get_provider('ibm-q')
        qcomp = provider.get_backend(device)
        job = execute(circuit, backend=qcomp, shots=shots)
        return "https://quantum-computing.ibm.com/results/"+job.job_id()

###############################################################################################################################

    # this function takes name of a gate (str)
    # and returns the matrix of the gate
    def gateToMatrix(self, gate, *radian):
        from qiskit import QuantumCircuit
        from qiskit import Aer
        from qiskit import execute
        if gate == "swap":
            circuit = QuantumCircuit(2)
            circuit.swap(0, 1)
            simulator = Aer.get_backend('unitary_simulator')
            result = execute(circuit, backend=simulator).result()
            return result.get_unitary()
        circuit = QuantumCircuit(1)
        if "(" in gate:
            angle = gate[:-1]
            if not radian:
                angle = gate[0:3]+str((float(gate[3:-1])*22)/(7*180))
            pythonLine = "circuit."+angle+",0)"
            exec(pythonLine)
        else:
            exec("circuit."+gate+"(0)")
        simulator = Aer.get_backend('unitary_simulator')
        result = execute(circuit, backend=simulator).result()
        return result.get_unitary()

###############################################################################################################################

    # this function applies number of controls on a gate
    # and returns matrix representation of the controlled gate
    def controlledGate(self, unitary, numOfControls=1):
        from math import log2

        old = len(unitary)
        new = int(2**(log2(old)+numOfControls))
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

        return controlledGate

###############################################################################################################################

    # this function returns the positions of the multi-Qubit custom gates
    def multiQubitCustomGate(self, column, start, customGates, gateName, end):
        from math import log2
        size = log2(len(customGates[gateName]))
        pos = [None]*int(size)
        pos[int(column[start][end+1:])] = start
        search = column[start][:end]
        for i in range(start+1, len(column)):
            if None not in pos:
                break
            if search == column[i][:end]:
                pos[int(column[i][end+1:])] = i
                column[i] = "i"
        return column, pos

###############################################################################################################################

    # this function applies noncontrolled gates on the circuit
    def nonControlledColumns(self,circuit, column, customGates, radian):
        # naming a custom gate
        # don't accept "." in any position

        for i in range(len(column)):
            if str(column[i]) == "i":
                continue
            if str(column[i]) == "m":
                circuit.measure(i, i)
                continue
            if str(column[i])[:7] == "custom_":
                if customGates == None:
                    print("send custom gates")
                else:
                    end = str(column[i]).find(".")
                    if end == -1:
                        end = len(column[i])
                    gateName = str(column[i])[7:end]
                    if len(customGates[gateName]) == 2:
                        circuit=self.addCustomGate(circuit, customGates[gateName], [i])
                        continue
                    else:
                        column, pos = self.multiQubitCustomGate(column, i, customGates, gateName, end)
                        circuit=self.addCustomGate(circuit, customGates[gateName], pos)
                        continue
            if str(column[i]) == "swap":
                p11 = i
                for j in range(i+1, len(column)):
                    if str(column[j]) == "swap":
                        p22 = j
                        column[j] = "i"
                        break
                circuit.swap(p11, p22)
                continue
            if "(" in str(column[i]):
                angle = column[i][:-1]
                if not radian:
                    angle = column[i][0:3] + str((float(column[i][3:-1])*22)/(7*180))
                pythonLine = "circuit."+angle+","+str(i)+")"
                exec(pythonLine)
                continue

            pythonLine = "circuit."+column[i]+"("+str(i)+")"
            exec(pythonLine)
        
        return circuit

###############################################################################################################################

    def controlledColumns(self, circuit, column, customGates, radian):
        c = []
        oc = []
        for i in range(len(column)):
            if str(column[i]) == "i":
                continue

            if str(column[i]) == "m":
                circuit.measure(i, i)
                column[i] = "i"

            if str(column[i]) == "c":
                c.append(i)
                column[i] = "i"

            elif str(column[i]) == "oc":
                oc.append(i)
                c.append(i)
                column[i] = "i"

        numOfControls = len(c)
        for i in oc:  # open control
            circuit.x(i)

        for i in range(len(column)):
            if str(column[i]) == "i":
                continue
            if str(column[i])[:7] == "custom_":
                if customGates == None:
                    print("send custom gates")
                else:
                    end = str(column[i]).find(".")
                    if end == -1:
                        end = len(column[i])
                    gateName = str(column[i])[7:end]
                    if len(customGates[gateName]) == 2:
                        pos = c+[i]
                    else:
                        column, pos = self.multiQubitCustomGate(column, i, customGates, gateName, end)
                        pos = c+pos
                    circuit=self.addCustomGate(circuit, self.controlledGate(customGates[gateName], numOfControls), pos)
                    continue
            if str(column[i]) == "swap":
                p1 = i
                for j in range(i+1, len(column)):
                    if str(column[j]) == "swap":
                        p2 = j
                        column[j] = "i"
                        break
                pos = c+[p1]+[p2]
                circuit=self.addCustomGate(circuit, self.controlledGate(self.gateToMatrix("swap", radian), numOfControls), pos)
                continue
            pos = c+[i]
            circuit=self.addCustomGate(circuit, self.controlledGate(self.gateToMatrix(column[i], radian), numOfControls), pos)

        for i in oc:  # open control
            circuit.x(i)
    
        return circuit

###############################################################################################################################

    def createCircuit(self, receivedDictionary):
        print("createCircuit")
        from qiskit import QuantumCircuit
        import numpy as np

        resetExist = False
        wires = int(receivedDictionary["wires"])
        
        radian = True
        if "radian" in receivedDictionary:
            radian = receivedDictionary["radian"]
                
        customGates = None
        if "custom" in receivedDictionary:
            customGates = receivedDictionary["custom"]
            for matrix in customGates.values():
                self.strToComplex(matrix)
        
        #kotta
        if "repeated" in receivedDictionary and receivedDictionary["repeated"] != {}:
            receivedDictionary["repeated"]['listOfPos']
            receivedDictionary['rows'] = self.repettion(receivedDictionary["rows"],receivedDictionary["repeated"]['listOfPos'],receivedDictionary["repeated"]['listOfRep'])
            #print(receivedDictionary)


        cols = np.transpose(receivedDictionary["rows"]).tolist()
        
        exeCount = len(cols)
        if "exeCount" in receivedDictionary:
            exeCount = receivedDictionary["exeCount"]
            
        circuit = QuantumCircuit(wires, wires)
        
        circuit=self.initState(circuit, receivedDictionary["init"])
        
        for i in range(exeCount):
            if "reset" in cols[i]:
                resetExist = True
            elif "c" in cols[i] or "oc" in cols[i]:
                circuit=self.controlledColumns(circuit, cols[i], customGates, radian)
            else:
                circuit=self.nonControlledColumns(circuit, cols[i], customGates, radian)
                
        return circuit,resetExist
        
###############################################################################################################################

    def draggable(self, receivedDictionary):
        
        device = 'ibmq_16_melbourne'
        if "device" in receivedDictionary:
            device = receivedDictionary["device"]
            
        shots = 1024
        if "shots" in receivedDictionary:
            shots = receivedDictionary["shots"]
        
        circuit=self.createCircuit(receivedDictionary)[0]
        stateVector=self.stateVector(circuit)
        reversedStateVector=self.reversedStateVector(stateVector,circuit.num_qubits)
        
        self.returnedDictionary["probabilities"] = self.separatedProbabilities(circuit,stateVector)
        self.returnedDictionary["blochSpheres"] = self.separatedBlochSpheres(circuit,stateVector)
        self.returnedDictionary["diracNotation"] = self.diracNotation(circuit,reversedStateVector)
        self.returnedDictionary["qasm"] = circuit.qasm()
        self.returnedDictionary["link"] = ""
        self.returnedDictionary['chart'] = self.graph(circuit, shots,reversedStateVector)
        
        
        if "API_TOKEN" in receivedDictionary:
            if receivedDictionary["API_TOKEN"] != "":
                self.returnedDictionary["link"] = self.runOnIBMQ(receivedDictionary["API_TOKEN"], circuit, shots, device)

###############################################################################################################################
    def createMatrix(self,receivedDictionary):
        print("createMatrix")
        circuit,resetExist=self.createCircuit(receivedDictionary)
    
        if not resetExist:
            self.returnedDictionary["matrixRepresentation"] = self.matrixRepresentation(circuit)  #separated reversed circuit
        else:
            self.returnedDictionary["matrixRepresentation"] = "you can't get matrixRepresentation while using reset gate"
###############################################################################################################################

    def getGates(self, circuit):
        cols = []
        # print(circuit.data[0][1][0].register.size)
        for i in range(len(circuit.data)):
            name = circuit.data[i][0].name
            # print(name)
            if name == "measure":
                name = "m"
            column = ['i']*circuit.data[0][1][0].register.size
            for j in range(len(circuit.data[i][1])):
                pos = circuit.data[i][1][j].index
                # print(pos)
                if 'c' == name[0]:
                    column[pos] = 'c'
                    name = name[1:]
                else:
                    column[pos] = name
                # print(column)
            cols.append(column)
        # print(cols)
        return cols

###############################################################################################################################

    def qasm(self, receivedDictionary):
        import numpy as np
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(1)
        circuit = circuit.from_qasm_str(receivedDictionary["qasm"])
        cols = []
        if("if" not in receivedDictionary["qasm"]):
            cols = self.getGates(circuit)

        shots = receivedDictionary["shots"]
        
        self.circutDrawing = self.draw(circuit)
        # print(cols)
        
        stateVector=self.stateVector(circuit)
        reversedStateVector=self.reversedStateVector(stateVector,circuit.num_qubits)
        
        self.returnedDictionary["probabilities"] = self.separatedProbabilities(circuit,stateVector)
        self.returnedDictionary["blochSpheres"] = self.separatedBlochSpheres(circuit,stateVector)
        self.returnedDictionary["diracNotation"] = self.diracNotation(circuit,reversedStateVector)
        #self.returnedDictionary["link"] = ""
        self.returnedDictionary['chart'] = self.graph(circuit, shots,reversedStateVector)
        self.returnedDictionary["qasmRows"] = np.transpose(cols).tolist()
        
        #if not resetExist:
            #self.returnedDictionary["matrixRepresentation"] = self.matrixRepresentation(circuit)  #separated reversed circuit
        #else:
            #self.returnedDictionary["matrixRepresentation"] = "you can't get matrixRepresentation while using reset gate"
        

###############################################################################################################################
    #{U1, U2, U3, CNOT}

    # this function decompose all gates to {U3,CNOT}
    # u3(θ,φ,λ)=[[cos(θ/2)          (−e^(λi))sin(θ/2)  ]
    #           [e^(φi)sin(θ/2)    (e^(λi+φi))cos(θ/2)]]
    # https://arxiv.org/pdf/1807.01703.pdf

    def decompose(self, circuit):
        while(circuit != circuit.decompose()):
            # print(circuit)
            circuit = circuit.decompose()
        return circuit

###############################################################################################################################

    def elementaryGates(self, rows, customGates):
        for matrix in customGates.values():
            self.strToComplex(matrix)
        import numpy as np
        #print(rows)
        columns = np.transpose(rows).tolist()
        #print(columns)
        i = 0
        while i < len(columns):
            c = []
            for j in range(len(columns[i])):
                if columns[i][j] == "i":
                    continue
                if columns[i][j] == "c" or columns[i][j] == "oc":
                    c.append(j)
                else:
                    gatePos = j
            if len(c) > 1:
                if columns[i][gatePos][7:] in customGates:
                    gateMatrix = customGates[columns[i][gatePos][7:]]
                else:
                    gateMatrix = self.gateToMatrix(columns[i][gatePos])
                if columns[i][gatePos][:7] == "custom_":
                    end = columns[i][gatePos].find(".")
                    #print(columns[i][gatePos], end)
                    if end == -1:
                        name = "√("+columns[i][gatePos][7:]+")"
                    else:
                        name = "√("+columns[i][gatePos][7:end]+")"
                else:
                    name = "√("+columns[i][gatePos]+")"
                if name not in customGates:
                    customGates[name] = self.sqrt(np.array(gateMatrix))
                name2 = name+"†"
                if name2 not in customGates:
                    customGates[name2] = np.matrix(
                        customGates[name]).getH().tolist()

                col = ["i"]*len(columns[i])
                col[c[0]] = columns[i][c[0]]
                col[gatePos] = "custom_"+name
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
                col[gatePos] = "custom_"+name2
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
                col[gatePos] = "custom_"+name
                for k in range(len(c)-2):
                    col[c[k+2]] = columns[i][c[k+2]]
                columns.insert(i+1, col)

                del columns[i]

            if len(c) == 2:
                i = i+4
            elif len(c) > 2:
                i = i-1
            i = i+1

        for matrix in customGates.values():
            # print(matrix)
            self.complexToStr(matrix)

        """colsss=[]    
        for i in range(len(columns)):
            if "custom_√(√(x))" in columns[i] or "custom_√(√(x))†" in columns[i] or "x" in columns[i]:
                colsss.append( columns[i])
        colsss.reverse()"""
        return {"rows": np.transpose(columns).tolist(), "custom": customGates}

###############################################################################################################################

    def strToComplex(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if(type(matrix[i][j]) == type("")):
                    matrix[i][j] = matrix[i][j].replace("i", "j")
                    matrix[i][j] = complex(matrix[i][j])
        return matrix

###############################################################################################################################

    def complexToStr(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if(type(matrix[i][j]) == type(0j)):
                    matrix[i][j] = str(matrix[i][j])
        return matrix

###############################################################################################################################

    def sqrt(self, gate):
        import numpy as np
        from scipy.linalg import fractional_matrix_power
        a = np.matrix(gate)
        return fractional_matrix_power(a, 0.5).tolist()

###############################################################################################################################
    #kotta
    def repettion(self, circuitList, listOfPositions, listOfNumberOfRepetition):
        import numpy as np
        dic = self.dicOfBlockAndPosition(circuitList, listOfPositions, listOfNumberOfRepetition)
        circuitList = np.array(circuitList)
    #repetedBlock , insertPostition , endPosition = blockToRepet(circutList,position)
        for key in dic:
            import numpy as np
            repetedBlock, insertPostition, numberOfRepetition = dic[key]['repetedBlock'], dic[key]['insertPostion'], dic[key]['NumberOfRepetition']
            for repet in range(numberOfRepetition-1):
                circuitList = np.insert(circuitList, insertPostition, repetedBlock, axis=1)
        return circuitList.tolist()
####################################################################################################################################################

    def blockToRepet(self, circutList, position):
        import numpy as np
        circutList = np.array(circutList)
        repetBlock = circutList[:, position[0]: position[1] + 1].transpose()
        return repetBlock, position[0], position[1]
#####################################################################################################################################################

    def dicOfBlockAndPosition(self, circutList, listOfPositions, listOfNumberOfRepetition):
        dicOfPos = {}
        for i in range(len(listOfPositions)):
            repetedBlock, insertPosition, endPosition = self.blockToRepet(
                circutList, listOfPositions[i])
            if i:
                previousInsertPosition = dicOfPos[i]['insertPostion']
                #print(self.factor(insertPosition, endPreviousPos))
                insertPosition = self.positionEquation(previousInsertPosition, listOfNumberOfRepetition[i-1], len(
                    dicOfPos[i]['repetedBlock']), self.factor(insertPosition, endPreviousPos))
            endPreviousPos = endPosition
            dicOfPos[i+1] = {'repetedBlock': repetedBlock, 'insertPostion': insertPosition,'NumberOfRepetition': listOfNumberOfRepetition[i]}

        return dicOfPos
#######################################################################################################################################################

    def positionEquation(self, previousInsertPosition, numberOfRepetition, lengthOfBlock, factor):
        return previousInsertPosition + factor + (numberOfRepetition * lengthOfBlock)
##############################################################################################################################

    def factor(self, startNextPosition, endPreviousPosition):
        fac = startNextPosition - endPreviousPosition
        if fac <= 0:
            return 0
        return fac - 1
#######################################################################################################################################################
