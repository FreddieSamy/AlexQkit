class Circuit():
    def __init__(self):
        self.histoGramGraph = None
        self.blochSphereGraph = None
        self.circutDrawing = None
        self.returnedDictionary = {}

###############################################################################################################################

    def initState(self, circuit, stateList, reversedWires=False):
        if reversedWires:
            stateList = stateList[::-1]
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
        # circuit.barrier()

###############################################################################################################################

    def stateVector(self, circuit):
        print("stateVector")
        from qiskit import Aer
        from qiskit import execute

        simulator = Aer.get_backend('statevector_simulator')
        result = execute(circuit, backend=simulator).result()
        statevector = result.get_statevector(decimals=4)
        return statevector

###############################################################################################################################

    def reversedStateVector(self, statevector, num_qubits):
        print("reversedStateVector")
        reversedStateVector = []
        statevector = statevector.tolist()
        for i in range(len(statevector)):
            pos = int(''.join(reversed(
                str(("{0:0"+str(num_qubits).replace('.0000', '')+"b}").format(i)))), 2)
            reversedStateVector.append(statevector[pos])
        return reversedStateVector

###############################################################################################################################

    def numberFormat(self, num, isImag=False):
        print("numberFormat")
        string = str(num)
        test = float(string)
        if test != 0:
            if test > 0:
                string = "+" if test == 1 else "+"+string
            else:
                string = "-" if test == -1 else string
            return string+"i" if isImag else string
        return ""

###############################################################################################################################

    def diracNotation(self, circuit):#, statevector):
        statevector=self.stateVector(circuit)
        diracNotation = ""
        for i in range(len(statevector)):
            if statevector[i] == 0:
                continue
            diracNotation += self.numberFormat(statevector[i].real)
            diracNotation += self.numberFormat(statevector[i].imag, True)
            diracNotation += "|" + \
                str(("{0:0"+str(circuit.num_qubits).replace('.0000', '')+"b}").format(i))+"⟩ "
        return diracNotation.lstrip("+")

###############################################################################################################################

    # this function returns readable matrix representation of the whole system
    # four digits after floating point

    # circuit mustn't be measured
    # we use "remove_final_measurements()" function to remove measurments

    def matrixRepresentation(self, circuit):
        print("matrixRepresentation")
        from qiskit import Aer
        from qiskit import execute

        temp = circuit.copy()
        temp.remove_final_measurements()

        simulator = Aer.get_backend('unitary_simulator')
        result = execute(temp, backend=simulator).result()
        unitary = result.get_unitary(decimals=4).tolist()
        # print(unitary)
        for i in range(len(unitary)):
            for j in range(len(unitary[i])):
                if unitary[i][j] == 0:
                    unitary[i][j] = "0"
                else:
                    string = str(unitary[i][j].real).replace(".0", "")
                    string = "" if float(string) == 0 else string
                    string += self.numberFormat(unitary[i][j].imag, True)
                    unitary[i][j] = string.lstrip("+")
        return unitary

###############################################################################################################################
    def separatedProbabilities(self, circuit, statevector):
        print("separatedProbabilities")
        res = []
        for j in range(circuit.num_qubits):
            # vector=[0,0]
            val = 0
            for i in range(len(statevector)):
                pos = str(
                    ("{0:0"+str(circuit.num_qubits).replace('.0000', '')+"b}").format(i))
                if pos[j] == '1':
                    # vector[1]+=abs(statevector[i])**2
                    val += abs(statevector[i])**2
                # else:
                    # vector[0]+=abs(statevector[i])**2

            """vector[0]=round(vector[0], 4)
            vector[1]=round(vector[1], 4)
            res=[vector]+res"""

            val = round(val*100, 2)
            res.insert(0, val)
            # separated state vectors
            """vector[0]=np.around(vector[0]**0.5, 8)
            vector[1]=np.around(vector[1]**0.5, 8)
            res=[vector]+res"""
            # print(res)
        return res

###############################################################################################################################

    def separatedBlochSpheres(self, circuit, statevector):
        print("separatedBlochSpheres")
        from qiskit.quantum_info import partial_trace
        pos = list(range(circuit.num_qubits))
        res = []
        for i in range(circuit.num_qubits):
            [[a, b], [c, d]] = partial_trace(
                statevector, pos[:i]+pos[i+1:]).data
            x = 2*b.real
            y = 2*c.imag
            z = a.real-d.real
            res.append([x, y, z])
        return res

###############################################################################################################################

    # this function applies a matrix (custom gate) to a circuit in reverse order of positions
    # positions must be list with numbers
    # we must check unitary before storing it
    # to check unitary use  "is_unitary_matrix(data)"

    # important note .. "according to Qiskit’s convention, first qubit is on the right-hand side"
    # ex: |01⟩  .. 1st qubit is 1 and 2nd qubit is 0
    # keep in mind that the matrix entered in correct order (left to right qubits)
    # so to correct the qiskit order we need to shift the custom matrix to the end (newPos=numOfQubits-pos-1 ) then reverse
    # you can check that here - https://qiskit-staging.mybluemix.net/documentation/terra/summary_of_quantum_operations.html

    def addCustomGate(self, normalCircuit, reversedCircuit, gateMatrix, positions):
        reversedPositions = []
        for i in range(len(positions)):
            reversedPositions.append(normalCircuit.n_qubits-positions[i]-1)
        reversedPositions.reverse()
        from qiskit.quantum_info.operators import Operator
        customGate = Operator(gateMatrix)
        normalCircuit.unitary(customGate, positions)
        reversedCircuit.unitary(customGate, reversedPositions)

###############################################################################################################################
   
    def graph(self, circuit, numberOfShots):#, statevector):
        print("graph")
        from qiskit import Aer
        from qiskit import execute
        statevector=self.stateVector(circuit)
        temp = circuit.copy()
        temp.remove_final_measurements()
        arr = []
        if temp == circuit:
            for i in range(len(statevector)):
                state = str(
                    ("{0:0"+str(circuit.num_qubits).replace('.0000', '')+"b}").format(i))
                arr.append([state, round(abs(statevector[i])**2, 4)])
            return arr
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(circuit, backend=simulator,
                         shots=numberOfShots).result()
        counts = result.get_counts(circuit)
        for i in range(2**circuit.num_qubits):
            state = str(
                ("{0:0"+str(circuit.num_qubits).replace('.0000', '')+"b}").format(i))
            if state in counts:
                arr.append([state, counts[state]/numberOfShots])
            else:
                arr.append([state, 0.0])
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

    # function to draw bloch spheres of the circuit
    def blochSphere(self, circuit):
        from qiskit import Aer
        from qiskit import execute
        from qiskit.visualization import plot_bloch_multivector
        simulator = Aer.get_backend('statevector_simulator')
        result = execute(circuit, backend=simulator).result()
        statevector = result.get_statevector()
        # reversed stateVector
        '''if reversedWires:
            temp=[]
            statevector=statevector.tolist()
            #print(statevector)
            for i in range(len(statevector)):
                
                pos=int(''.join(reversed(str(("{0:0"+str(circuit.n_qubits).replace('.0000','')+"b}").format(i)))),2)
                #print(i,pos)
                #print(statevector[pos])
                temp.append(statevector[pos])
            statevector=temp'''
        return plot_bloch_multivector(statevector)

###############################################################################################################################

    def runOnIBMQ(self, API_TOKEN, circuit, shots, device):
        print("runOnIBMQ")
        from qiskit import IBMQ
        from qiskit import execute
        IBMQ.enable_account(API_TOKEN)
        # print(device)
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
    def nonControlledColumns(self, normalCircuit, reversedCircuit, column, customGates, radian):
        # naming a custom gate
        # don't accept "custom_" in the begining of the name
        # don't accept "." in any position

        n = normalCircuit.n_qubits
        for i in range(len(column)):
            if str(column[i]) == "i":
                continue
            if str(column[i]) == "m":
                reversedCircuit.measure(n-i-1, n-i-1)
                normalCircuit.measure(i, i)
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
                        self.addCustomGate(
                            normalCircuit, reversedCircuit, customGates[gateName], [i])
                        continue
                    else:
                        column, pos = self.multiQubitCustomGate(
                            column, i, customGates, gateName, end)
                        self.addCustomGate(
                            normalCircuit, reversedCircuit, customGates[gateName], pos)
                        continue
            if str(column[i]) == "swap":
                p1 = n-i-1
                p11 = i
                for j in range(i+1, len(column)):
                    if str(column[j]) == "swap":
                        p2 = n-j-1
                        p22 = j
                        column[j] = "i"
                        break
                reversedCircuit.swap(p1, p2)
                normalCircuit.swap(p11, p22)
                continue
            if "(" in str(column[i]):
                angle = column[i][:-1]
                if not radian:
                    angle = column[i][0:3] + \
                        str((float(column[i][3:-1])*22)/(7*180))
                pythonLine = "reversedCircuit."+angle+","+str(n-i-1)+")"
                print(pythonLine)
                exec(pythonLine)

                pythonLine = "normalCircuit."+angle+","+str(i)+")"
                # print(pythonLine)
                exec(pythonLine)
                continue

            pythonLine = "reversedCircuit."+column[i]+"("+str(n-i-1)+")"
            # print(pythonLine)
            exec(pythonLine)

            pythonLine = "normalCircuit."+column[i]+"("+str(i)+")"
            # print(pythonLine)
            exec(pythonLine)

###############################################################################################################################

    def controlledColumns(self, normalCircuit, reversedCircuit, column, customGates, radian):
        c = []
        oc = []
        n = normalCircuit.n_qubits
        for i in range(len(column)):
            if str(column[i]) == "i":
                continue

            if str(column[i]) == "m":
                normalCircuit.measure(i, i)
                reversedCircuit.measure(n-i-1, n-i-1)
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
            normalCircuit.x(i)
            reversedCircuit.x(n-1-i)

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
                        column, pos = self.multiQubitCustomGate(
                            column, i, customGates, gateName, end)
                        pos = c+pos
                    self.addCustomGate(normalCircuit, reversedCircuit, self.controlledGate(
                        customGates[gateName], numOfControls), pos)
                    continue
            if str(column[i]) == "swap":
                p1 = i
                for j in range(i+1, len(column)):
                    if str(column[j]) == "swap":
                        p2 = j
                        column[j] = "i"
                        break
                pos = c+[p1]+[p2]
                self.addCustomGate(normalCircuit, reversedCircuit, self.controlledGate(
                    self.gateToMatrix("swap", radian), numOfControls), pos)
                continue
            pos = c+[i]
            self.addCustomGate(normalCircuit, reversedCircuit, self.controlledGate(
                self.gateToMatrix(column[i], radian), numOfControls), pos)

        for i in oc:  # open control
            reversedCircuit.x(n-1-i)
            normalCircuit.x(i)

###############################################################################################################################

    # takes json object that represent a circuit
    # returns json object with all results

    # ("cols" and "wires") are mandatory to get results
    # default number of shots is 1024
    # to run a circuit on IBMQ , "API_TOKEN" must be sent
    # to initialize the circuit , "init" must be sent as a vector ( i.e. [0,1,"+","-","i","-i"] )
    # any used custom gates must be sent
    #                           i.e. "custom":{
    #                                           "not":[[0,1],[1,0]],
    #                                           "I4":[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    #                                         }
    def createCircuit(self, receivedDictionary):
        from qiskit import QuantumCircuit
        import numpy as np

        print("reached in creatCircuit()")

        radian = True
        device = 'ibmq_16_melbourne'
        resetExist = False
        shots = 1024
        customGates = None

        if "radian" in receivedDictionary:
            radian = receivedDictionary["radian"]
        if "device" in receivedDictionary:
            device = receivedDictionary["device"]
        if "shots" in receivedDictionary:
            shots = receivedDictionary["shots"]
        if "custom" in receivedDictionary:
            customGates = receivedDictionary["custom"]
            for matrix in customGates.values():
                self.strToComplex(matrix)
        if "repeated" in receivedDictionary and receivedDictionary["repeated"] != {}:
            receivedDictionary["repeated"]['listOfPos']
            receivedDictionary['rows'] = self.repettion(receivedDictionary["rows"],receivedDictionary["repeated"]['listOfPos'],receivedDictionary["repeated"]['listOfRep'])
            print(receivedDictionary)

        if "rows" in receivedDictionary and "wires" in receivedDictionary:  # cols and wires are mandatory
            wires = int(receivedDictionary["wires"])
            cols = np.transpose(receivedDictionary["rows"]).tolist()
            normalCircuit = QuantumCircuit(wires, wires)
            reversedCircuit = QuantumCircuit(wires, wires)

            exeCount = len(cols)
            if "exeCount" in receivedDictionary:
                exeCount = receivedDictionary["exeCount"]

            if "init" in receivedDictionary:
                self.initState(
                    normalCircuit, receivedDictionary["init"], reversedWires=False)
                self.initState(reversedCircuit,
                               receivedDictionary["init"], reversedWires=True)

            for i in range(exeCount):
                if "reset" in cols[i]:
                    resetExist = True
                if "barrier" in cols[i]:
                    from more_itertools import locate
                    barrierPos = list(locate(cols[i], lambda x: x == 'barrier'))
                    normalCircuit.barrier(barrierPos)
                    reversedCircuit.barrier(barrierPos)
                elif "c" in cols[i] or "oc" in cols[i]:
                    self.controlledColumns(
                        normalCircuit, reversedCircuit, cols[i], customGates, radian)
                else:

                    self.nonControlledColumns(normalCircuit, reversedCircuit, cols[i], customGates, radian)

        self.blochSphereGraph = self.blochSphere(normalCircuit)
        self.histoGramGraph = self.graph(reversedCircuit, shots)
        self.circutDrawing = self.draw(normalCircuit)

        stateVector = self.stateVector(normalCircuit)
        self.returnedDictionary["probabilities"] = self.separatedProbabilities(
            normalCircuit, stateVector)
        self.returnedDictionary["blochSpheres"] = self.separatedBlochSpheres(
            normalCircuit, stateVector)
        self.returnedDictionary["diracNotation"] = self.diracNotation(reversedCircuit)
        #self.returnedDictionary["qasm"] = normalCircuit.qasm()
        self.returnedDictionary["link"] = ""
        self.returnedDictionary['chart'] = self.graph(reversedCircuit, shots)
                
        if "API_TOKEN" in receivedDictionary:
            if receivedDictionary["API_TOKEN"] != "":
                self.returnedDictionary["link"] = self.runOnIBMQ(
                    receivedDictionary["API_TOKEN"], normalCircuit, shots, device)
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

        device = 'ibmq_16_melbourne'
        if "device" in receivedDictionary:
            device = receivedDictionary["device"]
        shots = 1024
        if "shots" in receivedDictionary:
            shots = receivedDictionary["shots"]

        self.blochSphereGraph = self.blochSphere(circuit)
        self.histoGramGraph = self.graph(circuit, shots)
        self.circutDrawing = self.draw(circuit)
        # print(cols)
        if "API_TOKEN" in receivedDictionary:
            if receivedDictionary["API_TOKEN"] != "":
                self.returnedDictionary["diracNotation"] = self.diracNotation(circuit)
                self.returnedDictionary["qasm"] = receivedDictionary["qasm"]
                self.returnedDictionary["link"] = self.runOnIBMQ(receivedDictionary["API_TOKEN"], circuit, shots, device)
                self.returnedDictionary["qasmRows"] = np.transpose(cols).tolist()
                self.returnedDictionary['chart'] = self.graph(reversedCircuit, shots)
                # self.returnedDictionary["matrixRepresentation"]=self.matrixRepresentation(circuit) #self.matrixLatex(self.matrixRepresentation(circuit))
            else:
                self.returnedDictionary["diracNotation"] = self.diracNotation(circuit)
                self.returnedDictionary["qasm"] = receivedDictionary["qasm"]
                self.returnedDictionary["link"] = ""
                self.returnedDictionary["qasmRows"] = np.transpose(cols).tolist()
                self.returnedDictionary['chart'] = self.graph(reversedCircuit, shots)
                # self.returnedDictionary["matrixRepresentation"]=self.matrixRepresentation(circuit) #self.matrixLatex(self.matrixRepresentation(circuit))
        else:
            self.returnedDictionary["diracNotation"] = self.diracNotation(circuit)
            self.returnedDictionary["qasm"] = receivedDictionary["qasm"]
            self.returnedDictionary["link"] = ""
            self.returnedDictionary["qasmRows"] = np.transpose(cols).tolist()
            self.returnedDictionary['chart'] = self.graph(reversedCircuit, shots)
            # self.returnedDictionary["matrixRepresentation"]=self.matrixRepresentation(circuit) #self.matrixLatex(self.matrixRepresentation(circuit))

        # return self.returnedDictionary
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
        print(rows)
        columns = np.transpose(rows).tolist()
        print(columns)
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
                    print(columns[i][gatePos], end)
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
                col[c[1]] = columns[i][c[1]]
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
                col[c[0]] = columns[i][c[0]]
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
                print(self.factor(insertPosition, endPreviousPos))
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
