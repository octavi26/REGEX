import json
from LNFAaccept import Verify

def PolishForm(cuv):
    stack = []
    word = []

    for char in cuv:
        if char not in op:
            word.append(char)
        else:
            if char == "(":
                stack.append(char)
            elif char == ")":
                top = stack.pop()
                while top != "(":
                    word.append(top)
                    top = stack.pop()
            elif len(stack) == 0:
                stack.append(char)
            elif priority[char] >= priority[stack[-1]]:
                stack.append(char)
            else:
                while len(stack) > 0 and priority[char] < priority[stack[-1]]:
                    word.append(stack.pop())
                stack.append(char)
    while len(stack) > 0:
        word.append(stack.pop())

    cuv = "".join(word)
    # print(cuv)

    return cuv

def RegexNFA(cuv):
    Regex = []
    for char in cuv:
        if char in op:
            Regex.append(char)
        else:
            NFA = [[0, 1], [char], {(0, char) : [1]}, 0, [1]]
            Regex.append(NFA)

    stack_op = []
    stack_NFA = []
    for regex in Regex:
        if regex == ".":
            NFA1 = stack_NFA.pop()
            NFA2 = stack_NFA.pop()
            NFA = Concat(NFA2, NFA1)
            stack_NFA.append(NFA)
        elif regex == "|":
            NFA1 = stack_NFA.pop()
            NFA2 = stack_NFA.pop()
            NFA = OR(NFA2, NFA1)
            stack_NFA.append(NFA)
        elif regex == "*":
            NFA = stack_NFA.pop()
            NFA = Star(NFA)
            stack_NFA.append(NFA)
        elif regex == "+":
            NFA = stack_NFA.pop()
            NFA = Plus(NFA)
            stack_NFA.append(NFA)
        elif regex == "?":
            NFA = stack_NFA.pop()
            NFA = Question(NFA)
            stack_NFA.append(NFA)
        else:
            stack_NFA.append(regex)
        # print(*stack_NFA, sep="\n")
        # print()

    return stack_NFA.pop()

def Concat(NFA1, NFA2):
    #      Q,  S,  D,  q0, F
    NFA = [[], [], {}, -1, []]

    n = len(NFA1[0]) # Nr de stari
    NFA[0] = [i for i in range(n + len(NFA2[0]))]
    NFA[1] = list(set(NFA1[1]) | set(NFA2[1]))
    NFA[2] = NFA1[2]
    NFA[3] = NFA1[3]
    NFA[4] = [i + n for i in NFA2[4]]

    for pair in NFA2[2]:
         NFA[2][(pair[0] + n, pair[1])] = [i + n for i in NFA2[2][pair]]

    for q in NFA1[4]:
        try:
            NFA[2][(q, "~")].append(NFA2[3] + n)
        except:
            NFA[2][(q, "~")] = [NFA2[3] + n]

    return NFA

def OR(NFA1, NFA2):
    #      Q,  S,  D,  q0, F
    NFA = [[], [], {}, -1, []]

    n = len(NFA1[0]) # Nr de stari
    NFA[0] = [i for i in range(n + len(NFA2[0]) + 1)]
    NFA[1] = list(set(NFA1[1]) | set(NFA2[1]))
    NFA[2] = NFA1[2]
    NFA[3] = n
    NFA[4] = NFA1[4] + [i + n + 1 for i in NFA2[4]]

    for pair in NFA2[2]:
         NFA[2][(pair[0] + n + 1, pair[1])] = [i + n + 1 for i in NFA2[2][pair]]

    NFA[2][(n, "~")] = [NFA1[3], NFA2[3] + n + 1]

    return NFA

def Star(NFA):
    # NFA = (Q, Sigma, D, q0, F)
    n = len(NFA[0])
    NFA[0].append(n)
    NFA[2][(n, "~")] = [NFA[3]]
    NFA[3] = n
    for q in NFA[4]:
        try:
            NFA[2][(q, "~")].append(n)
        except:
            NFA[2][(q, "~")] = [n]
    NFA[4] = [n]

    return NFA

def Plus(NFA):
    # NFA = (Q, Sigma, D, q0, F)
    n = len(NFA[0])
    NFA[0].append(n)
    NFA[2][(n, "~")] = [NFA[3]]
    NFA[3] = n
    for q in NFA[4]:
        try:
            NFA[2][(q, "~")].append(n)
        except:
            NFA[2][(q, "~")] = [n]

    return NFA

def Question(NFA):
    # NFA = (Q, Sigma, D, q0, F)
    NFA[4].append(NFA[3])

    return NFA

if __name__ == "__main__":
    with open("data.json", "r") as file:
        data = json.load(file)


    op = ".|*+?()"
    priority = {
        "(" : 0,
        ")" : 0,
        "|" : 1,
        "." : 2,
        "+" : 3,
        "*" : 3,
        "?" : 3
    }

    # data = [{"regex" : "(a|b)*abb"}]
    for test in data:
        print(test["name"] + ": ", end="")
        cuv = test["regex"]
        print(cuv)

        # Add . opperator between values
        i = 1
        while i < len(cuv):
            if cuv[i] not in ".|*+?)" and cuv[i - 1] not in ".|(":
                cuv = cuv[:i] + "." + cuv[i:]
            i += 1

        cuv = PolishForm(cuv)
        Q, Sigma, D, q0, F = RegexNFA(cuv)

        # print(Q)
        # print("q0:", q0)
        # print("F:", *F)
        # for pair in D:
        #     print(pair[0], " --", pair[1], "-> ", D[pair], sep="")
        
        good = True
        for word in test["test_strings"]:
            if Verify(Q, Sigma, D, q0, F, word["input"]) != word["expected"]:
                good = False
                print("Not correct for word: " + word["input"])
        if good:
            print("Everything worked as expected!")

        print()
