# -*- coding: utf-8 -*-

import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections as mc

#----------------------------------------------Cuantos puntos --------------------------------------------------------
num = input("Escoja la cantidad de puntos a conectar: ")
n = int(num)
#----------------------------------------------Listas usadas --------------------------------------------------------
conectivos = ['O', 'Y', '>','<->']

#GENERAMOS LAS LETRAS PROPOSICIONALES
letrasProposicionales= []
for i in range(200, 200+(n**2)-n):
	#print(chr(i))
	letrasProposicionales.append(chr(i))

#---------------------------------------- ELIMINAR DOBLE NEGACION----------------------------------------------------------------

def del_double_neg(f):
    if "-" not in f:
        return f
    for i in range(0, len(f)-1):
        if f[i] == "-":
            if f[i+1] == "-":
                return del_double_neg(f[:i] + f[i+2:])
            else:
                return f[:i+1] + del_double_neg(f[i+1:])



#----------------------------------------------------------------------------TSEITIN-----------------------------------------------------------------

def tseitin_helper(f):
    f = del_double_neg(f)
    for i in range(0, len(f)):
        if f[i] == "=":
            left_branch = f[:i]
            right_branch = f[i+1:]
            for a in range(0, len(right_branch)):
                if right_branch[a] == "Y":
                    right_left_branch = right_branch[:a]
                    right_right_branch = right_branch[a+1:]
                    fnc = "(" + right_left_branch + "O" + "-" + left_branch + ")" + "Y" + "(" + right_right_branch + "O" + "-" + left_branch + ")" + "Y" + "(" + "-" + right_left_branch + "O" + "-" + right_right_branch + "O" + left_branch + ")"
                    return del_double_neg(fnc)

                elif right_branch[a] == "-":
                    fnc = "(" + "-" + left_branch + "O" + right_branch + ")" + "Y" + "(" + left_branch + "O" + "-" + right_branch + ")"
                    return del_double_neg(fnc)

                elif right_branch[a] == "O":
                    right_left_branch = right_branch[:a]
                    right_right_branch = right_branch[a+1:]
                    fnc = "(" + "-"+ right_left_branch + "O" + left_branch + ")" + "Y" + "(" + "-" + right_right_branch + "O" + left_branch + ")" + "Y" + "(" + right_left_branch + "O" + right_right_branch + "O" + "-" + left_branch + ")"
                    return del_double_neg(fnc)

def tseitin(A, letrasProposicionalesA):

	letrasProposicionalesB = []
	for i in range(500+(n**2)-n+1,300000):
		letrasProposicionalesB.append(chr(i))

	L  = []
	pila = []
	i = -1
	s = A [0]

	while len(A) > 0:
		if s in letrasProposicionalesA and len(pila) > 0 and pila[-1] == "-":
			i += 1
			atomo = letrasProposicionalesB[i]
			pila = pila[:-1]
			pila.append(atomo)
			L.append(atomo + "=" + "-" + s)
			A = A[1:]
			if len(s)>0:
				s = A[0]

		elif s == ")":
			w = pila[-1]
			o = pila[-2]
			v = pila[-3]
			pila = pila[:len(pila) -4]
			i += 1
			atomo = letrasProposicionalesB[i]
			L.append(atomo + "=" + v + o + w)
			s = atomo

		else:
			pila.append(s)
			A = A[1:]
			if len(A)>0:
				s = A[0]

	B = ""
	if i < 0:
		atomo = pila[-1]

	else:
		atomo = letrasProposicionalesB[i]

	for x in L:
		y = tseitin_helper(x)
		B += "Y" + y

	B = atomo + B
	return B


#----------------------------------------------------------------------FORMA CLAUSAL ----------------------------------------------------------------


def transformacion_clausulas(C):
    L = []

    while len(C)>0:
        S = C[0]
        if S == "O" or S == "(" or S==")":
            C = C[1:]

        elif S == "-":
            literal = S + C[1]
            L.append(literal)
            C = C[2:]

        else:
            L.append(S)
            C = C[1:]

    return L



def forma_clausal(C):
    L = []
    count = 0

    while len(C)>0:
        if count == len(C) or C[count] == "Y":
            L.append(transformacion_clausulas(C[:count]))
            C = C[count+1:]
            count = 0

        else:
            count +=1

    return L


def clausula2string(lista):
    string = ""
    lista2 = []
    for i in lista:
        for j in i:
            string += j
        lista2.append(string)
        string = ""

    return lista2

#---------------------------------------------------------------------DPLL--------------------------------------------------------

def clausulaUnitaria(lista) :
    for i in lista:
        if (len(i)==1):
            return i

        elif (len(i)==2 and i[0]=="-"):
            return i

    return None



def clausulaVacia(lista):
    for i in lista:
        if(i==''):
            return(True)

    return False


def unitPropagation(lista,interps):
    x = clausulaUnitaria(lista)

    while(x!= None and clausulaVacia(lista)!=True):
        if (len(x)==1):
            interps[str(x)]=1
            j = 0
            for i in range(0,len(lista)):
                lista[i]=re.sub('-'+x,'',lista[i])

            for i in range(0,len(lista)):
                if(x in lista[i-j]):
                    lista.remove(lista[i-j])
                    j+=1

        else:
            interps[str(x[1])]=0
            j = 0
            for i in range(0,len(lista)):
                if(x in lista[i-j]):
                    lista.remove(lista[i-j])
                    j+=1

            for i in range(0,len(lista)):
                lista[i]=re.sub(x[1],'',lista[i])

        x = clausulaUnitaria(lista)

    return(lista, interps)



def literal_complemento(lit):
    if lit[0] == "-":
        return lit[1]

    else:

        lit = "-" + lit
        return lit

def DPLL(lista, interps):
    lista, interps = unitPropagation(lista,interps)

    if(len(lista)==0):
        listaFinal = lista
        interpsFinal = interps
        return(lista,interps)

    elif("" in lista):
        listaFinal = lista
        interpsFinal = interps
        return (lista,{})

    else:
        listaTemp = [x for x in lista]

        for l in listaTemp[0]:
            if (len(listaTemp)==0):
                return (listaTemp, interps)

            if (l not in interps.keys() and l!='-'):
                break

        listaTemp.insert(0,l)
        lista2, inter2 = DPLL(listaTemp, interps)

        if inter2 == {}:
            listaTemp = [x for x in lista]
            a =literal_complemento(l)
            listaTemp.insert(0,a)
            lista2, inter2 = DPLL(listaTemp, interps)

        return lista2, inter2

#----------------------------------------------------------------------------RULES---------------------------------------------------------------


##----------------------------------RULE #3-------------------------------------

def create_lists_rule3( n, Letras):
	Lista1 = []
	Lista2 = []
	for i in range(0,n-1):
		tmp = []
		c = 0
		while (c != n - (len(Lista1) + 1)):
			if (len(tmp) == 0):
				tmp.append(Letras[i])
				c +=1
			else:
				tmp.append(Letras[(n*c)+i])
				c += 1
		Lista1.append(tmp)

	for i in range(n-1,n*(n-1), n-1):
		tmp = []
		c = 0
		while (c != n - (len(Lista2) + 1)):
			if (len(tmp) == 0):
				tmp.append(Letras[i])
				c +=1
			else:
				tmp.append(Letras[(n*c)+i])
				c += 1
		Lista2.append(tmp)
	return Lista1, Lista2


def regla_3 (Lista1, Lista2,n):
	values4points = {}
	values4points[3] = 1
	for i in range(4,n+1):
		value = values4points.get(i-1)
		values4points[i] = value + (i-1)
	c = 1
	string = ""
	for x in range(0, len(Lista1)):
		for i in range(0,len(Lista1[x])):
			if(c == 1):
				string += "((" + Lista1[x][i] + "Y" + "-" + Lista2[x][i] + ")" + "O" + "(" + Lista2[x][i] + "Y" + "-" + Lista1[x][i] + "))" + "Y"
				c += 1
			elif (c==2):
				string += (values4points.get(n)*"(") + "((" + Lista1[x][i] + "Y" + "-" + Lista2[x][i] + ")" + "O" + "(" + Lista2[x][i] + "Y" + "-" + Lista1[x][i] + "))" + "Y"
				c += 1
			else:
				string += "((" + Lista1[x][i] + "Y" + "-" + Lista2[x][i] + ")" + "O" + "(" + Lista2[x][i] + "Y" + "-" + Lista1[x][i] + "))" + ")" + "Y"
				c += 1

	string = string[:-1]
	return string

#------------------------------------------------------------------------------

#-------------------------------REGLA 2----------------------------------------

def create_lists_rule2(n, Letras):
	Lista = []

	for i in Letras:
		if len(Letras)>0:
			temp = []
			Lista.append(Letras[:n-1])
			Letras = Letras[n-1:]
	return Lista



def regla_2(n, Lista):

	c=1
	string = ""
	lista_string2 = []
	for sublist in Lista:

		for x in range(0, len(sublist)):
			temp = [a for a in sublist if a!=sublist[x]]
			u =1
			string2 = ""
			for s in temp:
				if u == 1:
					string2 += "(" + sublist[x] + "Y" + "-" + s + ")" + "Y"
					u += 1
				elif u == 2:
					string2 += (n-4)*"(" + "-" + s + "Y"
					u +=1

				else:
					string2 += "-" + s + ")" + "Y"
					u+=1
			lista_string2.append(string2[:-1])


	sublista = []
	for i in range(0, n):
		sublista.append(lista_string2[:(n-1)])
		del(lista_string2[:(n-1)])

	sublista_median_rules = []

	string = ""
	for i in sublista:
		c=1
		median_string = ""
		for a in range(0, len(i)):
			if c == 1:
				if n > 3:
					median_string += "(" + i[a] +")" + "O"
				else:
					median_string += i[a] + "O"
				c += 1
			elif c == 2:
				if n > 3:
					median_string += (n-2)*"(" + i[a] + ")" + "O"
				else:
					median_string += i[a]
				c += 1

			else:
				median_string += "(" + i[a] + "))" + "O"
				c += 1

		if n >3:
			sublista_median_rules.append(median_string[:-1])
		else:
			sublista_median_rules.append(median_string)

	count = 1
	for i in range(0, len(sublista_median_rules)):

		if count == 1:
			string += "(" + sublista_median_rules[i] + ")" + "Y"
			count += 1
		elif count == 2:
			string += (n-1)*"(" + sublista_median_rules[i] + ")" + "Y"
			count +=1

		else:
			string += "(" + sublista_median_rules[i] + "))" + "Y"
			count +=1

	return string[:-1]


#------------------------------------------------------------------------------

#---------------------------------REGLA1---------------------------------------

def create_list_rule1(n,Letras):
	Letras_Transpose_helper = create_lists_rule2(n,Letras)
	Letras_Transpose = []
	for i in range(0,len(Letras_Transpose_helper)):
		Letras_Transpose_helper[i].insert(i,"diagonal")
	for c in range(0,len(Letras_Transpose_helper)):
		temp = []
		for i in range(0,len(Letras_Transpose_helper)):
			if (Letras_Transpose_helper[i][c] == "diagonal"):
				continue
			temp.append(Letras_Transpose_helper[i][c])
		Letras_Transpose.append(temp)
	return Letras_Transpose

def regla_1(n, Lista):
	c=1
	string = ""
	lista_string2 = []
	for sublist in Lista:

		for x in range(0, len(sublist)):
			temp = [a for a in sublist if a!=sublist[x]]
			u =1
			string2 = ""
			for s in temp:
				if u == 1:
					string2 += "(" + sublist[x] + "Y" + "-" + s + ")" + "Y"
					u += 1
				elif u == 2:
					string2 += (n-4)*"(" + "-" + s + "Y"
					u +=1

				else:
					string2 += "-" + s + ")" + "Y"
					u+=1
			lista_string2.append(string2[:-1])


	sublista = []
	for i in range(0, n):
		sublista.append(lista_string2[:(n-1)])
		del(lista_string2[:(n-1)])

	sublista_median_rules = []

	string = ""
	for i in sublista:
		c=1
		median_string = ""
		for a in range(0, len(i)):
			if c == 1:
				if n > 3:
					median_string += "(" + i[a] +")" + "O"
				else:
					median_string += i[a] + "O"
				c += 1
			elif c == 2:
				if n > 3:
					median_string += (n-2)*"(" + i[a] + ")" + "O"
				else:
					median_string += i[a]
				c += 1

			else:
				median_string += "(" + i[a] + "))" + "O"
				c += 1

		if n >3:
			sublista_median_rules.append(median_string[:-1])
		else:
			sublista_median_rules.append(median_string)

	count = 1
	for i in range(0, len(sublista_median_rules)):

		if count == 1:
			string += "(" + sublista_median_rules[i] + ")" + "Y"
			count += 1
		elif count == 2:
			string += (n-1)*"(" + sublista_median_rules[i] + ")" + "Y"
			count +=1

		else:
			string += "(" + sublista_median_rules[i] + "))" + "Y"
			count +=1

	return string[:-1]



#----------------------------------LA REGLA-------------------------------------

def LaRegla(n, letras):
	list_rule3 = create_lists_rule3(n, letras)
	Rule3 = regla_3 (list_rule3[0] , list_rule3[1], n)
	list_rule2 = create_lists_rule2(n, letras)
	Rule2 = regla_2(n, list_rule2)
	list_rule1 = create_list_rule1(n, letras)
	Rule1 = regla_1(n, list_rule1)
	return "(" + Rule3 + ")" + "Y" + "((" + Rule2 + ")" + "Y" + "(" + Rule1 + "))"

#-----------------------------------------------------------------------------

#--------------------------------------------------------------------------PROCESSING--------------------------------------------------


def Process(formula):
	tseit = tseitin(formula, letrasProposicionales)
	clausula = forma_clausal(tseit)
	clausula_string = clausula2string(clausula)
	interpretacion = DPLL(clausula_string, {})
	interps_needed = {k: interpretacion[1][k] for k in letrasProposicionales if k in interpretacion[1]}
	return interpretacion[0], interps_needed


#---------------------------------------------------------MAIN--------------------------------------------------------

results = Process(LaRegla(n, letrasProposicionales))
print(results)
print("len", len(results[1]))
count = 0
for line, v in results[1].items():
    if v == 1:
        count +=1

print("num de interps verdaderas:", count)
#----------------------------GRAPHING----------------------------------------

mos = np.random.rand(n)
y = np.arange(1,n+1)

fig, ax = plt.subplots()
plt.scatter(y, mos)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

cant = n
for i in range(0, len(mos), cant):
	lines = []
	for j in range(0,cant-1):
		p = [(y[i+j], mos[i+j]), (y[i+j+1], mos[i+j+1])]
		lines.append(p)
	ti = [(y[0], mos[0]), (y[n-1], mos[n-1])]
	lines.append(ti)
	lc = mc.LineCollection(lines, colors = "red", linewidths = 1)
	ax.add_collection(lc)

plt.title("Point's Graph")
plt.grid(False)
plt.tight_layout()
plt.show()
