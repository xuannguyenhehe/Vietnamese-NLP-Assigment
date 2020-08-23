# main.py
# -------------
from vietnameseNLP import VietnameseNLP
import optparse
import os
import sys


# register arguments and set default values
def readCommand(argv):
    parser = optparse.OptionParser(
        description='Run public tests on student code')
    parser.add_option('--model-directory',
                      dest='modelRoot',
                      default='models',
                      help='Root model directory which contains models')
    parser.add_option('--test-directory',
                      dest='testRoot',
                      default='inputs',
                      help='Root test directory which contains inputs')
    parser.add_option('--model',
                      dest='modelFilename',
                      default='model01.txt',
                      help='File name which contains the model')                  
    parser.add_option('--input',
                      dest='testFilename',
                      default="input01.txt",
                      help='File name which contains the input')
    parser.add_option('--output',
                      dest="outputFilename",
                      default='output01.txt',
                      help='File name which contains the output')
    (options, _) = parser.parse_args(argv)
    return options

if __name__ == '__main__':
    options = readCommand(sys.argv)
    model = VietnameseNLP(options.modelRoot + '/' + options.modelFilename)
    lstDependency = model.DependencyGrammar(options.testRoot + '/' + options.testFilename)
    result = model.printDependencyGrammar(lstDependency)
    print(result)

    patternForm = model.PatternForm(lstDependency)
    relationGrammar = model.RelationGrammar(patternForm)
    result_a = model.printRelationGrammar(relationGrammar)
    print(result_a)

    logicalForm = model.LogicalForm(relationGrammar)
    result_b = model.printLogicalForm(logicalForm)
    print(result_b)

    retrieveForm = model.RetrieveForm(logicalForm)
    result_c = model.printRetrieveForm(retrieveForm)
    print(result_c)    

    resultdb = model.resultDB(retrieveForm)
    result_d = model.printResultDB(resultdb)
    print(result_d)

    f = open('./outputs/' + options.outputFilename, 'w', encoding='utf8')
    writeline = result + '\n' + result_a + '\n' + result_b + '\n' + result_c + '\n' + result_d
    f.write(writeline)
    f.close()
   