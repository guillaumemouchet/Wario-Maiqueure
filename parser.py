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
    pass

def p_statement(p):
    '''statement : assignement
                | while
                | block '''
    pass

def p_assignement(p):
    ''' assignement : IDENTIFIER '=' expression'''
    pass

def p_while(p):
    ''' while : WHILE expression '{' programme '}' '''
    pass

def p_block(p):
    ''' block : BLOCKNAME '(' listP ')' '''
    pass

def p_listP(p):
    ''' listP : expression
                | expression ',' listP '''
    pass

def p_expression_num_or_var(p):
    '''expression : NUMBER 
                | IDENTIFIER'''
    pass

def p_expression_paren(p):
    '''epxression : '(' expression ')' '''
    pass

def p_expression_op(p):
    '''expression : expression OP expression 
                | expression MUL_OP expression '''
    pass

