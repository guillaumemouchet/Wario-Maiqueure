# coding=utf-8
import AST
from AST import addToClass

# opcodes de la SVM
#    PUSHC <val>     pushes the constant <val> on the stack
#    PUSHV <id>      pushes the value of identifier <id> on the stack
#    SET <id>        pops a value from the top of stack and sets <id>
#    PRINT           pops a value from the top of stack and print it
#    ADD,SUB,DIV,MUL pops 2 values from the top of stack and compute them
#    USUB            changes the sign of the number on the top of stack
#    JMP <tag>       jump to :<tag>
#    JIZ,JINZ <tag>  pops a value from the top of stack and jump to :<tag> if (not) zero

# chaque opération correspond à son instruction d'exécution de la machine SVM


# Global id for the blocks, incremented 2 times per blocks
block_id = 1000

#List of first id of each block, to be added in the TERRAIN_MIDDLE.txt file
list_id_terrain = []

'''
return tuple[w,z,r] -> valued defined in ROTATION.txt
'''
def rotationToUnity(rotation:int):
	if(rotation>=360):
		rotation = rotation % 360
  
	match rotation:
		case 0:
			print("------> 0")
			return [1,0,0]
		case 90:
			print("------> 90")
			return [0.7071068,0.7071068,90]
		case 180:
			print("------> 180")
			return [0,1,180]
		case 270:
			print("------> 270")
   #TODO
			return [0.7071068,0.7071068,90]

            
# operations = {
# 	'+' : 'ADD',
# 	'-' : 'SUB',
# 	'*' : 'MUL',
# 	'/' : 'DIV'
# }
operations = {
    "+" : lambda x, y : x + y,
    "-" : lambda x, y : x - y,
    "*" : lambda x, y : x * y,
    "/" : lambda x, y : x / y
}

def whilecounter():
	whilecounter.current += 1
	return whilecounter.current
whilecounter.current = 0

# noeud de programme
# retourne la suite d'opcodes de tous les enfants
@addToClass(AST.ProgramNode)
def compile(self):
	bytecode = ""
	for c in self.children:
		bytecode += c.compile()
	return bytecode

# noeud terminal
# si c'est une variable : empile la valeur de la variable
# si c'est une constante : empile la constante
@addToClass(AST.TokenNode)
def compile(self):
	bytecode = ""
	if isinstance(self.tok, str):
		bytecode += "%s" % self.tok
	else:
		bytecode += "%s" % self.tok
	return bytecode
	
# noeud d'assignation de variable
# exécute le noeud à droite du signe =
# dépile un élément et le met dans ID
@addToClass(AST.AssignNode)
def compile(self):
	# bytecode += self.children[1].compile()
	# bytecode += "SET %s\n" % self.children[0].tok
	return str(self.children[1].tok)
	
# noeud d'affichage
# exécute le noeud qui suit le PRINT
# dépile un élément et l'affiche
@addToClass(AST.PrintNode)
def compile(self):
	bytecode = ""
	bytecode += self.children[0].compile()
	bytecode += "\n"
	return bytecode
	
# noeud d'opération arithmétique
# si c'est une opération unaire (nombre négatif), empile le nombre et l'inverse
# si c'est une opération binaire, empile les enfants puis l'opération
@addToClass(AST.OpNode)
def compile(self):
	bytecode = ""
	if len(self.children) == 1:
		if(self.op == "-" | self.op == "+"):
			bytecode = str(operations[self.op](0, self.children[0].tok))
		#else raise erreur
	else:
		a = self.children[0].tok
		b = self.children[1].tok
		res = str(operations[self.op](a, b))
		bytecode += res
	return bytecode

# Create block in format NAME(x,y,rot)
@addToClass(AST.BlockNode)
def compile(self):
    bytecode = ""
    bytecode += self.name
    bytecode += "("
    bytecode += self.children[0].compile()
    bytecode += ", "
    bytecode += self.children[1].compile()
    bytecode += ", "
    try:
        bytecode += self.children[2].compile()
    except:
        bytecode += "0"
    bytecode += ")\n"
    return bytecode
    
	
# noeud de boucle while
# saute au label de la condition défini plus bas
# insère le label puis le corps du body
# insère le label puis le corps de la condition
# réalise un saut conditionnel sur le résultat de la condition (empilé)
@addToClass(AST.WhileNode)
def compile(self):
	counter = whilecounter()
	bytecode = ""
	bytecode += f"{counter}\n"
	bytecode += f"{counter}: "
	bytecode += self.children[1].compile()
	bytecode += f"{counter}: "
	bytecode += self.children[0].compile()
	bytecode += f"{counter}\n"
	return bytecode
	
if __name__ == "__main__":
    from parser import parse
    import sys, os
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    print(ast)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0]+'.vm'    
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print ("Wrote output to", name)
