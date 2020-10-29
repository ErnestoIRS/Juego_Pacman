#A00827434 Ernesto García González
#A00827107 Regina González Quijano

from random import choice
from turtle import *
from freegames import floor, vector

#Variable que indica el puntaje.
state = {'score': 0}

#Puntero que indica el camino que sigue pacman
path = Turtle(visible=False)

#Puntero que indica en donde se va a mostrar el puntaje
writer = Turtle(visible=False)

#Vector que indica la dirección de movimiento
aim = vector(5, 0)

#Vector que indica la posición inicial de pac-man
pacman = vector(-40, -80)

#Vectores que indican la posición inicial de los fantasmas
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

#Matriz que indica la forma del laberinto. 0=no hay camino, 1=camino
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

#Función que se encarga de dibujar los recuadros que indican el camino
def square(x, y):
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    #Se dibuja un recuadro con las dimensiones dadas
    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

#Función que regresa la posición de cierto punto en el mapa
def offset(point):
    "Return offset of point in tiles."
    
    #Escala las posiciones en x y en y a las medidas de cada cuadro del mapa.
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

#Función que valida si el punto indicado por la funcion offset es parte del camino o no
def valid(point):
    "Return True if point is valid in tiles."
    index = offset(point)
    
    #Si las coordenadas del punto son un 0 en tiles, regresa false.
    if tiles[index] == 0:
        return False
    
    #Cambia las coordenadas de index para evaluar la posición de la "esquina" contraria, simulando un cuadrado
    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    #En caso de no cumplir las condiciones anteriores, regresa la posición dada inicialmente (true)
    return point.x % 20 == 0 or point.y % 20 == 0

#Función que dibuja el juego
def world():
    "Draw world using path."
    #Se indica el color del camino y de las barreras
    bgcolor('black')
    path.color('blue')
    
    #Evalua cuadro por cuadro en "tiles"
    for index in range(len(tiles)):
        tile = tiles[index]
        
        #Si el cuadro es 1 en tiles, se dibuja un cuadrado
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            
            #Si el cuadro es 1 en tiles, dibuja un punto blanco (comida).
            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')
                     
#Función para el movimiento del pacman y de los fantasmas
def move():
    "Move pacman and all ghosts."
    #Se inicializa el marcador
    writer.undo()
    writer.write(state['score'])

    clear()
    
    #Se valida si la posición a la que se dirige pac-man esta dentro delo camino, si no es asi no se mueve.
    if valid(pacman + aim):
        pacman.move(aim)

    #Regresa la posición actual de pac-man
    index = offset(pacman)

    #Si en la posición actual de pac-man hay comida, se cambia el valor de esa posición a 2 en tiles para simular que ya no hay comida
    #y se aumenta en 1 el marcador
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    #Función que se encarga de dibujar a pac-man en cada posicion a la que se mueve
    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    #Función que maneja el movimiento de los fantasmas
    for point, course in ghosts:
        
        #Se valida que exista camino hacia donde se dirige el fantasma
        if valid(point + course):
            point.move(course)
       
        #Si el fantasma llega al final del camino cambia de dirección tomando como prioridad la dirección de pac-man
        elif valid(point + aim):
            point.move(aim)
        
        #Si no esta disponible esa dirección, toma un camino aleatoria pero aumenta de velocidad.
        else:
            options = [
                vector(20, 0),
                vector(-20, 0),
                vector(0, 20),
                vector(0, -20),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y     
                   
        #Funcion que se encarga de dibujar a los fantasmas en cada posicion a la que se mueven.
        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    #Si la posición de pacman llega a chocar con la de los fantasmas, termina el juego.
    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return
    
    #Controla la frecuencia en la que se realiza la función move(). Controla la velocidad de todo.
    ontimer(move, 50)

#Determina si la dirección actual de pac-man puede ser modificada por las teclas. Esto dependiendo de si existe camino o no.
def change(x, y):
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

#Se crea la ventana de juego.
setup(420, 420, 370, 0)

#Se inicializa turtle
hideturtle()
tracer(False)

#Se inicializa el marcador en la posición dada
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()

#Claves de teclas para controlar el movimiento
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')

#Se inicia el juego
world()
move()
done()
