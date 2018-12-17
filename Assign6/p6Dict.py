#def declareLabel(tokenList, labelD, lineNumber)
#Purpose:
#     Stores the line number of a label in labelD
#Parameters:
#     tokenList: List which contains all tokens within a line
#     labelD: The dictionary of label line numbers
#     lineNumber: The line number of a label

def declareLabel(tokenList, labelD, lineNumber):
      token = tokenList[0][:-1].upper()
      if(token in labelD):
            print('***ERROR: label \'{}\' appears in multiple lines:: {} and {}'.format(token, labelD[token], lineNumber))
      else:
        labelD[token] = lineNumber

#def declareVar(tokenList, varTypeD, varValueD)
#Purpose:
#     Stores a variable type in varTypeD and a variable value in varValueD
#Parameters:
#     tokenList: List which contains all tokens within a line
#     varTypeD: The dictionary of variable types
#     varValueD: The dictionary of variable values

def declareVar(tokenList, varTypeD, varValueD):
      tokenType = tokenList[0].upper()
      tokenName = tokenList[1].upper()
      varTypeD[tokenName] = tokenType
      if(len(tokenList) is 2):
            varValueD[tokenName] = ""
      else:
            varValueD[tokenName] = tokenList[-1]
            
#def printLabels(labelD)
#Purpose:
#     Prints all labels in labelD in ascending order
#Parameters:
#     labelD: The dictionary of label line numbers

def printLabels(labelD):
     print("Labels:")
     print('\t{:>4} {:<12} {:8}'.format("", "Label", "Statement"))
     for i in sorted(labelD):
          print('\t{:>4} {:<12} {:8}'.format( "", i, labelD[i]))  
            
#def printVariables(varTypeD, varValueD)
#Purpose:
#     Prints all varTypeD variables in ascending order
#Parameters:
#     varTypeD: The dictionary of variable types
#     varValueD: The dictionary of variable values

def printVariables(varTypeD, varValueD):
     print("Variables:")
     print('\t{:>4} {:<12} {:8} {:<10}'.format("", "Variable", "Type", "Value"))
     for i in sorted(varTypeD):
          print('\t{:>4} {:<12} {:8} {:<10}'.format("", i, varTypeD[i], varValueD[i]))
