from collections import defaultdict
import copy
from random import choices
from string import ascii_lowercase
import random
from random import randint
import time

n=0


'''
In this notebook we implement two algoritms AC3,AC4, to achieve arch consistently
in a given a Constraint satisfaction problem(CSP).
Achieving arch consistency of CSP by applying an algorithms means that from a given
CSP P the algorithms will return a CSP P' such that P and P' are equivalent and P'
is arch consistent. 

The first basic algorithm to achieve arch consistency of CSP is AC1, but it could
be very inefficient since it have  a complexity in the worst case of O(a^3ne). 
This is due to the fact that the removal of any value from any domain would cause
all the elements of Q to be re-examined.

The main improvement made by AC3 is to examine only those binary-constraints which
 could be affected by the removal of values.
First AC3  create a queue Q containing each binary-constraints to be exterminated.
Then iterate over Q examining each binary-constraints with the function Revise 
(csp,x,y) that remove a value v from the domain of the variable X which do not have
compatible values in the domain of Y, if this happen all binary-constraints that 
contain the variable X has to be reexamined, then they are put back in the queue Q.
Since the length of Q is 2e (where e is the number of edges in the constraint graph),
in the worst case, Revise delete only one values from a domain, then 2*e*a 
(where a is the maximum domain size) will be re-examined, and on each call of revise
a^2 pairs of label are examined, the the upper bound of time complexity is O(a^3e)




def parse_neighbors(neighbors, variables=None):
    """Convert a string of the form 'X: Y Z; Y: Z' into a dict mapping
    regions to neighbors. The syntax is a region name followed by a ':'
    followed by zero or more region names, followed by ';', repeated for
    each region name. If you say 'X: Y' you don't need 'Y: X'.
    >>> parse_neighbors('X: Y Z; Y: Z') == {'Y': ['X', 'Z'], 'X': ['Y', 'Z'], 'Z': ['X', 'Y']}
    True
    """
    dic = defaultdict(list)
    for A,A_neibourg in neighbors.items():
        for B in A_neibourg:
            dic[A].append(B)
            dic[B].append(A)
    return dic
'''

class csp():
    '''Create a Constraint satisfaction problem object, composed by 
    a set of variable, a domain set for each variable, a set of neighbors for each variable,
    and a constraint function.
    The constraint function take in input two variable and two value, it return True if the combination
    satisfy the constrain, false otherwise.
    '''
    def __init__(self, variables, domains, neighbors, constraints):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        variables = variables or list(domains.keys())

        self.variables = copy.deepcopy(variables)
        self.domains = copy.deepcopy(domains)
        self.neighbors = self.parse_neighbors(copy.deepcopy(neighbors))
        self.constraints = constraints

    def delete(self, var, value):
        self.domains[var].remove(value)


    def parse_neighbors(self, neighbors):
        """Convert a string of the form 'X: Y Z; Y: Z' into a dict mapping
        regions to neighbors. The syntax is a region name followed by a ':'
        followed by zero or more region names, followed by ';', repeated for
        each region name. If you say 'X: Y' you don't need 'Y: X'.
        >>> parse_neighbors('X: Y Z; Y: Z') == {'Y': ['X', 'Z'], 'X': ['Y', 'Z'], 'Z': ['X', 'Y']}
        True
        """
        print(neighbors)
        dic = defaultdict(list)
        for A,A_neibourg in neighbors.items():
            for B in A_neibourg:
                dic[A].append(B)
                dic[B].append(A)
        return dic


def revise(csp, Xi, Xj):
    ''' The revise function take in input the csp problem and two variable. For each value in the domain
    of Xi it check that there is at least on value x in the domain of Yi that satisfy a constraint, if not
    it delete the value x from the domain of X. In at least one value from a domain is removed, the fiction
     return True, False otherwise
    '''
    revised = False
    satisfied=False
    global n

    for x in csp.domains[Xi][:]:
        for y in csp.domains[Xj]:
            n=n+1
            if(csp.constraints(Xi, x, Xj, y)):
                satisfied=True
                
        if(not satisfied):
            csp.delete(Xi, x)
            revised = True
        #if all(not csp.constraints(Xi, x, Xj, y) for y in csp.domains[Xj]):
        #   csp.delete(Xi, x)
        #   revised = True
    return revised




def ac3(csp):
    '''The function ac3 take in input a CSP problem, and it change directly it in a arch consistent CSP
    and return True. If this is not possible it return False.
    '''
    global n
    n=0
    #make the queue of arch in the graph
    queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]

    #untill there is no costraint to check
    while(queue):
        (Xi, Xj) = queue.pop()
        if revise(csp,Xi,Xj):
            if not csp.domains[Xi]:
                print(n)
                return False
                #in case a value is removed from the domain of Xi, all his neighbors must be checked.
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))

    print(n)
    n=0
    return True

'''
Further improvement can be made on the AC3 algorithm decreasing his time 
complexity. This algorithm is called AC4.
The main improvement of AC4 with respect to AC3 is that when a value v is
 removed from the domain of the
variable X (inside the revise function), it is not always necessary to 
examine all the binary constraints where correlated to the variable X. 
Precisely  we do not have to examine those value u that do not rely on v 
for support. Where for support we mean the compatible value in the domain 
of every other variable.

To identify the relevant label to be re-examined, AC4 need 3 specific data 
structure:
S, the support set, that memorize for each variable the variable-value pairs
 that it supports.
C, the table of counter, strictly correlated with S that count the the number
 of support that each label receives from each binary-constraint for the 
 subject variable
M, a Boolean matrix, full of zero at the beginning and where with one are 
marked the labels that have been rejected.
'''

def ac4(csp):
    global n
    n=0

    #get all the arch
    queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]

    List = []
    #create a the support dictonary of dictionary of list
    S = {}
    for var in csp.variables:
        S[var]={}
        for lab in csp.domains[var][:]:
            S[var][lab]=[]
    #create the matrix M
    M = {}
    for var in csp.variables:
        M[var]={}
        for lab in csp.domains[var][:]:
            M[var][lab]=0

    #create counter for support
    counter = {}
    for var1 in csp.variables:
        counter[var1]={}
        for var2 in csp.variables:
            counter[var1][var2]={}
            for lab in csp.domains[var1][:]:
                counter[var1][var2][lab]=0



    while(queue):
        
        (Xi, Xj) = queue.pop()

        for b in csp.domains[Xi][:]:
            total=0
            for c in csp.domains[Xj][:]:
                n=n+1
                #if Xi,b give satisfy the costrain with Xj, c add it to the support of Xj,b
                if (csp.constraints(Xi, b, Xj, c)):
                    total=total+1
                    S[Xj][c].append((Xi,b))
            #if Xi, b do not have any value that support it, delete it from the domain of Xi
            #and append in the List to be re-examinet Xi,b.
            if (total==0):
                csp.delete(Xi, b)
                M[Xi][b]=1
                List.append((Xi,b))
            else:
                counter[Xi][Xj][b]=total


    while(List):
        (Yi, y) = List.pop()
        for (Xi,x) in S[Yi][y]:
            n=n+1
            if (x in csp.domains[Xi]) :
                counter[Xi][Yi][x]=counter[Xi][Yi][x]-1
                #if x has not support from other variable, and is still on the domain of Xi
                #delete x from the domain of Xi, and put it on the list, such that the 
                #variable-value pairs that have it as support can be re-examinated.
                if ((counter[Xi][Yi][x]==0 ) and (M[Xi][x]==0)):
                    List.append((Xi,x))
                    csp.delete(Xi,x)
                    M[Xi][x]==1

    print(n)
    n=0
######################################################################################################################################



'''
#easy example
neighbors =  {'A': ['B'], 'B': ['A']}
domains = {'A': [0, 1, 2, 3, 4], 'B': [0, 1, 4, 9, 10]}
constraints = lambda X, x, Y, y: x % 2 == 0 and (x + y) == 4 and y % 2 != 0
constraints = lambda X, x, Y, y: (x % 2) == 0 and (x + y) == 4

def x_Y(X,x,Y,y):
    if(Y=='B'):
        if(y==x**2):
            return True
        else:
            return False
    else:
        if(y==x**(1/2)):
            return True
        else:
            return False
constraints= x_Y

'''
if(False):
    #australia color map problem
    neighbors =  {'WA': ['NT','SA'], 'NT': ['Q','SA'], 'SA': ['Q','NSW','V'], 'Q': ['NSW'], 'NSW': ['V'], 'V': [], 'T': []}
    domains =  {'WA': [1,2,3], 'NT': [1,2,3], 'SA': [1,2,3], 'Q': [1,2,3], 'NSW': [1,2,3], 'V': [1,2,3], 'T': [1,2,3]}
    constraints = lambda X, x, Y, y: x != y 
else:

    number_of_node = 40
    number_of_edge = 10
    max_domain = 70
    neighbors ={}
    domains={}
    constraints = lambda X, x, Y, y: x != y 

    nodes = ["".join(choices(ascii_lowercase, k=3)) for _ in range(number_of_node)]
    domains_value = [i for i in range(0,max_domain) ]

    for node in nodes:
        temp_list = list(nodes)
        temp_list.remove(node)
        random_neighbors = random.sample(temp_list, number_of_edge)
        

        neighbors[node] = random_neighbors
        domains[node] = random.sample(domains_value, randint(1,max_domain))


csp = csp(variables=None, domains=domains, neighbors=neighbors, constraints=constraints)
#print(domains)
#print(neighbors)

csp1= copy.deepcopy(csp)
csp2= copy.deepcopy(csp)


start_time = time.time()
print(ac3(csp1))
#print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
ac4(csp2)
#print("--- %s seconds ---" % (time.time() - start_time))


