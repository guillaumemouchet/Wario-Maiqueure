import ply.yacc as yacc
from lex import tokens
import AST
from AST import addToClass

operations = {
    "+" : lambda x, y : x + y,
    "-" : lambda x, y : x - y,
    "*" : lambda x, y : x * y,
    "/" : lambda x, y : x / y
}

vals = {}

def p_programme(p):
    '''programme : statement
                    | statement ';' programme'''
    try:
        p[0] = AST.ProgramNode([p[1]]+p[3].children)
    except:
        p[0] = AST.ProgramNode(p[1])

def p_statement(p):
    '''statement : assignement
                | while
                | block '''
    p[0] = p[1]

def p_assignement(p):
    ''' assignement : IDENTIFIER '=' expression'''
    vals[p[1]] = p[3]
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_while(p):
    ''' while : WHILE expression '{' programme '}' '''
    p[0] = AST.WhileNode([p[2],p[4]])

def p_block(p):
    ''' block : BLOCKNAME '(' listP ')' '''
    p[0] = AST.BlockNode(p[1], AST.ListPNode(p[3]))

def p_listP(p):
    ''' listP : expression
                | expression ',' listP '''
    try:
        p[0] = AST.ListPNode([p[1]]+p[3].children) #changer AST
    except:
        p[0] = AST.ListPNode(p[1])  #changer AST
        #p[0] = p[1] ?
def p_expression_num_or_var(p):
    '''expression : NUMBER 
                | IDENTIFIER''' 
    p[0] = AST.TokenNode(p[1])

def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]

def p_expression_op(p):
    '''expression : expression ADD_OP expression 
                | expression MUL_OP expression '''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_error(p):
    print ("Syntax error in line %d" % p.lineno)
    yacc.errok()

def parse(prog):
	return yacc.parse(prog)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
	import sys 
	import os
	
	prog = open(sys.argv[1]).read()
	result = yacc.parse(prog)
	print (result)

	os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
	graph = result.makegraphicaltree()
	name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
	graph.write_pdf(name)
	print("wrote ast to ", name)