import numpy as np
import re
def tokenization(input, lstLabel):
    for index in range(len(input)):
        if input[index] in lstLabel:
            pass
        else:
            while True:
                input[index] += ' ' + input[index + 1]    
                input.pop(index + 1)
                if input[index] in lstLabel:
                    break
        if index == len(input) - 1:
            return input

def nameVariable(input):
    list = input.split(" ")
    if len(list) == 1:
        return input[0].lower() + '1'
    else:
        return "".join([lst[0].lower() for lst in list]) + '1'

def grammaticalRelation(root, lstRelation):
    relation = lstRelation[root].relation.upper()
    namevar = nameVariable(root)
    name = root + '1'
    index = lstRelation[root].index
    lstChild = [lstRelation[child].head for child in lstRelation if lstRelation[child].arc[1] == lstRelation[root].index and lstRelation[child].relation != "punct"]
    clause = []
    
    if relation == "DEP":
        relation = "WH"
    if relation == "ROOT":
        relation = "PRED"
    if ''.join([letter[0] for letter in name.split(' ')]).isupper():
        relation = "NAME"
    if re.search("^[0-9]{2}[:][0-9]{2}HR.$", name):
        relation = "TIME"
        namevar = "t1"
 
    clause.append(Pattern(namevar, relation, name))
    for child in lstChild:
        clause.append(Pattern(namevar, lstRelation[child].relation, grammaticalRelation(lstRelation[child].head, lstRelation)))
    return clause

class Logical:
    def __init__(self, role, index_1, index_2):
        self.role = role
        self.index_1 = index_1
        self.index_2 = index_2

class Pattern:
    def __init__(self, namevar, relation, name):
        self.namevar = namevar
        self.relation = relation
        self.name = name

class Head:
    def __init__(self, index, head, arc, relation):
        self.index = index
        self.head = head
        self.arc = arc
        self.relation = relation
    def __str__(self):
        return "Index: " + str(self.index) +"\nHead: "+ str(self.head) +"\nArc: "+ str(self.arc)+"\nRelation: "+ str(self.relation)


class VietnameseNLP:
    def __init__(self, filename):
        lstHead = {}
        f = open(filename, 'r', encoding="utf8")
        lines = f.readlines()
        for line in lines:
            index, head, arc, relation = self.__extract_model(line)
            lstHead[head] = Head(index, head, arc, relation)
        f.close()
        self.lstHead = lstHead

    def representationGrammaticalRelation(self, clause):
        return '(' + clause[0].namevar + ' ' + clause[0].relation + ' ' + clause[0].name + ')' + "".join(['(' + child.namevar + ' ' + child.relation + ' ' + self.representationGrammaticalRelation(child.name)  + ')' for child in clause[1:]])
      
    def representationLogicalForm(self, clause):
        return '(' + clause[0].role + ' ' + clause[0].index_1 + ' ' + clause[0].index_2 + ')' + "".join(['(' + child.role + ' ' + child.index_1 + ' ' + self.representationLogicalForm(child.index_2)  + ')' for child in clause[1:]])

    def GrammaticalRelation(self, filename):
        f = open(filename, 'r', encoding="utf8")
        input = self.__extract_query(f.readline())
        #Create list of head
        listHead = [word for word in self.lstHead]
        #Create list of word of input from list of head
        listWord = tokenization(input, listHead)
        #Find root
        root = [word for word in listWord if self.lstHead[word].relation == "Root"][0]
        #Represent grammatical relation
        clause = grammaticalRelation(root, self.lstHead)
        # return result.replace("Root", "PRED")
        return clause

    def logicalForm(self, clause):
        logicalForm = []
        if clause[0].relation == "WH" or clause[0].relation == "NAME" or clause[0].relation == "TIME": 
            logicalForm.append(Logical(clause[0].relation, clause[0].name, clause[0].namevar))
        else:
            logicalForm.append(Logical("", clause[0].name, clause[0].namevar))
        for child in clause[1:]:
            if child.relation == "nsubj":
                logicalForm.append(Logical("AGENT", child.namevar, self.logicalForm(child.name)))
            elif child.relation == "obj":
                logicalForm.append(Logical("THEME", child.namevar, self.logicalForm(child.name)))
            elif child.relation == "nmod":
                logicalForm.append(Logical("AT-TIME", child.namevar, self.logicalForm(child.name)))
            else:
                logicalForm.append(Logical(child.relation.upper(), child.namevar, self.logicalForm(child.name)))
        return logicalForm
    def __extract_model(self, line):
        parts = line.split(';')
        index = parts[0]
        arc = np.array([parts[0], parts[2]])
        head = parts[1]
        relation = parts[3]
        return index, head, arc, relation

    def __extract_query(self, line):
        words = line.split(' ')
        return words