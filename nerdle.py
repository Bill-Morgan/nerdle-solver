from multiprocessing.sharedctypes import Value
from operator import truediv
from posixpath import split
import random
import re
from tokenize import String
from turtle import numinput
from unicodedata import digit

def nerdle():
    global possibleSolution
    possibleSolution = False
    for first in digits[0]:
        equation = first
        for second in digits[1]:
            equation = first + second
            for third in digits[2]:
                equation = first + second + third
                if not any(exclude in equation for exclude in excludes):
                    for forth in digits[3]:
                        equation = first + second + third + forth
                        if not any(exclude in equation for exclude in excludes):
                            for fifth in digits[4]:
                                equation = first + second + third + forth + fifth
                                if not any(exclude in equation for exclude in excludes):
                                    for sixth in digits[5]:
                                        equation = first + second + third + forth + fifth + sixth
                                        if not any(exclude in equation for exclude in excludes):
                                            for seventh in digits[6]:
                                                equation = first + second + third + forth + fifth + sixth + seventh
                                                if not any(exclude in equation for exclude in excludes):
                                                        for eighth in digits[7]:
                                                                equation = first + second + third + forth + fifth + sixth + seventh + eighth
                                                                if not any(exclude in equation for exclude in excludes):
                                                                    if (validate(equation)):
                                                                        possibleSolution = True
                                                                        return getResult(equation)
                                                                    
def validate(equation):
    global includes
    if not all(required in equation for required in includes):
        return False
    if not (isItNerdle(equation)):
        return False
    return isItMathle(equation)

def isItNerdle(equation):
    global excludes
    if (len(equation) != 8):
        return False
    if not all(eachChar in '0123456789+-*/=' for eachChar in equation):
        return False
    if any(exclude in equation for exclude in excludes):
        return False
    index = equation.find('=')
    if (index == 7 or equation.count('=') != 1):
        return False
    if any(eachChar in '+-*/' for eachChar in equation[index + 1:]):
        return False
    if not any(eachChar in "+-*/" for eachChar in equation[:index]):
        return False
    if re.search("[-+*\/=]0\d", equation):
        return False
    return True

def isItMathle(equation):
    eqIndex = equation.find('=')
    return (eval(equation[:eqIndex]) == int(equation[eqIndex + 1:]))

def getResult(equation):
    print ("    My Guess:  " + equation)
    result = input("How did I do?  ")
    if (result == '2' or result[:8] == '22222222'):
        return True
    if (len(result) != 8 or not all(each in ['0', '1', '2'] for each in result) or result[equation.find('=')] == '0'):
        if (len(result) == 8 and isItNerdle(result) and isItMathle(result)):
            return getResult(result)
        else:
            print ("\nI don't understand your input.\nPlease try again.")
            return getResult(equation)
    for each in '0123456789+-*/=':
        foundOneOrTwo = False
        foundZero = False
        index = equation.find(each)
        while (index >= 0):
            if (result[index] == '2'):
                digits[index] = [each]
                foundZero = False
            else:
                digits[index].remove(each)
                if (result[index] == '1' and not each in includes):
                    includes.append(each)
            foundZero = foundZero or result[index] == '0'
            foundOneOrTwo = foundOneOrTwo or result[index] in '12'
            nextIndex = equation[index + 1:].find(each)
            if (nextIndex >= 0):
                index += nextIndex + 1
            else:
                index = -1
        if (foundZero and not foundOneOrTwo):
            for digit in digits:
                if (len(digit) > 1 and each in digit):
                    digit.remove(each)
    return (False)

def randomizeOtimizeDigits():
    prioritiesList = ['/','*','-','+','1','2','3','4','5','6','7','8','9','0']
    random.shuffle(prioritiesList)
    for digit in digits:
        for prioity in prioritiesList:
            if (prioity in digit and prioity not in includes):
                digit.remove(prioity)
                digit.insert(0, prioity)
        random.shuffle(prioritiesList)

excludes = ['++', '+-', '+*', '+/', '+=', '+0', '-+', '--', '-*', '-/', '-=', '-0', '*+', '*-', '**', '*/', '*=', '*0', '/+', '/-', '/*', '//', '/=', '/0', '==']
includes = ['=']
digits = [['9','8','7','6','5','4','3','2','1'], ['+','-','*','/','8','7','6','5','4','3','2','1','0','9'], ['8','7','6','5','4','3','2','1','0','9','+','-','*','/'], ['-','*','/','8','7','6','5','4','3','2','1','0','9','+'], ['5','4','3','2','1','0','+','-','*','/','=','9','8','7','6'], ['=','9','8','7','6','5','4','3','2','1','0'], ['1','0','=','9','8','7','6','5','4','3','2'], ['2','1','0','9','8','7','6','5','4','3']]
possibleSolution = True
exclimation = "Woohoo!\n\n\n"
print ("\n\n\nput a 0 below each black, 1 below each purple and 2 below each green.\n")
randomizeOtimizeDigits()
while (not nerdle()):
    print()
    if (not possibleSolution):
        exclimation = "There was an invalid input. No solution found!\n\n\n"
        break
    randomizeOtimizeDigits()
print (exclimation)
