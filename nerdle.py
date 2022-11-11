import random
import re


def findEquation():
    # this 7 deep nested loop may look very inefficient but at this point, there are a maximum of about 60,000 possible total combinations
    # after processing the seed equations and most likely less than 5,000 combinations are left.
    global possibleSolution
    possibleSolution = False
    for first in digits[0]:
        equation = first
        for second in digits[1]:
            for third in digits[2]:
                for forth in digits[3]:
                    for fifth in digits[4]:
                        for sixth in digits[5]:
                            for seventh in digits[6]:
                                for eighth in digits[7]:
                                    equation = first + second + third + forth + fifth + sixth + seventh + eighth
                                    if (validate(equation)):
                                        possibleSolution = True
                                        return getResult(equation)


def validate(equation):
    global includes
    return all(required in equation for required in includes) and isNerdle(equation)


def isNerdle(equation):
    equalPos = equation.find('=')
    return ((len(equation) == 8) and
            (all(eachChar in '0123456789+-*/=' for eachChar in equation)) and
            (not re.search(r"[\+\-\*\/]{2}", equation)) and
            (equalPos in [4, 5, 6]) and
            (equation.count('=') == 1) and
            (not any(eachChar in '+-*/' for eachChar in equation[equalPos + 1:])) and
            (any(eachChar in "+-*/" for eachChar in equation[:equalPos])) and
            (not re.search(r"[-+*=]0\d", equation)) and
            (not re.search(r"\/0", equation)) and
            (eval(equation[:equalPos]) == int(equation[equalPos + 1:])))


def removeOperators(index):
    for operator in "+-*/=":
        if (operator in digits[index]):
            digits[index].remove(operator)


def getResult(equation, prompts=["      My Guess:  ", "  How did I do?  "]):
    print(prompts[0] + equation)
    result = input(prompts[1])
    if (result == '2' or result[:8] == '22222222'):
        return True
    if (len(result) != 8 or not all(each in ['0', '1', '2'] for each in result)):
        if (isNerdle(result)):
            return getResult(result, ["\n    Your Guess:  ", "How did you do?  "])
        else:
            print("\nI don't understand your input.\nPlease try again.")
            return getResult(equation, prompts)
    for each in '0123456789+-*/=':
        foundOne = False
        foundZero = False
        index = equation.find(each)
        while (index >= 0):
            if (result[index] == '2'):
                digits[index] = [each]
                foundZero = False
                if (each in "+-*/="):
                    removeOperators(index - 1)
                    removeOperators(index + 1)
            else:
                if(each in digits[index]):
                    digits[index].remove(each)
                if (result[index] == '1' and not each in includes):
                    includes.append(each)
            foundZero = foundZero or result[index] == '0'
            foundOne = foundOne or result[index] == '1'
            index = equation.find(each, index + 1)
        if (foundZero and not foundOne):
            for digit in digits:
                if (len(digit) > 1 and each in digit):
                    digit.remove(each)
    return (False)


def randomizeOptimizeDigits():
    prioritiesList = ['/', '*', '-', '+', '1', '2',
                      '3', '4', '5', '6', '7', '8', '9', '0']
    for digit in digits:
        random.shuffle(prioritiesList)
        for prioity in prioritiesList:
            if (prioity in digit and prioity not in includes):
                digit.remove(prioity)
                digit.insert(0, prioity)


includes = []
digits = [['0', '9', '8', '7', '6', '5', '4', '3', '2', '1'], ['+', '-', '*', '/', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0'], ['+', '-', '*', '/', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0'], ['+', '-', '*', '/', '9', '8', '7', '6', '5', '4', '3',
                                                                                                                                                                                                               '2', '1', '0'], ['+', '-', '*', '/', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0'], ['=', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0'], ['=', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0'], ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0']]
possibleSolution = True
exclimation = "Woohoo!\n\n\n"
print("\n\n\nput a 0 below each black, 1 below each purple and 2 below each green. Or, enter a new Nerdle equation to test.\n")
getResult("0+12/3=4")
if (len(digits[6]) == 1):
    getResult("9*8-65=7")
else:
    getResult("9*8-7=65")
if '=' not in digits[5] and '=' not in digits[6]:
    digits[4] = ['=']
    removeOperators(3)
    removeOperators(5)

randomizeOptimizeDigits()
while (not findEquation()):
    if (not possibleSolution):
        exclimation = "There was an invalid input. No solution found!\n\n\n"
        break
    randomizeOptimizeDigits()
print(exclimation)
