# In this subroutine, Buchberger's algorithm will be implemented to produce a Grobner basis for a provided list of polynomial. The result of this subroutine will be the main machine that will solve a system of polynomial equations.

from SimultPolynomialSolver import PolynomialArithmetic as PA
import copy
from SimultPolynomialSolver import GenPolyDiv as GPD
from SimultPolynomialSolver import AlgDictConv as ADC

# The following function will return the S-polynomial for two polynomials A and B provided. The S-polynomial is defined as:
'''
S(A, B) = PolyLCM(LT(A), LT(B)) * A / LT(A) - PolyLCM(LT(A), LT(B)) * B / LT(B)
'''

def S(A : dict, B : dict) -> dict:
    lcmMonomial = PA.PolyLCM(PA.LT(A), PA.LT(B))
    S = PA.PolySubtract(PA.DivbyMonomial(PA.PolyMult_minor(lcmMonomial, A), PA.LT(A)), PA.DivbyMonomial(PA.PolyMult_minor(lcmMonomial, B), PA.LT(B)))
    return S

# The following function is the Buchberger's algorithm which returns a list of polynomials which have a special property that allows us to use them for solving simultaneous equations of polynomials. This list is called a 'Grobner basis'. I will not go into the details and theory of these bases.

def Buchberger(P: list[dict]) -> list[dict]:
    if len(P) == 1:
        return P # Short-circuit case. A single polynomial is already a Grobner basis.

    M = PA.NumVars(P[0]) # Number of variables.

    Pcopy = P.copy()
    for p in Pcopy:
        if PA.Normalize(p) == PA.ZeroPoly(M):
            P.remove(p)

    G = copy.deepcopy(P) # Using 'G' as the list identifier is a standard, rather than a more apparent identifier.
    AlreadyKnown = [] # Stores (i, j) pairs whose S-polynomial gives zero remainder.

    while True:
        AddedNew = False
        TempG = copy.deepcopy(G)

        for i in range(len(TempG)):
            for j in range(i + 1, len(TempG)):

                if (TempG[i], TempG[j]) in AlreadyKnown:
                    continue  

                # Compute S-polynomial and remainder.
                Rem = GPD.GenPolyDiv(S(TempG[i], TempG[j]), TempG)[1]

                if PA.Normalize(Rem) == PA.ZeroPoly(M):
                    AlreadyKnown.append((TempG[i], TempG[j]))
                else:
                    G.append(Rem)
                    AddedNew = True
                    AlreadyKnown.append((TempG[i], TempG[j]))
                    break

            if AddedNew:
                break  

        if not AddedNew:  # No new polynomial was added. So, all S-polynomials reduce to zero. Thus, we are done
            break

    return G

# The following function turns a provided Grobner basis into a reduced Grobner basis. A reduced Grobner is more special because it makes computations easier and is always unique for a set of polynomials..
def ReducedGrobner(P : list[dict]) -> list[dict]:
    G = P.copy()
    M = PA.NumVars(P[0])

    # First, we turn the Grobner basis into a minimal Grobner basis.
    RedundPolys = []
    for i in range(len(G)):
        for j in range(len(G)):
            if i != j and PA.Divides(PA.LT(G[i]), PA.LT(G[j])) and G[i] not in RedundPolys:
                RedundPolys.append(G[j])

    for Poly in RedundPolys:
        if Poly in G:
            G.remove(Poly)

    for i in range(len(G)):
        coeff = list(PA.LT(G[i]).values())[0] # This thing gets the coefficient of the leading term of g which we will divide g by in the next line.
        G[i] = PA.MultbyConst(1 / coeff, G[i])

    # Now, we turn the minimal Grobner basis into a reduced one and return it.
    Remainders = []
    TempG = []
    for i in range(len(G)):
        TempG = G.copy()
        del TempG[i]
        Rem = GPD.GenPolyDiv(G[i], TempG)[1] # To extract remainder only from (QuotientList, Remainder).
        Remainders.append(Rem)
    
    return Remainders
