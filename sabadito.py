"""
Universidad Simon Bolivar

Autores:
	Adelina Figueira 15-10484
	Leonardo Duarte 17-10169
	

"""

import random
import pygame
import math


# Clase que almacena los datos de cada jugador
class Jugador():
	nombre = ""
	turno = 0
	lineas = 0
	puntos = 0


# Inicializa el super-tablero 
def variables(DimensionTab):
	T = [[[0 for casilla in range(0, DimensionTab)] for fila in range(0, DimensionTab)] for tablero in range(0, DimensionTab)]
	return T
	

# Inicializa los jugadores	
def jugadores():
	jugador1 = Jugador()
	jugador2 = Jugador()
	jugador1.turno = 1
	jugador1.puntos = 0
	jugador1.lineas = 0
	jugador2.turno = 2
	jugador2.puntos = 0
	jugador2.lineas = 0

	return jugador1, jugador2


# Funcion que dibuja un string en pantalla
def dibujarTexto(texto, font, superficie, x, y, color):
	objetotexto = font.render(texto, 1, color)
	rectangulotexto = objetotexto.get_rect()
	rectangulotexto.topleft = (x, y)
	superficie.blit(objetotexto, rectangulotexto)


# Funcion que dibuja los textos y tableros secundarios de la pantalla de juego
def letrajuego(screen,jugador1,jugador2,jugador11,jugador22,jugador111,jugador222,Dimension,X,Y):
	font=pygame.font.SysFont("OpenSansSemibold", 28)
	fuente=pygame.font.SysFont("OpenSansSemibold", 20)
	dibujarTablero(screen, 170, 200, X, Y,610,20, (4,126,126),Dimension)
	dibujarTablero(screen, 170, 200, X, Y,610,275, (4,126,126),Dimension)

	dibujarTablero(screen, 170, 200, X, Y,610,20, (0,0,0,100),Dimension)
	dibujarTablero(screen, 170, 200, X, Y,610,275, (0,0,0,100),Dimension)
	
	dibujarTexto(jugador1, font, screen, 620, 30, (255, 255, 255))
	dibujarTexto(jugador11, font, screen, 620, 100, (255, 200, 255))
	dibujarTexto(jugador111, fuente, screen, 620, 170, (255, 200, 255))
	dibujarTexto(jugador2, font, screen, 620, 290, (255, 255, 255))
	dibujarTexto(jugador22, font, screen, 620, 360, (255, 200, 255))
	dibujarTexto(jugador222, fuente, screen, 620, 430, (255, 200, 255))
	
	dibujarTexto("Utiliza las teclas de direccion para moverte entre tableros", fuente, screen, 27, 525, (255, 255, 255))
	dibujarTexto("Haz click en una casilla para seleccionarla", fuente, screen, 27, 550, (255, 255, 255))


# Funcion para obtener la Dimension a utilizar por el usuario
def dimension(dim, screen, negro, verde_feo):
	try:
		DimensionTab = dim
		assert(0 < DimensionTab <= 11)

		return DimensionTab
	
	except Exception:
		font = pygame.font.Font(None, 32)
		dibujarTexto("Debes introducir un numero entre 1 y 11.",font,screen, 50,520,negro)
		dibujarTexto("Vuelve a intentarlo.",font,screen, 50,553,negro)
		# Para volver a introducir la dimension
		return -1


# Verifica si la jugada es valida:
# Si un jugador escoge una posicion donde existe otro numero distinto de cero (numero por defecto) la jugada no es valida.
def esValida(superTablero, tablero, fila, casilla):
	casillaEscogida = superTablero[tablero][fila][casilla]

	if  casillaEscogida == 0:
		return True
	elif casillaEscogida == 1 or casillaEscogida == 2:
		return False


# Reemplaza la casilla escogida con el identificador del jugador
def reflejarEnTablero(superTablero, tablero, fila, casilla, turno):
	superTablero[tablero][fila][casilla] = turno


	return superTablero


# Verifica si todos los elementos de una lista son iguales
def verificarLista(lista):
	"""
		Si la cantidad de ocurrencias del primer elemento de la lista
		es igual al tamano de la lista, todos los elementos son 
		iguales.
	"""
	if lista != [] and lista.count(lista[0]) == len(lista) and lista[0] != 0:

		return True

	else:
		return False


# Caso especial al verificar listas.
# El argumento *args indica que aceptara una cantidad x de argumentos.
# La funcion ve si hay una linea hecha en cada lista dada.
def verificarListaCompleja(*args):
	numeroDeLineas = 0
	for lista in args:
		a = verificarLista(lista)
		if a:   
			numeroDeLineas += 1
		elif not a:
			pass

	return numeroDeLineas


# Verifica si se hizo una linea horizontal en la fila actual
def lineaHorizontalHecha(superTablero, tablero, fila):
	filaActual = superTablero[tablero][fila]
	
	return verificarLista(filaActual)

# Verifica si se hizo una linea vertical en la fila actual
def lineaVerticalHecha(superTablero, tablero, fila, casilla):
	
	"""
		El for itera sobre las FILAS del tablero manteniendo la casilla actual.
		Mientras tanto, coloca esos valores en un arreglo que corresponden
		a una columna del tablero.
	"""

	columnasEnTablero = []
	for filas in range(len(superTablero[tablero])):
		columnasEnTablero.append(superTablero[tablero][filas][casilla])
	
	"""
		El for itera sobre los TABLEROS manteniendo la casilla actual.
		Mientras tanto, coloca esos valores en un arreglo que corresponden
		a una columna en Z.
	"""

	columnasEnZ = []
	for Z in range(len(superTablero)):
		columnasEnZ.append(superTablero[Z][fila][casilla])

	# Luego, se verifica si hay una linea en esos arreglos de columnas.
	return verificarListaCompleja(columnasEnTablero, columnasEnZ)


# Funcion para ahorrar espacio al determinar si hay una linea diagonal en z
def diagonalesEnZ(superTablero, lista, argumento):
	for tableros in range(len(superTablero)):
		for fila in range(len(superTablero[tableros])):
			for casilla in range(len(superTablero[tableros][fila])):
				if argumento:
					lista.append(superTablero[tableros][fila][casilla])

	return lista


# Verifica si se hizo una linea diagonal en el tablero actual
def lineaDiagonalHecha(superTablero, tablero,filat,casillat):
	"""
		Coloca los elementos de la diagonal principal del tablero actual en un
		arreglo. Luego verifica si hay linea.
	"""
	
	diagonalEnTablero = []
	if filat == casillat:
		for fila in range(len(superTablero[tablero])):
			for casilla in range(len(superTablero[tablero][fila])):
				if fila == casilla:
					diagonalEnTablero.append(superTablero[tablero][fila][casilla])

	diagonalSecundariaEnTablero = []
	if casillat == len(superTablero)-1 - filat:
		for fila in range(len(superTablero[tablero])):
			for casilla in range(len(superTablero[tablero][fila])):
				if casilla == len(superTablero)-1 - fila:
					diagonalSecundariaEnTablero.append(superTablero[tablero][fila][casilla])

	lineas = verificarListaCompleja(diagonalEnTablero, diagonalSecundariaEnTablero)

	return lineas


# Revisa cuantas lineas en total se han hecho y devuelve ese numero
def lineaHecha(superTablero, tablero, fila, casilla, turno,jugadorActual):
	lineasVerticales = lineaVerticalHecha(superTablero, tablero, fila, casilla)
	lineasDiagonales = lineaDiagonalHecha(superTablero, tablero, fila, casilla)
	lineasTotales = jugadorActual.lineas

	if lineaHorizontalHecha(superTablero, tablero, fila):
		lineasTotales += 1
	if lineasVerticales > 0:
		lineasTotales += lineasVerticales
	if lineasDiagonales > 0:
		lineasTotales += lineasDiagonales

	return lineasTotales


# Anade lineas al jugador actual si tuvo alguna
def anadirLinea(lineasHechas, jugadorActual):
	jugadorActual.lineas = lineasHechas

	return jugadorActual.lineas


# Anade puntos al jugador actual si tuvo lineas hechas.
# El puntaje aumenta cuando se hace una linea, pero aumenta
# aun mas cuando se hace mas de una linea con una jugada.
def anadirPuntos(lineasHechas, jugadorActual):
	if lineasHechas > jugadorActual.lineas:
			jugadorActual.puntos += lineasHechas*1000
	return jugadorActual.puntos


# Elige aleatoriamente el primer jugador de la partida
def elegirJugador():
	turno = random.randint(1,2)

	return turno


# Alterna entre los 2 jugadores luego de una jugada valida
def cambiarJugador(turnoJugadorActual):
	
	if turnoJugadorActual == 1:
		pygame.mouse.set_cursor(*pygame.cursors.diamond)
		turno = 2
	
	elif turnoJugadorActual == 2:
		pygame.mouse.set_cursor(*pygame.cursors.broken_x)
		turno = 1

	return turno


# Devuelve un error y no suma al contador del while principal,
# por lo tanto el jugador actual no ha cumplido su turno
def error(screen):
	fuente=pygame.font.SysFont(None, 23)
	dibujarTexto("La jugada no es valida", fuente, screen, 617, 240, (255, 255, 255))
	

# Devuelve las variables iniciales a sus valores por defecto
def jugarDeNuevo():
	a = variables()
	return a


# variables necesarias para la parte grafica
def variablesPygame():
	X = 800
	Y = 600
	# Pantalla principal
	screen = pygame.display.set_mode((X,Y))
	# Colores
	blanco = [251, 245, 239]
	negro = (20,20,20)
	verde_feo = [4, 126, 126]
	azul = [0, 0, 126]
	gris = [190, 190, 190]
	gris_claro = [222, 222, 222]
	gris_oscuro = [126, 126, 126]
	# Cursor de menu
	pygame.mouse.set_cursor(*pygame.cursors.tri_left)
	clock = pygame.time.Clock()
	# Imagenes
	Pc95 = pygame.image.load("recursos/pc.png").convert_alpha()
	iconos = pygame.image.load("recursos/iconos.png").convert()
	winlogo = pygame.image.load("recursos/winlogo.png").convert_alpha()
	botonx = pygame.image.load("recursos/botonx.png").convert()
	sabiasque = pygame.image.load("recursos/sabiasque.png").convert()

	# Dimensiones del rectangulo del menu
	anchoRectWin = 580
	altoRectWin = 400
	posRectWinX = X/2 - anchoRectWin/2
	posRectWinY = Y/2 - altoRectWin/2
	posCuadros = posRectWinX + 20 + 410 + 15

	rectJugar,rectRankings,rectSalir,rectExtras = dibujarRectInteractivos(screen, posCuadros, posRectWinY, winlogo, negro, gris,X,Y)
	

	return [X,Y,screen,blanco,negro,verde_feo,azul,gris,gris_claro,gris_oscuro,clock,Pc95,iconos,winlogo,botonx,sabiasque,rectJugar,rectRankings,rectSalir,rectExtras,anchoRectWin,altoRectWin,posRectWinX,posRectWinY,posCuadros]


# Dibuja un rectangulo de tamano variable con el borde superior e izquierdo blanco y el derecho e inferior negro,
# tambien se pueden invertir los bordes. Funciona para construir velozmente los rectangulos del menu. Las lineas
# son las sombras de los rectangulos. 
def dibujarRectanguloWin95(superficie, posRectX, posRectY, anchoRect, altoRect, grosorL1, grosorL2, inverso=False, bienvenida=False):
	# Bienvenida es el rectangulo central, se hace este caso para implementar el rectangulo azul superior
	if inverso and not bienvenida:
		gris_claro = [126, 126, 126]
		gris_oscuro = [190, 190, 190]
		negro = [190, 190, 190]
		gris = [222, 222, 222]
		azul = [222, 222, 222]
	# Rectangulo normal
	elif not inverso and bienvenida:
		gris_claro = [222, 222, 222]
		gris_oscuro = [126, 126, 126]
		negro = [0, 0, 0]
		gris = [190, 190, 190]
		azul = [0, 0, 126]
	# Rectangulo inverso
	elif not inverso and not bienvenida:
		gris_claro = [251, 245, 239]
		gris_oscuro = [126, 126, 126]
		negro = [0, 0, 0]
		gris = [190, 190, 190]
		azul = [190, 190, 190]
	
	# Rectangulo base relleno de gris
	rect =pygame.draw.rect(superficie, gris, [posRectX, posRectY, anchoRect, altoRect])
	# Rectangulo azul (solo en bienvenida)
	pygame.draw.rect(superficie, azul, [posRectX, posRectY, anchoRect-2, 20])
	# Sombras
	pygame.draw.line(superficie, gris_claro, [posRectX, posRectY], [posRectX, posRectY + altoRect], grosorL1)
	pygame.draw.line(superficie, gris_claro, [posRectX, posRectY], [posRectX + anchoRect, posRectY], grosorL1)
	pygame.draw.line(superficie, gris_oscuro, [posRectX-1, posRectY + altoRect-1], [posRectX + anchoRect-1, posRectY + altoRect-1], grosorL2)
	pygame.draw.line(superficie, gris_oscuro, [posRectX + anchoRect-1, posRectY + altoRect-1], [posRectX + anchoRect-1, posRectY-1], grosorL2)
	pygame.draw.line(superficie, negro, [posRectX, posRectY + altoRect], [posRectX + anchoRect, posRectY + altoRect], grosorL2)
	pygame.draw.line(superficie, negro, [posRectX + anchoRect, posRectY + altoRect], [posRectX + anchoRect, posRectY], grosorL2)
	return rect


# Dibuja la superficie total del menu. La funcion crea desde el fondo hasta las lineas que sirven de sombra para los rectangulos.
# Al crear cada objeto, se asegura que al momento de cambiar la resolucion de la ventana los objetos quedan en la misma posicion relativa,
# esto se debe a que las posiciones de cada objeto dependen del tamano del rectangulo principal (A excepcion de algunos rectangulos).
def dibujarMenu(X,Y,screen,blanco,negro,verde_feo,azul,gris,gris_claro,gris_oscuro,Pc95,iconos,winlogo,botonx,sabiasque):
	## Esenciales

	# Fondo
	screen.fill(verde_feo)
	# Rectangulo de la barra
	pygame.draw.rect(screen, gris, [0, Y-30, X, 30])
	# Sombra de la barra (No se usa la funcion anterior por tener un solo borde de sombra)
	pygame.draw.line(screen, blanco, [0,Y-29], [X,Y-29], 2)
	
	## Rectangulos

	# Longitud en X del rectangulo central
	anchoRectWin = 580
	# Longitud en Y del rectangulo central
	altoRectWin = 400
	# Posicion en X del rectangulo central
	posRectWinX = X/2 - anchoRectWin/2
	# Posicion en Y del rectangulo central
	posRectWinY = Y/2 - altoRectWin/2
	# Posicion de los cuadrados pequenos a la izquierda del rectangulo central
	posCuadros = posRectWinX + 20 + 410 + 15

	# Rectangulo Central
	dibujarRectanguloWin95(screen, posRectWinX, posRectWinY, anchoRectWin, altoRectWin, 2, 1, False, True)
	# Rectangulo inverso grande
	dibujarRectanguloWin95(screen, posRectWinX + 20, posRectWinY + 80, 410, 300, 1, 1, True)
	
	# Linea separadora
	pygame.draw.line(screen, gris_oscuro, [posCuadros,posRectWinY + 80 + 75 + 64], [posCuadros + 120, posRectWinY + 80 + 75 + 64], 1)
	pygame.draw.line(screen, blanco, [posCuadros,posRectWinY + 80 + 75 + 65], [posCuadros + 120, posRectWinY + 80 + 75 + 65], 1)
   
	# Rectangulo pestana
	dibujarRectanguloWin95(screen, 76, Y - 23, 150, 20, 1, 1, True)
	# Rectangulo Reloj
	dibujarRectanguloWin95(screen, X - 72, Y - 23, 70, 20, 1, 1, True)
	# Rectangulo esquina ventana equis
	dibujarRectanguloWin95(screen, posRectWinX + 580 - 19, posRectWinY + 4, 15, 15, 1, 1)
	
	##Imagenes

	# Blitear (colocar en la superficie) la pc
	screen.blit(Pc95, (posRectWinX + 20 + 130, posRectWinY + 80 + 140))
	# Blitear los iconos del escritorio
	screen.blit(iconos, (0,0))
	# Blitear la X del boton de la esquina
	screen.blit(botonx,(posRectWinX + 580 - 16, posRectWinY + 7))
	# Blitear bombillo sabias que
	screen.blit(sabiasque, (posRectWinX + 40,posRectWinY + 90))

	## Fuentes y textos

	# Bienvenido A
	bienvenidoA = pygame.font.SysFont("serif", 36, True).render("Conecta N!", False, negro, gris)
	# La vieja
	windows = pygame.font.SysFont("arial black", 35).render("WIN", False, negro, gris)
	# 95
	numero95 = pygame.font.SysFont("calibri", 40).render("95", True, blanco, gris)
	
	# Nombre de la ventana
	welcomeVentana = pygame.font.SysFont("freepixelregular", 15, True).render("Conecta N!", False, blanco, azul)
	# Nombre de la ventana en la barra
	welcomeBarra = pygame.font.SysFont("freepixelregular", 13, True).render("Conecta N!", False, negro, gris_claro)
	# Hora
	tiempo = pygame.font.SysFont("freepixelregular", 15).render("1:20 AM", False, negro, gris_claro)
	# Texto sabias que
	sabiasqueTexto0 = pygame.font.SysFont("freepixelregular", 15, True).render("Sabias que...", False, negro, gris_claro)
	# Texto sabias que contenido 
	sabiasqueTexto1 = pygame.font.SysFont("freepixelregular", 15).render("Puedes usar este boton!", False, negro, gris_claro)

	# Bliteo de los textos
	screen.blit(bienvenidoA, (posRectWinX + 20, posRectWinY + 32))
	screen.blit(windows, (posRectWinX + 217, posRectWinY + 27))
	screen.blit(numero95, (posRectWinX + 305, posRectWinY + 36))
	screen.blit(welcomeVentana, (posRectWinX + 4,posRectWinY + 4))
	screen.blit(welcomeBarra, (80, Y - 18))
	screen.blit(tiempo, (X - 68, Y - 20))
	screen.blit(sabiasqueTexto0, (posRectWinX + 90,posRectWinY + 100))
	screen.blit(sabiasqueTexto1, (posRectWinX + 90,posRectWinY + 150))  


# Dibuja los rectangulos de estilo win95 que pueden ser clickeados
def dibujarRectInteractivos(screen, posCuadros, posRectWinY, winlogo, negro, gris,X,Y):


	anchoRectWin = 580
	altoRectWin = 400
	posRectWinX = X/2 - anchoRectWin/2
	posRectWinY = Y/2 - altoRectWin/2
	posCuadros = posRectWinX + 20 + 410 + 15

	

	# Rectangulo Jugar
	rectJ = dibujarRectanguloWin95(screen, posCuadros, posRectWinY + 80, 120, 25, 1, 1)
	# Rectangulo Rankings
	rectR = dibujarRectanguloWin95(screen, posCuadros, posRectWinY + 80 + 25 + 8, 120, 25, 1, 1)
	# Rectangulo Salir
	rectS = dibujarRectanguloWin95(screen, posCuadros, posRectWinY + 80 + 75 + 81, 120, 25, 1, 1)
	# Rectangulo Extras
	rectE = dibujarRectanguloWin95(screen, 2, Y - 23, 70, 20, 1, 1)
	# Blitear logo win95
	screen.blit(winlogo, (4,Y - 21))   

	# Jugar
	jugar = pygame.font.SysFont("freepixelregular", 15).render("Jugar", False, negro, gris)
	# Rankings
	rankings = pygame.font.SysFont("freepixelregular", 15).render("Rankings", False, negro, gris)
	# Extras
	start = pygame.font.SysFont("freepixelregular", 13, True).render("Extras", False, negro, gris)
	# Salir
	salir = pygame.font.SysFont("freepixelregular", 15).render("Salir", False, negro, gris)

	screen.blit(jugar, (posCuadros + 40,posRectWinY + 85))
	screen.blit(rankings, (posCuadros + 30,posRectWinY + 118))
	screen.blit(salir, (posCuadros + 40,posRectWinY + 80 + 75 + 86))
	screen.blit(start, (23,Y - 18))

	return [rectJ,rectR,rectS,rectE]


# Funcion que determina si el raton esta sobre un rectangulo del menu y lo resalta
def ratonSobre(rect,posX,posY,largo,alto,tamano,texto,bool,posXfont,posYfont,screen,winlogo, negro, gris,X,Y):

	if rect.collidepoint(pygame.mouse.get_pos()):
		# Dibuja un rectangulo negro sin relleno
		pygame.draw.rect(screen, negro, [posX,posY,largo,alto], 1)
		# Dibuja el texto encima
		font = pygame.font.SysFont("{}".format("freepixelregular"),tamano, bool).render("{}".format(texto),False,negro,gris)
		screen.blit(winlogo, (4,Y - 21))
		screen.blit(font,(posXfont,posYfont))
		
		return True

	elif not rect.collidepoint(pygame.mouse.get_pos()):
		return False


# Funcion que invierte los colores del rectangulo al presionarlo
def click(posX, posY, largo, alto,texto,posXfont,posYfont,negro,gris_claro,winlogo,screen,Y,tamano=15,bool=False):
	# Dibuja un rectangulo inverso encima
	dibujarRectanguloWin95(screen, posX, posY, largo, alto, 1, 1, True)
	# Dibuja el texto correspondiente
	font = pygame.font.SysFont("{}".format("freepixelregular"),tamano, bool).render("{}".format(texto),False,negro,gris_claro)
	screen.blit(winlogo, (4,Y - 21))
	screen.blit(font,(posXfont,posYfont))


# Funcion que dibuja un rectangulo con bordes redondeados de tamaño variable
def dibujarTablero(superficie, largoTab, altoTab, X, Y,posX,posY, color,Dimension,booleano=False):
	# Dibuja una superficie que permite transparencias
	rectTablero = pygame.Surface((largoTab, altoTab)).convert_alpha()
	tablero_centro = rectTablero.get_rect()
	negro = (0,0,0,255)
	rectTablero.fill((0,0,0,0))
	p = 0
	q = 0
	r = 0
	s = 0
	# Dibuja los rectangulos y circulos que lo conforman
	pygame.draw.rect(rectTablero, color, [0,30, 100, altoTab-60])
	pygame.draw.circle(rectTablero,color,(30,altoTab-30),30)
	pygame.draw.rect(rectTablero, color, [30,0, largoTab-60, 100])
	pygame.draw.circle(rectTablero,color,(30,30),30)
	pygame.draw.rect(rectTablero, color, [largoTab-100,30, 100, altoTab-60])
	pygame.draw.circle(rectTablero,color,(largoTab-30,30),30)
	pygame.draw.rect(rectTablero, color, [30,altoTab-100, largoTab-60, 100])
	pygame.draw.circle(rectTablero,color,(largoTab-30,altoTab-30),30)
	pygame.draw.rect(rectTablero,color,[100,100, largoTab-200, altoTab-200])

	# Si es un tablero de juego, dibuja las lineas sobre el tablero
	if booleano:
		
		for nums in range(Dimension-1):
			pygame.draw.line(rectTablero,negro,[0+(largoTab//Dimension)+p,0],[0+(largoTab//Dimension)+p,altoTab],2)
			pygame.draw.line(rectTablero,negro,[0,(altoTab//Dimension)+q],[largoTab,(altoTab//Dimension)+q],2)
			p += largoTab//Dimension
			q += altoTab//Dimension

	superficie.blit(rectTablero,(posX, posY))

	return rectTablero


# Funcion que dibuja cada tablero jugable y devuelve cada casilla en ellos
def dibujarCositos(verde_feo,screen,X,Y,oscuro,Dimension,numeroDeTabs):
	# Dimensiones del tablero
	largoTab = int(2.9*X//4)
	altoTab = int(9.5*Y//10)
	diagTab = math.sqrt(largoTab*largoTab + altoTab*altoTab)
	screen.fill(verde_feo)
	rectTablero= dibujarTablero(screen, largoTab, altoTab, X, Y,15,15, oscuro,Dimension)
	tableros = []
	pos = []
	colores = [(244,67,54,200),(33,150,243,200),(139,195,74,200),(255,87,34,200),(233,30,99,200),(3,169,244,200),(205,220,57,200),(121,85,72,200),(156,39,176,200),(0,188,212,200),(255,235,59,200)]
	p = 0
	q = -56
	r = 0
	s = 0


	# Por cada tablero en el numero de tableros especificado dibuja un tablero y lo coloca en la lista tableros, al igual que su posicion
	for nums in range(numeroDeTabs):
		tableros.append(dibujarTablero(screen, 348, 344, X, Y, 15 + largoTab//2-(215+q)+p, 15 + altoTab//2-(117-q)-p,colores[nums],Dimension,True))
		pos.append([15 + largoTab//2-(215+q)+p,15 + altoTab//2-(117-q)-p])
		q += 30
		p += 25

	casillas = dibujarCasillas(Dimension,largoTab,altoTab,numeroDeTabs, screen)
	return tableros, casillas, pos


# Funcion que determina si el mouse esta sobre una casilla
def ratonSobreCasillas(rect):
	if rect.collidepoint(pygame.mouse.get_pos()):
		return True


# Funcion que dibuja las casillas en un tablero
def dibujarCasillas(Dimension,largoTab,altoTab,numeroDeTabs,screen):
	# Dibuja una superficie que permite transparencias
	superficie = pygame.Surface((348*2, 344*2)).convert_alpha()
	casillas = []
	filas = []
	r = 0
	s = 0
	p = 0 + 25*numeroDeTabs
	q = -56+ 30*numeroDeTabs

	# Por cada casilla dibuja una casilla y la coloca en la lista casillas
	for columna in range(Dimension):
		r = 0
		filas = []
		for fila in range(Dimension):
			filas.append(pygame.draw.rect(superficie,(0,0,0,255),[15 + largoTab//2-(215+q)+p+r,15 + altoTab//2-(117-q)-p+s,348//Dimension,344//Dimension]))
			r += 348//Dimension
		casillas.append(filas)
		s += 344//Dimension

	return casillas


# Funcion que dibuja la ficha en la posicion valida
def dibujarFicha(superficie, rect, screen, posX,posY,mult,turno,verde_feo,X,Y,oscuro,Dimension,numeroDeTabs,fila,casilla):
	# Dibuja los tableros que estan detras del actual
	dibujarCositos(verde_feo,screen,X,Y,oscuro,Dimension,numeroDeTabs-1)

	# Carga la imagen a dibujar
	if turno == 1:
		imagen = pygame.image.load("recursos/X{}.png".format(Dimension))

	elif turno == 2:
		imagen = pygame.image.load("recursos/O{}.png".format(Dimension))
	
	# Dibuja la imagen		
	pos = superficie.get_rect()
	q = 6*mult
	p = 5*mult
	superficie.blit(imagen,(26//Dimension + (348//Dimension)*casilla,21//Dimension + (344//Dimension)*fila))
	screen.blit(superficie,(posX+5*p-5*q,posY-5*p+5*q))
	
	return superficie


# Funcion que dibuja los tableros que sobran al cambiar de tablero
def imprimirTablerosRestantes(verde_feo,screen,largoTab,altoTab,X,Y,oscuro,Dimension,lista):
	screen.fill(verde_feo)
	# Tablero del fondo
	rectTablero = dibujarTablero(screen, largoTab, altoTab, X, Y,15,15, oscuro,Dimension)
	p = 0
	q = -56

	for tablero in lista:
		screen.blit(tablero, (15 + largoTab//2-(215+q)+p, 15 + altoTab//2-(117-q)-p))
		p += 25
		q += 30

	
# Funcion que dibuja el texto del menu donde se ingresan los nombres y la dimension
def entradatexto(screen):
	font = pygame.font.SysFont("OpenSansSemibold", 32)
	screen.fill([4, 126, 126])
	dibujarTexto("Haz click en una casilla antes de escribir.", font, screen, 34, 270, (251, 245, 239))
	dibujarTexto("Luego de ingresar la dimension presiona Enter.", font, screen, 34, 320, (251, 245, 239))
	dibujarTexto("Introduzca el nombre de los jugadores: ", font, screen, 34, 30, [251, 245, 239])
	dibujarTexto("Jugador 1: ", font, screen, 40, 105, [251, 245, 239])
	dibujarTexto("Jugador 2: ", font, screen, 40, 208, [251, 245, 239])
	dibujarTexto("Introduzca tamano del tablero: ", font, screen, 34, 380, [251, 245, 239])
	box1 = dibujarRectanguloWin95(screen, 234, 110, 233, 40, 2, 1)
	box2 = dibujarRectanguloWin95(screen, 234, 212, 233, 40, 2, 1)
	dimension = dibujarRectanguloWin95(screen, 234, 450, 233, 40, 2, 1)
	return box1, box2, dimension


# Funcion que dibuja el menu final del resultado
def resultado(jugador1, jugador2, font, screen,Dimension):
	screen.fill((4,126,126))
	# Rectangulo de fondo
	dibujarTablero(screen,700,500,800,600,50,50,(0,0,0,100),Dimension)

	# Dibuja el ganador
	if jugador1.lineas>jugador2.lineas:
		dibujarTexto(str(jugador1.nombre)+", has ganado", font, screen, 268-10*len(jugador1.nombre), 70, (255, 255, 255))
		dibujarTexto("con "+str(jugador1.lineas)+" lineas", font, screen, 275, 123, (255, 255, 255))
	elif jugador2.lineas>jugador1.lineas:
		dibujarTexto(str(jugador2.nombre)+", has ganado", font, screen, 268-10*len(jugador2.nombre), 70, (255, 255, 255))
		dibujarTexto("con "+str(jugador2.lineas)+" lineas", font, screen, 275, 123, (255, 255, 255))
	elif jugador2.lineas==jugador1.lineas:
		dibujarTexto("Empatados", font, screen, 270, 50, (255, 255, 255))

	# Dibuja los puntajes
	dibujarTexto("Puntaje Total: ", font, screen, 60,186,(255,255,255))
	dibujarTexto(jugador1.nombre + ": " + str(jugador1.puntos), font, screen, 60,249,(255,255,255))
	dibujarTexto(jugador2.nombre + ": " + str(jugador2.puntos), font, screen, 60,302,(255,255,255))

	dibujarTexto("Quieres jugar otra partida?", font, screen, 100, 400,(255,255,255))
	# Rectangulos de salir o no
	rectsi = dibujarRectanguloWin95(screen, 150, 480, 200, 50, 2, 1)
	rectno  = dibujarRectanguloWin95(screen, 450, 480, 200, 50, 2, 1)
	dibujarTexto("Si", font, screen, 230, 473,(20,20,20))
	dibujarTexto("No", font, screen, 520, 473,(20,20,20))

	return rectsi, rectno


# Funcion que dibuja la pantalla final antes de salir del juego
def salir(font, screen):
	screen.fill([4, 126, 126])
	dibujarTexto("Gracias por jugar!", font, screen, 260, 260, (255,255,255))

# Funcion que dibuja el menu de los rankings
def rancc(screen):
	font = pygame.font.SysFont("OpenSansSemibold", 32)
	screen.fill([4, 126, 126])
	dibujarTablero(screen,300,500, 800, 600,50,30,(0,0,0,100),1)
	dibujarTexto("Rankings", font, screen, 90, 30, (255,255,255))
	
	# Botones
	volveralmenu = dibujarRectanguloWin95(screen, 400, 100, 300, 50, 2, 1)
	salir2  = dibujarRectanguloWin95(screen, 400, 400, 300, 50, 2, 1)

	dibujarTexto("Volver al menu", font, screen, 430, 100,(20,20,20))
	dibujarTexto("Salir", font, screen, 500, 400,(20,20,20))

	# Lee el archivo con los puntajes y los escribe
	f = open("nombrepuntaje.txt","r+")
	s = f.readlines()
	for i in range(len(s)):
		if i<10:
			dibujarTexto(s[i], font, screen, 90, 100+40*i, (255,255,255))

	return volveralmenu, salir2


# Funcion que guarda los puntajes
def guardarpuntajes(jugador1,jugador2):

	f = open("nombrepuntaje.txt","r+")
	s = f.readlines()
	if jugador1.puntos<jugador2.puntos:
		f.writelines(str(jugador2.nombre)+"   "+str(jugador2.puntos)+'\n')
	elif jugador2.puntos<jugador1.puntos:
		f.writelines(str(jugador1.nombre)+"   "+str(jugador1.puntos)+'\n')
	elif jugador1.puntos==jugador2.puntos:
		f.writelines(str(jugador1.nombre)+"   "+str(jugador1.puntos)+'\n')
		f.writelines(str(jugador2.nombre)+"   "+str(jugador2.puntos)+'\n')
	f.close()

# Funcion que dibuja el menu de extras
def dibujarExtras(screen, dimAltas, reiniPunt):
	font = pygame.font.SysFont("OpenSansSemibold", 32)
	screen.fill((4,126,126))

	dibujarTablero(screen,640,400, 800, 600,80,80,(0,0,0,100),1)
	# Rectangulos
	VolvermenuExtras = dibujarRectanguloWin95(screen, 250,500,300,50,2,1)
	dibujarTexto("Volver al menu", font, screen, 285, 500, (0,0,0))
	# Activa la opcion de jugar con mayor facilidad en tableros de dimensiones altas
	# Cada jugada se registra en todos los tableros
	dibujarTexto("Poder jugar en", font, screen, 150, 100, (255,255,255))
	dibujarTexto("dimensiones altas", font, screen, 150, 135,(255,255,255))
	jugarEnDimA = dibujarRectanguloWin95(screen, 550,125, 100, 50, 2,1)
	if dimAltas:
		dibujarRectanguloWin95(screen, 550,125, 100, 50, 2,1)
		dibujarTexto("ON", font, screen, 570, 125,(0,0,0))
	elif not dimAltas:
		dibujarRectanguloWin95(screen, 550,125, 100, 50, 2,1)
		dibujarTexto("OFF",font,screen,570,125,(0,0,0))
	# Reinicia los puntajes
	dibujarTexto("Reiniciar puntajes", font, screen, 150, 250,(255,255,255))
	reiniciarPunt = dibujarRectanguloWin95(screen, 550, 250, 100, 50,2,1)
	if reiniPunt:
		dibujarRectanguloWin95(screen, 550, 250, 100, 50,2,1)
		dibujarTexto("DO", font, screen, 570, 250,(0,0,0))
		reiniPunt = False
	elif not reiniPunt:
		dibujarRectanguloWin95(screen, 550, 250, 100, 50,2,1)
		dibujarTexto("DO",font,screen,570,250,(0,0,0))

	return VolvermenuExtras, jugarEnDimA, reiniciarPunt


def main():
	## Pygame 
	#Inicializacion
	pygame.init()

	# Variables
	X,Y,screen,blanco,negro,verde_feo,azul,gris,gris_claro,gris_oscuro,clock,Pc95,iconos,winlogo,botonx,sabiasque,rectJugar,rectRankings,rectSalir,rectExtras,anchoRectWin,altoRectWin,posRectWinX,posRectWinY,posCuadros = variablesPygame()
	icono = pygame.image.load("recursos/icono.png")
	pygame.display.set_icon(icono)
	pygame.display.set_caption('Conecta N!')
	largoTab = int(2.9*X//4)
	altoTab = int(9.5*Y//10)
	iniciarMenu = True
	empezarJuego = False
	iniciarRank=False
	iniciarMenu = True
	iniciarExtras = False
	jugador1, jugador2 = jugadores()
	iniciarNombres=False
	runningJuego = False
	Dimension = -1
	dimensionString = ""
	enBox1 = False
	enBox2 = False

	font = pygame.font.SysFont("OpenSansSemibold", 32)
	enCuadroDim = False
	oscuro = (0,0,0,100)
	tablerosGuardados = []
	running = True
	aResultado = False
	imagen = pygame.image.load("recursos/pc.png")

	margenLeft=133
	margenSup=145
	lado = 87

	dimAltas = False
	reiniPunt = False
	runningExtras = False
	###############################################
	


	while running:
		
		# Limita al while para que solo haga 60 ciclos en 1 segundo
		clock.tick(60)
		if iniciarMenu:
			# Dibuja el menu
			dibujarMenu(X,Y,screen,blanco,negro,verde_feo,azul,gris,gris_claro,gris_oscuro,Pc95,iconos,winlogo,botonx,sabiasque)
			# Inicia los botones del menu
			rectJugar,rectRankings,rectSalir,rectExtras = dibujarRectInteractivos(screen, posCuadros, posRectWinY, winlogo, negro, gris,X,Y)
			enJugar = ratonSobre(rectJugar,posCuadros, posRectWinY + 80, 120, 25, 15,"Jugar", False,posCuadros + 40,posRectWinY + 85, screen, winlogo, negro, gris,X,Y)
			enRankings = ratonSobre(rectRankings,posCuadros, posRectWinY + 80 + 25 + 8, 120, 25, 15,"Rankings", False,posCuadros + 30,posRectWinY + 118, screen, winlogo, negro, gris,X,Y)
			enSalir = ratonSobre(rectSalir,posCuadros, posRectWinY + 80 + 75 + 81, 120, 25,15,"Salir", False, posCuadros + 40,posRectWinY + 80 + 75 + 86, screen, winlogo, negro, gris,X,Y)
			enExtras = ratonSobre(rectExtras,2, Y - 23, 70, 20, 13,"Extras", True,23,Y - 18, screen, winlogo, negro, gris,X,Y)

		# Ciclo que revisa cada evento que obtiene pygame
		for event in pygame.event.get():
			# Boton de salir de la ventana
			if event.type == pygame.QUIT:
				running = False
			# Evento de presionar un boton del mouse
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					# Si esta en el menu
					if iniciarMenu:
						# Depende en que lugar se dio click
						if enJugar:
							# Empieza la inicializacion de los nombres y la dimension
							click(posCuadros, posRectWinY + 80, 120, 25,"Jugar",posCuadros + 40,posRectWinY + 85,negro,gris_claro,winlogo,screen,Y)
							iniciarNombres = True
							box1, box2, cuadroDimension = entradatexto(screen)
							iniciarMenu = False
							empezarJuego = False
						elif enRankings:
							# Empieza la pantalla de rankings
							click(posCuadros, posRectWinY + 80 + 25 + 8, 120, 25,"Rankings",posCuadros + 30,posRectWinY + 118,negro,gris_claro,winlogo,screen,Y)
							iniciarMenu = False
							iniciarRank= True
						elif enSalir:
							# Sale del programa
							click(posCuadros, posRectWinY + 80 + 75 + 81, 120, 25,"Salir", posCuadros + 40,posRectWinY + 80 + 75 + 86,negro,gris_claro,winlogo,screen,Y)
							iniciarMenu = False
							running = False
							salir(font, screen)
						elif enExtras:
							# Empieza la pantalla de extras
							click(2, Y - 23, 70, 20,"Extras",23,Y - 18,negro,gris_claro,winlogo,screen,Y)   
							iniciarMenu = False
							iniciarExtras = True
					if iniciarRank:
						# Si esta en rankings
						# Iniciar el menu de rankings
						volveralmenu, salir2 = rancc(screen)
						if volveralmenu.collidepoint(pygame.mouse.get_pos()):
							iniciarMenu = True
							iniciarRank = False
						elif salir2.collidepoint(pygame.mouse.get_pos()):
							iniciarMenu = False
							running = False
							iniciarRank = False
							salir(font, screen)
					# Si esta en el menu extras
					if runningExtras:
						# Si dio click en volver al menu
						if extrasMenu.collidepoint(pygame.mouse.get_pos()):
							iniciarMenu = True
							runningExtras = False
							iniciarExtras = False
						# Si dio click en dimensiones altas
						elif extrasDimA.collidepoint(pygame.mouse.get_pos()) and not dimAltas:
							dimAltas = True
						# Si dio click en dimensiones altas mientras esta encendido
						elif extrasDimA.collidepoint(pygame.mouse.get_pos()) and dimAltas:
							dimAltas = False
						# Si dio click en reiniciar puntajes
						elif extrasRePunt.collidepoint(pygame.mouse.get_pos()):
							reiniPunt = True
							open('nombrepuntaje.txt', 'w').close()

					if iniciarNombres:
						# Si esta en la pantalla de iniciar los nombres 
						if box1.collidepoint(pygame.mouse.get_pos()):
							enBox1 = True
						if not box1.collidepoint(pygame.mouse.get_pos()):
							enBox1 = False
						if box2.collidepoint(pygame.mouse.get_pos()):
							enBox2 = True
						if not box2.collidepoint(pygame.mouse.get_pos()):
							enBox2 = False
						if cuadroDimension.collidepoint(pygame.mouse.get_pos()):
							enCuadroDim = True
						if not cuadroDimension.collidepoint(pygame.mouse.get_pos()):
							enCuadroDim = False

					if aResultado:
						# Si esta en la pantalla de resultado
						if rectsi.collidepoint(pygame.mouse.get_pos()):
							iniciarNombres = True
							box1, box2, cuadroDimension = entradatexto(screen)
							iniciarMenu = False
							empezarJuego = False
							p = 8*len(jugador1.nombre)
							q = 8*len(jugador2.nombre)
							r = 8*len(dimensionString)
							
							dibujarTexto(jugador1.nombre, font, screen,105+(251+233)//2-p, 105, negro)
							dibujarTexto(jugador2.nombre, font, screen, 105+(251+233)//2-q, 208, negro)
							dibujarTexto(dimensionString, font, screen, 125+(251+233)//2-r, 445, negro)
							guardarpuntajes(jugador1,jugador2)
							jugador1.puntos=0
							jugador2.puntos=0
							jugador1.lineas=0
							jugador2.lineas=0

						elif rectno.collidepoint(pygame.mouse.get_pos()):
							aResultado = False
							salir(font, screen)
							running = False
							guardarpuntajes(jugador1,jugador2)

					if runningJuego and len(tableros) > 0:
						# Si esta en la pantalla de juego
						if 0 < espacioLibre <= Dimension*Dimension*Dimension:
							# Si hay espacios libres en el tablero
							for fil in range(len(casillas)):
								for casilla in range(len(casillas[fil])): 
									if ratonSobreCasillas(casillas[fil][casilla]):
										z , y, x = numTableroActual, fil, casilla
										# Si es valida
										if esValida(superTablero, z, y, x):
											if not dimAltas:
												# Se refleja en el tablero de texto y en el grafico
												superTablero = reflejarEnTablero(superTablero,z,y,x,jugadorActual.turno)
												tableros[numTableroActual] = dibujarFicha(tableroActual,casillas[fil][casilla],screen,pos[0][0],pos[0][1],numTableroActual,jugadorActual.turno,verde_feo,X,Y,oscuro,Dimension,numeroDeTabs,y,x)
												lineasHechas = lineaHecha(superTablero, z,y,x,jugadorActual.turno,jugadorActual)
												letrajuego(screen,jugador1.nombre,jugador2.nombre,"lineas: "+str(jugador1.lineas),"lineas: "+str(jugador2.lineas),"Puntos: "+str(jugador1.puntos),"Puntos: "+str(jugador2.puntos),Dimension,X,Y)
												# Si se hizo una linea
												if lineasHechas > 0:
													jugadorActual.puntos = anadirPuntos(lineasHechas, jugadorActual)
													jugadorActual.lineas = anadirLinea(lineasHechas, jugadorActual)
													letrajuego(screen,jugador1.nombre,jugador2.nombre,"lineas: "+str(jugador1.lineas),"lineas: "+str(jugador2.lineas),"Puntos: "+str(jugador1.puntos),"Puntos: "+str(jugador2.puntos),Dimension,X,Y)
												lineasHechas = 0
												espacioLibre += -1
												# Si no quedan mas espacios libres
												if espacioLibre == 0:
													runningJuego = False
													aResultado = True
													font2 = pygame.font.SysFont("OpenSansSemibold", 45)
													pygame.mouse.set_cursor(*pygame.cursors.tri_left)
													rectsi, rectno = resultado(jugador1, jugador2, font2, screen,Dimension)
												# Si quedan espacios libres
												elif espacioLibre > 0:
													if cambiarJugador(jugadorActual.turno) == 1:
														jugadorActual = jugador1
														letrajuego(screen,jugador1.nombre,jugador2.nombre,"lineas: "+str(jugador1.lineas),"lineas: "+str(jugador2.lineas),"Puntos: "+str(jugador1.puntos),"Puntos: "+str(jugador2.puntos),Dimension,X,Y)
													elif cambiarJugador(jugadorActual.turno) == 2:
														jugadorActual = jugador2
														letrajuego(screen,jugador1.nombre,jugador2.nombre,"lineas: "+str(jugador1.lineas),"lineas: "+str(jugador2.lineas),"Puntos: "+str(jugador1.puntos),"Puntos: "+str(jugador2.puntos),Dimension,X,Y)
													# Dibuja el turno del jugador actual
													dibujarTexto(jugadorActual.nombre + ", es tu turno", font, screen, 240-10*len(jugadorActual.nombre),60,(255,255,255))
											if dimAltas:
												for i in range(Dimension):
													superTablero = reflejarEnTablero(superTablero,i,y,x,jugadorActual.turno)
													tableros[i] = dibujarFicha(tableroActual,casillas[fil][casilla],screen,pos[0][0],pos[0][1],i,jugadorActual.turno,verde_feo,X,Y,oscuro,Dimension,numeroDeTabs,y,x)
												lineasHechas = lineaHecha(superTablero, z,y,x,jugadorActual.turno,jugadorActual)
												letrajuego(screen,jugador1.nombre,jugador2.nombre,"lineas: "+str(jugador1.lineas),"lineas: "+str(jugador2.lineas),"Puntos: "+str(jugador1.puntos),"Puntos: "+str(jugador2.puntos),Dimension,X,Y)
												# Si se hizo una linea
												if lineasHechas > 0:
													jugadorActual.puntos = anadirPuntos(lineasHechas, jugadorActual)
													jugadorActual.lineas = anadirLinea(lineasHechas, jugadorActual)
													letrajuego(screen,jugador1.nombre,jugador2.nombre,"lineas: "+str(jugador1.lineas),"lineas: "+str(jugador2.lineas),"Puntos: "+str(jugador1.puntos),"Puntos: "+str(jugador2.puntos),Dimension,X,Y)
												lineasHechas = 0
												espacioLibre += -Dimension
												# Si no quedan mas espacios libres
												if espacioLibre == 0:
													runningJuego = False
													aResultado = True
													font2 = pygame.font.SysFont("OpenSansSemibold", 45)
													pygame.mouse.set_cursor(*pygame.cursors.tri_left)
													rectsi, rectno = resultado(jugador1, jugador2, font2, screen,Dimension)
												# Si quedan espacios libres
												elif espacioLibre > 0:
													if cambiarJugador(jugadorActual.turno) == 1:
														jugadorActual = jugador1
														letrajuego(screen,jugador1.nombre,jugador2.nombre,"lineas: "+str(jugador1.lineas),"lineas: "+str(jugador2.lineas),"Puntos: "+str(jugador1.puntos),"Puntos: "+str(jugador2.puntos),Dimension,X,Y)
													elif cambiarJugador(jugadorActual.turno) == 2:
														jugadorActual = jugador2
														letrajuego(screen,jugador1.nombre,jugador2.nombre,"lineas: "+str(jugador1.lineas),"lineas: "+str(jugador2.lineas),"Puntos: "+str(jugador1.puntos),"Puntos: "+str(jugador2.puntos),Dimension,X,Y)
													# Dibuja el turno del jugador actual
													dibujarTexto(jugadorActual.nombre + ", es tu turno", font, screen, 240-10*len(jugadorActual.nombre),60,(255,255,255))
										# Si no es valida se vuelve a realizar la vuelta
										elif not esValida(superTablero, z,y,x):
											error(screen)
			# Si se presiono una tecla							
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					# Cuando se presiona la flecha hacia abajo
					if runningJuego:
						# Cambia el tablero actual
						# El tablero lo coloca en una lista de tableros guardados y dibuja los restantes. Cada vez que se presiona abajo se añade otro tablero hasta quedar 1
						if len(tableros) > 1:
							numeroDeTabs = numeroDeTabs-1
							tablerosGuardados.append(tableros.pop(numTableroActual))
							numTableroActual = len(tableros)-1 
							tableroActual = tableros[numTableroActual]
							imprimirTablerosRestantes(verde_feo,screen,largoTab,altoTab,X,Y,oscuro,Dimension,tableros)
							casillas = dibujarCasillas(Dimension,largoTab,altoTab,numeroDeTabs, screen)
							dibujarTexto(jugadorActual.nombre + ", es tu turno", font, screen, 240-10*len(jugadorActual.nombre),60,(255,255,255))
							letrajuego(screen,jugador1.nombre,jugador2.nombre,"lineas: "+str(jugador1.lineas),"lineas: "+str(jugador2.lineas),"Puntos: "+str(jugador1.puntos),"Puntos: "+str(jugador2.puntos),Dimension,X,Y)

				# Si esta en el menu de ingresar los nombres
				if iniciarNombres:
					p = 8*len(jugador1.nombre)
					q = 8*len(jugador2.nombre)
					r = 8*len(dimensionString)
					# Si la tecla es enter y se dio click en el cuadro de dimensiones
					if event.key == pygame.K_RETURN and enCuadroDim:
						Dimension = dimension(int(dimensionString), screen, negro, verde_feo)
						if Dimension == -1:
							Dimension = dimension(int(dimensionString), screen, negro, verde_feo)

						elif Dimension != -1:
							empezarJuego = True
							iniciarNombres = False
					# Si la tecla es borrar y se dio click en el cuadro de jugador 1
					elif event.key == pygame.K_BACKSPACE and enBox1:
						# Eliminar el ultimo caracter
						jugador1.nombre=jugador1.nombre[:-1]
						# Dibujar el rectangulo otra vez
						dibujarRectanguloWin95(screen, 234, 110, 233, 40, 2, 1)
						dibujarTexto(jugador1.nombre, font, screen,105+(251+233)//2-p, 105, negro)

					# Si la tecla es borrar y se dio click en el cuadro de jugador 2
					elif event.key == pygame.K_BACKSPACE and enBox2:
						# Eliminar el ultimo caracter
						jugador2.nombre=jugador2.nombre[:-1]
						# Dibujar el rectangulo otra vez
						dibujarRectanguloWin95(screen, 234, 212, 233, 40, 2, 1)
						dibujarTexto(jugador2.nombre, font, screen, 105+(251+233)//2-q, 208, negro)

					# Si la tecla es borrar y se dio click en el cuadro de dimensiones
					elif event.key == pygame.K_BACKSPACE and enCuadroDim:
						# Eliminar el ultimo caracter
						dimensionString=dimensionString[:-1]
						# Dibujar el rectangulo otra vez
						dibujarRectanguloWin95(screen, 234, 450, 233, 40, 2, 1)
						dibujarTexto(dimensionString, font, screen, 125+(251+233)//2-r, 445, negro)

					# Si el nombre tiene menos de 10 caracteres y se dio click en el cuadro de jugador 1
					elif len(jugador1.nombre) < 10 and enBox1:
						# Se escribe la tecla presionada
						jugador1.nombre+=event.unicode
						dibujarRectanguloWin95(screen, 234, 110, 233, 40, 2, 1)
						dibujarTexto(jugador1.nombre, font, screen, 95+(251+233)//2-p, 105, negro)

					# Si el nombre tiene menos de 10 caracteres y se dio click en el cuadro de jugador 2
					elif len(jugador2.nombre) < 10 and enBox2:
						# Se escribe la tecla presionada
						jugador2.nombre+=event.unicode
						dibujarRectanguloWin95(screen, 234, 212, 233, 40, 2, 1)
						dibujarTexto(jugador2.nombre, font, screen, 95+(251+233)//2-q, 208, negro)

					# Si el nombre tiene menos de 10 caracteres y se dio click en el cuadro de jugador 1
					elif len(dimensionString) < 2 and enCuadroDim:
						# Se escribe la tecla presionada
						dimensionString+=event.unicode
						dibujarRectanguloWin95(screen, 234, 450, 233, 40, 2, 1)
						dibujarTexto(dimensionString, font, screen, 100+(251+233)//2-r, 445, negro)

				# Si se presiona la flecha hacia arriba
				if event.key == pygame.K_UP:
					if runningJuego:
						# Se añaden los tableros guardados a la lista de tableros y se dibujan
						if len(tablerosGuardados) > 0:
							numeroDeTabs = numeroDeTabs+1
							tableros.append(tablerosGuardados.pop(len(tablerosGuardados)-1))
							numTableroActual = len(tableros)-1 
							tableroActual = tableros[numTableroActual]
							imprimirTablerosRestantes(verde_feo,screen,largoTab,altoTab,X,Y,oscuro,Dimension,tableros)
							casillas = dibujarCasillas(Dimension,largoTab,altoTab,numeroDeTabs, screen)
							dibujarTexto(jugadorActual.nombre + ", es tu turno", font, screen, 240-10*len(jugadorActual.nombre),60,(255,255,255))
							letrajuego(screen,jugador1.nombre,jugador2.nombre,"lineas: "+str(jugador1.lineas),"lineas: "+str(jugador2.lineas),"Puntos: "+str(jugador1.puntos),"Puntos: "+str(jugador2.puntos),Dimension,X,Y)
		# Si se inicio el menu extras
		if iniciarExtras:
			extrasMenu, extrasDimA, extrasRePunt= dibujarExtras(screen, dimAltas, reiniPunt)
			runningExtras = True
		
		if empezarJuego:
			# Si el juego va a empezar, se inicializan las variables
			OtraPartida = True
			tablerosGuardados = []
			superTablero = variables(Dimension)
			numeroDeTabs = Dimension
			tableros, casillas, pos = dibujarCositos(verde_feo,screen,X,Y,oscuro,Dimension,Dimension)
			numTableroActual = len(tableros)-1
			tableroActual = tableros[numTableroActual]
			runningJuego = True
			empezarJuego = False
			espacioLibre = Dimension*Dimension*Dimension
			turno = elegirJugador()
			letrajuego(screen,jugador1.nombre,jugador2.nombre,"lineas: "+str(jugador1.lineas),"lineas: "+str(jugador2.lineas),"Puntos: "+str(jugador1.puntos),"Puntos: "+str(jugador2.puntos),Dimension,X,Y)
			# Si hay espacio libre se cambia el cursor de acuerdo al jugador actual
			if espacioLibre <= Dimension*Dimension*Dimension:
				
				if turno == jugador1.turno:
					jugadorActual = jugador1
					pygame.mouse.set_cursor(*pygame.cursors.broken_x)
				
				elif turno == jugador2.turno:
					jugadorActual = jugador2
					pygame.mouse.set_cursor(*pygame.cursors.diamond)

			dibujarTexto(jugadorActual.nombre + ", es tu turno", font, screen, 240-10*len(jugadorActual.nombre),60,(255,255,255))
		# Actualiza la superficie
		pygame.display.flip()
	# Congela el juego antes de cerrar
	pygame.time.wait(1000)

main()
