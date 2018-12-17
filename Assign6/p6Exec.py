import sys
import traceback
from p6Dict import declareLabel, declareVar, printLabels, printVariables

#exception classes

class TooFewOperands(Exception):
    def __init__(self, *args, **kwargs):
            super().__init__(self, *args, **kwargs)

class VarNotDefined(Exception):
    def __init__(self, *args, **kwargs):
            super().__init__(self, *args, **kwargs)

class LabelNotDefined(Exception):
    def __init__(self, *args, **kwargs):
            super().__init__(self, *args, **kwargs)

class InvalidExpression(Exception):
    def __init__(self, *args, **kwargs):
            super().__init__(self, *args, **kwargs)

class InvalidValueType(Exception):
    def __init__(self, *args, **kwargs):
            super().__init__(self, *args, **kwargs)

#variableParse(variableToken)
#Purpose:
#    Get literal value of string or int value of numeric
#Parameter:
#    variableToken: The variable to be analyzed

def variableParse(variableToken):

  if variableToken[0] == "\"":
    return variableToken.replace("\"", "")
  else:
    try:
      return int(variableToken)
    except:
      raise InvalidValueType("'%s' is NOT numeric" %variableToken)
      
#operatorParse(operatorToken, op1, op2)

def operatorParse(operatorToken, op1, op2):
  try:
    operandValue1 = int(op1)
  except:
    raise InvalidValueType("'%s' is NOT numeric" %op1)
  try:
    operandValue2 = int(op2)
  except:
    raise InvalidValueType("'%s' is NOT numeric" %op2)
  if operatorToken == '+':
    return operandValue1 + operandValue2
  if operatorToken == '-':
    return operandValue1 - operandValue2 
  if operatorToken == '>':
    return operandValue1 > operandValue2 
  if operatorToken == '>=':
    return operandValue1 >= operandValue2  

#expressionParse(expr, lineNum, varValueD)
#Purpose:
#    Iterate through a BEEP statement in order to determine what operation needs to be performed.
#    Match variables to the appropriate dictionaries.
#Parameters:
#    expr: The expression to be analyzed.
#    lineNum: The number of the line that causes an error
#    varValueD: The dictionary of variable values     

def expressionParse(expr, lineNum, varValueD):
    
  try:
    if len(expr) == 1: #check for a varLiteral
      if expr[0].upper() in varValueD.keys():
        return varValueD[expr[0].upper()]
      else:
        return variableParse(expr[0])

    elif len(expr) == 3: #three variables in expression necessitates evaluation        
            op = ["*", "+", "-", ">", ">=", "&"] #check for operator
            if expr[0] not in op:
                raise InvalidValueType("'%s' is NOT a valid operator" % (expr[0]))
            else:    
              if expr[0] == '*': #check for '* varLiteral varNumber' 
                endToken = expr[-1].upper().strip()
                stringReplication = 0
                if endToken not in varValueD.keys(): #last token not in value dictionary
                  stringReplication = variableParse(endToken)
                else: #get numeric value of last token from dictionary
                  try:
                    stringReplication = int(varValueD[endToken])
                  except:
                    raise InvalidValueType("'%s' is NOT numeric" %(varValueD[expr[-1]]))
                varLtr = expr[1].upper().strip()
                if varLtr in varValueD.keys():
                  return str(varValueD[varLtr] * stringReplication)
                else:
                  return str(expr[1].strip() * stringReplication)
                  
              if expr[0] in op[1:-1]: #check if expr has '+', '-', '>', or '>='
                expressionOperand = []
                for mathToken in expr[1:]: #check if last two tokens are numeric
                  mathToken = mathToken.upper().strip()
                  if mathToken not in varValueD.keys(): #check if token is in variable dictionary
                    exprOp = variableParse(mathToken)
                  else:
                    try:
                      exprOp = int(varValueD[mathToken])
                    except:
                      raise InvalidValueType("'%s' is NOT numeric" %mathToken)
                  expressionOperand.append(exprOp)

                return operatorParse(expr[0],expressionOperand[0], expressionOperand[1])
    else: #expression has >3 variables and is therefore invalid
              raise InvalidExpression("Invalid Expression")
            
  except (TooFewOperands, InvalidExpression, InvalidValueType) as e:
    print("*** line %d error detected ***" % lineNum)
    print("%-10s %d *** %s ***" % (" ", lineNum, str(e.args[1])))
  except Exception as e:
    print("*** line %d error detected ***" % lineNum)
    print(e)
  except:
    print("*** line %d error detected ***" % lineNum)
    traceback.print_exc()

#assignVariable(tokenList, lineNum, varValueD, varTypeD)
#Purpose:
#    Assign values to variables found in BEEP statement
#Parameters:
#    tokenList: List which contains all tokens within a line
#    lineNum: The number of the line that causes an error
#    varValueD: The dictionary of variable values
#    varTypeD: The dictionary of variable types

def assignVariable(tokenList, lineNum, varValueD, varTypeD):

  try:
    assignToken = tokenList[0].upper()
    if assignToken not in varValueD.keys(): #check if variable not in value dictionary
      raise VarNotDefined("'%s' referenced variable is NOT defined" % assignToken)
    else: #check for operations in statement and assign to value dictionary
        exprToken = expressionParse(tokenList[1:], lineNum, varValueD)
        varValueD[assignToken] = exprToken
  except VarNotDefined as e:
    print("*** line %d error detected ***" % lineNum)
    print("%-10s %d *** %s ***" % (" ", lineNum, str(e.args[1])))
      
#printVariable(tokenList, lineNum, varValueD, varTypeD)
#Purpose:
#    Print out the variables in a BEEP statement
#Parameters:
#    tokenList: List which contains all tokens within a line
#    lineNum: The number of the line that causes an error
#    varValueD: The dictionary of variable values
#    varTypeD: The dictionary of variable types

def printVariable(tokenList, lineNum, varValueD, varTypeD):

  try:
      for printToken in tokenList:
        if printToken[0] == '"': #check if statement begins with "
          print(printToken.replace('"', ''), end = ' ')
        elif (printToken.upper() not in varValueD.keys()): #check if variable not in value dictionary
          raise VarNotDefined("'%s' referenced variable is NOT defined" % printToken)
        else: #print out variables
          printValue = varValueD[printToken.upper()]
          printType = varTypeD[printToken.upper()]
          if printType == 'string': #print string
            print(printValue.replace('"', ''), end = ' ')
          else:
            print(printValue, end = ' ')
      print()
      
  except VarNotDefined as e:
        print ("*** line %d error detected ***" % lineNum)
        print("%-10s %d *** %s ***" % (" ", lineNum, str(e.args[1])))

#statementExecute(tokenList, lineNum, varValueD, varTypeD, labelD
#Purpose:
#    Find and execute commands within a line of BEEP code 
#Parameters:
#    tokenList: List which contains all tokens within a line
#    lineNum: The number of the line that causes an error
#    varValueD: The dictionary of variable values
#    varTypeD: The dictionary of variable types
#    labelD: The dictionary of label line numbers
def statementExecute(tokenList, lineNum, varValueD, varTypeD, labelD):

  statementKey = tokenList[0].upper()
  
  #check if PRINT command
  if statementKey == 'PRINT':
    printVariable(tokenList[1:], lineNum, varValueD, varTypeD)
    return

    #check if ASSIGN command
  elif statementKey ==  'ASSIGN':
    assignVariable(tokenList[1:], lineNum, varValueD, varTypeD)
    return

  #check if expression true or false
  elif statementKey ==  'IF':
    flagCheck= expressionParse(tokenList[1:4], lineNum, varValueD)
    if isinstance(flagCheck, bool) and flagCheck is True:
      try:
        checkLine = int(labelD[tokenList[-1].upper()])
        return checkLine
      except:
        raise LabelNotDefined("Label undefined")
    else:
      return

  #check if GOTO and return line number, else return exception if not in labelD
  elif statementKey == 'GOTO':
    try:
      checkLine = int(labelD[tokenList[-1].upper()])
      return checkLine
    except:
      raise LabelNotDefined("'%s' Label undefined" % tokenList[-1])
  
  else:
    raise InvalidExpression("Statement NOT valid")
       
#executeBEEP(statementsInBEEP, varValueD, varTypeD, labelD)
#Purpose:
#    Execute the BEEP statement
#Parameters:
#    statementsInBEEP: Dictionary of BEEP statements
#    varValueD: The dictionary of variable values
#    varTypeD: The dictionary of variable types
#    labelD: The dictionary of label line numbers
#    Verbose: Boolean flag used if '-v' present in command line
def executeBEEP(statementsInBEEP, varValueD, varTypeD, labelD, Verbose = False):
  
  lineCount = 0
  totalLinesCounted = 0
  executeToken = list(statementsInBEEP.values())
  executeResult = None
  
  while lineCount < len(executeToken):

    #line currently being executed
    curToken = executeToken[lineCount]
    lineToken = curToken.split()
    
    #increment linesCounted and print statement if -v flag detected
    if not len(lineToken) == 0:
      totalLinesCounted += 1
      if Verbose:
        print ("executing line {}: {}".format(lineCount+1, curToken))
      
    #ignore empty lines
    if len(lineToken) == 0:
      lineCount += 1
      continue
      
    #ignore VAR lines
    if lineToken[0] == 'VAR':
      lineCount += 1
      continue
      
    #list of statement operators
    statementOps = ['PRINT', 'ASSIGN', 'IF', 'GOTO']

    #check if it is statement and run
    try:
      if lineToken[0].upper() in statementOps:
        executeResult = statementExecute(lineToken, lineCount+1, varValueD, varTypeD, labelD)
      elif lineToken[1].upper() in statementOps:
        executeResult = statementExecute(lineToken[1:], lineCount+1, varValueD, varTypeD, labelD)
      if isinstance(executeResult, int):
        lineCount = executeResult - 2
    except (LabelNotDefined, InvalidExpression) as e:
      print ("*** line %d error detected ***" % (lineCount + 1))
      print("%-10s %d *** %s ***" % (" ", (lineCount + 1), str(e.args[1])))
      lineCount += 1
      continue
        
    #increment line counter  
    lineCount += 1
    
    #total line limit of 5000
    if totalLinesCounted > 5000:
      break
      
  print("execution ends, %d lines executed" % totalLinesCounted)
