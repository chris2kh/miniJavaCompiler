#!/usr/bin/python
# -*- coding: utf-8 -*-
import ply.lex as lex
import ply.yacc as yacc
from lexicalAnalyzer import tokens
from ast import *


#  Tokens I can dismiss when I am ready to build the abstract syntax tree
notRelevantCharacters = [',','[',']','{','}','(',')',';','.']

# function that will be used to create the abstract syntax tree nodes in every production
def capture(p, category):
  children = []
  
  for child in p[1:]:
    if child not in notRelevantCharacters:
      children.append(child)
  p[0] = Node(children, category)

precedence =(
    ('right', '='),
    ('left', 'or'),
    ('left', 'and'),
    ('left', 'equal', 'notEqual'),
    ('left', '>','<','lessOrEqual','greaterOrEqual'),
    ('left', '+','-'),
    ('left', '*','/','%'),
    ('right', '!','new','uminus'),
    ('left', '[',']','(',')')
)

# grammar rules

def p_PROGRAM(p):
  '''PROGRAM : CLASS_DECL_LIST
              | epsilon'''
  capture(p, "PROGRAM")

def p_CLASS_DECL_LIST(p):
  '''CLASS_DECL_LIST : CLASS_DECL
                     | CLASS_DECL CLASS_DECL_LIST'''
  capture(p, "CLASS DECLARATION LIST")

def p_CLASS_DECL(p):
  '''CLASS_DECL : class id extends id '{' FIELD_OR_METHOD_DECL_LIST '}'
                | class id extends id '{' '}'
                | class id '{' FIELD_OR_METHOD_DECL_LIST '}'
                | class id '{' '}' '''
  capture(p, "CLASS DECLARATION")
  
def p_FIELD_OR_METHOD_DECL_LIST(p):
  '''FIELD_OR_METHOD_DECL_LIST : FIELD_DECL 
                               | FIELD_DECL FIELD_OR_METHOD_DECL_LIST
                               | METHOD_DECL
                               | METHOD_DECL FIELD_OR_METHOD_DECL_LIST '''
  capture(p, "FIELD OR METHOD DECLARATION LIST")
                    
def p_FIELD_DECL(p):
  '''FIELD_DECL : TYPE id ';'
                | TYPE id LIST_AUX_IDS ';' '''
  capture(p, "FIELD DECLARACION")
  
def p_LIST_AUX_IDS(p):
  '''LIST_AUX_IDS : ',' id 
                  | ',' id LIST_AUX_IDS'''
  capture(p, "AUX IDS LIST")

def p_METHOD_DECL(p):
  '''METHOD_DECL : TYPE id '(' ')' BLOCK
                 | TYPE id '(' FORMALS ')' BLOCK
                 | void id '(' ')' BLOCK
                 | void id '(' FORMALS ')' BLOCK'''
  capture(p, "METHOD DECLARATION")
  
def p_FORMALS(p):
  '''FORMALS : TYPE id
             | TYPE id ',' FORMALS '''
  capture(p, "FORMALS")
                       
def p_TYPE(p):
  '''TYPE : int 
          | boolean 
          | string 
          | id 
          | TYPE '[' ']' '''
  capture(p, "TYPE")

def p_BLOCK(p):
  '''BLOCK : '{' '}'
           | '{' VAR_DECL_STATEMENTS_LIST '}' '''
  capture(p, "BLOCK")
  
def p_VAR_DECL_STATEMENTS_LIST(p):
  '''VAR_DECL_STATEMENTS_LIST :  VAR_DECL
                              |  VAR_DECL VAR_DECL_STATEMENTS_LIST
                              |  STATEMENT
                              |  STATEMENT VAR_DECL_STATEMENTS_LIST'''
  capture(p, "VARIABLE,DECLARATION AND STATEMENT LIST") 

def p_VAR_DECL(p):
  '''VAR_DECL : TYPE id LIST_IDS_EXPRESSIONS ';'
              | TYPE id ';' 
              | TYPE id '=' EXPRESSION LIST_IDS_EXPRESSIONS ';'
              | TYPE id '=' EXPRESSION ';' '''
  capture(p, " VARIABLE DECLARATION")

def p_LIST_IDS_EXPRESSIONS(p):
  '''LIST_IDS_EXPRESSIONS : ',' id
                          | ',' id '=' EXPRESSION
                          | ',' id LIST_IDS_EXPRESSIONS
                          | ',' id '=' EXPRESSION LIST_IDS_EXPRESSIONS '''
  capture(p, "IDS AND EXPRESSIONS LIST")
                          
def p_STATEMENT(p):
  '''STATEMENT : ASSIGN ';'
               | CALL ';'
               | return EXPRESSION ';'
               | return ';'
               | if '(' EXPRESSION ')' STATEMENT else STATEMENT
               | if '(' EXPRESSION ')' STATEMENT
               | while '(' EXPRESSION ')' STATEMENT
               | break ';'
               | continue ';'
               | BLOCK '''
  capture(p, "STATEMENT")
  
def p_ASSIGN(p):
  '''ASSIGN : LOCATION '=' EXPRESSION'''
  capture(p, "ASSIGNMENT")
  
def p_LOCATION(p):
  '''LOCATION : id
              | EXPRESSION '.' id
              | id '[' EXPRESSION ']' '''
  capture(p, "LOCATION")
  
def p_CALL(p):
  '''CALL : METHOD '(' ACTUALS ')'
          | METHOD '(' ')' ''' 
  capture(p, "CALL")
  
def p_METHOD(p):
  '''METHOD : id
            | EXPRESSION '.' id '''
  capture(p, "METHOD")

def p_ACTUALS(p):
  '''ACTUALS : EXPRESSION
             | EXPRESSION ',' ACTUALS '''
  capture(p, "ACTUALS")
  
def p_EXPRESSION(p):
  '''EXPRESSION : LOCATION
                | CALL
                | this
                | new id '(' ')'
                | new TYPE '[' EXPRESSION ']'
                | EXPRESSION '.' length
                | BINARY_EXPRESSION
                | '!' EXPRESSION
                | '-' EXPRESSION %prec uminus
                | LITERAL
                | '(' EXPRESSION ')' '''
  capture(p, "EXPRESSION")

def p_BINARY(p):
  '''BINARY_EXPRESSION : EXPRESSION '+' EXPRESSION
                       | EXPRESSION '-' EXPRESSION
                       | EXPRESSION '*' EXPRESSION
                       | EXPRESSION '/' EXPRESSION
                       | EXPRESSION '%' EXPRESSION
                       | EXPRESSION and EXPRESSION
                       | EXPRESSION or EXPRESSION
                       | EXPRESSION '<' EXPRESSION
                       | EXPRESSION lessOrEqual EXPRESSION
                       | EXPRESSION '>' EXPRESSION
                       | EXPRESSION greaterOrEqual EXPRESSION
                       | EXPRESSION equal EXPRESSION
                       | EXPRESSION notEqual EXPRESSION '''
  capture(p, "BINARY EXPRESSION")

def p_LITERAL(p):
  '''LITERAL : number
             | binary
             | hexa
             | scientific
             | charArray
             | true
             | false
             | null '''
  capture(p, "LITERAL")

def p_epsilon(p):
    'epsilon :'
    pass
  
def p_error(p):
    print("Syntax error for token '"+ str(p.value) +"' found at line number " + str(p.lineno))

parser = yacc.yacc()
programs = {
    '1' : 'quickSortMiniJava.txt',
    '2' : 'testOk1.txt',
    '3' : 'testErrors1.txt',
    '4' : 'testErrors2.txt',
    '5' : 'empty.txt'
}

choice = ""

while(choice != "-1"):
    print("\n  Welcome to this miniJava syntactic analyzer  \n")
    print("  please press a number corresponding to the program you want to analyze  ")
    print("  1. quicksort           ")
    print("  2. test ok 1           ")
    print("  3. test with errors 1  ")
    print("  4. test with errors 2  ")
    print("  5. empty file          ")
    print("  Press -1 to exit     \n")
    choice = raw_input()

    if choice in programs:
        sourceCode = open('test/' + programs[choice], 'r').read()
        rootNode = parser.parse(sourceCode)
        DOTcode = rootNode.generateDOTcode()
        file = open('DOTcode.txt', 'w+')
        file.write(DOTcode)
        file.close()
        print("\n  Success!! a file called DOTcode.txt was created in this directory    "\
              "\n  now you can go to webgraphviz.com and use the generated DOT code to  "\
              "\n  draw a nice abstract sintax tree for your minijava program            ")
    elif choice != "-1":
        print("\n Please choose a valid number \n")                   
