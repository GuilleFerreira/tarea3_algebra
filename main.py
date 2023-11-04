import numpy as np

# Función que cambia el estado de las luces adyacentes de la matriz
# que recibe y en las coordenadas que recibe.
def changeLights(matrix, row, col):
    n = len(matrix)
    actual = (0, 0)
    up = (-1, 0)
    bottom = (1, 0)
    left = (0, -1)
    right = (0, 1)

    for rowDirection, colDirection in [actual, up, bottom, left, right]:
        new_row, new_col = row + rowDirection, col + colDirection
        
        #Chequea si las coords estan dentro de la matriz
        if 0 <= new_row < n and 0 <= new_col < n: 
            matrix[new_row][new_col] = 1 - matrix[new_row][new_col]

#Funcion que devuelve True si la matriz está toda apagado y 
#False en caso contrario
def allLightsOff(matrix):
    n = len(matrix)
    return np.array_equal(np.zeros((n, n), dtype=int), matrix)
     
def lightsOutSolution(initialMatrix):
    n = len(initialMatrix)

    #Funcion que recorre la matriz de manera recursiva, de izquierda a derecha y
    # de arriba hacia abajo buscando la solucion.
    def iterateMatrix(matrix, row, col):

        #Si ya se recorrio toda la matriz, se verifica si todas las luces
        #estan apagadas.
        if row == n:
            return allLightsOff(matrix), []
        
        #Si no se ha recorrido todo, se calcula la siguiente celda hacia la que 
        #se debe mover.
        next_row, next_col = row, col + 1
        if next_col == n:
            next_row, next_col = row + 1, 0

        #Se hace una llamada recursiva en la que NO se presiona la luz actual.
        #noPressingLight indicara si no presionar la luz actual conduce a un tablero
        #apagado y noPressingLight_Lights sera una lista de las luces que se deben presionar
        #en esa rama del arbol de recursion
        noPressingLight, noPressingLight_Lights = iterateMatrix(matrix.copy(), next_row, next_col)
        
        #Se presiona la luz actual
        changeLights(matrix, row, col)

        #Se hace una llamada recursiva en la que se presiona la luz actual.
        #pressingLight indica que si la luz actual conduce a un tablero apagado
        #y pressingLight_Lights sera una lista de las luces que se deben presionar en 
        #esa rama del arbol de recursion 
        pressingLight, pressingLight_Lights = iterateMatrix(matrix.copy(), next_row, next_col)

        #Si conduce a un tablero apagado, se agrega la celda actual a la lista
        #y se devuelve pressingLight, pressingLight_Lights, esto significa que esta
        #celda es parte de la solucion.
        if(pressingLight):
            pressingLight_Lights.append((row, col))
            return pressingLight, pressingLight_Lights
        return noPressingLight, noPressingLight_Lights
    
    #Me quedo con la lista de la funcion, no con el valor booleano 
    _, lightsToPress = iterateMatrix(initialMatrix.copy(), 0, 0)
    
    #Itera a traves de todos los indices posibles de un vector n^2 que representa todas las luces del tablero.
    #Cada indice "i" es una luz en el tablero.
    #Para cada indice "i" se calcula la coordenada de fila(i // n) y columna(i % n) y se verifica
    #si esta presente en lightsToPress, que tiene las coordeandas de la solucion del juego.
    #Si estan, el valor en el vector creado va a ser 1, y si no, 0.
    solutionVector = [1 if (i // n, i % n) in lightsToPress else 0 for i in range(n**2)]
    return solutionVector

# Pide al usuario el tamaño de la matriz, verificando que sea un numero y sea mayor o igual a 2
def pedirN():
    while True:
        try:
            n = int(input("\nIngrese el tamaño de la matriz cuadrada: "))
            n = int(n)
            if n >= 2:
                break
            else:
                print("El número debe ser mayor o igual a 2. Intente nuevamente.")
        except ValueError:
            print("Eso no es un número entero válido. Intente nuevamente.")
    return n

def crearMatriz(n):
    # Crear una matriz de ceros de tamaño n x n
    matriz = np.zeros((n, n), dtype=int)

    # Pedir al usuario que ingrese las filas de la matriz separadas por comas
    print("\nIngrese las filas de la matriz separadas por comas (0s Verde y 1s Rojo):")
    for i in range(n):
        fila_input = input(f"Fila {i + 1}: ").strip().split(',')
        
        while len(fila_input) != n:
            print(f"Debe ingresar exactamente {n} valores por fila.")
            fila_input = input(f"Fila {i + 1}: ").strip().split(',')

        try:
            fila = [int(valor) for valor in fila_input]
            if all(valor == 0 or valor == 1 for valor in fila):
                matriz[i] = fila
            else:
                print("Los valores deben ser 0 o 1. Intente nuevamente.")
                i -= 1  # Volver a pedir la fila si los valores no son 0 o 1
        except ValueError:
            print("Ingrese solo valores numéricos (0 o 1). Intente nuevamente.")

    # Mostrar la matriz resultante
    return matriz

# Imprime el vector en "formato matriz" para que sea mas amigable al usuario.
def convertirVector(vector,n):
    texto = "\nSolución"
    fila_actual = 1
    for i in range(0, len(vector), n):
        fila = vector[i:i + n]
        #print(f"Fila {fila_actual}: {fila}")
        texto += f"\nFila {fila_actual}: {fila}"
        fila_actual += 1
    texto += "\n"
    print(texto)
    return

# Funcion principal que llama a todas las funciones necesarias para resolver el problema.
def jugar():
    n = pedirN()
    matriz = crearMatriz(n)
    solucion = lightsOutSolution(matriz)
    convertirVector(solucion,n)
    print("Vector solución:", solucion, "\n")
    return

# Permite jugar varias veces.
while True:
    jugar()
    jugar_de_nuevo = input("¿Quieres jugar de nuevo? (s/n): ")
    if jugar_de_nuevo.lower() != 's':        
        break
    print("\n======================================================")

print("\nGracias por jugar.\n")