

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
	arch = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]

	Q = 0
	S = {}
	

	#for each arch or from another point of view for each possible costrain
	while(queue):
		
		(Xi, Xj) = queue.pop()

		for b in csp.domains[Xi][:]:
			total = 0
			for c in csp.domains[Yi][:]:
				if (csp.constraints(Xi, b, Xj, c)):
					#increment counter(vi, ai, vj) and add (vi, ai) to S[vj, aj]
					total = total + 1
					s[Xj][c].append((Xi,x))



######################################################################################################################################
'''
neighbors =  {'A': ['B'], 'B': ['A']}
domains = {'A': [0, 1, 2, 3, 4], 'B': [0, 1, 2, 3, 4]}
constraints = lambda X, x, Y, y: x % 2 == 0 and (x + y) == 4 and y % 2 != 0
constraints = lambda X, x, Y, y: (x % 2) == 0 and (x + y) == 4


csp = csp(variables=None, domains=domains, neighbors=neighbors, constraints=constraints)

print(ac3(csp))'''