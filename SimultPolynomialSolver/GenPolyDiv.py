# This is the implementation of the general polynomial division for multiple variables. The list P will be the system of polynomials that will be entered.

from SimultPolynomialSolver import PolynomialArithmetic as PA
import copy

IsTask3 = False

def GenPolyDiv(A : dict, P : list[dict]) -> (list[dict], dict):
    F = copy.deepcopy(A)           # These F and Div are to make sure A and P remain unchanged.
    Div = copy.deepcopy(P)         # Div stands for (list of) divisors.
    M = PA.NumVars(F)

    Quot, Rem = [PA.ZeroPoly(M) for _ in range(len(Div))], PA.ZeroPoly(M) # Quotient set and Reaminder.

    while PA.Normalize(F) != PA.ZeroPoly(M):
        i = 0
        while i < len(Div):
            divisor = Div[i]

            if PA.Divides(PA.LT(divisor), PA.LT(F)):
                quotient = PA.DivbyMonomial(PA.LT(F), PA.LT(divisor))
                Quot[i] = PA.PolyAdd(Quot[i], quotient)
                F = PA.PolySubtract(F, PA.PolyMult_minor(quotient, divisor))
                break
            else:
                i = i+1

        if i == len(Div):
            LeadingTerm = PA.LT(F)
            Rem = PA.PolyAdd(Rem, LeadingTerm)
            F = PA.PolySubtract(F, LeadingTerm)

    if IsTask3:
        dec = int(input("Enter number of decimal places to approximate result's coefficients to: "))
        Rem = PA.RoundPoly(Rem, dec)
        QuotCopy = copy.deepcopy(Quot)
        for i in range(len(Quot)):
            quotient = QuotCopy[i]
            Quot[i] = PA.RoundPoly(quotient, dec)

    return (Quot, Rem)

