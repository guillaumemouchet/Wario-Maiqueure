# coding=utf-8
import AST
from AST import addToClass
import shutil

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
	rotation = int(rotation)
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
			return [-0.7071068,0.7071068,270]
		case _:
			print("------> Not found")
			return [1,0,0]




            
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

vars = {}

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
		try:
			bytecode += str(vars[self.tok])
		except:
			bytecode += "ERROR IN TOKEN NODE"
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
	try:
		vars.update({self.children[0].tok : int(self.children[1].tok)})
	except:
		vars.update({self.children[0].tok : int(self.children[1].compile())})
	#return str(self.children[1].tok)
	#print("clé:", self.children[0].tok)
	#print("valeur:", self.children[1].tok)

	return ""
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
		bytecode = str(operations[self.op](0, self.children[0].tok))
		#else raise erreur
	else:
		print("self.children[0].tok", self.children[0].tok)
		print("self.children[1].tok",self.children[1].tok)
		try:
			a = int(self.children[0].tok)
			b = int(self.children[1].tok)
		except:
			a = int(vars.get(self.children[0].tok))
			b = int(self.children[1].tok)
		print("opnode values",a,b)
		res = str(operations[self.op](a, b))
		bytecode += res
	return bytecode

# Create block in format NAME(x,y,rot)
@addToClass(AST.BlockNode)
def compile(self):
	global block_id
	offsety = 0
	offsetx = 0.5
	AAAAA = block_id
	BBBBB = block_id + 1
 
	if self.name == "BRICK":
		offsety = 0.5
	
	XXXXX = int(self.children[0].compile()) + offsetx
	YYYYY = int(self.children[1].compile()) + offsety
	try:
		RRRRR = self.children[2].compile()
	except:
		RRRRR = 0
   	
	WWWWW, ZZZZZ, RRRRR = rotationToUnity(RRRRR)

	list_id_terrain.append(AAAAA)

	fileName = self.name
 
	source = "./prefabs/"+ fileName + ".txt"
	destination = "./result/"+ fileName + str(AAAAA) + ".txt"
	shutil.copyfile(source, destination)
	with open(destination, 'r') as file:
		data = file.read()
		data = data.replace("AAAAA", str(AAAAA))
		data = data.replace("BBBBB", str(BBBBB))
		data = data.replace("XXXXX", str(XXXXX))
		data = data.replace("YYYYY", str(YYYYY))
		data = data.replace("WWWWW", str(WWWWW))
		data = data.replace("ZZZZZ", str(ZZZZZ))
		data = data.replace("RRRRR", str(RRRRR))

	with open(destination, 'w') as file:
	
		# Writing the replaced data in our
		# text file
		file.write(data)
  
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
    
    
	block_id +=2
	return bytecode
    
	
# noeud de boucle while
# saute au label de la condition défini plus bas
# insère le label puis le corps du body
# insère le label puis le corps de la condition
# réalise un saut conditionnel sur le résultat de la condition (empilé)
@addToClass(AST.WhileNode)
def compile(self):
	print("While node 1 ", self.children)
	print("While node 2 ",self.children[1].compile())
	print("While node 3", self.children[0].compile())
	counter = whilecounter()
	
	bytecode = ""
	print("While counter", counter)
	
	while (int(self.children[0].compile())<=0):
		bytecode += str(self.children[1].compile())
	return bytecode

def terrain_middle():
	fileName = "TERRAIN_MIDDLE"
	source = "./prefabs/"+ fileName + ".txt"	

	destination = "./result/"+ fileName + "_Modified.txt"
  
	#Create Terrain Middle
	open(destination, 'x')
 
	with open(source, 'r') as file:
		data = file.read()

	for item in list_id_terrain:
		datalocal = data
		datalocal = datalocal.replace("AAAAA", str(item))
  
		with open(destination, 'a') as file:
			file.write(datalocal+"\n")
   
def start_of_exec():
    #Remove old result files
	directories = os.listdir("./result/")

	for file in directories:
		print(file)
		os.remove("./result/"+file)
  
def end_of_exec():
	terrain_middle()
	# Fuse all and name it Projet Compilateur.unity 

	HEADER = "./prefabs/HEADER.txt"
	TERRAIN_HEADER = "./prefabs/TERRAIN_HEADER.txt"
	TERRAIN_MIDDLE_Modified = "./result/TERRAIN_MIDDLE_Modified.txt"
	TERRAIN_FOOTER = "./prefabs/TERRAIN_FOOTER.txt"
 
	# Get all Brick and Spike files created
	name_of_files = []
	directories = os.listdir("./result/")
	for file in directories:
		if(file != "TERRAIN_MIDDLE_Modified.txt"):
			name_of_files.append(file)
   
	FOOTER = "./prefabs/FOOTER.txt"
 
	# Create final File
	project = "./Coding in Flow 2D Project/Assets/Scenes/Projet Compilateur.unity"
	if os.path.exists(project):
		os.remove(project)
    
	open(project, 'x')
 
 
	# Read all the files
	with open(HEADER, 'r') as file:
		header_data = file.read()
  
	with open(TERRAIN_HEADER, 'r') as file:
		terrain_header_data = file.read()
   
	with open(TERRAIN_MIDDLE_Modified, 'r') as file:
		terrain_middle_data = file.read()
   
	with open(TERRAIN_FOOTER, 'r') as file:
		terrain_footer_data = file.read()
   
	content_of_file = []
	for nameFile in name_of_files:
		with open("./result/"+nameFile, 'r') as file:
			content_of_file.append(file.read())

	with open(FOOTER, 'r') as file:
		footer_data = file.read()
   
   
   # Append all the files to the new one
	with open(project, 'a') as file:

			file.write(header_data+"\n")
			file.write(terrain_header_data+"\n")

			file.write(terrain_middle_data+"\n")

			file.write(terrain_footer_data+"\n")

			for content in content_of_file:
				file.write(content+"\n")
			file.write(footer_data+"\n")
   
   	# Add Manually the result to the unity project
	print("Projet Compilateur.unity Created succesfully, please reload project in Unity")

	

	

if __name__ == "__main__":
    from parser import parse
    import sys, os
    start_of_exec()
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    print(ast)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0]+'.vm'    
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print ("Wrote output to", name)
    end_of_exec()
