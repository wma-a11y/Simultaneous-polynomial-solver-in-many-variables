# This subroutine contains code that will convert polynomials from dictionary form to algebraic and from algebraic to dictionary form.
# In algebraic form, polynomials will be written in the lexicographic order starting from the least term and ending at the leading term. The ordering will use the convention x_0 > x_1 > x_2 > ...

from SimultPolynomialSolver import PolynomialArithmetic as PA
import copy

eps = PA.eps

# This function rewrites the dictionary in the ascending order provided by the lexicography first.
def AscOrder(P : dict) -> dict:
    X, Y = {}, P.copy()

    for i in range(len(list(Y.keys()))):
        muldeg = min(list(Y.keys()))
        coeff = Y[muldeg]

        X[muldeg] = coeff

        del Y[muldeg]

    return X

# This function will take a multidegree like (1, 2, 0, 3) and return the string "x_0 x_1^2 x_3^3" (notice how x_2^0 = 1, so is not written).

def MuldegToMonomial(muldeg : tuple) -> str:
    M = len(muldeg)
    monom = ""

    for i in range(M):
        if muldeg[i] == 1:
            monom = monom + "x_" + str(i) + " "
        elif muldeg[i] > 1:
            monom = monom + "x_" + str(i) + "^" + str(muldeg[i]) + " "

    return monom[:-1]

# Conversely from above, this function will take a monomial string in a desired form and some additional necessary information to give a multidegree.
def MonomialToMuldeg(monom : list[str], M : int) -> tuple:
    MuldegList = [0 for i in range(M)]

    for Vari in monom:
        index = int(Vari.split("_")[1].split("^")[0])
        if len(Vari.split("^")) == 1:
            power = 1
        else:
            power = int(Vari.split("^")[1])

        MuldegList[index] = power

    muldeg = tuple(i for i in MuldegList)

    return muldeg

# Purposes of the following two functions are evident from name.

def DictToAlg(P : dict) -> str:
    Polynomial = ""
    P = AscOrder(P)
    M = PA.NumVars(P)

    for muldeg in P.keys():
        coeff = P[muldeg]
        if abs(coeff.imag) <= eps:
            coeff_str = str(coeff.real)
        else:
            if abs(coeff.real) <= eps:
                coeff_str = str(coeff.imag) + "j"
            else:
                coeff_str = str(coeff)
            
        if muldeg == tuple(0 for _ in range(M)):
            Polynomial = Polynomial + coeff_str + " + "
        else:
            Polynomial = Polynomial + coeff_str + str(" ") + MuldegToMonomial(muldeg) + " + "

    return Polynomial[:-3]

def AlgToDict(Polynomial: str) -> dict:
    ListTerms = Polynomial.split(" + ")
    ListCoeffs = []
    ListMuldegs = []
    P = {}

    # Counting the number of variables involved.
    M = 0
    for Term in ListTerms:
        X = Term.split(" ")
        del X[0]
        for Vari in X:
            VariIndex = int(Vari.split("_")[1].split("^")[0])
            if VariIndex >= M:
                M = VariIndex + 1

    if M == 0:
        Const = ListTerms[0]
        return {
            (0,): complex(Const)
            }
    
    # Saving the coefficients and multidegrees.
    for Term in ListTerms:
        X = Term.split(" ")
        coeff = complex(X[0])
        ListCoeffs.append(coeff)

        del X[0]
        monom = X
        muldeg = MonomialToMuldeg(monom, M)

        P[muldeg] = coeff

    return AscOrder(PA.Normalize(P))

def AlgToDictNonRed(Polynomial : str, M : int) -> dict:
    ListTerms = Polynomial.split(" + ")
    P = {}

    # Counting the number of variables involved.
    N = 0
    for Term in ListTerms:
        X = Term.split(" ")
        del X[0]
        for Vari in X:
            VariIndex = int(Vari.split("_")[1].split("^")[0])
            if VariIndex >= N:
                N = VariIndex + 1            

    if M < N:
        return "Error. Polynomial entered has more variables than expected."
    elif M == N:
        ListCoeffs = []
        ListMuldegs = []

        for Term in ListTerms:
            X = Term.split(" ")
            coeff = complex(X[0])
            ListCoeffs.append(coeff)

            del X[0]
            monom = X
            muldeg = MonomialToMuldeg(monom, M)

            P[muldeg] = coeff

        return PA.Normalize(P)
    else:
        P = AlgToDictNonRed(Polynomial, N)
        items = copy.deepcopy(list(P.items()))
        for i in range(len(items)):
            muldeg, coeff = items[i]
            NewMuldeg = muldeg + tuple(0 for i in range(M - N))
            del P[muldeg]
            P[NewMuldeg] = coeff

        return P
