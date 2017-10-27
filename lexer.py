#!/usr/bin/python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------
#lexer.py
#
#autor: Rafael Alessandro Ramos
#date: 12-9-2017
#-------------------------------------------------------------------------

import ply.lex as lex

class Lexer:

	def __init__(self):
		self.lexer = lex.lex(debug=False, module=self, optimize=False)
	
	reserved = {
				'inteiro' 	: 'INTEIRO',
				'flutuante' : 'FLUTUANTE',
				'repita' 	: 'REPITA',
				'até' 		: 'ATE',
				'retorna' 	: 'RETORNA',
				'principal' : 'PRINCIPAL',
				'se' 		: 'SE',
				'então'		: 'ENTAO',
				'senão' 	: 'SENAO',
				'escreva' 	: 'ESCREVA',
				'leia' 		: 'LEIA',
				'fim' 		: 'FIM'
				}
	tokens = [
			'SOMA',
			'SUBTRACAO',
			'MULTIPLICACAO',
			'DIVISAO', 
			'IGUALDADE', 
			'VIRGULA', 
			'ATRIBUICAO', 
			'MENOR', 
			'MAIOR', 
			'MENOR_IGUAL', 
			'MAIOR_IGUAL', 
			'ABRE_PAR', 
			'FECHA_PAR', 
			'DOIS_PONTOS', 
			'ABRE_COL',
			'FECHA_COL',
			'E_LOGICO', 
			'OU_LOGICO', 
			'ESPACO', 
			'NEGACAO',
			'ID',
			'NUMERO',
			'DECIMAL',
			'CIENTIFICA',
			#'COMENTARIO'
			] + list(reserved.values())

	# Regular expression rules for simple tokens
	t_SOMA 			=	r'\+'
	t_SUBTRACAO 	=	r'-'
	t_MULTIPLICACAO =	r'\*'
	t_DIVISAO 		=	r'/'
	t_IGUALDADE 	=	r'='
	t_VIRGULA 		=	r','
	t_ATRIBUICAO 	=	r':='
	t_MENOR 		=	r'\<'
	t_MAIOR 		=	r'\>'
	t_MENOR_IGUAL 	=	r'<='
	t_MAIOR_IGUAL 	= 	r'>='
	t_ABRE_PAR 		=	r'\('
	t_FECHA_PAR 	=	r'\)'
	t_DOIS_PONTOS 	= 	r':'
	t_ABRE_COL 		=	r'\['
	t_FECHA_COL 	=	r'\]'
	t_E_LOGICO 		=	r'&&'
	t_OU_LOGICO 	=	r'\|\|'
	t_ESPACO 		=	r'\ '
	t_NEGACAO 		=	r'\!'
	
	# A string containing ignored characters (spaces and tabs)
	t_ignore  = ' \t'

	def t_CIENTIFICA(self, t):
		r'((\d+)(\.\d+)(e(\+|\-)?(\d+)) | (\d+)e(\+|\-)?(\d+))'
		t.type = self.reserved.get(t.value,'CIENTIFICA')
		return t

	def t_DECIMAL(self, t):
		r'\-?\d+\.+\d*'
		t.type = self.reserved.get(t.value,'DECIMAL')
		return t
		
	def t_NUMERO(self, t):
		r'\-?\d+'
		t.type = self.reserved.get(t.value,'NUMERO')
		return t

	# Define a rule so we can track line numbers
	def t_newline(self, t):
	    r'\n+'
	    t.lexer.lineno += len(t.value)

	# Error handling rule
	def t_error(self, t):
	    print("Illegal character '%s'" % t.value[0])
	    t.lexer.skip(1)

	def t_ID(self, t):
	    r'[a-zA-Zà-ú][a-zA-Zà-ú_0-9]*'
	    t.type = self.reserved.get(t.value,'ID')    # Check for reserved words
	    return t

	def t_COMMENT(self, t):
	    r'\{[^}]*[^{]*\}'
	    #t.type = self.reserved.get(t.value,'COMENTARIO')
	    #return t

	def test(self, code):
		lex.input(code)
		while True:
			t = lex.token()
			if not t:
				break
			print(t)

if __name__ == '__main__':
	from sys import argv
	lexer = Lexer()
	f = open(argv[1])
	lexer.test(f.read())