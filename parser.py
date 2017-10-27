#!/usr/bin/python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------
#parser.py
#
#autor: Rafael Alessandro Ramos
#date: 05-10-2017
#-------------------------------------------------------------------------

import ply.yacc as yacc
from lexer import Lexer
from graphviz import Digraph

class Tree:

    def __init__(self, type_node, child=[], value=''):
        self.type = type_node
        self.child = child
        self.value = value

    def __str__(self):
        return self.type

class Parser:

    def __init__(self, code):
        lex = Lexer()
        self.tokens = lex.tokens
        self.precedence = (
            ('left', 'IGUALDADE', 'NEGACAO', 'MAIOR_IGUAL', 'MENOR_IGUAL', 'MENOR', 'MAIOR'),
            ('left', 'SOMA', 'SUBTRACAO'),
            ('left', 'MULTIPLICACAO', 'DIVISAO'),
        )
        parser = yacc.yacc(debug=False, module=self, optimize=False)
        self.ast = parser.parse(code)
    
    def p_programa(self, p):
        'programa : lista_declaracoes'
        p[0] = Tree('programa', [p[1]])

    def p_lista_declaracoes_1(self, p):
        'lista_declaracoes : lista_declaracoes declaracao'
        p[0] = Tree('lista_declaracoes', [p[1], p[2]])
        
    def p_lista_declaracoes_2(self, p):
        'lista_declaracoes : declaracao'
        p[0] = Tree('lista_declaracoes', [p[1]])    

    def p_declaracao(self, p):
        '''
        declaracao : declaracao_variaveis
                    | inicializacao_variaveis
                    | declaracao_funcao
        '''
        p[0] = Tree('declaracao', [p[1]])

    def p_declaracao_variaveis(self, p):
        'declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis'
        p[0] = Tree('declaracao_variaveis', [p[1], p[3]])

    def p_inicializacao_variaveis(self, p):
        'inicializacao_variaveis : atribuicao'
        p[0] = Tree('inicializacao_variaveis', [p[1]])

    def p_lista_variaveis_1(self, p):    
        'lista_variaveis : lista_variaveis VIRGULA var'
        p[0] = Tree('lista_variaveis', [p[1], p[3]])
    
    def p_lista_variaveis_2(self, p):
        'lista_variaveis : var'
        p[0] = Tree('lista_variaveis', [p[1]])

    def p_var_1(self, p):
        'var : ID'
        p[0] = Tree('var', [], p[1])

    def p_var_2(self, p):
        'var : ID indice'
        p[0] = Tree('var', [p[2]], p[1])

    def p_indice_1(self, p):
        'indice : indice ABRE_COL expressao FECHA_COL'
        p[0] = Tree('indice', [p[1], p[3]])

    def p_indice_2(self, p):
        'indice : ABRE_COL expressao FECHA_COL'
        p[0] = Tree('indice', [p[2]])

    def tipo_1(self, p):
        'tipo : tipo DOIS_PONTOS'
        p[0] = Tree('tipo', [p[1]], p[2])

    def p_tipo_2(self, p):
        '''
        tipo : INTEIRO
            | FLUTUANTE
        '''
        p[0] = Tree('tipo', [], p[1])

    def p_declaracao_funcao_1(self, p):
        'declaracao_funcao : tipo cabecalho'
        p[0] = Tree('declaracao_funcao', [p[1], p[2]])
        
    def p_declaracao_funcao_2(self, p):
        'declaracao_funcao : cabecalho'
        p[0] = Tree('declaracao_funcao', [p[1]])

    def p_cabecalho_1(self, p):
        'cabecalho : PRINCIPAL ABRE_PAR lista_parametros FECHA_PAR corpo FIM'
        p[0] = Tree('cabecalho', [p[3], p[5]], p[1])

    def p_cabecalho_2(self, p):
        'cabecalho : ID ABRE_PAR lista_parametros FECHA_PAR corpo FIM'
        p[0] = Tree('cabecalho', [p[3], p[5]], p[1])

    def p_lista_parametros_1(self, p):
        'lista_parametros : lista_parametros VIRGULA parametro'
        p[0] =  Tree('lista_parametros', [p[1], p[3]])

    def p_lista_parametros_2(self, p):
        '''
        lista_parametros : parametro
                         | vazio
        '''
        p[0] =  Tree('lista_parametros', [p[1]])

    def p_parametro_1(self, p):
        'parametro : tipo DOIS_PONTOS ID'
        p[0] =  Tree('parametro', [p[1]], p[3])

    def p_parametro_2(self, p):
        'parametro : parametro ABRE_COL FECHA_COL'
        p[0] =  Tree('parametro', [p[1]])

    def p_corpo_1(self, p):
        'corpo : corpo acao'
        p[0] = Tree('corpo', [p[1], p[2]])
        
    def p_corpo_2(self, p):
        'corpo : vazio'
        p[0] = Tree('corpo', [p[1]])

    def p_acao(self, p):
        '''
        acao : expressao
            | declaracao_variaveis
            | se
            | repita
            | leia
            | escreva
            | retorna
            | error
        '''
        p[0] = Tree('acao', [p[1]])

    def p_se_1(self, p):
        'se : SE expressao ENTAO corpo FIM'
        p[0] = Tree('se', [p[2], p[4]])
        
    def p_se_2(self, p):        
        'se : SE expressao ENTAO corpo SENAO corpo FIM'
        p[0] = Tree('se', [p[2], p[4], p[6]])

    def p_repita(self, p):
        'repita : REPITA corpo ATE expressao'
        p[0] = Tree('repita', [p[2], p[4]])

    def p_atribuicao(self, p):
        'atribuicao : var ATRIBUICAO expressao'
        p[0] = Tree('atribuicao', [p[1], p[3]])

    def p_leia(self, p):
        'leia : LEIA ABRE_PAR ID FECHA_PAR'
        p[0] = Tree('leia', [], p[3])        

    def p_escreva(self, p):
        'escreva : ESCREVA ABRE_PAR expressao FECHA_PAR'
        p[0] = Tree('escrreva', [p[3]], p[1])

    def p_retorna(self, p):
        'retorna : RETORNA ABRE_PAR expressao FECHA_PAR'
        p[0] = Tree('retorna', [p[3]], p[1])
        
    def p_expressao(self, p):
        '''
        expressao : expressao_simples
                | atribuicao
        '''
        p[0] = Tree('expressao', [p[1]])

    def p_expressao_simples_1(self, p):
        'expressao_simples : expressao_aditiva'
        p[0] = Tree('expressao_simples', [p[1]])
        
    def p_expressao_simples_2(self, p):
        'expressao_simples : expressao_simples operador_relacional expressao_aditiva'
        p[0] = Tree('expressao_simples', [p[1], p[2], p[3]])
    
    def p_expressao_aditiva_1(self, p):
        'expressao_aditiva : expressao_multiplicativa'
        p[0] = Tree('expressao_aditiva', [p[1]])
        
    def p_expressao_aditiva_2(self, p):
        'expressao_aditiva : expressao_aditiva operador_soma expressao_multiplicativa'
        p[0] = Tree('expressao_aditiva', [p[1], p[2], p[3]])

    def p_expressao_multiplicativa_1(self, p):
        'expressao_multiplicativa : expressao_unaria'
        p[0] = Tree('expressao_multiplicativa', [p[1]])

    def p_expressao_multiplicativa_2(self, p):
        'expressao_multiplicativa : expressao_multiplicativa operador_multiplicacao expressao_unaria'
        p[0] = Tree('expressao_multiplicativa', [p[1], p[2], p[3]])
    
    def p_expressao_unaria_1(self, p):
        'expressao_unaria : fator'
        p[0] = Tree('expressao_unaria', [p[1]])

    def p_expressao_unaria_2(self, p):
        'expressao_unaria : operador_soma fator'
        p[0] = Tree('expressao_unaria', [p[1], p[2]])
    
    def p_operador_logico(self, p):
        '''
        operador_relacional : MENOR
                            | MAIOR
                            | IGUALDADE
                            | MENOR_IGUAL
                            | MAIOR_IGUAL
        '''
        p[0] = Tree('operador_logico', [], p[1])

    def p_operador_soma(self, p):
        '''
        operador_soma : SOMA
                    | SUBTRACAO
        '''
        p[0] = Tree('operador_soma', [], p[1]) 

    def p_operador_multiplicacao(self, p):
        '''
        operador_multiplicacao : MULTIPLICACAO
                                | DIVISAO
        '''
        p[0] = Tree('operador_multiplicacao', [], p[1])
    
    def p_fator_1(self, p):
        'fator : ABRE_PAR expressao FECHA_PAR'
        p[0] = Tree('fator', [p[2]])

    def p_fator_2(self, p):
        '''
        fator : var
            | chamada_funcao
            | numero
        '''
        p[0] = Tree('fator', [p[1]])

    def p_numero(self, p):
        ''' 
        numero : NUMERO
                | DECIMAL
                | CIENTIFICA
        '''
        p[0] = Tree('numero', [], p[1])

    def p_chamada_funcao_1(self, p):
        'chamada_funcao : ID ABRE_PAR lista_argumentos FECHA_PAR'
        p[0] = Tree('chamada_funcao', [p[3]], p[1])

    def p_lista_argumentos_1(self, p):
        'lista_argumentos  : lista_argumentos VIRGULA expressao'
        p[0] = Tree('lista_argumentos', [p[1], p[3]])

    def p_lista_argumentos_2(self, p):
        '''
        lista_argumentos : expressao
                        | vazio
        '''
        p[0] = Tree('lista_argumentos', [p[1]])

    def p_vazio(self, p):
        'vazio : '

    def p_error(self, p):
        if p:
            print("Erro sintático: '%s', linha %d" % (p.value, p.lineno))
            exit(1)
        else:
            yacc.restart()
            print('Erro sintático: definições incompletas!')
            exit(1)

def printTreeTerminal(node, level='-'):
    if node != None :
        print('%s %s \t%s' %(level, node.type, node.value))
        for son in node.child:
            printTreeTerminal(son, level+'-')
        

def printTreeText(node, w, i):
    if node != None :
        value1 = node.type + str(i)
        i += 1
        for son in node.child:
            w.edge(value1, str(son) + str(i))
            printTreeText(son, w, i)

if __name__ == '__main__':
    from sys import argv, exit
    f = open(argv[1])
    tree = Parser(f.read())

    printTreeTerminal(tree.ast)
    
    w = Digraph('G', filename='./Saidas/ArvoreRepr.gv')
    printTreeText(tree.ast, w, i = 0)
    w.view()


    file_object = open("./Saidas/SaidaArvore.txt", "w")
    file_object.write(w.source)
    file_object.close()
