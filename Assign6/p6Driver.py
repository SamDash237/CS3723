#!/usr/bin/python
import sys
from p6Dict import *
from p6Exec import *


#p6Driver.py
#Purpose:
#    Driver for the program. Implements all dictionaries and reads in file from sys.argv[1].
#    If first statement in list is VAR, variable declared using declareVar().
#    If first statement in list ends with  :, label declared using declareLabel().
#    At the end of the program, all variables and labels are printed with printVariables and printLabels, followed by the execution.

varTypeD = {}
varValueD = {}
labelD = {}
statementsInBEEP = {}
     
print(sys.argv, len(sys.argv))

if len(sys.argv) < 2:
  print ("Too few arguments")
  sys.exit(1)
  
file = open(sys.argv[1], "r", encoding='latin-1')

print("BEEP source code in " + sys.argv[1] + ":")
i = 0
while True:
    fileLine = file.readline()
    if fileLine == "":
        break
    i += 1    
    fileLine = fileLine.rstrip('\n')

    print("%*d, %s" %(3, i, fileLine))
    
    line = fileLine.lstrip()
    
    statementsInBEEP[i] = line
    
    lineTokens = line.split()
    
    if len(lineTokens) == 0:
      continue 
    
    if(lineTokens[0][-1] == ':'): #checks for label
        declareLabel(lineTokens, labelD, i)
        lineTokens = lineTokens[1:]
    if(lineTokens[0] == 'VAR'): #checks for variable
        declareVar(lineTokens[1:], varTypeD, varValueD)

printVariables(varTypeD, varValueD)
printLabels(labelD)
file.close()

print("execution begins...")

if sys.argv[-1] == '-v':
    executeBEEP(statementsInBEEP, varValueD, varTypeD, labelD, True)
else:
    executeBEEP(statementsInBEEP, varValueD, varTypeD, labelD)
