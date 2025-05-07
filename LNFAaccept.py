# Nume: Radu DImitrie Octavian
# Grupa: 152
# Compilator: python3


def Parse(Q, Sigma, D, S, F):
    text_file = input("Config file name: ")
    if "." in text_file:
        text_file = text_file[:text_file.find(".")]
    fin = open(text_file + ".txt", "r")

    Sigma.append('~')
    state = "end"
    for line in fin:
        # Scapam de comentarii (comentariu ironic)
        line = line.strip()
        if line[0] == "#":
            continue
        if "#" in line:
            line = line[:line.find("#")]
        
        if line in ["States:", "Sigma:", "Transitions:", "End"]:
            state = line.lower()[:len(line) - 1 if ":" in line else len(line)]
            continue

        # print(state)

        if state == "states":
            L = line.replace(",", " ").split()
            if len(L) > 3:
                return False
            try:
                nr = int(L[0][1:])
            except:
                return False

            if nr in Q:
                return False
            Q.append(nr)

            if len(L) == 3 and ("S" not in L or "F" not in L):
                return False
            if len(L) == 2 and "S" not in L and "F" not in L:
                return False
            if "S" in L and S[0] != -1:
                return False
            
            if "S" in L:
                S[0] = nr
            if "F" in L:
                F.append(nr)


        elif state == "transitions":
            L = line.replace(",", " ").split()
            if len(L) != 3:
                return False
            try:
                q1 = int(L[0][1:])
                q2 = int(L[2][1:])
            except:
                return False
            if q1 not in Q or q2 not in Q or L[1] not in Sigma:
                return False
            if (q1, L[1]) not in D:
                D[(q1, L[1])] = []
            D[(q1, L[1])].append(q2)


        elif state == "sigma":
            if line in Sigma:
                return False
            Sigma.append(line)
        else:
            continue

    if S[0] == -1:
        return False
    
    return True

def Verify(Q, Sigma, D, q0, F, cuv):
    cuv = "".join(['~' if i % 2 == 0 else cuv[i // 2] for i in range(2 * len(cuv) + 1)])
    currentState = [q0]
    nextState = []
    while len(cuv) != 0:
        nextState = []

        for state in currentState:
            if cuv[0] == '~':
                # print((state, cuv[0]))
                # print(D)
                queue = [state]
                while len(queue) > 0:
                    st = queue[0]
                    queue = queue[1:]
                    if st not in nextState:
                        nextState.append(st)
                    if (st, '~') in D:
                        for q in D[(st, "~")]:
                            if q not in nextState:
                                queue.append(q)
            else:
                if (state, cuv[0]) in D:
                    nextState.extend(D[(state, cuv[0])])
        cuv = cuv[1:]
        currentState = nextState
        
    for state in currentState:
        if state in F:
            return True
    return False


if __name__ == "__main__":
    D = {}
    Q = []
    S = [-1]
    F = []
    Sigma = []
    valid = Parse(Q, Sigma, D, S, F)
    q0 = S[0]

    if not valid:
        print("Something went wrong.")
    else:
        print("Config file verrified succesfuly!")
        print("q0:", q0)
        print("F:", *F)
        for pair in D:
            print(pair[0], " --", pair[1], "-> ", D[pair], sep="")
        while True:
            cuv = input("Cuvant de verificat: ")
            print(cuv)
            if Verify(Q, Sigma, D, q0, F, cuv):
                print("Cuvant acceptat!")
            else:
                print("neacceptat :(")