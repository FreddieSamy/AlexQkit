from stateVectorNormalization import Normalization
from repeat import Repeat
from results import Results
from qiskit import QuantumCircuit
import qiskit.circuit.library.standard_gates as gates
from qiskit.circuit.library import Reset
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
        self.gatesObjects={
                "X":gates.XGate(),
                "Y":gates.YGate(),
                "Z":gates.ZGate(),
                "H":gates.HGate(),
                "S":gates.SGate(),
                "T":gates.TGate(),
                "Sdg":gates.SdgGate(),
                "Tdg":gates.TdgGate(),
                "Swap":gates.SwapGate(),
                "Reset":Reset()
                }

###############################################################################################################################

    def setter(self,receivedDictionary):
        """
        set the data for a new circuit 
        """
        self.radian = receivedDictionary["radian"]
        self.exeCount = receivedDictionary["exeCount"]
        self.num_qubits = int(receivedDictionary["wires"])
        self.circuit = QuantumCircuit(self.num_qubits, self.num_qubits)
        self.init=receivedDictionary["init"]
        
        if receivedDictionary["repeated"] != {}: #apply loops if exist
            oldSize=len(receivedDictionary["rows"][0])
            self.cols = Repeat.repettion(receivedDictionary["rows"], receivedDictionary["repeated"]['listOfPos'], receivedDictionary["repeated"]['listOfRep'])
            self.cols = np.transpose(self.cols).tolist()
            newSize=len(self.cols)
            self.exeCount+=(newSize-oldSize)
        else: #frontend deals with wires and backend deals with columns, so we need to transpose it
            self.cols = np.transpose(receivedDictionary["rows"]).tolist() #2D list contains circuit gates 

###############################################################################################################################
       
    def subCircuitSetter(self,receivedDictionary):
        """
        set the data for a sub-circuit 
        """
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
            if stateList[i] == "0":
                continue
            elif stateList[i] == "1":
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
        
        custom gates represented as ..  c<num_qubits>_<name>.<index>
        
        ex.. col=["i","c2_not.1","i","c2_not.0"] -> name=not, num_qubits=2 pos=[3,1] 
        means that not is a 2 qubit gate should apply to the 2nd and the 4th wire
        the first input for this gate is the 4th wire and the second input is th 2nd wire 
        
        indices give us the arrangement of the input wires to the gate
        indices must start with 0 and end with n-1  ex.. 3 qubit gate indices are 0,1,2 in any order
        
        naming a custom gate..
        don't accept "." in any position
        """
        pointPos = column[firstAppear].find(".")
        underscorePos = column[firstAppear].find("_")
        if pointPos == -1:
            pointPos = len(column[firstAppear])
        gateName = str(column[firstAppear])[underscorePos+1:pointPos]
        if int(column[firstAppear][1:underscorePos]) == 1: #one wire
            pos=[firstAppear]
        else:
            index=int(column[firstAppear][pointPos+1:])
            pos=[firstAppear]
            #pos.insert(index,firstAppear)
            for i in range(firstAppear+1, len(column)):
                if column[firstAppear][:pointPos] == column[i][:pointPos]:
                    index=int(column[i][pointPos+1:])
                    pos.insert(index,i)  #arrange the input wires according to the indices
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
            if str(column[j]) == "Swap":
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
            #empty -> do nothing
            if str(column[i]) != "i":
                #measurement
                if column[i] == "M": 
                    self.circuit.measure(i, i)
                #custom gates
                elif column[i][0] == "c": 
                    column, pos, gateName = self.customGateInfo(column, i)
                    self.circuit.append(self.gatesObjects[gateName], pos)
                #swap
                elif column[i] == "Swap":
                    column,pos=self.swapPos(column,i)
                    self.circuit.swap(pos[0],pos[1])
                #gates with angles rx,ry,rz
                elif "(" in column[i]:  
                    gate=self.gatesWithAngles(column[i])
                    self.circuit.append(gate,[i])
                #any other gate
                else:
                    self.circuit.append(self.gatesObjects[column[i]], [i])

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

    def gatesWithAngles(self,gatename):
        """
        return gate object of rx, ry and rz
        """
        name=gatename[0:2].upper()
        angle = gatename[3:-1]
        if not self.radian:
            angle = str((float(angle)*3.14)/180)
        pythonLine="global gate; gate=gates."+name+"Gate("+angle+")"
        exec(pythonLine)
        return gate
            
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
            gateName=column[i]
            #controlled custom gates
            if gateName[0] == "c":
                column, pos, gateName = self.customGateInfo(column, i)
                pos = c+pos
                gate=self.gatesObjects[gateName].control(numOfControls)
                self.circuit.append(gate,pos)
                continue
            #controlled swap
            if str(column[i]) == "Swap":
                column,pos=self.swapPos(column,i)
                pos = c+pos
                gate=gates.SwapGate().control(numOfControls)
                self.circuit.append(gate,pos)
                continue
            pos = c+[i]
            #gates with angles rx,ry,rz
            if "(" in str(column[i]): 
                gate=self.gatesWithAngles(column[i]).control(numOfControls)
                self.circuit.append(gate,pos)
                continue
            #any other controlled gate
            gate=self.gatesObjects[gateName].control(numOfControls)
            self.circuit.append(gate,pos)

        for i in oc:   #applying x gate before and after a closed control to convert it to an open control
            self.circuit.x(i)

###############################################################################################################################
            
    def conditionalLoop(self,column,index):
        r=Results(self.circuit)
        newInitialization=Normalization.buildLoopCond(self.num_qubits,column,r.reversedStatevector)
        if all(ele == 0 for ele in newInitialization):
            raise Exception("conditional loop at column "+str(index)+" will never be satisfied (infinite loop)")
        self.circuit=QuantumCircuit(self.num_qubits, self.num_qubits)
        self.circuit.initialize(newInitialization,list(range(self.num_qubits-1,-1,-1)))
            
###############################################################################################################################

    def createDraggableCircuit(self):
        """
        applies all gates of the draggable circuit to self.citcuit
        and returns the circuit after construction
        
        dealing with cols as a representation of the circuit 
        cols is a 2D list contains every gate of the circuit in its position
        
        ex.. cols=[["h","i"], ["c","x"]]  entanglement  
        circuit with 2 wires 
        
        gates representation in cols..
        x,y,z,h,s,t,sdg,tdg,rx(<angle>),ry(<angle>),rz(<angle>),reset
        i : empty places (identity)
        m : measure
        ● : control
        ○ : open control
        swap : to swap two qubits it must be in the same column at the qubits positions
               ex.. ["swap","i","swap"] to swap q0 with q2
               swap must appear exactly two times if needed in the column  
               
        custom gates represented as ..  c<num_qubits>_<name>.<index>
        ex.. ["i","c2_not.1","i","c2_not.0"] -> name=not, num_qubits=2, pos=[3,1] 
        all custom gates stored in self.gatesObjects as Gate() objects
        """
        self.initState() #apply (init list) initial values to the citcuit
        for i in range(self.exeCount):  #stop at tracing line position
              
            if self.cols[i][0][0]=="l": #check if the column is a conditional loop column given as ["loop.0","loop.1","loop.*",...]
                self.conditionalLoop(self.cols[i],i)
            elif "●" in self.cols[i] or "○" in self.cols[i]: # check if the column contains controls
                self.controlledColumns(self.cols[i])         # it will be checked in the frontend and receive a list of flags
            else:                                            # control flags [q0,q1,...]
                self.nonControlledColumns(self.cols[i])
        
        return self.circuit
    
###############################################################################################################################
    
    def createQasmCircuit(self,qasmText):
        """
        constructs a circuit from the qasm code and returns it
        """
        tempCircuit = QuantumCircuit(1)
        self.circuit = tempCircuit.from_qasm_str(qasmText)
        
        return self.circuit
    
############################################################################################################################### 