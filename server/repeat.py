import numpy as np
class Repeat :
    def __init__(self):
        pass
############################################################################################################################### 
    @classmethod
    def repettion(cls, circuitList, listOfPositions, listOfNumberOfRepetition):
        dic = cls().dicOfBlockAndPosition(circuitList, listOfPositions, listOfNumberOfRepetition)
        circuitList = np.array(circuitList)
        for key in dic:
            repetedBlock, insertPostition, numberOfRepetition = dic[key]['repetedBlock'], dic[key]['insertPostion'], dic[key]['NumberOfRepetition']
            #for repet in range(numberOfRepetition-1):
            #    circuitList = np.insert(circuitList, insertPostition, repetedBlock, axis=1)
            repeat = 0
            while repeat < numberOfRepetition-1 :
                circuitList = np.insert(circuitList, insertPostition, repetedBlock, axis=1)
                repeat+=1
        print(circuitList.tolist())
        return circuitList.tolist()
    
###############################################################################################################################

    def blockToRepet(self, circutList, position):
        circutList = np.array(circutList)
        repetBlock = circutList[:, position[0]: position[1] + 1].transpose()
        return repetBlock, position[0], position[1]
    
###############################################################################################################################

    def dicOfBlockAndPosition(self, circutList, listOfPositions, listOfNumberOfRepetition):
        dicOfPos = {}
        endPreviousPos = 0
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