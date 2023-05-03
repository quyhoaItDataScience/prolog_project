import copy
from collections import defaultdict


class Predicate:
    def __init__(self, str, implies=None):
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
    return var[0].isupper()

def processVar(query: Predicate, KB:list):
    #relation: [(pre.variables, Predicate)]
    mp = defaultdict(list)
    for pre in KB:
        mp[pre.relation].append((pre.variables, pre.implies))
    if query.relation not in mp:
        return
    #if have implies
    if mp[query.relation][0][1]:
        #implies is currently an object
        implies = mp[query.relation][0][1]
        query.relation = implies.relation
        processVar(query, KB)
        return
    #index of where you need to look for
    idxQuery = []
    for i, var in enumerate(q.variables):
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
            print(variables[0])
    if cnt == 0:
        print("No unification")
            
# query is Predicate
def process(query: Predicate, KB: list) -> bool:
    mp = defaultdict(list)
    for pre in KB:
        mp[pre.relation].append((pre.variables, pre.implies))
    if query.relation not in mp:
        return 0
    if mp[query.relation][0][1]:
        #implies is currently an object
        implies = mp[query.relation][0][1]
        query.relation = implies.relation
        process(query, KB)
    for variables in mp[query.relation]:
        if variables[0] == query.variables:
            return 1
    return 0

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
    predicates = readFile()
    kb = []
    results = []
    for pre in predicates:
        if ":-" not in pre:
            predicate = Predicate(pre)
        else:
            a, b = pre.split(":-")  # syntax of query: pred1:-pred2
            predicate = Predicate(a, Predicate(b))
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
        print(results)
        if 2 not in results:
            if 0 in results or None in results:
                print("False")
            else:
                print("True")
