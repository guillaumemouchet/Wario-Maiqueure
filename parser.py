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
    p[0] = AST.BlockNode(p[1], p[3])

def p_listP(p):
    ''' listP : expression 
                | expression ',' listP '''   
    try:
        p[0] = [p[1]]+p[3]
    except:
        p[0] = [p[1]]


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
    
def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])

def p_error(p):
    print ("Syntax error in line %d" % p.lineno)
    yacc.errok()

def parse(prog):    
	return yacc.parse(prog)

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)


yacc.yacc(outputdir='generated')

@addToClass(AST.Node)
def thread(self, lastNode):
    for c in self.children:
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)
    return self

@addToClass(AST.WhileNode)
def thread(self, lastNode):
    mem = lastNode

    lastNode = self.children[0].thread(lastNode)
    lastNode.addNext(self)
    lastNode = self.children[1].thread(self)

    lastNode.addNext(mem.next[-1])
    return self


def thread(tree):
    entry = AST.EntryNode()
    tree.thread(entry)
    return entry


if __name__ == "__main__":
    from parser import parse
    import os, sys
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    entry = thread(ast)

    os.environ["PATH"] += os.pathsep + \
        'C:\\Program Files (x86)\\Graphviz2.38\\bin\\'
    graph = ast.makegraphicaltree()
    entry.threadTree(graph)
    name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
    graph.write_pdf(name)
    print("wrote ast to ", name)