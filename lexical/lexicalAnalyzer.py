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


tokens = [
    'comma',
    'rightBracket',
    'leftBracket',
    'plus',
    'minus',
    'multiplication',
    'division',
    'assign',
    'notEqual',
    'equal',
    'not',
    'rightBrace',
    'leftBrace',
    'greater',
    'greaterOrEqual',
    'less',
    'lessOrEqual',
    'or',
    'and',
    'leftParentheses',
    'rightParentheses',
    'identifier',
    'hexa',
    'number',
    'string',
    'stringError',
    'semicolon',
    'dot',	
    'modulus',
    'singleComment',
    'multiComment',
    'multiCommentError',
    'binary',
    'scientific'
] + list(keywords.values())

# regular expressions for tokens
t_comma             =   r','
t_rightBracket      =   r'\['
t_leftBracket       =   r'\]'
t_plus              =   r'\+'
t_minus             =   r'\-'
t_multiplication    =   r'\*'
t_division          =   r'\/'
t_assign            =   r'='
t_notEqual          =   r'!='
t_equal             =   r'=='
t_not               =   r'!'
t_rightBrace        =   r'{'
t_leftBrace         =   r'}'
t_greater           =   r'>'
t_greaterOrEqual    =   r'>='
t_less              =   r'<'
t_lessOrEqual       =   r'=<'
t_or                =   r'(\|\|)|or'
t_and               =   r'and|&&'
t_leftParentheses   =   r'\('
t_rightParentheses  =   r'\)'
t_semicolon         =   r';'
t_dot               =   r'\.'
t_modulus           =   r'%'

# some tokens are defined as functions 
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_string(t):
    r'".*"'
    return t
   
def t_stringError(t):
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

def t_multiCommentError(t):
    r'/\*(.|\n)+$'
    print("\n*************************ERROR!!!!!***************************")	
    print("multiline comment not closed at line %d" %t.lineno)
    print("**************************************************************\n")

def t_binary(t):
    r'b’[01]+’'
    # use string manipulation to get 0s and 1s 
    start = t.value.find("’")
    # symbol ’  takes 3 characters 
    finish = t.value.find("’",start + 3)
    binary  = t.value[start + 3:finish]
    print(" binary %s is %d base-10" %(binary,int(binary,2)))
    t.value = int(binary,2)
    return t

def t_identifier(t):
    r'([a-zA-Z_]+[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9_]*[a-zA-ZáéíóúñÁÉÍÓÚÑ_]+)|[a-zA-Z]'
    # here I catch all words token, including keywords.
    # if keyword is found, change token type to the specific keyword category
    t.type = keywords.get(t.value,'identifier')

    # if token was not  keyword, look for spanish characters and replace them 
    if t.type == "identifier":
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
    r'(-)?(\d+)' 
    t.value = int(t.value)
    if t.value < -2147483648 or t.value > 2147483647:
        print("\n*************************ERROR!!!!!***************************")
        print("number %d found at line %d is not allowed" \
        %(t.value,t.lineno))
        print("**************************************************************\n")
    else: 
        return t


analyzer = lex.lex()
sourceCode = open('correctInput.txt', 'r').read()
analyzer.input(sourceCode)

while True:
    token = analyzer.token()
    if not token:
        break      # end of list
    print(token)
