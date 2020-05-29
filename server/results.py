from qiskit import Aer
from qiskit import IBMQ
from qiskit import execute
from qiskit.quantum_info import partial_trace
from qiskit.visualization import plot_bloch_vector
        
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class Results():

    def __init__(self,circuit):
        self.defaultBlochSphere=self.figToResponse(plot_bloch_vector([0,0,1]))
        self.circuit=circuit
        self.num_qubits=self.circuit.num_qubits
        self.circutDrawing=self.draw()
        self.statevector=self.stateVector()
        self.reversedStatevector=self.reversedStateVector()
        
###############################################################################################################################   
        
    def setter(self,shots,API_TOKEN,device,circuit):
        self.shots=int(shots)
        self.API_TOKEN=API_TOKEN
        self.device=device
        self.circuit=circuit
        self.num_qubits=self.circuit.num_qubits
        self.circutDrawing=self.draw()
        self.statevector=self.stateVector()
        self.reversedStatevector=self.reversedStateVector()
        
###############################################################################################################################   
    
    def setCircuit(self,circuit):
        self.circuit=circuit
        self.num_qubits=self.circuit.num_qubits
        self.circutDrawing=self.draw()
        self.statevector=self.stateVector()
        self.reversedStatevector=self.reversedStateVector()
        
###############################################################################################################################  
    
    # this function returns the state vector of a circuit

    # important note .. "according to Qiskit’s convention, first qubit is on the right-hand side"
    # ex: |01⟩  .. 1st qubit is 1 and 2nd qubit is 0
    # so we can correct that by by using reversedStateVector() function
    # you can check that here - https://qiskit-staging.mybluemix.net/documentation/terra/summary_of_quantum_operations.html

    def stateVector(self):    
        simulator=Aer.get_backend('statevector_simulator')
        result=execute(self.circuit,backend=simulator).result()
        statevector=result.get_statevector(decimals=4)
        return statevector.tolist()
    
###############################################################################################################################
           
    # this function returns the state vector for the reversed wires   ex..  factor of |001⟩ will be the factor of |100⟩ 
    # to correct qiskit convention
    # according to Qiskit’s convention, first qubit is on the right-hand side
    # ex: |01⟩  .. 1st qubit is 1 and 2nd qubit is 0

    def reversedStateVector(self):
        reversedStatevector=[]
        for i in range(len(self.statevector)):
            pos=int(''.join(reversed(str(("{0:0"+str(self.num_qubits).replace('.0000','')+"b}").format(i)))),2)
            reversedStatevector.append(self.statevector[pos])
        return reversedStatevector
        
###############################################################################################################################

    # function to enhance dirac notation and matrix representation numbers

    def numberFormat(self,num,isImag=False):
        string=str(num)
        if num!=0:
            if num>0:
                string="+" if num==1 else "+"+string
            else:
                string="-" if num==-1 else string
            return string+"i" if isImag else string
        return ""

###############################################################################################################################
        
    # this function returns dirac notation of the circuit
    # neglects terms with zero probability
    # four digits after floating point

    # important note .. "according to Qiskit’s convention, first qubit is on the right-hand side"
    # ex: |01⟩  .. 1st qubit is 1 and 2nd qubit is 0
    # we corrected that by passing reversedWires=True


    def diracNotation(self):
        diracNotation=""
        for i in range(len(self.reversedStatevector)):
            if self.reversedStatevector[i]==0:
                continue
            diracNotation+=self.numberFormat(self.reversedStatevector[i].real)
            diracNotation+=self.numberFormat(self.reversedStatevector[i].imag,True)
            diracNotation+="|"+str(("{0:0"+str(self.num_qubits).replace('.0000','')+"b}").format(i))+"⟩ "
        return diracNotation.lstrip("+")

###############################################################################################################################
        
    # this function returns readable matrix representation of the whole system
    # four digits after floating point

    # circuit mustn't be measured
    # we use "remove_final_measurements()" function to remove measurments
    # measurements between gates leed to an error (we cann't get matrix representation for these circuits) (need to check)
    # including the initialization gates (need to check)

    def matrixRepresentation(self,decimals=8):
        temp = self.circuit.copy()
        temp.remove_final_measurements()
    
        simulator = Aer.get_backend('unitary_simulator')
        result = execute(temp, backend=simulator).result()
        unitary = result.get_unitary(decimals=decimals).tolist()
        for i in range(len(unitary)):
            for j in range(len(unitary[i])):
                if unitary[i][j]==0:
                    unitary[i][j]="0"
                else:
                    string=str(unitary[i][j].real).replace(".0", "")
                    string="" if unitary[i][j].real==0 else string
                    string+=self.numberFormat(unitary[i][j].imag,True)
                    unitary[i][j]=string.lstrip("+")
        return unitary
        
###############################################################################################################################

    # returns probability of |1⟩ for every wire in a list

    def separatedProbabilities(self):
        res = []
        for j in range(self.num_qubits):
            val = 0
            for i in range(len(self.statevector)):
                pos = str(("{0:0"+str(self.num_qubits).replace('.0000', '')+"b}").format(i))
                if pos[j] == '1':
                    val += abs(self.statevector[i])**2
            val = round(val*100, 2)
            res.insert(0, val)
        return res

###############################################################################################################################

    def graph(self):
        """
        returns the probability of every state as 2D list [ [state, probability], ... ] to be presented on the chart
        probability of a state = its count / total number of shots
        """
        graphData = []
        temp = self.circuit.copy()
        #we apply measurments to all wires to prevent losing counts
        #unmeasured circuits will return all counts as zeros
        temp.measure(list(range(self.num_qubits)),list(range(self.num_qubits-1,-1,-1)))
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(temp, backend=simulator,shots=self.shots).result()
        counts = result.get_counts(temp)
        for i in range(2**self.num_qubits):
            #the next line.. to get the states ex.. i=1 state= 001 for circuit with 3 wires
            #converts i to binary with zero left padding  .. len(state) equals to the number of the wires
            state = str(("{0:0"+str(self.num_qubits).replace('.0000', '')+"b}").format(i)) 
            if state in counts:
                #counts dictionary doesn't contain states with zero probability
                graphData.append([state,counts[state]/self.shots])
            else:
                #we need to append all states even the states with zero probability to display it in the chart
                graphData.append([state,0.0])
        return graphData

###############################################################################################################################       
   
    def figToResponse(self,fig):
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
 
############################################################################################################################### 
        
    def draw(self):
        """
        returns image of the circuit as response object
        """
        fig=self.circuit.draw(output='mpl')
        return self.figToResponse(fig)
    
###############################################################################################################################
        
    # returns polar coordinates for every wire to be represented on bloch spheres

    def separatedBlochSpheres(self):
    
        pos=list(range(self.num_qubits))
        res={}
        for i in range(self.num_qubits):
            [[a, b], [c, d]] = partial_trace(self.statevector, pos[:i]+pos[i+1:]).data
            x = 2*b.real
            y = 2*c.imag
            z = a.real-d.real
            fig=plot_bloch_vector([x,y,z])#,title="qubit "+str(i)
            res[i]=self.figToResponse(fig)
        return res

###############################################################################################################################

    # runs a circuit on a real quantum computer (IBM Q devices) and returns a link of the results

    def runOnIBMQ(self):
        IBMQ.save_account(self.API_TOKEN)
        IBMQ.load_account()
        provider = IBMQ.get_provider('ibm-q')
        qcomp = provider.get_backend(self.device)
        job = execute(self.circuit, backend=qcomp, shots=self.shots)
        return "https://quantum-computing.ibm.com/results/"+job.job_id()

############################################################################################################################### 
        
    def draggableCircuitResults(self):
        returnedDictionary={}
        self.blochSpheres=self.separatedBlochSpheres()
        returnedDictionary["probabilities"] = self.separatedProbabilities()
        #returnedDictionary["blochSpheres"] = self.separatedBlochSpheres()
        returnedDictionary["diracNotation"] = self.diracNotation()
        returnedDictionary["link"] = ""
        returnedDictionary['chart'] = self.graph()
        try:
            returnedDictionary["qasm"] = self.circuit.qasm()
        except Exception:
            #str(Exception)
            returnedDictionary["qasm"] = "//You are using custom gate\n//with size more than 2 qubits\n//sorry, this version doesn't support that\n//qiskit version 0.14.1"
            
        if self.API_TOKEN != "":
            returnedDictionary["link"] = self.runOnIBMQ()
        
        return returnedDictionary
    
###############################################################################################################################
    
    def qasmCircuitResults(self):
        returnedDictionary={}
        self.circutDrawing = self.draw()
        self.blochSpheres=self.separatedBlochSpheres()
        returnedDictionary["wires"]=self.num_qubits
        returnedDictionary["probabilities"] = self.separatedProbabilities()
        #returnedDictionary["blochSpheres"] = self.separatedBlochSpheres()
        returnedDictionary["diracNotation"] = self.diracNotation()
        returnedDictionary['chart'] = self.graph()
        returnedDictionary["link"] = ""
        #returnedDictionary["qasmRows"] = np.transpose(cols).tolist()
        
        if self.API_TOKEN != "":
            returnedDictionary["link"] = self.runOnIBMQ()
        
        return returnedDictionary
    
############################################################################################################################### 