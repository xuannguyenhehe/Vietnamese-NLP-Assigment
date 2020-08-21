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
    (options, _) = parser.parse_args(argv)
    return options

if __name__ == '__main__':
    options = readCommand(sys.argv)
    model = VietnameseNLP(options.modelRoot + '/' + options.modelFilename)
    clause = model.GrammaticalRelation(options.testRoot + '/' + options.testFilename)
   
    result_a = model.representationGrammaticalRelation(clause)
    print(result_a)
  
    logicalForm = model.logicalForm(clause)
    result_b = model.representationLogicalForm(logicalForm)
    print(result_b)
    # result = model.approx_inference(options.testRoot + '/' + options.testFilename)
    # print('%0.5f' % result)
   