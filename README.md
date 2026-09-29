# Simultaneous-polynomial-solver-in-many-variables
Whenever I code, I like to code mathematics; I like to bring mathematics to life. When I was first learning Python in Feb 2026, I had two months prior learnt about solving multivariable polynomial equations through section 9.6 in Dummit and Foote edition 3. I thought why not try to write a Python project at this it would be very fun.

To understand what terms like "Grobner bases", "Buchberger's algorithm", and "lexicographic ordering" mean you need knowledge about quite a few technical things. As stated above, I was learning these through section 9.6 of Dummit and Foote titled: "Polynomials in several variables over a field and Grobner bases". It would be optimal if you have read this exact book and section, but even if you do not want to get into the weeds of Ring theory and Algebraic Geometry, you can still use solving systems of polynomials (the option 2 in the menu shown when running Main), but you must still understand what a lexicographic ordering is which I explain next.

As also stated above, this was my earliest (large) Python project. Aside from a python file doing integer GCD/LCM, this is my first Python project, and so I learnt as I was doing this. That is why you will find "beginner footprints" all over. In fact, I was set out on coding my own polynomial solver which is when I realized numpy exists and used that. 

Nevertheless, I kept this in my computer after months and months on end. Today, I thought why not I publish this on my GitHub maybe someone will find it worthwhile which would be amazing. There are many improvements too which I have not done because to me it was technically complete even for any practical purposes of myself. I talk about potential improvement avenues if you are interested at the end of this README file.

## Lexicographic ordering

An ordering is any way to sort a collection of elements so that recalling them or using them is convenient.

Have you ever seen how a dictionary is indexed? If you go in the section for A you will find that all words that begin with A are not randomly jumbled. Just like how at the "global" layer of the dictionary, all words are ordered from A to Z, inside one particular letter, words are ordered A-Z again. So that a word starting with "Aa" comes before a word starting with "Ab" and likewise continuing down the string, a word starting with "Aaa" (if it existed in the English language) would be ordered before a word starting with "Aab". This is called the "Lexicographic ordering" or also called the "Dictionary ordering". 

What that means is that we begin with an initial rule "A must come before B which must come before C and on and on until Z". We can denote this through inequality signs because the character coming before gets priority over a character coming after, so $A>B, A>N, X>Y>Z, A>B>C>\cdots>Y>Z$. But what if we have a string with two letters/characters? Consider "AB" and "BA". We want to order them. Well, we look at the first character in the string: "A" and "B". We know that $A>B$, and thus $AB>BA$. It did not matter that the second characters were $B<A$, the first characters got priority and determined the ordering. Just like how in a dictionary "Abacus" would come before "Baseball". Consider now "ABC" and "AA". The first characters are "A" and "A" which are the same, so we have no determinable ordering between the two. So, if the first characters are the same, we move to the second "B" and "A". Well, "A>B", so since we now have a definite rule, our work stops and we obtain $AA>ABC$, even if the character lengths are different.

Now, recall polynomials in multiple variables. Think of the variables as strings, so a term $x^2y^3z$ as a string would be "xxyyyz". Think of a polynomial as a finite sum of strings like these (with a coefficient). In one variable, say x, we have a natural ordering: $x^n>x^m$ iff $n>m$, but there is no natural way to order polynomials in multiple variables that is also useful for defining a (general) polynomial division algorithm, which requires a monotonous term. So, just like a dictionary, we may impose initial ordering $x>y>z$. With this, we can compare with is greater or has the highest priority between say two monomial terms $2x^2y^3z$ and $3.14y^9z^5$ using the lexicographic ordering. Since $x>y$, it follows that $2x^2y^3z>3.14y^9z^5$ by comparing the first string characters, even though $2<3.14$ (which is completely irrelevant here). This can be systematized to comparing multi-degrees, so the multidegree of $2x^2y^3z$ would be the coordinate (2, 3, 1) and for the second one would be (0, 9, 5). We compare the first coordinate $2>0$, so the first monomial is greater, even though the succeeding coordinates are far greater. If you know set theory and/or algebra, you will realize comparing indices/powers of terms this way is equivalent to using a lexicographic ordering on $(N_0^n, \leq)$. It does not have to be this particular ordering, it can be $y>x>z$ or $z>y>x$, which will affect how you will write the monomial terms and which will be leading term.

This ordering is important because it allows us to define a leading term of a polynomial because it allows to define the general polynomial division algorithm which is an extension of the polynomial long division one learns in high school/A levels.

## How to use this solver.

This program does four tasks but it is mainly for solving simultaneous polynomial equations. For example, solving:

$$\begin{aligned} 
x^2 + 10xy + 25y^2 &= 100 \\ 
y^3 - 13y^2z - 64yz^2 + 23 &= 33 \\ 
z^2 - 10 &= 0 
\end{aligned}$$

However, we do not input like this. We index the variables $x, y, z$ as `x_0`, `x_1`, `x_2`, and on this basis, a lexicographic ordering will be implemented, with `x_0` greatest. 
So, variables are written/indexed as 

`x_0`, `x_1`, `x_2`, `x_3`,..., 

and again `x_0` is greatest in the ordering. This ordering will be used to solve the system. 

The system of equations will be input so that the right hand side of the equation is 0. For example, the first one will therefore be input as

`x_0^2 + 10 x_0 x_1 + 25 x_1^2 + -100`, 

if `x_0 = x, x_1 = y, x_2 = z`. 

Make sure that in each term, the smaller x index is written left of bigger ones. So, `x_1 x_2` not `x_2 x_1`, and `x_0 x_1` not `x_1 x_0`.

The program will take the polynomial as a string and perform operations on it to extract necessary information. For that, a format will be followed for inputting polynomials. 

Each term will be separated by `" + "` (a plus sign surrounded by spaces). Notice how it is written ` + -100`, not ` - 100`. For each term, instead of writing the variables and coefficients together, we separate them for ease and readability by a single space `“ “`. So, take 
`10 x_0 x_1`. Notice the spaces. In contrast, `10x_0x_1` will not be valid and cause errors and malfunction. For another example, in equation 2, the term $-13y^2z$ will be input as

`-13 x_1^2 x_2`.

In this repository there is a test file which was a large scale testing I did testing everything of this solver in PowerShell and I believe it shows all the capabilities of the program and I would actually recommend seeing it since it gives an idea of what types of outputs are possible.

## Potential improvements

This is a list of things I have thought and an AI has recommended me over months and months. 

New avenues.
1. Lexicographic ordering is only one type of ordering in computational algebra. From what I have seen, there is also something called "GrevLex", and I even saw it in the exercises of Dummit and Foote but I cared not to do them, so I do not know how that works. Even if I knew, I would not have implemented it. This I have heard would improve the elimination of ideals. If you do write this, I might not be able to understand the code behind it, unless I learnt the theory, but I would love to hear if it did improve efficiency.
2. I used NumPy. Why not try SymPy? That is a big regret, because if I had chosen that, I would not have to make so many "short-circuit texts" where the user checked for floating point errors. I elected to continue with NumPy nevertheless because using a module just did not feel that satisfying.

Polishing.
1. The input, interpreting, and outputting is very very clunky. You have to follow the rules established on how to input word to word or it will crash completely. You can improve this by improving how the program receives inputs and creating flexibility.
2. Remove the beginner footprints. Change, for example, range(len(...)) to something of your choice which would be more efficient.
3. I remember in one of my very very earlier testing there was this polynomial system I was trying to solve, it took forever and did not give an output. I think I had gone and fixed the issue, but I am not certain if I did. I think the number of variables (M) was either 3 or 4, but I have solved many systems since then, including my test log file, and I do not think I have encountered that error again.
4. Keep testing to find new bugs and if you want try to fix them!

## Final note

I wont be so active on this repository. This was more an artistic endeavour that for my I am not so passionate anymore. So, I might not actively read or reply on this repository, that is why you are free to use it if you find utility in it. Thanks!
