# In this subroutine, there will be code to solve a single variable polynomial which will come in handy in solving polynomials in several variables.

from SimultPolynomialSolver import PolynomialArithmetic as PA
from SimultPolynomialSolver import GenPolyDiv as GPD
from SimultPolynomialSolver import AlgDictConv as ADC
import numpy as NP

eps = PA.eps

IsTask1 = False

def Solve(F : dict) -> list[float]:
    N = list(PA.LT(F).keys())[0][0]
     
    if PA.Normalize(F) == PA.ZeroPoly(1):
        return "any"
    elif N == 0:
        return "none"

    Poly = list(F.items())
    CoeffList = [0 for i in range(N + 1)]

    for i in range(len(Poly)):
        deg = Poly[i][0][0]
        coeff = Poly[i][1]
        CoeffList[N - deg] = coeff

    AllRootsNumpy = NP.roots(CoeffList)
    AllRoots = AllRootsNumpy.tolist()
    RealRoots = []
    NonRealRoots = []
    for root in AllRoots:
        if abs(root.imag) <= eps:
            RealRoots.append(root.real)
        else:
            NonRealRoots.append(root)

    if IsTask1:
        dec = int(input("Enter number of decimal places to approximate result to: "))
        RealRootsCopy = []
        for root in RealRoots:
            RealRootsCopy.append(round(root, dec))

        NonRealRootsCopy = []
        for root in NonRealRoots:
            NonRealRootsCopy.append(PA.round_complex(root, dec))

        Roots = RealRootsCopy + NonRealRootsCopy
        return Roots

    Roots = RealRoots + NonRealRoots

    return Roots
