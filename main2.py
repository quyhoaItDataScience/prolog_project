from collections import defaultdict


class Predicate:
    def __init__(self, str, implies=None):
        # index of (
        idx = str.index("(")
        self.relation = str[:idx]
        self.variables = []
        self.implies = [] #list of Predicate
        curString = ""
        for i in range(idx + 1, len(str)):
            if str[i].isalpha():
                curString += str[i]
            if str[i] == ",":
                self.variables.append(curString)
                curString = ""
            if str[i] == ")":
                self.variables.append(curString)
                break

    def __eq__(self, __value) -> bool:
        if (self.relation != __value.relation or
                self.variables != __value.variables):
            return False
        return True

    def print(self):
        print(f"Variables: {self.variables}")
        print('\n')
    def __str__(self) -> str:
        return f"Relations:{self.relation} Variables:{self.variables}\n"
    def addSubPredicate(self, subPredicate):
        self.implies.append(subPredicate)

    def countVar(self):
        counter = 0
        for v in self.variables:
            if isVar(v):
                counter += 1
        return counter


def readFile():
    f = open("text.txt", "r")
    return f.read().split('\n')

def isVar(var: str):
    return var[0].isupper()

def helperVar(query: Predicate, mp) -> list:
    res = []
    idxQuery = []
    for i, var in enumerate(query.variables):
        if not isVar(var):
            idxQuery.append(i)
    cnt = 0
    for variables in mp[query.relation]:
        isEqual = True
        for i in range(len(variables[0])):
            if i not in idxQuery:
                continue
            if variables[0][i] != query.variables[i]:
                isEqual = False
                break
        if isEqual:
            cnt += 1
            res.append(variables[0])
            
    if cnt == 0:
        # -1 means no unification
        res.append(-1)
    return res
#print variables
def printArray(matrix): 
    for el in matrix:
        print(el[0])

def find_common(list1, list2) -> list:
    res = []
    for el1 in list1: 
        if el1 in list2:
            res.append(el1)

    return res
def processVar(query: Predicate, KB:list):
    #relation: [(pre.variables, Predicate)]
    mp = defaultdict(list)
    for pre in KB:
        mp[pre.relation].append((pre.variables, pre.implies))
    if query.relation not in mp:
        return print("No unification")
    #if have implies
    if mp[query.relation][0][1]:
        #implies is a list      
        implies = mp[query.relation][0][1]
        query.relation = implies[0].relation
        prevVariables = helperVar(query, mp)
        if len(implies) == 1:
            return print(prevVariables)
        for i in range(1, len(implies)):
            query.relation = implies[i].relation
            nextVariables = helperVar(query, mp)
            prevVariables = find_common(prevVariables, nextVariables)
            if not prevVariables:
                return print("No unification")       
        return printArray(prevVariables)
        
        
    #index of where you need to look for
    res = helperVar(query, mp)
    if -1 in res:
        return print("No unification")
    printArray(res)
def processVar1(query: Predicate, KB: list) -> bool:
    #A map with format relation:List[(variables, implies)]
    mp = defaultdict(list)
    for pre in KB:
        mp[pre.relation].append((pre.variables, pre.implies))
    curRes = []   
    implies = []
    if query.relation not in mp:
        return print("No unification")
    #if not have implies
    if not mp[query.relation][0][1]:
        curRes = helperVar(query, mp)
        if -1 in curRes:
            return print("No unification")
        return printArray(curRes)
    #find first common in map Predicate
    if query.relation in mp:
        #[(variables, implies)]
        implies = mp[query.relation][0][1]
        n = len(implies)
        #if have implies, fistImplies is an object Predicate
        firstImplies = implies[0]
        while firstImplies:
            if mp[firstImplies.relation][0][1]:
                firstImplies = mp[firstImplies.relation][0][1][0]
            else: 
                break
        query.relation = firstImplies.relation
        curRes = helperVar(query, mp)
        if n == 1:
            return printArray(curRes)
    
    # if n > 1
    def helper(query: Predicate, mp, curRes):
        res = []
        #if not have relation in KB
        if query.relation not in mp:
            res.append("No unification")
            return res
        # if not have implies
        if not mp[query.relation][0][1]:
            res = helperVar(query, mp)
            print("helper", curRes, res)
            commonBetweenTwo = find_common(curRes, res)

            if commonBetweenTwo:
                return commonBetweenTwo
            else:
                return []
        # if have implies
        #implies is a list of Predicate
        implies = mp[query.relation][0][1]
        for i in range(len(implies)):
            query.relation = implies[i].relation
            if not helperVar(query, mp):
                return []
            res = helperVar(query, mp)
            commonBetweenTwo = find_common(res, curRes)
            if not commonBetweenTwo:
                return []
            curRes = commonBetweenTwo
        return res
    
    for i in range(1, len(implies)):
        query.relation = implies[i].relation
        nextRes = helper(query, mp, curRes)
        if not nextRes:
            return print("No found")       
        curRes = nextRes
    return printArray(curRes)

# query is Predicate
def process(query: Predicate, KB: list) -> bool:
    #A map with format relation:List[(variables, implies)]
    mp = defaultdict(list)
    for pre in KB:
        mp[pre.relation].append((pre.variables, pre.implies))
    #if not have relation in KB
    if query.relation not in mp:
        return 0
    # if not have implies
    if not mp[query.relation][0][1]:
        for variables in mp[query.relation]:
            if variables[0] == query.variables:
                return 1
        return 0
    # if have implies
    #implies is a list of Predicate
    implies = mp[query.relation][0][1]
    for i in range(len(implies)):
        query.relation = implies[i].relation
        if not process(query, KB):
            return 0
    return 1
    

def splitQuery(q: str) -> list:
    qArr = []
    currString = ""
    i = 0
    while i < len(q):
        currString += q[i]
        if q[i] == ")":
            qArr.append(currString)
            currString = ""
            while i + 1 < len(q) and not q[i + 1].isalpha():
                i += 1
        i += 1
    return qArr


if __name__ == "__main__":
    predicates = readFile()
    kb = []
    results = []
    for pre in predicates:
        if ":-" not in pre:
            predicate = Predicate(pre)
        else:
            a, implies = pre.split(":-")  # syntax of query: pred1:-pred2
            implies = splitQuery(implies)
            predicate = Predicate(a)
            for impli in implies:
                subPredicate = Predicate(impli)
                predicate.addSubPredicate(subPredicate)
        kb.append(predicate)
    # get user input
    while (True):
        print("?- ", end="")
        results = [2]
        inp = input()
        qArr = [Predicate(query) for query in splitQuery(inp)]
        for q in qArr:
            if q.countVar():
                processVar1(q, kb)
            else:
                if 2 in results:
                    results.remove(2)
                results.append(process(q, kb))
        if 2 not in results:
            if 0 in results:
                print("False")
            else:
                print("True")
