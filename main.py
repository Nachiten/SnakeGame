import pygame
import random

# import time
# from datetime import datetime

pygame.init()


class Arriba:
    def moverse(self):
        realizarMovimiento(0, -1)


class Abajo:
    def moverse(self):
        realizarMovimiento(0, 1)


class Derecha:
    def moverse(self):
        realizarMovimiento(1, 0)


class Izquierda:
    def moverse(self):
        realizarMovimiento(-1, 0)


def realizarMovimiento(offsetX, offsetY):
    global run
    global posicionAAgregar
    global cantComidaRecogida
    global segundosDelay

    posAnteriorBloque = posicionesVibora[0]

    moverPrimerBloque(offsetX, offsetY)
    if choqueConVibora():
        run = False

    # print("Cant comida recogida: " + str(cantComidaRecogida))

    if recogiComida():
        cantComidaRecogida += 1

        if cantComidaRecogida % 3 == 0:
            segundosDelay = max(0.03, segundosDelay - 0.05)
            print("Segundos delay cambia a: " + str(segundosDelay))

        agregarUnBloque()
        generarComidaEnPosicionRandom()

    for num in range(1, len(posicionesVibora)):
        # Si es la ultima posicion dejo la referencia
        # para cuando agregue un nuevo bloque
        if num == len(posicionesVibora) - 1:
            posicionAAgregar = posicionesVibora[num]
            # print("Posicion a agregar: " + str(posicionAAgregar))

        posAnteriorBloqueCopia = posicionesVibora[num]
        posicionesVibora[num] = posAnteriorBloque
        posAnteriorBloque = posAnteriorBloqueCopia


def generarComidaEnPosicionRandom():

    global posicionComida

    while True:
        posX = random.randint(0, cantColumnas - 1)
        posY = random.randint(0, cantFilas - 1)

        posicionFinal = (posX, posY)

        if not esPosicionDeSerpiente(posicionFinal):
            break

    posicionComida = posicionFinal


def esPosicionDeSerpiente(posicion):
    for unaPosicion in posicionesVibora:
        if unaPosicion == posicion:
            return True
    return False


def recogiComida():
    return posicionesVibora[0] == posicionComida


def choqueConVibora():
    for num in range(1, len(posicionesVibora)):
        if posicionesVibora[num] == posicionesVibora[0]:
            print("Chocaste con la vibora")
            return True
    return False


def moverPrimerBloque(offsetX, offsetY):
    posX = posicionesVibora[0][0]
    posY = posicionesVibora[0][1]

    posicionFinalX = posX + offsetX
    posicionFinalY = posY + offsetY

    # print("PosFinalX(antes): " + str(posicionFinalX))
    # print("PosFinalY(antes): " + str(posicionFinalY))

    if posicionFinalX == -1:
        posicionFinalX = cantColumnas - 1

    if posicionFinalX == cantColumnas:
        posicionFinalX = 0

    if posicionFinalY == -1:
        posicionFinalY = cantFilas - 1

    if posicionFinalY == cantFilas:
        posicionFinalY = 0

    # print("PosFinalX(dsp): " + str(posicionFinalX))
    # print("PosFinalY(dsp): " + str(posicionFinalY))

    posicionesVibora[0] = (posicionFinalX, posicionFinalY)


def dibujarRectangulo(colores, fila, columna):
    pygame.draw.rect(ventana,
                     colores,  # Color
                     (y + fila * (alto + 3), x + columna * (ancho + 3), ancho,
                      alto))  # posx, posy, ancho, alto


def dibujarTabla():
    # Generar matriz de cuadrados
    for columnaFuncion in range(0, cantFilas):
        for filaFuncion in range(0, cantColumnas):

            color = colorBloquesFondo

            # Evaluar las posiciones de los bloques iniciales
            for (unaFila, unaCol) in posicionesVibora:
                if (filaFuncion == unaFila) & (columnaFuncion == unaCol):
                    color = colorVibora

                    # Estoy en la cabeza, va de color distinto
                    if (unaFila, unaCol) == posicionesVibora[0]:
                        color = colorCabeza
                    break

            dibujarRectangulo(color, filaFuncion, columnaFuncion)


def dibujarComida():
    dibujarRectangulo(colorComida, posicionComida[0], posicionComida[1])


def obtenerInput():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            global run
            run = False
        if evento.type == pygame.KEYDOWN:
            pass

    pressed = pygame.key.get_pressed()

    global direccionActual
    global movimiento

    if pressed[pygame.K_LEFT]:
        if direccionActual != "D":
            print("Moviendo Izquierda")
            direccionActual = "I"
            movimiento = Izquierda()
        else:
            print("No puedo moverme Izquierda porque me estoy moviendo Derecha")
    if pressed[pygame.K_RIGHT]:
        if direccionActual != "I":
            print("Moviendo Derecha")
            direccionActual = "D"
            movimiento = Derecha()
        else:
            print("No puedo moverme Derecha porque me estoy moviendo Izquierda")
    if pressed[pygame.K_UP]:
        if direccionActual != "AB":
            print("Moviendo Arriba")
            direccionActual = "AR"
            movimiento = Arriba()
        else:
            print("No puedo moverme Arriba porque me estoy moviendo Abajo")
    if pressed[pygame.K_DOWN]:
        if direccionActual != "AR":
            print("Moviendo Abajo")
            direccionActual = "AB"
            movimiento = Abajo()
        else:
            print("No puedo moverme Abajo porque me estoy moviendo Arriba")
    if pressed[pygame.K_p]:
        agregarUnBloque()


def agregarUnBloque():
    posicionesVibora.append(posicionAAgregar)
    print("Se agrega un bloque en: " + str(posicionAAgregar))


def ejecutarUnMovimiento():
    obtenerInput()
    movimiento.moverse()
    dibujarTabla()
    dibujarComida()
    actualizarContadorPuntos()
    pygame.display.update()
    pygame.time.delay(int(segundosDelay * 1000 / 4))
    obtenerInput()
    pygame.time.delay(int(segundosDelay * 1000 / 4))
    obtenerInput()
    pygame.time.delay(int(segundosDelay * 1000 / 4))
    obtenerInput()
    pygame.time.delay(int(segundosDelay * 1000 / 4))


def actualizarContadorPuntos():
    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', 12)

    # create a text suface object,
    # on which text is drawn on it.
    text = font.render('Cantidad Puntos: ' + str(cantComidaRecogida), True, (200, 200, 200), (0, 0, 0))

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object.
    textRect.center = (500, 20)

    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    ventana.blit(text, textRect)


# Comienza ejecucion

# Variables Importantes [Globales]
# Posicion Bloques
x = 20
y = 20

# Tamaño bloques
ancho = 11
alto = 11
# Matriz
cantFilas = 20
cantColumnas = 20

# Configuracion
anchoVentana = 600  # Default 900x900
altoVentana = 600
segundosDelay = 0.2
estaEnPausa = True
colorBloquesFondo = (50, 50, 50)
colorVibora = (255, 50, 50)
colorCabeza = (255, 0, 0)
colorComida = (0, 255, 0)


pygame.display.set_caption("Snake Game")

posicionesVibora = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0)]

# Setup Inicial
ventana = pygame.display.set_mode((anchoVentana, altoVentana))

# Direccion de movimiento
direccionActual = "AB"
movimiento = Abajo()

posicionAAgregar = (0, 0)
posicionComida = (0, 0)
cantComidaRecogida = 0

generarComidaEnPosicionRandom()


run = True

while run:
    ejecutarUnMovimiento()


while True:
    obtenerInput()
    pygame.time.delay(int(0.5 * 1000))

pygame.quit()
