import re

class tree:
	def __init__(self, label, children = None):
		self.label = label
		self.children = children if children is not None else []

	def __str__(self):
		return self.strHelper() + ";"

	def strHelper(self):
		if not self.children:
			return self.label
		newick_string = "("
		for index, child in enumerate(self.children, 1): #starting at 1 saves an add operation per loop
			if index != len(self.children):
				newick_string += child.strHelper() + ","
			else:
				newick_string += child.strHelper()
		newick_string += ")" + self.label
		return newick_string

	def __repr__(self):
		return "Tree: " + str(self)

	def __len__(self):
		count = 1
		for node in self.children:
			count += len(node)
		return count

	def isLeaf(self):
		return len(self.children) == 0



class ParserException(Exception):
	"""
	Exception class for parse_newick
	"""
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return self.msg

# ts is the token stream - in this case just a string and the lexar is yielding 1 char at a time
def lexer(ts):
	for char in re.sub("\s+", "", ts):
		yield char
	yield "$" # End of Input char - states EOI

# Parse_newick Should raise the following ParserException errors when appropriate:
# * Terminating semi-colon missing.
# * Expected label missing.
# * Missing command or ) where expected.
# (You may add others as you see fit.)
#
# Spacing should not matter: "(a,b)c;", and " ( a  ,  b ) c; " should result in idential
# trees.
# terminal set: a-zA-Z0-9,)(;
def parse_newick(ts):
	"""
	Take a newick string and return the corresponding tree object.
	"""
	token_gen = lexer(ts)
	try:
		current, t = T(next(token_gen), token_gen)
		if current != "$":
			raise ParserException("Symbols after terminating semicolon.")
		return t
	except ParserException as pe:
		return pe.msg

def T(current, token_gen):
	current, t = S(current, token_gen)
	if current == ";":
		return next(token_gen), t
	else:
		raise ParserException("Terminating semicolon missing.")

def S(current, token_gen):
	if re.match("\w+", current):
		label = current
		while True:
			current = next(token_gen)
			if re.match("\w+", current):
				label += current
			else:
				return current, tree(label)

	elif current == "(":
		current, children = SPrime(next(token_gen), token_gen)
		if current != ")":
			raise ParserException("Missing closing ')'.")

	else:
		raise ParserException("Invalid token - Missing label or token not in terminal set")

	return S(next(token_gen), token_gen)

def SPrime(current, token_gen):
	stree = tree("sprime")
	if current == ")":
		return current, stree

	while True:
		current, t = S(current, token_gen)
		stree.children.append(t)
		if current != ",":
			break
		current = next(token_gen)

	return current, stree


