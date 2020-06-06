from itertools import product

class BooleanFunction:
    def __init__(self):
        pass

    #  Build a circuit without specified indecies
    @classmethod
    def buildBooleanCircuit(cls,variables,boolFunc):
        truthTable = cls().buildTruthTable(variables,boolFunc)# Deduce truth table
        normalFormEqn = cls().normalForm(truthTable,variables)# Compute normal form
        productNormalForm = cls().productOfNormalFn(normalFormEqn) # compute product of normal form equations
        optmiziedEqn = cls().optmizationCancelation(productNormalForm) # Optmize the equation if two similar terms are exist .
        optmiziedEqn = cls().term_XOR_one(optmiziedEqn)# Check if there is one on the last normal form equation
        dicOfVariabels = {} 
        target = "x"
        closedControll = "●"
        openControll = "○"
        dicOfVariabels = cls().assignOrderOfVaribles(variables) # Dictionary for assign variables ordere
        lenRow = len(variables.split(",")) # Split varibales for count how many rows 
        lenColumn = len(optmiziedEqn) # Count how many terms are exist in optimized normal form equation 
        booleanCircuit = cls().intalize2Darray(lenRow,lenColumn) # Intialize 2d arrays with is
        booleanCircuit.append([target]*lenColumn)# Insert the target in last row
        booleanCircuit = cls().assignBooleanCircuit(booleanCircuit,optmiziedEqn,dicOfVariabels,closedControll,openControll)# Construct Circiut .
        return {'wires' : lenRow+1 ,'init' : ['0']*(lenRow+1), 'rows': booleanCircuit}

    # Build a circuit with specified user indecies
    @classmethod
    def buildBooleanCircuit_indecies(cls,variables,boolFunc,indecies):
        circuit = cls().buildBooleanCircuit(variables,boolFunc)  
        columns = len(circuit['rows'][0])
        rows = cls().castInt_max(indecies) + 1
        booleanCircuit = []
        booleanCircuit = cls().intalize2Darray(rows,columns)
        indexOfVariable = 0
        for index in indecies :
            booleanCircuit[index] = circuit['rows'][indexOfVariable]
            indexOfVariable+=1
        circuit['wires'] = rows
        circuit['init'] = ['0']*rows
        circuit['rows'] = booleanCircuit 
        return circuit
        
# This method build a truth table of the function that given by user using class product from itertools packge
    def buildTruthTable(self,variables,fn) :
        try :
            nVars = variables.count(',')+1
            
        except :
            return "variable error"
        table = list(product([False, True], repeat=nVars))
        u = ''
        for i in range(len(table)):
            for j in range(nVars):
                table[i] = list(table[i])
                u += str(table[i][j])+','
            u = u.rstrip(',')
            conc = variables+"="+u
            toExec = """
exec(conc)
fnToExec = 'flag = '+ fn
exec(fnToExec)
table[i].append(flag)
"""  
            exec(toExec)           
            u = ''
        return table
# calculate the normal form for truth table
    def normalForm(self,table,variables):
        variables = variables.split(',')
        normalformEqns = []
        normalformEqn = []
        for row in table : # Iterate on every row in the table to compute the normal form of it .
            if row[-1] == False : # The last column in the row is the result of function  that given by user .
                continue
            else:
                for i in range(len(row)-1):
                    if row[i] == False :
                        normalformEqn.append([variables[i],'1']) # if the variable is false Put XOR one 
                    else :
                        normalformEqn.append([variables[i]])
                normalformEqns.append(normalformEqn)
                normalformEqn = []
        return normalformEqns
    
    def productOfNormalFn(self,normalFnEqns): # Compute the product normal form for every terms .
        def helpOptmizationProudct(product):
            tempStr = ""
            productOptmize = []
            for i in product:
                for j in list(i):
                    for k in j :
                        if k != '1':      
                            tempStr+=k+"."
                        
                    if tempStr == "" :
                        tempStr ='1'
                    tempStr = tempStr.strip('.')
                    productOptmize.append(tempStr)
                    tempStr = ""
            return productOptmize
        
        pEqns = []
        for i in normalFnEqns :
            pEqns.append(product(*i))
        return helpOptmizationProudct(pEqns)
    
    def optmizationCancelation(self,collectedProduct): # Cancel every two similar  terms
        n = len(collectedProduct) # Take the length after made product on normal form equations .
        index = 1
        prevStart = 0
        while n > index :
            while index < n :
                if collectedProduct[prevStart] == collectedProduct[index]:
                    collectedProduct.pop(index)
                    collectedProduct.pop(prevStart)
                    index = prevStart + 1
                    n-=2
                    break
                else :
                    index+=1

            if prevStart + 1 != index :
                prevStart += 1
                index = prevStart + 1
        return collectedProduct

    def assignBooleanCircuit(self,booleanCircuit,optmiziedEqn,dicOfVariabels,closedControll,openControll):
        for row in range(len(optmiziedEqn)) :
            for element in optmiziedEqn[row].split('.') :
                
                if "not" in element :
                    indexele = dicOfVariabels[element.split(" ")[1]]
                    booleanCircuit[indexele][row] = openControll
                else:
                    indexele =  dicOfVariabels[element]
                    booleanCircuit[indexele][row] = closedControll
        return booleanCircuit

    def intalize2Darray(self,rows,columns): #intialize 2d list with i 
       return [["i" for col in range(columns)] for row in range(rows)]

    def assignOrderOfVaribles(self,variables): # Maping for order variables value like if user wrote x,y,z so x is 0 y is 1 etc.
        count = 0
        dicOfVariabels = {}
        for var in variables.split(",") :
            dicOfVariabels[var] = count
            count+=1
        return dicOfVariabels

    def isOne(self,optmiziedEqn): # Check if there is one after made optmization canceltion to XOR by lowest term length
        for termIndex in range(len(optmiziedEqn)) :
            if optmiziedEqn[termIndex] == "1" :
                optmiziedEqn.pop(termIndex)
                return True
        return False

    def smallestTermLength(self,optmiziedEqn): # XOR the smallest term With one if any .
        indexOfTerm = 0
        term = optmiziedEqn[0].split('.')
        lestTermLength = len(term)
        for termIndex in range(1,len(optmiziedEqn)) :
            tempTerm = optmiziedEqn[termIndex].split('.')
            if len(tempTerm) < lestTermLength and optmiziedEqn[termIndex] != "1" :
                lestTermLength = len(tempTerm)
                indexOfTerm = termIndex
                term = tempTerm
                if lestTermLength == 1 :
                    break
        return {'term' : term ,'index' : indexOfTerm }

    def term_XOR_one(self,optmiziedEqn): #Apply term XOR one
        if self.isOne(optmiziedEqn) :
            dicOfTerm = self.smallestTermLength(optmiziedEqn)
            tempStrTerm = ""
            for element in dicOfTerm["term"] :
                tempStrTerm += "not " + element+"."
            tempStrTerm = tempStrTerm.strip('.')
            optmiziedEqn[dicOfTerm['index']] = tempStrTerm
        return optmiziedEqn

    def castInt_max(self,arr): # Casting array to int to extract maximum variables 
        maxi = 0
        for ind in range(len(arr))  :
            arr[ind] = int(arr[ind])
            if maxi < arr[ind]:
                maxi = arr[ind]
        return maxi
  

# v = "x,y,z"
# fn = "x or y and z"
# indecies = ['2', '4', '1','3']
# print(BooleanFunction.buildBooleanCircuit(v,fn)['rows'])
#print(BooleanFunction.buildBooleanCircuit_indecies(v,fn,indecies)['rows'])
#for i in BooleanFunction.buildBooleanCircuit_indecies(v,fn,indecies)['rows']:
#for i in BooleanFunction.buildBooleanCircuit(v,fn)['rows']:
#    print(i)