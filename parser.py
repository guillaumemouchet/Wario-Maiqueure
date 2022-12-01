import ply.yacc as yacc
from lex import tokens
import AST
from AST import addToClass

operations = {
    "+" : lambda x, y : x + y,
    "-" : lambda x, y : x - y
}

vals = {}

def p_programme(p):
    '''programme : statement
                    | statement ';' programme'''
    try:
        p[0] = AST.ProgramNode([p[1]+p[3].children])
    except:
        p[0] = AST.ProgramNode(p[1]) 

def p_statement(p):
    '''statement : assignement
                    | structure
                    | PRINT expression'''
    try:
        p[0] = AST.PrintNode(p[2])
    except:
        p[0] = p[1]

def p_structure(p):
    '''structure : WHILE expression '{' programme '}' '''
    p[0] = AST.WhileNode(p[2], p[4])

def p_expression_op(p):
    '''expression : expression ADD_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]

def p_assignement(p):
    ''' assignement : IDENTIFIER '=' expression '''
    vals[p[1]] = p[3]
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])