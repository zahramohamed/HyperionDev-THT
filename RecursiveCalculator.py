# Recurisve Calculator Task
# Author: Zahra Mohamed
# Date: 26 August 2023

operators = ["+", "-", "*", "/", "^"]
operands = ["a", "b", "c", "d"]
invalid = "Invalid Expression"

# Function takes in a list of terms in the expression
def calculate(exp):
    simplified = False # Used for algerbraic expressions

    # BODMAS must be considered
    # Brackets first: this must be done carefully because there can be nested brackets
    if ("(" in exp):
        x = exp.index("(")
        y = exp.index(")")
        subExp = exp[x+1:y]

        # Check if there are nested brackets, if there are, find the corresponding closed bracket
        n = subExp.count("(")
        m = subExp.count(")")
        brackets = 1
        if (n != m):
            for i, term in enumerate(exp[x+1:]):
                if (term == "("):
                    brackets += 1
                elif (term == ")"):
                    brackets -= 1
                
                if (brackets == 0):
                    y = (x+1) + i
                    break
        
        ans = calculate(exp[x+1:y])
        return calculate(exp[:x] + [ans] + exp[y+1:])
    # Division second 
    if ("/" in exp):
        op = exp.index('/')

        if ((isNumeral(exp[op-1])) and (isNumeral(exp[op+1]))):
            ans = exp[op-1] / exp[op+1]
            exp = exp[:op-1] + [ans] + exp[op+2:]
            return calculate(exp)
        elif (exp[op-1] == exp[op+1]):
            return calculate(exp[:op-1] + exp[op+2:])
        else:
            ans = [exp[op-1:op+2]]
            exp = exp[:op-1] + [ans] + exp[op+2:]
            return calculate(exp)
    # Multiplication third (also includes index)
    if ("*" in exp):
        op = exp.index('*')
        cond1 = isNumeral(exp[op-1])
        cond2 = isNumeral(exp[op+1])
        if (cond1 and cond2):
            ans = [exp[op-1] * exp[op+1]]
        elif cond1:
            ans = numAlgMult(exp[op-1], exp[op+1])
        elif cond2:
            ans = numAlgMult(exp[op+1], exp[op-1])
        else:
            cond1 = type(exp[op-1]) == list
            cond2 = type(exp[op+1]) == list
            if cond1 or cond2:
                ans = polynomialMult(exp[op-1], exp[op+1])
        exp = exp[:op-1] + ans + exp[op+2:]
        return calculate(exp)
    if ("^" in exp):
        op = exp.index('^')
        ans = (exp[op-1]) ** (exp[op+1])
        exp = exp[:op-1] + [ans] + exp[op+2:]
        return calculate(exp)
    # Addition fourth
    if ("+" in exp):
        op = exp.index('+')
        # Terms can only be added together if they're like
        like, type = likeTerms(exp[op-1], exp[op+1])
        if like:
            if type == 1:
                ans = exp[op-1] + exp[op+1]
            else:
                a1 = readNumeral(exp[op-1])
                a2 = readNumeral(exp[op+1])

                if a1 == -1:
                    a1 = 1
                    term = exp[op-1]
                else:
                    term = exp[op-1][a1:]
                    a1 = float(exp[op-1][:a1])

                if a2 == -1:
                    a2 = 1
                else:
                    a2 = float(exp[op+1][:a2])

                a = a1 + a2
                ans = str(a) + term
        else:
            # Try and find a like term in the expression 
            for i, e in enumerate(exp):
                if i in range (op-1, op+2):
                    pass
                elif i in operators:
                    pass
                else:
                    like, type = likeTerms(exp[op-1], exp[op+1])
                    if like:
                        if type == 1:
                            ans = exp[op-1] + exp[op+1]
                        else:
                            a1 = readNumeral(exp[op-1])
                            a2 = readNumeral(exp[op+1])

                            if a1 == -1:
                                a1 = 1
                                term = exp[op-1]
                            else:
                                term = exp[op-1][a1:]
                                a1 = float(exp[op-1][:a1])

                            if a2 == -1:
                                a2 = 1
                            else:
                                a2 = float(exp[op+1][:a2])

                            a = a1 + a2
                            ans = str(a) + term
                    else:
                        pass
            exp = exp[:op-1] + [ans] + exp[op+2:]
            return calculate(exp)
    # Subtraction last
    if ("-" in exp):
        op = exp.index('-')
        ans = exp[op-1] - exp[op+1]
        exp = exp[:op-1] + [ans] + exp[op+2:]
        return calculate(exp)
    if (len(exp) == 1):
        return exp[0]
    else:
        invalidMessage()
        return

def splitExp(inp):
    exp = [] # List of terms
    brackets = 0 # To ensure brackets are closed 
    neg = False

    # Expressions can only start with an open bracket, a numeral (positive or negative) or a variable
    inp = inp.strip() # Remove leading and trailing whitespace
    if (len(inp) == 0):
        return []
    
    # Check if it starts with a brackets
    check_bracket = True 
    while (check_bracket): 
        if (inp[0] == "("): 
            exp.append("(")
            inp = inp[1:]
            inp = inp.strip() # Remove leading and trailing whitespace
            brackets += 1
            if (len(inp) == 0):
                return []
        else:
            check_bracket = False
    
    # Check if its a negative numeral
    if (inp[0]=="-"):
        neg = True
        inp = inp[1:]
        inp = inp.strip() # Remove leading and trailing whitespace

    # Check if it starts with a numeral or variable
    i = readNumeral(inp)
    if (i > 0):
        n = float(inp[:i])
        if (neg):
            n *= -1
            
        exp.append(n)
        inp = inp[i:]
        inp = inp.strip() # Remove leading and trailing whitespace

        if (len(inp) == 0):
            if (brackets == 0):
                return [n]
            else:
                return []
    elif (inp[0] in operands):
        var = inp[0]
        exp.append(var)
        inp = inp[1:]
        inp = inp.strip() # Remove leading and trailing whitespace

        if (len(inp) == 0):
            if (brackets == 0):
                return var
            else:
                return []
    else: 
        if (inp[0] != ")"):
            return []
    
    # Split the rest of the expression: groups of operator then operand
    # Brackets can only start after an operator (or bracket) and must end after a number (or bracket)
    # According to the assignment brief, the expression can only contain variables without indices or preceding constants
    while (inp != ""):
        # Check for operator
        if (inp[0] in operators):
            exp.append(inp[0])
            inp = inp[1:]
            inp = inp.strip() # Remove leading and trailing whitespace

            if (len(inp) == 0):
                return []
            
            # Check for operand
            # Numeral
            i = readNumeral(inp)
            if (i > 0):
                n = float(inp[:i])
                exp.append(n)
                inp = inp[i:]
                inp = inp.strip() # Remove leading and trailing whitespace
            # Variable
            elif (inp[0] in operands):
                exp.append(inp[0])
                inp = inp[1:]
                inp = inp.strip() # Remove leading and trailing whitespace

            # If not an operand, it can be a brackets followed by an operand
            else: 
                # First check that the expression isnt empty
                if (len(inp) == 0):
                    return []
            
                found_bracket = False   # Found a bracket
                check_bracket = True    # Stop looping if a bracket isnt found (using 2 bools is simplest)
                while (check_bracket): 
                    if (inp[0] == "("): 
                        exp.append("(")
                        inp = inp[1:]
                        inp = inp.strip() # Remove leading and trailing whitespace
                        brackets += 1
                        found_bracket = True
                        if (len(inp) == 0):
                            return []
                    else:
                        check_bracket = False
                
                if (found_bracket):
                    i = readNumeral(inp)
                    if (i > 0):
                        n = float(inp[:i])
                        exp.append(n)
                        inp = inp[i:]
                        inp = inp.strip() # Remove leading and trailing whitespace
                    elif (inp[0] in operands):
                        exp.append(inp[0])
                        inp = inp[1:]
                        inp = inp.strip() # Remove leading and trailing whitespace
                    else:
                        return []
                else:
                    return []
        # If not an operator, can be a closed bracket
        else:
            # Check if there are open brackets, if not return invalid
            if (brackets > 0):
                check_bracket = True 
                found_bracket = False
                while (check_bracket): 
                    if (inp[0] == ")"): 
                        exp.append(")")
                        inp = inp[1:]
                        inp = inp.strip() # Remove leading and trailing whitespace
                        brackets -= 1
                        found_bracket = True

                        if (len(inp) == 0):
                            check_bracket = False
                        if (brackets == 0):
                            check_bracket = False
                    else:
                        check_bracket = False

                # If there are no closed brackets then return invalid
                if (not found_bracket):
                    return []
            else:
                return [] 
    return exp


def likeTerms(term1, term2):
    if isNumeral(term1) and isNumeral(term2):
        return True, 1
    else: 
        like = False
        for var in operands:
            if ((var in term1) == (var in term2)):
                like = True
            else: 
                like = False
                break
        
        if not like:
            return False, 0
        
        if ("^" in term1) == ("^" in term2):
            start1 = term1.index("^")
            start2 = term2.index("^")
            index1 = term1[start1+1:readNumeral(term1[start1 + 1])]
            index2 = term2[start2+1:readNumeral(term2[start2 + 1])]
            return index1 == index2, 3
        else:
            return True, 2

def numAlgMult(term1, term2):
    result = []
    for i in term2:
        if i in operators:
            if term1 < 0:
                if i == "-":
                    result.append("+")
                elif i == "+":
                    result.append("-")
                else:
                    result.append(i)
            else:
                result.append(i)
        else:
            if isNumeral(term1) and isNumeral(i):
                result.append(term1*i)
            if i in operands:
                result.append(str(term1) + i)
            else:
                a = readNumeral(i)
                if (a > 0):
                    result.append(str(term1*float(i[:a])) + i[a:])
    return result

def algMult(term1, term2):
    cond1 = term1 in operands
    cond2 = term2 in operands
    if cond1 and cond2:
        if term1 == term2:
            return "2" + term1
        else:
            return term1 + term2
    if cond1:
        if term1 in term2:
            n = term2.index(term1)
            if n+1 == "^":
                i = readNumeral(term2[n+2:])
                index = term2[n+2:i] + 1
                return term2[:n+2] + index + term2[i:]
            else:
                return term2[:n+1] + "^2" + term2[n+1:]
        else:
            return term2 + term1
    elif cond2:
        if term2 in term1:
            n = term1.index(term2)
            if n+1 == "^":
                i = readNumeral(term1[n+2:])
                index = term1[n+2:i] + 1
                return term1[:n+2] + index + term1[i:]
            else:
                return term1[:n+1] + "^2" + term1[n+1:]
        else:
            return term1 + term2
        
def polynomialMult(term1, term2):
    result = []
    for pos1, i in enumerate(term1):
        if i==0:
            if i in operators:
                pass
            else:
                signi = "+"
        else:
            if i in operators:
                pass
            else:
                signi = term1[pos1-1]

        for pos2, j in enumerate(term2):
            if j==0:
                if j in operators:
                    pass
                else:
                    signj = "+"
            else:
                if j in operators:
                    pass
                else:
                    signj = term2[pos2-1]

            cond1 = isNumeral(i)
            cond2 = isNumeral(j)
            if cond1 and cond2:
                if signi == signj:
                    result.append("+")
                else:
                    result.append("-")
                result.append(i*j)
            elif cond1:
                result = result + numAlgMult(i, j)
            elif cond2:
                result = result + numAlgMult(j, i)
            else:
                if signi == signj:
                    result.append("+")
                else:
                    result.append("-")
                result.append(algMult(i, j))

    return result

# Checks whether a string is a float
def isNumeral(s):
    try:
        float(s)
        return True
    except:
        return False

# Reads the first numeral from a string stream
def readNumeral(inp):
    # Read full numeral from string, return position where the numeral ends
    if (isNumeral(inp[0])):
        n = inp[0]
        i = 1
        if (len(inp) == i):
            return i
        
        while (isNumeral(n + inp[i])): # Find the numeral in the string
            n += inp[i]
            i += 1
            if (len(inp) == i):
                return i

        return i
    else:
        return -1

def invalidMessage():
    print(invalid)
    exit(0)

def main():
    inp = input()
    expList = splitExp(inp)

    if (expList == []):
        invalidMessage()
    else:
        ans = calculate(expList)
        # Eliminate decimal if there are no decimal places
        if (ans - int(ans) == 0):
            print(str(int(ans)))
        else:
            print(str(ans))



if __name__ == "__main__":
    main()








