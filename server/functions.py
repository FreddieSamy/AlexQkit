class Circuit():
    def __init__(self):
        self.returnedDictionary = None
        self.histoGramGraph = None
        self.blochSphereGraph = None
        self.wires = None

    
    
###############################################################################################################################
    
    #this function takes list of initial states and apply equivalent gates in reverse order

    #important note .. "according to Qiskit’s convention, first qubit is on the right-hand side"
    #ex: |01⟩  .. 1st qubit is 1 and 2nd qubit is 0
    #so we corrected that by applying all gates in reverse order  (newPos= numOfQubits - pos - 1)
    #you can check that here - https://qiskit-staging.mybluemix.net/documentation/terra/summary_of_quantum_operations.html

    #you can intialize your circuit with vector that represent your initialization
    #to initialize two qubits with |1⟩ ( initialize a system of two wires by |11⟩  ) ... circuit.initialize([0,0,0,1],[0,1])

    #qiskit always start with |0⟩ state
    #|1⟩ state equivalent to X|0⟩
    #|+⟩ state equivalent to H|0⟩
    #|-⟩ state equivalent to H|1⟩ = HX|0⟩
    #|i⟩ = |↻⟩ state equivalent to S|+⟩ = SH|0⟩
    #|-i⟩ = |↺⟩ state equivalent to S|-⟩ = SH|1⟩ = SHX|0⟩ 

    #then this function applies barrier after initial states

    #dirac notation doc - https://docs.microsoft.com/en-us/quantum/concepts/dirac-notation

    def initState(self,circuit,stateList):
        n=circuit.n_qubits
        for i in range(len(stateList)):
            if str(stateList[i])=="0":
                continue
            elif str(stateList[i])=="1":
                circuit.x(n-i-1)
            elif stateList[i]=="+":
                circuit.h(n-i-1)
            elif stateList[i]=="-":
                circuit.x(n-i-1)
                circuit.h(n-i-1)
            elif stateList[i]=="i":
                circuit.h(n-i-1)
                circuit.s(n-i-1)
            elif stateList[i]=="-i":
                circuit.x(n-i-1)
                circuit.h(n-i-1)
                circuit.s(n-i-1)
        circuit.barrier()
        
    #testing
    """from qiskit import *

    qr=QuantumRegister(6)
    cr=ClassicalRegister(6)
    circuit=QuantumCircuit(qr,cr)

    initState(circuit,["0","1","+","-","i","-i"])

    circuit.h(0)
    circuit.x(0)

    circuit.measure(qr,cr)
    simulator=Aer.get_backend('qasm_simulator')
    result=execute(circuit,backend=simulator).result()

    circuit.draw(output='mpl')"""

###############################################################################################################################


    #this function returns dirac notation of the circuit
    #neglects terms with zero probability
    #four digits after floating point

    #important note .. "according to Qiskit’s convention, first qubit is on the right-hand side"
    #ex: |01⟩  .. 1st qubit is 1 and 2nd qubit is 0
    #we corrected this in another functions 

    def diracNotation(self,circuit):
        from qiskit import Aer
        from qiskit import execute
        #temp=circuit.copy()
        #temp.remove_final_measurements()
        
        simulator=Aer.get_backend('statevector_simulator')
        result=execute(circuit,backend=simulator).result()
        statevector=result.get_statevector()
        #print(float("{0:.4f}".format(float(statevector[0]**2))))
        diracNotation=""
        for i in range(len(statevector)):
            if statevector[i].real==0 and statevector[i].imag==0:
                continue
            if statevector[i].real!=0:
                if diracNotation!="":
                    if statevector[i].real>0:
                        string="{0:.4f}".format(statevector[i].real).replace('.0000','')
                        string="" if abs(float(string))==1 else string
                        diracNotation+="+ "+string
                    else:
                        string="{0:.4f}".format(statevector[i].real*-1).replace('.0000','')
                        string="" if abs(float(string))==1 else string
                        diracNotation+="- "+string
                else:
                    string="{0:.4f}".format(statevector[i].real).replace('.0000','')
                    string="" if abs(float(string))==1 else string
                    diracNotation+=string
                if statevector[i].imag!=0:
                    if statevector[i].imag>0:
                        string="{0:.4f}".format(statevector[i].imag).replace('.0000','')
                        string="" if abs(float(string))==1 else string
                        diracNotation+="+ "+string+"i"
                    else:
                        string="{0:.4f}".format(statevector[i].imag*-1).replace('.0000','')
                        string="" if abs(float(string))==1 else string
                        diracNotation+="- "+string +" i"
            elif statevector[i].imag!=0:
                if statevector[i].imag>0:
                    string="{0:.4f}".format(statevector[i].imag).replace('.0000','')
                    if float(string)==1:
                        diracNotation+="+ i" if diracNotation!="" else "+ i"
                    else:
                        diracNotation+="+ "+string+" i"
                else:       
                    string="{0:.4f}".format(statevector[i].imag*-1).replace('.0000','')
                    if float(string)==-1:
                        diracNotation+="- i" if diracNotation!="" else "- i"
                    else:
                        diracNotation+="- "+string+" i" 
                
            diracNotation+=" |"+str(("{0:0"+str(circuit.n_qubits).replace('.0000','')+"b}").format(i))+"⟩ "
        return diracNotation

    #testing
    """from qiskit import *
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)


    circuit.h(0)
    circuit.cx(0,1)

    #circuit.measure(qr,cr)

    print(diracNotation(circuit))"""

###############################################################################################################################


    #this function returns readable matrix representation of the whole system
    #four digits after floating point

    #circuit mustn't be measured
    #we use "remove_final_measurements()" function to remove measurments


    def matrixRepresentation(self,circuit):
        from qiskit import Aer
        from qiskit import execute
    
        temp=circuit.copy()
        temp.remove_final_measurements()
    
        simulator = Aer.get_backend('unitary_simulator')
        result = execute(temp, backend=simulator).result()
        unitary = result.get_unitary()
        #print(unitary)
        matrix=list()
        for i in range(len(unitary)):
            matrix.append(list())
            for j in range(len(unitary[i])):
                matrix[i].append
                if unitary[i][j].real==0 and unitary[i][j].imag==0:
                    matrix[i].append("0")
                if unitary[i][j].real!=0:
                    matrix[i].append(str("{0:.4f}".format(unitary[i][j].real)).replace('.0000',''))
                    if unitary[i][j].imag!=0:
                        matrix[i][j]+="+"+str("{0:.4f}".format(unitary[i][j].imag).replace('.0000',''))+" i"
                elif unitary[i][j].imag!=0:
                    matrix[i].append(str("{0:.4f}".format(unitary[i][j].imag)+" i").replace('.0000',''))
            
        return matrix

    #testing
    """from qiskit import *
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)


    circuit.x(0)
    circuit.cx(0,1)

    circuit.measure(qr,cr)
    circuit.measure(qr,cr)
    circuit.measure(qr,cr)

    print(circuit)

    print("Matrix Representation before measurement")
    print(matrixRepresentation(circuit))"""
    
###############################################################################################################################

    #displays matrix with mathimatical format
    
    def matrixLatex(self,matrix):
        from IPython.display import display, Markdown
        gate_latex = '\\begin{pmatrix}'
        for line in matrix:
            for element in line:
                gate_latex += str(element) + '&'
            gate_latex  = gate_latex[0:-1]
        
            gate_latex +=  ' \\\\ '
        gate_latex  = gate_latex[0:-4]
        gate_latex += '\end{pmatrix}'
        return display(Markdown(gate_latex))#gate_latex


    #testing
    """from qiskit import *
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)


    circuit.x(0)
    circuit.cx(0,1)

    circuit.measure(qr,cr)

    print("Matrix Representation before measurement")
    matrixLatex(matrixRepresentation(circuit))"""

###############################################################################################################################
    
    #this function applies a matrix (custom gate) to a circuit in reverse order of positions
    #positions must be list with numbers
    #we must check unitary before storing it 
    #to check unitary use  "is_unitary_matrix(data)"

    #important note .. "according to Qiskit’s convention, first qubit is on the right-hand side"
    #ex: |01⟩  .. 1st qubit is 1 and 2nd qubit is 0
    #keep in mind that the matrix entered in correct order (left to right qubits)
    #so to correct the qiskit order we need to shift the custom matrix to the end (newPos=numOfQubits-pos-1 ) then reverse
    #you can check that here - https://qiskit-staging.mybluemix.net/documentation/terra/summary_of_quantum_operations.html


    def addCustomGate(self,circuit,gateMatrix,positions):
        circuit.n_qubits-len(positions)
        for i in range(len(positions)):
            positions[i]=circuit.n_qubits-positions[i]-1
        positions.reverse()
        from qiskit.quantum_info.operators import Operator
        customGate=Operator(gateMatrix)
        circuit.unitary(customGate,positions)
        
    
    #testing
    """from qiskit import *

    qr=QuantumRegister(4)
    cr=ClassicalRegister(4)
    circuit=QuantumCircuit(qr,cr)
    Matrix=[[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]
    
    addCustomGate(circuit,Matrix,[0,1])
    
    circuit.measure(qr,cr)
    simulator=Aer.get_backend('qasm_simulator')
    result=execute(circuit,backend=simulator).result()
    
    matrixLatex(matrixRepresentation(circuit))

    circuit.draw(output='mpl')"""
    
###############################################################################################################################

    #this function returns matplotlib figure of the probabilities
    #we can use the count data to draw a plot histogram with probabilities
    #plot_histogram(graphData(circuit,numberOfShots))
    #divide all counts by number of shots to get probabilities 
    
    #circuit must be measured to get counts
    #count data will return all zeros if we don't apply measurements
    #we should disply probabilities of the system anyway, we can get it from the "statevector" 
    #probability = |statevector elements| ** 2

    def graph(self,circuit,numberOfShots):
        from qiskit import Aer
        from qiskit import execute
        from qiskit.tools.visualization import plot_histogram
        
        temp=circuit.copy()
        temp.remove_final_measurements()
        if temp==circuit:
            simulator=Aer.get_backend('statevector_simulator')
            result=execute(circuit,backend=simulator).result()
            statevector=result.get_statevector()
            dic={}
            for i in range(len(statevector)):
                state=str(("{0:0"+str(circuit.n_qubits).replace('.0000','')+"b}").format(i))
                dic[state]=round(abs(statevector[i])**2,4)

            return plot_histogram(dic,figsize=(10,6))
        
        simulator=Aer.get_backend('qasm_simulator')
        result=execute(circuit,backend=simulator,shots=numberOfShots).result()
        counts=result.get_counts(circuit)
        dic={}
        for i in range(2**circuit.n_qubits):
            state=str(("{0:0"+str(circuit.n_qubits).replace('.0000','')+"b}").format(i))
            if state in counts:
                dic[state]=counts[state]/numberOfShots
            else:
                dic[state]=0.0
    
        return plot_histogram(dic,figsize=(10,6))

    """#testing 
    from qiskit import *
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)

    circuit.h(0)
    circuit.cx(0,1)
    
    #circuit.measure(qr,cr)
    graph(circuit,1024*2)"""

###############################################################################################################################

    #drawing of the circuit
    def draw(self,circuit):
        from qiskit import Aer
        from qiskit import execute
        
        simulator=Aer.get_backend('qasm_simulator')
        execute(circuit,backend=simulator).result()
        #%matplotlib inline
        return circuit.draw(output='mpl')

    #testing
    """from qiskit import *
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)

    circuit.x(0)
    circuit.cx(0,1)

    circuit.measure(qr,cr)
    draw(circuit)"""

###############################################################################################################################

    #function to draw bloch spheres of the circuit
    def blochSphere(self,circuit):
        from qiskit import Aer
        from qiskit import execute
        from qiskit.visualization import plot_bloch_multivector
        simulator=Aer.get_backend('statevector_simulator')
        result=execute(circuit,backend=simulator).result()
        statevector=result.get_statevector()
        return plot_bloch_multivector(statevector)


    #testing
    """from qiskit import *
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)

    circuit.x(0)
    circuit.cx(0,1)

    circuit.measure(qr,cr)
    blochSphere(circuit)"""
    
    
###############################################################################################################################
    
    
    #we have to check this with multiple users 
    #it saves API_TOKEN locally 
    def runOnIBMQ(self,API_TOKEN,circuit,shots):
        from qiskit import IBMQ
        from qiskit import execute
        IBMQ.save_account(API_TOKEN)
        IBMQ.load_account()
        provider=IBMQ.get_provider('ibm-q')
        qcomp=provider.get_backend('ibmq_16_melbourne')
        job=execute(circuit,backend=qcomp,shots=shots)
        return "https://quantum-computing.ibm.com/results/"+job.job_id()

    #testing
    """API_TOKEN=""
    
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)
    circuit.h(0)
    circuit.cx(0,1)

    job=runOnIBMQ(API_TOKEN,circuit)

    #print("https://quantum-computing.ibm.com/results/"+job.job_id())

    #from qiskit.tools.monitor import job_monitor
    #job_monitor(job)"""

###############################################################################################################################
    
    #this function takes name of a gate (str)
    #and returns the matrix of the gate 
    def gateToMatrix(self,gate):
        from qiskit import QuantumCircuit
        from qiskit import Aer
        from qiskit import execute
        if gate=="swap":
            circuit=QuantumCircuit(2)
            circuit.swap(0,1)
            simulator = Aer.get_backend('unitary_simulator')
            result = execute(circuit, backend=simulator).result()
            return result.get_unitary()
        circuit=QuantumCircuit(1)
        exec("circuit."+gate+"(0)")
        simulator = Aer.get_backend('unitary_simulator')
        result = execute(circuit, backend=simulator).result()
        return result.get_unitary()

    """#testing
    matrixLatex(gateToMatrix("x"))"""


###############################################################################################################################

    #this function applies number of controls on a gate
    #and returns matrix representation of the controlled gate
    def controlledGate(self,unitary,numOfControls=1):
        from math import log2
    
        old=len(unitary)
        new=int(2**(log2(old)+numOfControls))
        controlledGate=[]
    
        for i in range(new):
            controlledGate.append([])
            for j in range(new):
                if (i>=new-old) and (j>=new-old):
                    controlledGate[i].append(unitary[i-new+old][j-new+old])
                elif i==j:
                    controlledGate[i].append(1)
                else:
                    controlledGate[i].append(0)

        return controlledGate
    
    """#testing
    circuit=QuantumCircuit(3)
    ccx=controlledGate(gateToMatrix("x"),2)
    matrixLatex(ccx)
    addCustomGate(circuit,ccx,[0,1,2])
    matrixLatex(matrixRepresentation(circuit))
    circuit.draw()"""
            
        
###############################################################################################################################

    #this function returns the positions of the multi-Qubit custom gates
    def multiQubitCustomGate(self,circuit,column,start,customGates,gateName,end):
        from math import log2
        size=log2(len(customGates[gateName]))
        pos=[None]*int(size)
        pos[int(column[start][end+1:])]=start
        search=column[start][:end]
        for i in range(start+1,len(column)):
            if None not in pos:
                break
            if search==column[i][:end]:
                pos[int(column[i][end+1:])]=i
                column[i]="i"
        return column,pos 
    
###############################################################################################################################
    
    #this function applies noncontrolled gates on the circuit
    def nonControlledColumns(self,circuit,column,customGates):
        #naming a custom gate
        #don't accept "custom_" in the begining of the name
        #don't accept "." in any position
        for i in range(len(column)):
            if str(column[i])=="i":
                continue
            if str(column[i])=="m":
                circuit.measure(circuit.n_qubits-i-1,circuit.n_qubits-i-1)
                continue
            if str(column[i])[:7]=="custom_":
                if customGates==None:
                    print("send custom gates")
                else:
                    end=str(column[i]).find(".")
                    if end==-1:
                        end=len(column[i])
                    gateName=str(column[i])[7:end]
                    if len(customGates[gateName])==2:
                        self.addCustomGate(circuit,customGates[gateName],[i])
                        continue
                    else:
                        column,pos=self.multiQubitCustomGate(circuit,column,i,customGates,gateName,end)
                        self.addCustomGate(circuit,customGates[gateName],pos)
                        continue
            if str(column[i])=="swap":
                p1=circuit.n_qubits-i-1
                for j in range(i+1,len(column)):
                    if str(column[j])=="swap":
                        p2=circuit.n_qubits-j-1
                        column[j]="i"
                        break
                circuit.swap(p1,p2)
                continue
            pythonLine="circuit."+column[i]+"("
            pythonLine+=str(circuit.n_qubits-i-1)
            pythonLine+=")"
            #print(pythonLine)
            exec(pythonLine)
        
    #testing
    """from qiskit import QuantumCircuit
    customGates = {
                   "not":[[0,1],[1,0]],
                   "I4":[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
                   }
    column=["h","custom_not","swap","custom_I4.0","swap","custom_I4.1"]
    '''["h"],
    ["x"],
    ["y"],
    ["z"],
    ["s"],
    ["sdg"],
    ["t"],
    ["tdg"],
    ["","","","","","custom_not"],
    ["","","","custom_I4.1","","custom_I4.0"]  '''
    circuit=QuantumCircuit(6)
    nonControlledColumns(circuit,column,customGates)
    circuit.draw()
    #matrixLatex(matrixRepresentation(circuit))"""
    
    
###############################################################################################################################
    
    def controlledColumns(self,circuit,column,customGates):
        c=[]
        oc=[]
        for i in range(len(column)):
            if str(column[i])=="i":
                continue
            
            if str(column[i])=="m":
                circuit.measure(circuit.n_qubits-i-1,circuit.n_qubits-i-1)
                column[i]="i"
        
            if str(column[i])=="c":
                c.append(i)
                column[i]="i"
                
            elif str(column[i])=="oc":
                oc.append(i)
                c.append(i)  
                column[i]="i"
        
        numOfControls=len(c)
        for i in oc:                                       #open control 
            circuit.x(circuit.n_qubits-1-i)
            
        for i in range(len(column)):
            if str(column[i])=="i":
                continue
            if str(column[i])[:7]=="custom_":
                if customGates==None:
                    print("send custom gates")
                else:
                    end=str(column[i]).find(".")
                    if end==-1:
                        end=len(column[i])
                    gateName=str(column[i])[7:end]
                    if len(customGates[gateName])==2:
                        pos=c+[i]
                    else:
                        column,pos=self.multiQubitCustomGate(circuit,column,i,customGates,gateName,end)
                        pos=c+pos
                    self.addCustomGate(circuit,self.controlledGate(customGates[gateName],numOfControls),pos)
                    continue
            if str(column[i])=="swap":
                p1=i
                for j in range(i+1,len(column)):
                    if str(column[j])=="swap":
                        p2=j
                        column[j]="i"
                        break
                pos=c+[p1]+[p2]
                self.addCustomGate(circuit,self.controlledGate(self.gateToMatrix("swap"),numOfControls),pos)
                continue
            pos=c+[i]
            self.addCustomGate(circuit,self.controlledGate(self.gateToMatrix(column[i]),numOfControls),pos)
        
                
        for i in oc:                                        #open control 
            circuit.x(circuit.n_qubits-1-i)

        
    #testing
    """from qiskit import QuantumCircuit
    customGates = {
                   "not":[[0,1],[1,0]],
                   "I4":[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
                   }
    column=["x","custom_not","oc","","c","x","swap","swap"]
    '''["h"],
    ["x"],
    ["y"],
    ["z"],
    ["s"],
    ["sdg"],
    ["t"],
    ["tdg"],
    ["","","","","","custom_not"],
    ["","","","custom_I4.1","","custom_I4.0"]  '''
    circuit=QuantumCircuit(9)
    controlledColumns(circuit,column,customGates)
    circuit.draw()
    #matrixLatex(matrixRepresentation(circuit))"""
    
    
###############################################################################################################################

    #the main function
    #takes json object that represent a circuit
    #returns json object with all results
    
    #("cols" and "wires") or "qasm" in received json object is mandatory to get results
    #default number of shots is 1024
    #to run a circuit on IBMQ , "API_TOKEN" must be sent 
    #to initialize the circuit , "init" must be sent as a vector ( i.e. [0,1,"+","-","i","-i"] )
    #any used custom gates must be sent 
    #                           i.e. "custom":{
    #                                           "not":[[0,1],[1,0]],
    #                                           "I4":[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    #                                         }
    def createCircuit(self,receivedDictionary):
        from qiskit import QuantumCircuit
        import numpy as np
    
        print("reached in creatCircuit()")
        
        shots=1024
        customGates=None
        if "shots" in receivedDictionary:
            shots=receivedDictionary["shots"]
        if "custom" in receivedDictionary:
            customGates=receivedDictionary["custom"]
    
    
        if "qasm" in receivedDictionary:
            circuit=QuantumCircuit(1)
            circuit=circuit.from_qasm_str(receivedDictionary["qasm"])
        
        elif "rows" in receivedDictionary and "wires" in receivedDictionary: #cols and wires are mandatory
            wires=int(receivedDictionary["wires"])
            cols=np.transpose(receivedDictionary["rows"]).tolist()
            circuit=QuantumCircuit(wires,wires)
        
            if "init" in receivedDictionary:
                self.initState(circuit,receivedDictionary["init"])
        
            for i in range(len(cols)):
                if cols[i]==["barrier"]:
                    circuit.barrier()
                elif "c" in cols[i] or "oc" in cols[i]:
                    self.controlledColumns(circuit,cols[i],customGates)
                else:
                    self.nonControlledColumns(circuit,cols[i],customGates)
                    
        else:
            return {}
    
        if "API_TOKEN" in receivedDictionary:
 
            self.returnedDictionary={"diracNotation":self.diracNotation(circuit),
                                "matrixRepresentation":self.matrixRepresentation(circuit),
                                "qasm":circuit.qasm(),
                                "blochSphere":self.blochSphere(circuit),
                                "graph":self.graph(circuit,shots),
                                "draw":self.draw(circuit),
                                "circuit":circuit
                                  }
            
        else:
            self.returnedDictionary={"diracNotation":self.diracNotation(circuit),
                                "matrixRepresentation":self.matrixRepresentation(circuit), #self.matrixLatex(self.matrixRepresentation(circuit)),
                                "qasm":circuit.qasm(),
                                "blochSphere":self.blochSphere(circuit),
                                "graph":self.graph(circuit,shots),
                                "draw":self.draw(circuit),
                                "circuit":circuit
                                  }

        return self.returnedDictionary
        
        
    
        
    #testing 
    #from qiskit import circuit

    #run on simulator
    """dic={
         "wires":6,
         "cols":[["h"],
                 ["x"],
                 ["y"],
                 ["z"],
                 ["s"],
                 ["sdg"],
                 ["t"],
                 ["tdg"],
                 ["barrier"],
                 ["","swap","swap"],
                 ["","c","x"],
                 ["","oc","x"],
                 ["barrier"],
                 ["","","","c","swap","swap"],
                 ["","","","oc","swap","swap"],
                 ["","","","c","c","x"],
                 ["","","","oc","oc","x"],
                 ["barrier"],
                 ["","","c","c","swap","swap"],
                 ["","","oc","oc","swap","swap"],
                 ["","","c","c","c","x"],
                 ["","","oc","oc","oc","x"],
                 ["barrier"],
                 ["","","","","","custom_not"],
                 ["","","","custom_I4.0","","custom_I4.1"],
                 ["barrier"],
                 ["","","","","c","custom_not"],
                 ["","","c","custom_I4.0","c","custom_I4.1"],
                 ["barrier"],
                 ["","","","","oc","custom_not"],
                 ["","","oc","custom_I4.0","oc","custom_I4.1"],
                 ["barrier"],
                 ["m","m","m","m","m","m"]
                 ],
         "init":[0,1,"+","-","i","-i"],
         "shots":2048,
         "custom":{
                   "not":[[0,1],[1,0]],
                   "I4":[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
                   }
         }"""
    """dic={
         "wires":2,
         "cols":[["h",""],
                 ["c","x"]],
         "shots":2048
         }"""
     
    #dic={"qasm":'OPENQASM 2.0;include "qelib1.inc";qreg q1[2];creg c1[2];x q1[0];cx q1[0],q1[1];measure q1[0] -> c1[0];measure q1[1] -> c1[1];'}

    #run on IBMQ
    """dic={
     "API_TOKEN":""
     "wires":6,
     "cols":[["h"],
             ["x"],
             ["y"],
             ["z"],
             ["s"],
             ["sdg"],
             ["t"],
             ["tdg"],
             ["barrier"],
             ["","c","h"],
             ["","c","x"],
             ["","c","y"],
             ["","c","z"],
             ["","oc","h"],
             ["","oc","x"],
             ["","oc","y"],
             ["","oc","z"],
             ["","swap","swap"],
             ["barrier"],
             ["","","","c","c","x"],
             ["","","","c","swap","swap"],
             ["","","","oc","oc","x"],
             ["","","","oc","swap","swap"],
             ["barrier"],
             ["","","","","","custom_not"],
             ["","","","custom_I4","","custom_I4"]],
     "init":[0,1,"+","-","i","-i"],
     "shots":2048,
     "custom":{
               "not":[[0,1],[1,0]],
               "I4":[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
               }
     }
    
    createCircuit(dic)
    c=createCircuit(dic)["circuit"]
    draw(c)"""

###############################################################################################################################
    #{U1, U2, U3, CNOT}

    #this function decompose all gates to {U3,CNOT}
    #u3(θ,φ,λ)=[[cos(θ/2)          (−e^(λi))sin(θ/2)  ]
    #           [e^(φi)sin(θ/2)    (e^(λi+φi))cos(θ/2)]]
    #https://arxiv.org/pdf/1807.01703.pdf

    def decompose(self,circuit):
        while(circuit!=circuit.decompose()):
            #print(circuit)
            circuit=circuit.decompose()
        return circuit

    #testing
    """from qiskit import *

    circuit=QuantumCircuit(3,3)

    circuit.ccx(0,1,2)
    circuit=decompose(circuit)
    print("\n\nToffoli gate decomposition:")
    circuit.draw(output='mpl')"""
###############################################################################################################################