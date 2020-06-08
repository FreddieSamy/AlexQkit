from itertools import product
from math import sqrt
class Normalization :
    def __init__(self):
        pass
# you can call this method without instantiate the whole class (as) CertainLoop.buildLoopCond(numWires,wiresep,stateVector).
    @classmethod
    def buildLoopCond(cls,numWires,wiresep,stateVector):
        dicPosabilities = cls().collectedPosabilities(numWires,wiresep,stateVector)
        sqrtSumPosabilities = sqrt(cls().sumStateVector(dicPosabilities))
        updatedStateVector = cls().updatedStateVec(len(stateVector),dicPosabilities,sqrtSumPosabilities)
        return updatedStateVector
   
# this method collect the posabilities based on condation like "01","01*""011","*01*" and etc .
    def collectedPosabilities(self,numWires,wiresSep,stateVector):
        dicsaveStateVec = {} # Dictionary for saving the states that satisifies condation to compute .
        generatePosWires = list(product(["0","1"],repeat=numWires)) # Generat every possible values for wires ,then Cast the returned product to list for manipulation
        for ind in range(len(generatePosWires)) :
            flag = 0
            for index in range(len(wiresSep)) :
                if wiresSep[index][-1] != "*" :
                    if generatePosWires[ind][index] != wiresSep[index][-1] :
                        flag = 1
                        break
            if flag == 0 and stateVector[ind] != 0j: # If state satisfies condation will insert in dictionary
                dicsaveStateVec[ind] = stateVector[ind]
        return dicsaveStateVec
        
# this method calculate the summation of condtion based on state vector 
    def sumStateVector(self,stateVector):
        summ = 0
        for state in stateVector :
            summ += abs(stateVector[state]**2) 
        return summ
    
#this method update the state vector based on condition of user  
    def updatedStateVec(self,lengthStateVector,dicPosabilities,sqrtSumPosabilities):
        stateVector = [0j]*lengthStateVector
        for i in dicPosabilities :
            stateVector[i] =  dicPosabilities[i] / sqrtSumPosabilities
        return stateVector

#the bellow lines are test cases for 3 wires and 4 wires

#numWires = 3
#stateVector = [(0.5-0j), (-0.5+0j), 0j, 0j, (0.5-0j), (-0.5+0j), 0j, 0j]
#wiresep = "0*1"
#print(CertainLoop.buildLoopCond(numWires,wiresep,stateVector))

#numWires = 4
#wiresep = "**01"
#stateVector = [0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, (0.7071+0j), 0j, (0.7071+0j), 0j, 0j, 0j, 0j] 
#print(Normalization.buildLoopCond(numWires,wiresep,stateVector))
