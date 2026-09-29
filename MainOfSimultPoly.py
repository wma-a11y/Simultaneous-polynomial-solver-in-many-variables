from SimultPolynomialSolver import PolynomialArithmetic as PA
from SimultPolynomialSolver import AlgDictConv as ADC
from SimultPolynomialSolver import PolyEqSolver as PES
from SimultPolynomialSolver import Elimination as Elim
from SimultPolynomialSolver import GenPolyDiv as GPD
from SimultPolynomialSolver import Buchberger as Buch
import copy

# Main
RunCount = 0
while True:
    RunCount = RunCount + 1
    if RunCount == 1:
        PA.eps = float(input("Enter a number which will be used as a zero approximate in float numbers: ")) #eps stands for epsilon.
    else:
        epsContinue = input("Would you like to continue with this zero approximate? 'Yes' or 'No': ")
        if epsContinue == "No" or epsContinue == "no":
            PA.eps = float(input("Enter a number which will be used as a zero approximate in float numbers: ")) #eps stands for epsilon.
            
    print("This program can do the following things: ")
    print("1. Solve a polynomial equal to zero in one variable. This is the only thing that is specific to one variable.")
    print("2. Solve a system of polynomial equations in any number of variables.")
    print("3. Do General Polynomial Division of a polynomial by a list of polynomials, again in multiple variables.")
    print("4. Given a list of polynomials, compute their Grobner basis and/or their reduced Grobner basis.")
    print("5. Stop.")
    Task = int(input("Select any number from 1 to 5 to do the specified task: "))
    Continue = True
    
    if Task == 1:
        PES.IsTask1 = True
        print("Enter the single variable polynomial to solve.")
        Polynomial = ADC.AlgToDictNonRed(input(), 1)
        Roots = PES.Solve(Polynomial)
        print("Solutions are: ")
        print(Roots)
        PES.IsTask1 = False
    elif Task != 5:
        M = int(input("Enter the maximum number of variables (M): "))

        if Task == 2:
            Cache = []
            while Continue == True:
                Elim.IsTask2 = True
                Polynomials = []

                i = 0
                for p in Cache:
                    Polynomials.append(p)
                    i = i + 1

                while True:
                    print("Enter the", i + 1, "polynomial. Enter 'Stop' to finish. Do not enter any zero polynomial.")
                    Poly = input()
                    if Poly == "Stop" or Poly == "stop":
                        break
                    else:
                        p = ADC.AlgToDictNonRed(Poly, M)
                        Polynomials.append(p)
                        Cache.append(p)
                        i = i + 1

                Sol = Elim.Solutions(Polynomials)
                if isinstance(Sol, str):
                    print(Sol)
                else:
                    SolCopy = copy.deepcopy(Sol)
                    for i in range(len(SolCopy)):
                        point = SolCopy[i]
                        listpt = list(point)
                        for j in range(len(point)):
                            coord = point[j]
                            if isinstance(coord, complex) and abs(coord.imag) <= PA.eps:
                                listpt[j] = coord.real

                        Sol[i] = tuple(listpt)

                    Sol = set(Sol)
                    print("Solutions are: ")
                    for point in Sol:
                        print(point)
                Elim.IsTask2 = False

                print("Would you like to continue this task again with these same polynomials with perhaps some additions and deletions? Enter 'Continue' to continue and 'Stop' to stop and finish this task.")
                Cont = input()
                while True:
                    if Cont == "Stop" or Cont == "stop":
                        Continue = False
                        break
                    elif Cont == "Continue" or Cont == "continue":
                        print("These are all the polynomials saved in Cache with their indices:")
                        for i in range(len(Cache)):
                            p = Cache[i]
                            print(str(i) + ".", ADC.DictToAlg(p))
                        Tup = input("Enter the indices of polynomials as a list which you would like to reuse (e.g., '[2]' or '[0, 3]' or '0, 3' ): ")
                        Tup = Tup.strip("[]").split(",")
                        TempCache = Cache.copy()
                        Cache = []
                        if Tup[0] != "":
                            for i in Tup:
                                Index = int(i)
                                Cache.append(TempCache[Index])
                        break
                    else:
                        print("Invalid input: '" + Cont + "'. Try again.")
                        Cont = input()
        elif Task == 3:
            DividendCache, DivisorCache = [], []
            while Continue == True:
                GPD.IsTask3 = True
                if DividendCache == []:
                    print("Enter the dividend polynomial.")
                    Dividend = ADC.AlgToDictNonRed(input(), M)
                    DividendCache.append(Dividend)
                else:
                    Dividend = DividendCache[0]
                    
                i = 0
                Divisors = []
                if DivisorCache == []:
                    print("Entering the list of divisor polynomials. Do not enter any zero polynomial.")
                else:
                    for p in DivisorCache:
                        Divisors.append(p)
                        i = i + 1
                
                while True:
                    print("Enter the", i + 1, "divisor polynomial. Enter 'Stop' to stop finish.")
                    Poly = input()
                    if Poly == "Stop" or Poly == "stop":
                        break
                    else:
                        p = ADC.AlgToDictNonRed(Poly, M)
                        Divisors.append(p)
                        DivisorCache.append(p)
                        i = i + 1

                Result = GPD.GenPolyDiv(Dividend, Divisors)
                print("Quotients are:")
                for quotient in Result[0]:
                    print(ADC.DictToAlg(quotient))
                print(", and Remainder is:")
                print(ADC.DictToAlg(Result[1]))
                GPD.IsTask3 = False

                print("Would you like to continue this task again with this dividend? Answer 'Yes' or 'No'.")
                DividendCont = input()
                while True:
                    if DividendCont == "No" or DividendCont == "no":
                        DividendContinue = False
                        DividendCache = []
                        break
                    elif DividendCont == "Yes" or DividendCont == "yes":
                        DividendContinue = True
                        break
                    else:
                        print("Invalid input: '" + DividendCont + "'. Try again.")
                        DividendCont = input()

                print("Would you like to continue this task again with these divisors? Answer 'Yes' or 'No'.")
                DivisorCont = input()
                while True:
                    if DivisorCont == "No" or DivisorCont == "no":
                        DivisorContinue = False
                        DivisorCache = []
                        break
                    elif DivisorCont == "Yes" or DivisorCont == "yes":
                        DivisorContinue = True
                        print("These are all the polynomials saved in Divisors' Cache with their indices:")
                        for i in range(len(DivisorCache)):
                            p = DivisorCache[i]
                            print(str(i) + ".", ADC.DictToAlg(p))
                        Tup = input("Enter the indices of polynomials as a list which you would like to reuse (e.g., '[2]' or '[0, 3]' or '0, 3' ): ")
                        Tup = Tup.strip("[]").split(",")
                        TempCache = DivisorCache.copy()
                        DivisorCache = []
                        if Tup[0] != "":
                            for i in Tup:
                                Index = int(i)
                                DivisorCache.append(TempCache[Index])
                        break
                    else:
                        print("Invalid input: '" + DivisorCont + "'. Try again.")
                        DividendCont = input()

                Continue = DividendContinue or DivisorContinue
        else:
            Cache = []
            while Continue == True:
                Polynomials = []

                i = 0
                for p in Cache:
                    Polynomials.append(p)
                    i = i + 1
                
                while True:
                    print("Enter the", i + 1, "polynomial. Enter 'stop' to finish. Do not enter any zero polynomial.")
                    Poly = input()
                    if Poly == "Stop" or Poly == "stop":
                        break
                    else:
                        p = ADC.AlgToDictNonRed(Poly, M)
                        Polynomials.append(p)
                        Cache.append(p)
                        i = i + 1

                Choice = int(input("Enter 1 for just a Grobner basis and 2 for a Reduced Grobner basis: "))
                dec = int(input("Enter number of decimal places to approximate result's coeffecients to: "))
                G = Buch.Buchberger(Polynomials)
                if Choice == 1:
                    for i in range(len(G)):
                        g = G[i]
                        G[i] = PA.RoundPoly(g, dec)

                    print("Grobner basis is:")
                    for g in G:
                        print(ADC.DictToAlg(g))
                else:
                    G = Buch.ReducedGrobner(G)
                    for i in range(len(G)):
                        g = G[i]
                        G[i] = PA.RoundPoly(g, dec)
                    
                    print("Reduced Grobner basis is:")
                    for g in G:
                        print(ADC.DictToAlg(g))

                print("Would you like to continue this task again with these same polynomials with perhaps some additions and deletions? Enter 'Continue' to continue and 'Stop' to stop and finish this task.")
                Cont = input()
                while True:
                    if Cont == "Stop" or Cont == "stop":
                        Continue = False
                        break
                    elif Cont == "Continue" or Cont == "continue":
                        print("These are all the polynomials saved in Cache with their indices:")
                        for i in range(len(Cache)):
                            p = Cache[i]
                            print(str(i) + ".", ADC.DictToAlg(p))
                        Tup = input("Enter the indices of polynomials as a list which you would like to reuse (e.g., '[2]' or '[0, 3]' or '0, 3' ): ")
                        Tup = Tup.strip("[]").split(",")
                        TempCache = Cache.copy()
                        Cache = []
                        if Tup[0] != "":
                            for i in Tup:
                                Index = int(i)
                                Cache.append(TempCache[Index])
                        break
                    else:
                        print("Invalid input: '" + Cont + "'. Try again.")
                        Cont = input()
    else:
        break
