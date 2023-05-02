import copy

class Predicate:
    def __init__(self, str, implies = None):
        # index of (
        idx = str.index("(")
        self.relation = str[:idx]
        self.variables = []
        self.implies = implies
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
        print(f"Relation: {self.relation}")
        print(f"Variables: {self.variables}")
        print('\n')

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
    firstLetter = var[0]
    if firstLetter.isupper():
        return True
    return False

def unify(a: Predicate, b:Predicate): #rule: first param: query
    
    aCopy = copy.deepcopy(a)
    bCopy = copy.deepcopy(b)
    for i in range(len(aCopy.variables)):
        if isVar(aCopy.variables[i]):
            aCopy.variables[i] = b.variables[i]
    for i in range(len(bCopy.variables)):
        if isVar(bCopy.variables[i]):
            bCopy.variables[i] = a.variables[i]

    return aCopy,bCopy

#query is Predicate
def process(query: Predicate, KB: list):
    global checkTruth, isPrint
    global results
    for predicate in KB:
        post_unify_predicate = unify(query, predicate)[0]
        if post_unify_predicate == query:
            checkTruth = True
        if not predicate.implies:
            for p in KB:
                if post_unify_predicate == p and not checkTruth:    
                    isPrint = True
                    post_unify_predicate.print()
                if post_unify_predicate == p and checkTruth:
                    results.append(1)
                    return
            results.append(0)
        
        elif predicate.relation == query.relation:
            after_unify_predicate=unify(predicate.implies,query)
            results.clear()
            checkTruth = False
            process(after_unify_predicate[0], KB)          



    # if not checkTruth:
    #     print("No unification found")


def splitQuery(q: str) -> list:
    qArr = []
    currString = ""
    i = 0
    while i < len(q):
        currString += q[i]
        if q[i] == ")":
            if i == len(q) - 1:
                qArr.append(currString)
                break
            qArr.append(currString)
            currString = ""
            i += 1
        i += 1
    return qArr


if __name__ == "__main__":
    checkTruth = False
    predicates = readFile()
    kb = []
    results = []
    for pre in predicates:
        if ":-" not  in pre:
            predicate = Predicate(pre)
        else:
            a,b = pre.split(":-") #syntax of query: pred1:-pred2
            predicate = Predicate(a, Predicate(b))
        kb.append(predicate)

    #get user input
    while(True):
        print("?- ",end="")
        checkTruth = False
        isPrint = False
        results.clear()
        inp = input()
        qArr = [Predicate(query) for query in splitQuery(inp)]
        for q in qArr:
            process(q, kb)
            if isPrint: 
                continue
            if 0 in results and checkTruth:
                print("False")
                break
        if isPrint:
            continue
        if 0 not in results and checkTruth:
            print("True")