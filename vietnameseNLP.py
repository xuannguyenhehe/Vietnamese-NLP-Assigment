import numpy as np
import re
from pymongo import MongoClient
import unidecode

def cityName(name):
    if name == "HUẾ":
        return "HUE"
    if name == "HỒ":
        return "HCMC"
    if name == "ĐÀ":
        return "DANANG"

def tokenization(input, lstToken):
    for index in range(len(input)):
        if input[index] in lstToken:
            pass
        else:
            while True:
                input[index] += ' ' + input[index + 1]    
                input.pop(index + 1)
                if input[index] in lstToken:
                    break
        if index == len(input) - 2:
            return input[:-1]

def dependencyGrammar(lstWord, lstToken):
    lstHead = {}
    #Find verb/root
    verb = [word for word in lstWord if lstToken[word].typ == "V"][0]
    indexVerb = lstWord.index(verb)
    lstHead[verb] = Head(indexVerb, verb, np.array([indexVerb, -1]), "Root")
    #Find det
    det = [word for word in lstWord if lstToken[word].typ == "DET"]
    if len(det) == 1:
        indexDet = lstWord.index(det[0])  
        if indexDet == 0:
            lstHead[det[0]] = Head(indexDet, det[0], np.array([indexDet, indexVerb]), "det_wh")
        else:
            noun = lstWord[indexDet - 1]
            if lstToken[noun].typ == "N":
                lstHead[det[0]] = Head(indexDet, det[0], np.array([indexDet, indexDet - 1]), "det_wh")
    else:
        indexDet0 = lstWord.index(det[0]) 
        indexDet1 = lstWord.index(det[1]) 
        lstHead[det[0]] = Head(indexDet0, det[0], np.array([indexDet0, indexDet0 + 1]), "det")
        lstHead[det[1]] = Head(indexDet1, det[1], np.array([indexDet1, indexDet0 - 1]), "det_wh")
    #Find subj
    subj = [word for word in lstWord[:indexVerb + 1] if lstToken[word].typ == "N"][-1]
    indexSubj = lstWord.index(subj)  
    lstHead[subj] = Head(indexSubj, subj, np.array([indexSubj, indexVerb]), "nsubj")
    #Find obj
    obj = [word for word in lstWord[indexVerb:] if lstToken[word].typ == "PRO"][-1]
    indexObj = lstWord.index(obj)  
    lstHead[obj] = Head(indexObj, obj, np.array([indexObj, indexVerb]), "nobj")
    #Find pobj
    pobj = [word for word in lstWord[indexVerb:] if lstToken[word].typ == "PRO_TIME"]
    if pobj:
        indexPobj = lstWord.index(pobj)  
        lstHead[pobj] = Head(indexPobj, pobj, np.array([indexPobj, indexVerb]), "pobj")
    #Find nmod
    for index in range(len(lstWord)):
        pro = lstWord[index]
        if lstToken[pro].typ == "PRO":
            if lstToken[lstWord[index - 1]].typ == "N":
                nmod = lstWord[index - 1]
                indexNmod = lstWord.index(nmod)  
                lstHead[nmod] = Head(indexNmod, nmod, np.array([indexNmod, index]), "nmod")
    #Find pmod
    for index in range(len(lstWord)):
        pro_time = lstWord[index]
        if lstToken[pro_time].typ == "PRO_TIME":
            if lstToken[lstWord[index - 1]].typ == "P":
                pmod = lstWord[index - 1]
                indexPmod = lstWord.index(pmod)  
                lstHead[pmod] = Head(indexPmod, pmod, np.array([indexPmod, index]), "pmod")
    return lstHead

class Function:
    def __init__(self, typ, name, place, time):
        self.typ = typ
        self.name = name
        self.place = place
        self.time = time

class RetrieveF:
    def __init__(self, command, var, lstFunction):
        self.command = command
        self.var = var
        self.lstFunction = lstFunction

class Logical:
    def __init__(self, role, var, child):
        self.role = role
        self.var = var
        self.child = child

class RelationGrammar:
    def __init__(self, role, value1, value2):
        self.role = role
        self.value1 = value1
        self.value2 = value2

class Pattern:
    def __init__(self, var, relation, value):
        self.var = var
        self.relation = relation
        self.value = value

class Dependency:
    def __init__(self, relation, head, tail):
        self.relation = relation
        self.head = head
        self.tail = tail
class Head:
    def __init__(self, index, head, arc, relation):
        self.index = index
        self.head = head
        self.arc = arc
        self.relation = relation

class Token:
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ

class VietnameseNLP:
    def __init__(self, filename):
        lstToken = {}
        f = open(filename, 'r', encoding="utf8")
        lines = f.readlines()
        for line in lines:
            name, typ = self.__extract_model(line)
            lstToken[name] = Token(name, typ)
        f.close()
        self.lstToken = lstToken

    def DependencyGrammar(self, filename):
        f = open(filename, 'r', encoding="utf8")
        input = self.__extract_query(f.readline())
        #Create list of token
        listToken = [token for token in self.lstToken]
        #Create list of word of input from list of head
        listWord = tokenization(input, listToken)
        #Represent grammatical relation
        result = dependencyGrammar(listWord, self.lstToken)
        lstDependency = {}
        for element in result:
            relation = result[element].relation
            index = result[element].arc[1]
            if index != -1:
                for ele in result:
                    if result[ele].index == index:
                        head = ele
                lstDependency[relation] = Dependency(relation, head, element)
            else:
                continue
        return lstDependency

    def printDependencyGrammar(self, lstDependency):
        result = ""
        for element in lstDependency:
            result += lstDependency[element].relation + '(' + lstDependency[element].head + ',' + lstDependency[element].tail + ')\n'
        return result

    def PatternForm(self, lstDependency):
        lstPattern = []
        for dep in lstDependency:
            if dep == "det_wh":
                lstPattern.append(Pattern('s1', 'WH-Q', None))
            if dep == "nsubj":
                lstPattern.append(Pattern('s1', 'PRED', lstDependency[dep].head))
                lstPattern.append(Pattern('s1', 'TNS', 'PRES'))
                lstPattern.append(Pattern('s1', 'LSUBJ', lstDependency[dep].tail.upper()))
            if re.search("^.obj$", dep):
                name = 'NAME ' + lstDependency[dep].tail[0] + '1 ' + lstDependency[dep].tail.upper()
                lstPattern.append(Pattern('s1', 'LOBJ', name))
        return lstPattern

    def RelationGrammar(self, relationGrammar):
        lstRelationGrammar = []
        for pat in relationGrammar:
            relation = pat.relation
            var = pat.var
            value = pat.value
            if relation == "WH-Q":
                lstRelationGrammar.append(RelationGrammar("WH-QUERY", var, None))
            if relation == "PRED" or relation == "TNS":
                lstRelationGrammar.append(RelationGrammar(value.upper(), var, None))
            if relation == "LSUBJ":
                lstRelationGrammar.append(RelationGrammar("AGENT", var, value))
            if relation == "LOBJ":
                name = value.split(' ')
                if re.search("^[0-9]{2}[:][0-9]{2}HR$", name[2]):
                    lstRelationGrammar.append(RelationGrammar("AT-TIME", var, value))
                else:
                    lstRelationGrammar.append(RelationGrammar("TO-LOC", var, value))
        return lstRelationGrammar

    def printRelationGrammar(self, relationGrammar):
        result = ""
        for element in relationGrammar:
            value2 = ' (' + element.value2 + ')' if element.value2 else ''
            result += '(' + element.role + ' ' + element.value1 + value2 + ')\n'
        return result

    def LogicalForm(self, relationGrammar):
        lstLogicalForm = []
        role = ""
        var = relationGrammar[0].value1
        child = []
        for re in relationGrammar:
            if re.role == "WH-QUERY":
                role += re.role
                continue
            elif re.role not in ["PRES", "AGENT", "TO-LOC", "AT-TIME", "WH-QUERY"]:
                role += '(' + re.role + ' ' + re.value1 + ' '
                continue
            elif re.role == "PRES":
                role += re.role + ')'
                continue
            else:
                child.append(re)
        lstLogicalForm.append(Logical(role, var, child))
        return lstLogicalForm

    def printLogicalForm(self, logicalForm):
        result = ''
        for log in logicalForm:
            child = ''
            for ch in log.child:
                child += '[' + ch.role + ' ' + ch.value1 + ' ' + ch.value2 + ']'
            result += '(' + log.role + ' ' + log.var + ' ' + child + ')'
        return result

    def RetrieveForm(self, logicalForm):
        if len(logicalForm) == 1:
            log = logicalForm[0]
            role = log.role
            lstFunction = []
            command = "PRINT-ALL"
            var = '?b'
            lstFunction.append(Function("BUS", var, None, None))
            if re.findall("ĐẾN", role):
                for ch in log.child:
                    if ch.role == "TO-LOC":
                        lstFunction.append(Function("ATIME", var, ch.value2, None))
                    if ch.role == "AT-TIME":
                        lstFunction.append(Function("ATIME", var, None, ch.value2))
            if re.findall("XUẤT PHÁT", role):
                for ch in log.child:
                    if ch.role == "TO-LOC":
                        lstFunction.append(Function("DTIME", var, ch.value2, None))
                    if ch.role == "AT-TIME":
                        lstFunction.append(Function("DTIME", var, None, ch.value2))
        return RetrieveF(command, var, lstFunction)

    def printRetrieveForm(self, retrieveForm):
        lstFunc = ""
        command = retrieveForm.command
        var = retrieveForm.var
        for re in retrieveForm.lstFunction:
            typ = re.typ
            name = re.name
            place = re.place
            time = re.time
            if typ == "BUS":
                lstFunc += '(' + typ + ' ' + name + ')'
            elif place and time:
                lstFunc += '(' + typ + ' ' + name + ' ' + '(' + place + ')' + ' ' +  '(' + time + '))'
            elif place:
                lstFunc += '(' + typ + ' ' + name + ' ' + '(' + place + ')' +')'
            elif time:
                lstFunc += '(' + typ + ' ' + name + ' ' + '(' + time + ')' +')'
        return '(' + command + ' ' + var + ' ' + lstFunc + ')'

    def resultDB(self, retrieveForm):
        myclient = MongoClient("mongodb+srv://user:ye1gkjKBIWGxjVEpUFxCoAjNnAdEeRYpiLeE4guhP4FxUHtGYCPMzdd11TtoJAyA@multidisciplinary-lt0bz.azure.mongodb.net/<dbname>?authSource=admin&replicaSet=Multidisciplinary-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass%20Community&retryWrites=true&ssl=true")
        mydb = myclient["vietnameseNLP"]
        lstResult = []
        if retrieveForm.var == "?b":
            mycol = mydb["schedule"]
            myquery = []
            for fu in retrieveForm.lstFunction[1:]:
                typ = fu.typ
                place = fu.place
                time = fu.time
                place = place.split(' ')[2] if place else None
                time = time.split(' ')[2] if time else None
                if place and time:
                    myquery.append({ "type": typ, "place": place, "time": time })
                elif place:
                    myquery.append({ "type": typ, "place": cityName(place)})
                elif time:
                    myquery.append({ "type": typ, "time": time })
            mydoc = mycol.find({"$and": myquery})
            for x in mydoc:
                lstResult.append(x["name"])
        return lstResult

    def printResultDB(self, resultdb):
        if len(resultdb) == 0:
            return 'Không tìm được dữ liệu'
        else:
            result = ""
            for re in resultdb:
                result += re + ' '
            return result

    def __extract_model(self, line):
        parts = line.split(';')
        name = parts[0]
        typ = parts[1]
        return name, typ

    def __extract_query(self, line):
        words = line.split(' ')
        return words