import numpy as np
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
    relation = lstRelation[root].relation
    namevar = nameVariable(root)
    name = root + '1'
    index = lstRelation[root].index
    lstChild = [lstRelation[child].head for child in lstRelation if lstRelation[child].arc[1] == lstRelation[root].index and lstRelation[child].relation != "punct"]
    return '(' + namevar + ' ' + relation + ' ' + name + ')' + "".join(['(' + namevar + ' ' + lstRelation[child].relation + ' ' + grammaticalRelation(lstRelation[child].head, lstRelation) + ')' for child in lstChild])

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
        result = grammaticalRelation(root, self.lstHead)
        return result.replace("Root", "PRED")

    def LogicalForm(self, grammaticalRelation):
        return grammaticalRelation.upper()

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