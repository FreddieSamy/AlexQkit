class Circuit():
    def __init__(self):
        self.histoGramGraph = None
        self.blochSphereGraph = None
        self.circutDrawing = None
        self.returnedDictionary={}
    
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

    def initState(self,circuit,stateList,reversedWires=True):
        if reversedWires:
            n=circuit.n_qubits
        else:
            n=1
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
        #circuit.barrier()

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
        return gate_latex  #display(Markdown(gate_latex))

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


    def addCustomGate(self,normalCircuit,reversedCircuit,gateMatrix,positions):
        n=normalCircuit.n_qubits-len(positions)
        reversedPositions=[]
        for i in range(len(positions)):
            reversedPositions.append(n-positions[i]-1)
        reversedPositions.reverse()
        from qiskit.quantum_info.operators import Operator
        customGate=Operator(gateMatrix)
        normalCircuit.unitary(customGate,positions)
        reversedCircuit.unitary(customGate,reversedPositions)
    
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
    
###############################################################################################################################

    #drawing of the circuit
    def draw(self,circuit):
        from qiskit import Aer
        from qiskit import execute
        
        simulator=Aer.get_backend('qasm_simulator')
        execute(circuit,backend=simulator).result()
        #%matplotlib inline
        return circuit.draw(output='mpl')

###############################################################################################################################

    #function to draw bloch spheres of the circuit
    def blochSphere(self,circuit):
        from qiskit import Aer
        from qiskit import execute
        from qiskit.visualization import plot_bloch_multivector
        simulator=Aer.get_backend('statevector_simulator')
        result=execute(circuit,backend=simulator).result()
        statevector=result.get_statevector()
        ##reversed stateVector
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
        
    #we have to check this with multiple users 
    #it saves API_TOKEN locally 
    def runOnIBMQ(self,API_TOKEN,circuit,shots,device):
        from qiskit import IBMQ
        from qiskit import execute
        IBMQ.save_account(API_TOKEN)
        IBMQ.load_account()
        provider=IBMQ.get_provider('ibm-q')
        qcomp=provider.get_backend(device)
        job=execute(circuit,backend=qcomp,shots=shots)
        return "https://quantum-computing.ibm.com/results/"+job.job_id()

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
        if "(" in gate:
            pythonLine="circuit."+gate[:-1]+",0)"
            exec(pythonLine)
        else:
            exec("circuit."+gate+"(0)")
        simulator = Aer.get_backend('unitary_simulator')
        result = execute(circuit, backend=simulator).result()
        return result.get_unitary()

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
    
###############################################################################################################################

    #this function returns the positions of the multi-Qubit custom gates
    def multiQubitCustomGate(self,column,start,customGates,gateName,end):
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
    def nonControlledColumns(self,normalCircuit,reversedCircuit,column,customGates):
        #naming a custom gate
        #don't accept "custom_" in the begining of the name
        #don't accept "." in any position
        
        n = normalCircuit.n_qubits
        for i in range(len(column)):
            if str(column[i])=="i":
                continue
            if str(column[i])=="m":
                reversedCircuit.measure(n-i-1,n-i-1)
                normalCircuit.measure(i,i)
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
                        self.addCustomGate(normalCircuit,reversedCircuit,customGates[gateName],[i])
                        continue
                    else:
                        column,pos=self.multiQubitCustomGate(column,i,customGates,gateName,end)
                        self.addCustomGate(normalCircuit,reversedCircuit,customGates[gateName],pos)
                        continue
            if str(column[i])=="swap":
                p1=n-i-1
                p11=i
                for j in range(i+1,len(column)):
                    if str(column[j])=="swap":
                        p2=n-j-1
                        p22=j
                        column[j]="i"
                        break
                reversedCircuit.swap(p1,p2)
                normalCircuit.swap(p11,p22)
                continue
            if "(" in str(column[i]):
                pythonLine="reversedCircuit."+column[i][:-1]+","+str(n-i-1)+")"
                #print(pythonLine)
                exec(pythonLine)
                
                pythonLine="normalCircuit."+column[i][:-1]+","+str(i)+")"
                #print(pythonLine)
                exec(pythonLine)
                continue
            
            pythonLine="reversedCircuit."+column[i]+"("+str(n-i-1)+")"
            #print(pythonLine)
            exec(pythonLine)
            
            pythonLine="normalCircuit."+column[i]+"("+str(i)+")"
            #print(pythonLine)
            exec(pythonLine)
    
###############################################################################################################################
    
    def controlledColumns(self,normalCircuit,reversedCircuit,column,customGates):
        c=[]
        oc=[]
        n = normalCircuit.n_qubits
        for i in range(len(column)):
            if str(column[i])=="i":
                continue
            
            if str(column[i])=="m":
                normalCircuit.measure(i,i)
                reversedCircuit.measure(n-i-1,n-i-1)
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
            normalCircuit.x(i)
            reversedCircuit.x(n-1-i)
            
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
                        column,pos=self.multiQubitCustomGate(column,i,customGates,gateName,end)
                        pos=c+pos
                    self.addCustomGate(normalCircuit,reversedCircuit,self.controlledGate(customGates[gateName],numOfControls),pos)
                    continue
            if str(column[i])=="swap":
                p1=i
                for j in range(i+1,len(column)):
                    if str(column[j])=="swap":
                        p2=j
                        column[j]="i"
                        break
                pos=c+[p1]+[p2]
                self.addCustomGate(normalCircuit,reversedCircuit,self.controlledGate(self.gateToMatrix("swap"),numOfControls),pos)
                continue
            pos=c+[i]
            self.addCustomGate(normalCircuit,reversedCircuit,self.controlledGate(self.gateToMatrix(column[i]),numOfControls),pos)
        
                
        for i in oc:                                        #open control 
            reversedCircuit.x(n-1-i)
            normalCircuit.x(i)
    
###############################################################################################################################

    #takes json object that represent a circuit
    #returns json object with all results
    
    #("cols" and "wires") are mandatory to get results
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
        
        device='ibmq_16_melbourne'
        resetExist=False
        shots=1024
        customGates=None
        exeCount=0
        if "device" in receivedDictionary:
            device=receivedDictionary["device"]
        if "exeCount" in receivedDictionary:
            exeCount=receivedDictionary["exeCount"]
        if "shots" in receivedDictionary:
            shots=receivedDictionary["shots"]
        if "custom" in receivedDictionary:
            customGates=receivedDictionary["custom"]
        
        if "rows" in receivedDictionary and "wires" in receivedDictionary: #cols and wires are mandatory
            wires=int(receivedDictionary["wires"])
            cols=np.transpose(receivedDictionary["rows"]).tolist()
            normalCircuit=QuantumCircuit(wires,wires)
            reversedCircuit=QuantumCircuit(wires,wires)
        
            if "init" in receivedDictionary:
                self.initState(normalCircuit,receivedDictionary["init"],reversedWires=False)
                self.initState(reversedCircuit,receivedDictionary["init"],reversedWires=True)
        
            for i in range(exeCount):
                if "reset" in cols[i]:
                    resetExist=True
                if cols[i]==["barrier"]:
                    normalCircuit.barrier()
                    reversedCircuit.barrier()
                elif "c" in cols[i] or "oc" in cols[i]:
                    self.controlledColumns(normalCircuit,reversedCircuit,cols[i],customGates)
                else:
                    
                    self.nonControlledColumns(normalCircuit,reversedCircuit,cols[i],customGates)
                    
                   
        self.blochSphereGraph = self.blochSphere(normalCircuit)
        self.histoGramGraph = self.graph(reversedCircuit,shots)
        self.circutDrawing = self.draw(normalCircuit)
    
        if "API_TOKEN" in receivedDictionary:
            if receivedDictionary["API_TOKEN"] !="":
                self.returnedDictionary["diracNotation"]=self.diracNotation(reversedCircuit)
                self.returnedDictionary["qasm"]=normalCircuit.qasm()
                self.returnedDictionary["link"]=self.runOnIBMQ(receivedDictionary["API_TOKEN"],normalCircuit,shots,device)
                if not resetExist:
                    self.returnedDictionary["matrixRepresentation"]=self.matrixRepresentation(reversedCircuit) #self.matrixLatex(self.matrixRepresentation(circuit))
                else:
                    self.returnedDictionary["matrixRepresentation"]="you can't get matrixRepresentation while using reset gate"
            else:
                self.returnedDictionary["diracNotation"]=self.diracNotation(reversedCircuit)
                self.returnedDictionary["qasm"]=normalCircuit.qasm()
                self.returnedDictionary["link"]=""
                if not resetExist:
                     self.returnedDictionary["matrixRepresentation"]=self.matrixRepresentation(reversedCircuit) #self.matrixLatex(self.matrixRepresentation(circuit))
                else:
                    self.returnedDictionary["matrixRepresentation"]="you can't get matrixRepresentation while using reset gate"
            
        
        else:
            self.returnedDictionary["diracNotation"]=self.diracNotation(reversedCircuit)
            self.returnedDictionary["qasm"]=normalCircuit.qasm()
            self.returnedDictionary["link"]=""
            if not resetExist:
                self.returnedDictionary["matrixRepresentation"]=self.matrixRepresentation(reversedCircuit) #self.matrixLatex(self.matrixRepresentation(circuit))
            else:
                    self.returnedDictionary["matrixRepresentation"]="you can't get matrixRepresentation while using reset gate"
            

        #return self.returnedDictionary
###############################################################################################################################
    
    def getGates(self,circuit):
        cols=[]
        #print(circuit.data[0][1][0].register.size)
        for i in range(len(circuit.data)):
            name=circuit.data[i][0].name
            #print(name)
            column=['i']*circuit.data[0][1][0].register.size
            for j in range(len(circuit.data[i][1])):
                pos=circuit.data[i][1][j].index
                #print(pos)
                if 'c' == name[0]:
                    column[pos]='c'
                    name=name[1:]
                else:
                    column[pos]=name
                #print(column)
            cols.append(column)
        #print(cols) 
        return cols
    
###############################################################################################################################

    def qasm(self,receivedDictionary):
        from qiskit import QuantumCircuit
        circuit=QuantumCircuit(1)
        circuit=circuit.from_qasm_str(receivedDictionary["qasm"])
        cols=self.getGates(circuit)
        
        device='ibmq_16_melbourne'
        if "device" in receivedDictionary:
            device=receivedDictionary["device"]
        shots=1024
        if "shots" in receivedDictionary:
            shots=receivedDictionary["shots"]
            
        self.blochSphereGraph = self.blochSphere(circuit)
        self.histoGramGraph = self.graph(circuit,shots)
        self.circutDrawing = self.draw(circuit)    
        if "API_TOKEN" in receivedDictionary:
            if receivedDictionary["API_TOKEN"] !="":
                self.returnedDictionary["diracNotation"]=self.diracNotation(circuit)
                self.returnedDictionary["qasm"]=receivedDictionary["qasm"]
                self.returnedDictionary["link"]=self.runOnIBMQ(receivedDictionary["API_TOKEN"],circuit,shots,device)
                self.returnedDictionary["cols"]=cols
                self.returnedDictionary["matrixRepresentation"]=self.matrixRepresentation(circuit) #self.matrixLatex(self.matrixRepresentation(circuit))
            else:
                self.returnedDictionary["diracNotation"]=self.diracNotation(circuit)
                self.returnedDictionary["qasm"]=receivedDictionary["qasm"]
                self.returnedDictionary["link"]=""
                self.returnedDictionary["matrixRepresentation"]=self.matrixRepresentation(circuit) #self.matrixLatex(self.matrixRepresentation(circuit))
        else:
            self.returnedDictionary["diracNotation"]=self.diracNotation(circuit)
            self.returnedDictionary["qasm"]=receivedDictionary["qasm"]
            self.returnedDictionary["link"]=""
            self.returnedDictionary["cols"]=cols
            self.returnedDictionary["matrixRepresentation"]=self.matrixRepresentation(circuit) #self.matrixLatex(self.matrixRepresentation(circuit))

        #return self.returnedDictionary
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

###############################################################################################################################