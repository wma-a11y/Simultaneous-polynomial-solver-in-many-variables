# In this subroutine, the final step to actualy get the values for solutions to a system of polynomial equations will be done. We will proceed by elimination of variables.

from SimultPolynomialSolver import PolynomialArithmetic as PA
import copy
from SimultPolynomialSolver import Buchberger as Buch
from SimultPolynomialSolver import GenPolyDiv as GPD
from SimultPolynomialSolver import PolyEqSolver as PES
import sys

eps = PA.eps

def Eval(P : dict, coords : tuple) -> dict:
    n = len(coords)
    PResult = {}

    for muldeg, coeff in P.items():
        CoeffNew = coeff
        MuldegNew = list(muldeg)

        for i in range(-1, -n-1 , -1):
            CoeffNew = CoeffNew * (coords[i] ** muldeg[i])                

        MuldegNew = tuple(MuldegNew[:-n])

        PResult = PA.PolyAdd(PResult, {MuldegNew: CoeffNew})
    
    return PResult

def EliminateFirstVariable(A : dict) -> dict:
    Z = {}

    for muldeg, coeff in A.items():
        if muldeg == ():
            return A
        muldeg_list = list(muldeg)
        del muldeg_list[0]
        NewMuldeg = tuple(muldeg_list)
        Z[NewMuldeg] = coeff
    
    return Z

def EliminateLeftVariables(g : dict, N : int) -> dict:
    Ans = copy.deepcopy(g)

    for i in range(N + 1):
        Ans = EliminateFirstVariable(Ans)

    return Ans

def UnitTuple(i : int, M : int) -> tuple:
    coord = list(0 for _ in range(M))
    coord[i] = 1
    return tuple(coord)

def LeadMuldeg(g : dict) -> tuple:
    return list(PA.LT(g).keys())[0]

def MonicGCD(X : list[dict]) -> dict: # For univariate only.
    return Buch.ReducedGrobner(Buch.Buchberger(X))[0]

# There were some errors caused by non termination of almost zero terms in some test runs, because the eps chosen was too small to round them to 0. This is a check for that.
def Has_spurious_constant(G : list[dict], eps):
    for g in G:
        # If polynomial has no variables and its constant term is tiny but nonzero
        if all(deg == 0 for deg in LeadMuldeg(g)):
            const_val = list(g.values())[0]  # assuming dict form {monomial: coeff}
            if abs(const_val) < 10*eps and abs(const_val) > eps:
                return True
    return False

# The main purpose of this entire program.

def Solutions(P: list[dict]) -> list[tuple]:
    breakage = False
    
    M = PA.NumVars(P[0])


    P = [p for p in P if PA.Normalize(p) != PA.ZeroPoly(M)]
    for p in P:
        if LeadMuldeg(p) == tuple(0 for _ in range(M)): # If any constant surpassing tolerance has been entered. 
            return "No solutions."

    if P == []:
        return "Max solution space." # Zero ideal.


    G = Buch.Buchberger(P)
    for g in G:
        if LeadMuldeg(g) == tuple(0 for _ in range(M)):
            print("Either the system has no solution or a spurious constant has appeared due to a very small tolerance in the Grobner basis calculation.")
            print("Check the result of said Grobner basis calculation below and verify.")
            print("Info: if the constant polynomial that appears has magnitude that is just above tolerance, then it is likely there is a spurious constant. Here, choose a slightly bigger tolerance and try again.")
            print("Info: if however the constant is far larger than tolerance, like greater than 1, then it is likely that the system has no solution.")
            breakage = True

    if breakage:
        print("Grobner basis that was computed. It will be output in dictionary form:")
        for g in G:
            print(g)

        sys.exit(1)
    
    G = Buch.ReducedGrobner(G)

    if M == 1:
        Values = PES.Solve(G[0])
        if Values == "none":
            return "No solutions."
        else:
            return [(value,) for value in Values]


    Points, Sol = [], []

    # Find all polynomials in only x_{M-1}. There will only be no more than one such polynomial.
    G_elim = []
    for g in G:
        if LeadMuldeg(g) < UnitTuple(M - 2, M):
            g_elim = EliminateLeftVariables(g, M - 2)
            G_elim.append(g_elim)

    if G_elim == []:
        value = complex(input("The " + str(M-1) + " elimination ideal is 0. Thus, enter a value for x_" + str(M-1) + ": "))
        Points.append((value,))
    else:
        Values = PES.Solve(G_elim[0])
        for value in Values: # G_elim[0] is not constant. Every complex nonconstant polynomial has a root, so Values != [] (Fundamental theorem of Algebra).
            Points.append((value,))

    for i in range(M - 2, 0, -1):
        TempPoints = Points
        Points = []

        G_elimPrev = G_elim.copy()
        G_elim = []
        for g in G:
            if LeadMuldeg(g) < UnitTuple(i - 1, M):
                G_elim.append(EliminateLeftVariables(g, i - 1))

        if G_elim == G_elimPrev:
            value = complex(input("The variable x_" + str(i) + " is free. Give a value for it: "))
            for point in TempPoints:
                Points.append((value,) + point)
        else:
            for point in TempPoints:
                G_eval = []
                for g in G_elim:
                    g_eval = PA.Normalize(Eval(g, point))
                    G_eval.append(g_eval)

                F = MonicGCD(G_eval)
                Values = PES.Solve(F)
                if Values == "none":
                    continue
                elif Values == "any":
                    value = complex(input("For point " + str(tuple("x_" + str(k) for k in range(i + 1, M))) + " = " + str(point) + ", x_" + str(i) + " is free. Enter a value for it: "))
                    Points.append((value,) + point)
                else:
                    for value in Values:
                        Points.append((value,) + point)
                        
    for point in Points:
        G_eval = []
        for g in G:
            g_eval = PA.Normalize(Eval(g, point))
            G_eval.append(g_eval)

        F = MonicGCD(G_eval)
        Values = PES.Solve(F)
        if Values == "none":
            continue
        elif Values == "any":
            value = complex(input("For point " + str(tuple("x_" + str(k) for k in range(1, M))) + " = " + str(point) + ", x_" + str(0) + " is free. Enter a value for it: "))
            Sol.append((value,) + point)
        else:
            for value in Values:
                Sol.append((value,) + point)
    
    if Sol == []:
        return "No solutions."
    else:
        if IsTask2:
            dec = int(input("Enter number of decimal places to approximate result to: "))
            RoundedSol = []
            for point in Sol:
                RoundedPoint = []
                for coord in point:
                    if isinstance(coord, complex):
                        RoundedPoint.append(PA.round_complex(coord, dec))
                    else:
                        RoundedPoint.append(round(coord, dec))

                RoundedSol.append(tuple(RoundedPoint))

            return RoundedSol
        else:
            return Sol
