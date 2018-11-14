

class csp():
	
	def __init__(self, variables, domains, neighbors, constraints):
		"""Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
		variables = variables or list(domains.keys())

		self.variables = variables
		self.domains = domains
		self.neighbors = neighbors
		self.constraints = constraints

	def delete(self, var, value):
		self.domains[var].remove(value)

def ac3(csp):

	#make the queue of arch in the graph

	queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]

	while(queue):
		(Xi, Xj) = queue.pop()
		if revise(csp,Xi,Xj):
			if not csp.domains[Xi]:
				return False
			for Xk in csp.neighbors[Xi]:
				if Xk != Xj:
					queue.append((Xk, Xi))

	for Xi in csp.variables:
		print(Xi)
		for x in csp.domains[Xi][:]:
			print("      "+str(x))

	return True



def revise(csp, Xi, Xj):

	revided = False

	for x in csp.domains[Xi][:]:
		# If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
		if all(not csp.constraints(Xi, x, Xj, y) for y in csp.domains[Xj]):
			csp.delete(Xi, x)
			revised = True
	return revised

from collections import defaultdict



def different_values_constraint(A, a, B, b):
	return a != b

#######################################################################################



def ac4(csp):

	#get all the arch
	queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]

	List = []
	#create a the support dictonary of dictionary of list
	S = {}
	for var in csp.variables:
		S[var]={}
		for lab in csp.domains[var][:]:
			S[var][lab]=[]

	#create counter
	counter = {}
	for var1 in csp.variables:
		counter[var1]={}
		for var2 in csp.variables:
			counter[var1][var2]={}
			for lab in csp.domains[var1][:]:
				counter[var1][var2][lab]=0



	#for each arch or from another point of view for each possible costrain
	while(queue):
		
		(Xi, Xj) = queue.pop()

		for b in csp.domains[Xi][:]:
			for c in csp.domains[Xj][:]:
				if (csp.constraints(Xi, b, Xj, c)):
					#increment counter(vi, ai, vj) and add (vi, ai) to S[vj, aj]
					counter[Xi][Xj][b]=counter[Xi][Xj][b]+1
					S[Xj][c].append((Xi,b))
			if (counter[Xi][Xj][b]==0):
				List.append((Xi,b))
				csp.delete(Xi, b)


	while(List):
		(Yi, y) = List.pop()

		for (Xi,x) in S[Yi][y]:
			if (x in csp.domains[Xi]) :
				counter[Xi][Yi][y]=counter[Xi][Yi][y]-1
				List.append((Xi,x))
				csp.delete(Xi,x)



######################################################################################################################################

neighbors =  {'A': ['B'], 'B': ['A']}
domains = {'A': [0, 1, 2, 3, 4], 'B': [0, 1, 2, 3, 4]}
constraints = lambda X, x, Y, y: x % 2 == 0 and (x + y) == 4 and y % 2 != 0
constraints = lambda X, x, Y, y: (x % 2) == 0 and (x + y) == 4


csp = csp(variables=None, domains=domains, neighbors=neighbors, constraints=constraints)


print(ac4(csp))

for Xi in csp.variables:
	print(Xi)
	for x in csp.domains[Xi][:]:
		print("      "+str(x))