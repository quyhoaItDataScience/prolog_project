from collections import defaultdict


class Predicate:
    def __init__(self, string):
        # Extract relation and variables from string
        left_paren_idx = string.index("(")
        right_paren_idx = string.index(")")
        self.relation = string[:left_paren_idx]
        self.variables = string[left_paren_idx+1:right_paren_idx].split(",")
        # Initialize implies as an empty list
        self.implies = []

    def __eq__(self, other):
        return (self.relation == other.relation and
                self.variables == other.variables)

    def __str__(self):
        return f"Relation: {self.relation}, Variables: {self.variables}"

    def addSubPredicate(self, subPredicate):
        self.implies.append(subPredicate)

    def countVar(self):
        return sum(1 for v in self.variables if isVar(v))


def readFile():
    f = open("BritishRoyalFamily.txt", "r")
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

def find_common(list1, list2) -> list:
    res = []
    for el1 in list1: 
        if el1 in list2:
            res.append(el1)

    return res
def processVar(query: Predicate, KB: list) -> bool:
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
        return print(curRes)
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
            return print(curRes)
    
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
            # print("helper", curRes, res) for debug
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
        return curRes
    
    for i in range(1, len(implies)):
        query.relation = implies[i].relation
        nextRes = helper(query, mp, curRes)
        if not nextRes:
            return print("No unification")       
        curRes = nextRes
    return print(curRes)

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

def validateInput(string):
    if not string or "%" in string: 
        return False
    return True

if __name__ == "__main__":
    predicates = readFile()
    kb = []
    results = []
    for pre in predicates:
        if not validateInput(pre): 
            continue
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
                processVar(q, kb)
            else:
                if 2 in results:
                    results.remove(2)
                results.append(process(q, kb))
        if 2 not in results:
            if 0 in results:
                print("False")
            else:
                print("True")
