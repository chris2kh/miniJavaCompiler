#!/usr/bin/python
# -*- coding: utf-8 -*-
import ply.lex as lex


keywords  = {
    'class'   : 'class',
    'return'  : 'return',
    'this'    : 'this',
    'extends' : 'extends',
    'if'      : 'if',
    'new'     : 'new',
    'void'    : 'void',
    'else'    : 'else',
    'length'  : 'length',
    'int'     : 'int',
    'while'   : 'while',
    'true'    : 'true',
    'boolean' : 'boolean',
    'break'   : 'break',
    'false'   : 'false',
    'string'  : 'string',
    'continue': 'continue',
    'null'    : 'null',
}

# these will be replaced by "_"
spanishCharacters = ['á','é','í','ó','ú','ñ','Á','É','Í','Ó','Ú','Ñ']


literals = [',','[',']','+','-','*','/','=','!','{','}','>','<','(',')',';','.','%']



tokens = [
    'notEqual',
    'equal',
    'greaterOrEqual',
    'lessOrEqual',
    'or',
    'and',
    'id',
    'hexa',
    'number',
    'charArray',
    'errorCharArray',
    'singleComment',
    'multiComment',
    'errorMultiComment',
    'binary',
    'scientific'
] + list(keywords.values())

# some tokens could be defined simply defined as a sequence of specific characters...
t_notEqual          =   r'!='
t_equal             =   r'=='
t_greaterOrEqual    =   r'>='
t_lessOrEqual       =   r'=<'
t_or                =   r'\|\|'
t_and               =   r'&&'
t_ignore            =   " \t"

#  ...others are better defined inside functions are regex

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_charArray(t):
    r'".*"'
    return t
   
def t_errorCharArray(t):
    # Open quotes must be closed. Otherwise, its an error 
    r'".+(\n|$)'
    print("\n*************************ERROR!!!!!***************************")	
    print("quotes not closed found at line number  %d" %t.lineno)
    print("**************************************************************\n")
    # the \n found here is not going to be detected in the function t_newline()	
    # so we increment line number here to keep right our counting
    t.lexer.lineno += 1
	
def t_error(t):
    print("\n*************************ERROR!!!!!***************************")	
    print("character '%s' found at line %d not recognized" %(t.value[0],t.lineno))
    print("**************************************************************\n")
    t.lexer.skip(1)

def t_singleComment(t):
    r'//.*\n'
    # the \n found here is not going to be detected in the function t_newline()	
    # so we increment line number here to keep right our counting
    t.lexer.lineno += 1
    return t

def t_multiComment(t):
    # the ? symbol in the regular expression means the expression 
    # will be evaluated in lazy mode and not greedy mode, which is the default.
    # if greedy mode were used, there would be a problem if there are many multiline comments
    # in the code, as the regex would match everything from the first /* to the last */ 
    r'/\*(.|\n)*?\*/'
    # the \n found here is not going to be detected in the function t_newline()	
    # so we increment line number here to keep right our counting
    t.lexer.lineno += t.value.count("\n")
    return t

def t_errorMultiComment(t):
    r'/\*(.|\n)+$'
    print("\n*************************ERROR!!!!!***************************")	
    print("multiline comment not closed at line %d" %t.lineno)
    print("**************************************************************\n")
    return t

def t_binary(t):
    r'b’[01]+’'
    # usetext manipulation to get 0s and 1s 
    start = t.value.find("’")
    # symbol ’  takes 3 characters 
    finish = t.value.find("’",start + 3)
    binary  = t.value[start + 3:finish]
    print(" binary %s is %d base-10" %(binary,int(binary,2)))
    t.value = int(binary,2)
    return t

def t_id(t):
    r'([a-zA-Z_]+[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9_]*[a-zA-ZáéíóúñÁÉÍÓÚÑ_]+)|[a-zA-Z]'
    # here I catch all words token, including keywords.
    # if keyword is found, change token type to the specific keyword category
    t.type = keywords.get(t.value,'id')

    # if token was not  keyword, look for spanish characters and replace them 
    if t.type == "id":
        for character in spanishCharacters:
            t.value = t.value.replace(character,'_')
    return t

def t_hexa(t):
    r'0[xx][0-9a-fa-f]+'
    print(" hexa number %s is %d base-10" \
    %(t.value,int(t.value,16)))
    t.value = int(t.value,16)
    return t

def t_scientific(t):
    r'-?[0-9](\.\d+)?[ee]-?\d+'
    t.value=float(t.value)
    return t

def t_number(t):
    r'(\d+)' 
    t.value = int(t.value)
    if t.value < -2147483648 or t.value > 2147483647:
        print("\n*************************ERROR!!!!!***************************")
        print("number %d found at line %d is not allowed" \
        %(t.value,t.lineno))
        print("**************************************************************\n")
    else: 
        return t

analyzer = lex.lex()