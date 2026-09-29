# Here, functions to define addition, subtraction and multiplication of polynomials will be written. The function to get the leading multidegree, i.e., the multidegree that is greatest by the lexicographic ordering, will also be given.

eps = 0

# Leading term function. Will return the term in the polynomial which is the greatest by the lexicographic ordering implemented. It will return as a polynomial of one term (called a 'monomial').
def LT(A : dict) -> dict:
    muldeg = max(list(A.keys()))
    return {
        muldeg: A[muldeg]
        }

# Provides the zero polynomial.
def ZeroPoly(Num : int) -> dict:
    return {tuple(0 for i in range(Num)): 0.0j}

# Finds number of maxmimum variables in a given polynomial.
def NumVars(A : dict) -> int:
    return len(list(A.keys())[0])

# Use to make sure zero terms do not appear in nonzero polynomials.
def Normalize(A: dict) -> dict:
    Z = {}
    
    for key, value in A.items():
        val = value
        if abs(value) > eps:
            Z[key] = val

    if Z == {}:
        return ZeroPoly(NumVars(A))
    else:
        return Z

# Polynomial addition.
def PolyAdd(A: dict, B: dict) -> dict:
    Z = A.copy() # Add term from A.  

    # Add terms from B, check which add, which add to zero, and if they add to zero, then remove them.
    for key, value in B.items():
        if key in Z:
            Z[key] = Z[key] + value
        else:
            Z[key] = value

    return Normalize(Z)

# Polynomial multiplication by a 'monomial' - a polynomial with only one term. This function will be used to do general polynomial multiplication.
def PolyMult_minor(A : dict, B : dict) -> dict: # A is the monomial here and B is a general polynomial.
    X, Y = list(A.keys()), list(B.keys())
    Z = {}

    for j in range(len(Y)):
        muldeg = tuple(x + y for x, y in zip(X[0], Y[j]))
        coeff = A[X[0]] * B[Y[j]]
        if abs(coeff) > eps: # This is to handle the boundary case when A or B is the zero polynomial.
            Z[muldeg] = coeff

    if Z == {}:
        M = NumVars(A)
        return ZeroPoly(M)
    else:
        return Normalize(Z)

# Handles the case when multiplying polynomial by a constant to make code-writing efficient. Num can be float, integer, or complex.
def MultbyConst(Num, B : dict) -> dict:
    M = NumVars(B)
    return PolyMult_minor({tuple(0 for i in range(M)): complex(Num)}, B)

# Polynomial subtraction. This will be done adding the negation of the polynomial we are subtracting. In other words, A - B = A + (-B).
def PolySubtract(A : dict, B : dict) -> dict:
    return PolyAdd(A, MultbyConst(-1, B))

# General polynomial multiplication. It will successively use PolyMult_minor and add the results.
def PolyMult(A : dict, B : dict) -> dict:
    Z = ZeroPoly(NumVars(A))
    
    for muldeg, coeff in A.items():
        monomial = {muldeg: coeff}
        Z = PolyAdd(Z, PolyMult_minor(monomial, B))

    return Normalize(Z)

# This function will check whether one monomial (A) divides another monomial (B). This will be used in general polynomial division.
def Divides(A : dict, B : dict) -> bool:
    if Normalize(A) == ZeroPoly(NumVars(A)):
        return True
    
    muldegA, muldegB = list(A.keys())[0], list(B.keys())[0] # Since A and B are both monomials, there is only one multi-degree.
    muldegA, muldegB = list(muldegA), list(muldegB) # We convert them into lists from tuples for easier use.

    i = 0
    while i < len(muldegA):
        if muldegA[i] > muldegB[i]:
            return False
        else:
            i = i+1

    return True

# This function will be used in general polynomial division and calculating S-polynomials in the code. We assume the input is sensible; that B does divide A.
def DivbyMonomial(A : dict, B : dict) -> dict: # We assume here A is a general polynomial and B is a monomial. We are doing A/B here.

    if len(list(A.keys())) == 1: # Checks if A is a monomial
        muldegA, coeffA, muldegB, coeffB = list(A.keys())[0], list(A.values())[0], list(B.keys())[0], list(B.values())[0]

        coeffResult = coeffA / coeffB
        muldegResult = tuple(x - y for x, y in zip(muldegA, muldegB))
        return Normalize({muldegResult: coeffResult})
    
    Z = ZeroPoly(NumVars(A))
    for key, value in A.items():
        Z = PolyAdd(Z, DivbyMonomial({key: value}, B))

    return Normalize(Z)

# The following function will be used directly to calculate S-polynomials.
# LCM of two monomials A and B of coefficient 1.0.
def PolyLCM(A : dict, B : dict) -> dict:
    X, Y = list(A.keys())[0], list(B.keys())[0]
    return {tuple(max(x, y) for x, y in zip(X, Y)): 1.0}

def round_complex(z : complex, dec : int) -> complex:
    real_part = round(z.real, dec)
    imag_part = round(z.imag, dec)
    return complex(real_part, imag_part)

def RoundPoly(A : dict, dec : int) -> dict:
    for muldeg, coeff in A.items():
        if abs(coeff.imag) <= eps:
            coeff = round(coeff.real, dec)
            A[muldeg] = coeff
        else:
            coeff = round_complex(coeff, dec)
            A[muldeg] = coeff

    return A
