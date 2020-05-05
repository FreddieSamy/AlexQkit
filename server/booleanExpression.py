from itertools import product
class Booleanfunction:
    def __init__(self):
        pass
    def buildTruthTable(self,vars,fn) :
        nVars = vars.count(',')+1
        table = list(product([False, True], repeat=nVars))
        u = ''
        for i in range(len(table)):
            for j in range(nVars):
                table[i] = list(table[i])
                u += str(table[i][j])+','
            u = u.strip(',')
            conc = vars+"="+u
            toExec = """
exec(conc)
fnToExec = 'flag = '+ fn
exec(fnToExec)
table[i].append(flag)
"""  
            exec(toExec)           
            u = ''
        return table


    def normalForm(self,table,vars):
        vars = vars.split(',')
        normalformEqns = []
        normalformEqn = []
        for row in table :
            if row[-1] == False :
                continue
            else:
                for i in range(len(row)-1):
                    if row[i] == False :
                        normalformEqn.append([vars[i],'1'])
                    else :
                        normalformEqn.append([vars[i]])
                normalformEqns.append(normalformEqn)
                normalformEqn = []
        return normalformEqns
    
    def productOfNormalFn(self,normalFnEqns):
        def helpOptmizatioProudct(product):
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
        return helpOptmizatioProudct(pEqns)
    
    def optmizationCancelation(self,collectedProduct):
        n = len(collectedProduct) 
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

    def assignBooleanCircuit(self,booleanCircuit,optmiziedEqn,dicOfVariabels,closedControll):
        for row in range(len(optmiziedEqn)) :
            for element in optmiziedEqn[row].split('.') :
                indexele = dicOfVariabels[element]
                booleanCircuit[indexele][row] = closedControll
        return booleanCircuit

    def intalize2Darray(self,rows,columns):
       return [["i" for col in range(columns)] for row in range(rows)]

    def assignOrderOfVaribles(self,vars):
        count = 0
        dicOfVariabels = {}
        for var in vars.split(",") :
            dicOfVariabels[var] = count
            count+=1
        return dicOfVariabels
    @classmethod
    def buildBooleanCircuit(cls,vars,boolFunc):
        truthTable = cls().buildTruthTable(vars,boolFunc)
        normalFormEqn = cls().normalForm(truthTable,vars)
        productNormalForm = cls().productOfNormalFn(normalFormEqn)
        optmiziedEqn = cls().optmizationCancelation(productNormalForm)
        dicOfVariabels = {}
        target = "x"
        closedControll = "c"
        dicOfVariabels = cls().assignOrderOfVaribles(vars)
        lenRow = len(vars.split(","))
        lenColumn = len(dicOfVariabels)
        booleanCircuit = cls().intalize2Darray(lenRow,lenColumn)
        booleanCircuit.append([target]*lenColumn)
        booleanCircuit = cls().assignBooleanCircuit(booleanCircuit,optmiziedEqn,dicOfVariabels,closedControll)
        return {'wires' : lenRow+1 ,'init' : ['0']*(lenRow+1), 'rows': booleanCircuit}