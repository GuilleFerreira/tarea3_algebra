import numpy as np

def lightsOut(matriz, n):
    luces = [] # Sistema de equaciones
    for i in range(n):
        for j in range(n):
            luz = [0] * (n ** 2 + 1) # Inicializa la luz (ecuación) que contendrá los valores de la misma
            luz[i * n + j] = 1  # Coeficiente de la luz actual
            luz[-1] = matriz[i][j]  # Resultado esperado (encendido o apagado)

            lucesCercanas = [
                (i - 1, j),  # Luz superior
                (i + 1, j),  # Luz inferior
                (i, j - 1),  # Luz izquierda
                (i, j + 1),  # Luz derecha
            ]

            for x, y in lucesCercanas:
                if 0 <= x < n and 0 <= y < n:
                    luz[x * n + y] = 1  # Coeficientes de las luces cercanas

            luces.append(luz)

    # Eliminación gaussiana
    for i in range(n ** 2):
        fila = i
        while fila < n ** 2 and luces[fila][i] == 0:
            fila += 1

        if fila == n ** 2:
            continue

        luces[i], luces[fila] = luces[fila], luces[i]

        for j in range(i + 1, n ** 2):
            if luces[j][i] == 1:
                for k in range(i, n ** 2 + 1):
                    luces[j][k] ^= luces[i][k]

    # Sustitución hacia atrás
    solucion = [luces[i][-1] for i in range(n ** 2)]
    for i in range(n ** 2 - 1, -1, -1):
        for j in range(i + 1, n ** 2):
            solucion[i] ^= luces[i][j] & solucion[j]

    solucionTemp = [solucion[i * n: (i + 1) * n] for i in range(n)]
    solucionVector = [element for row in solucionTemp for element in row]
    return solucionVector


# Pide al usuario el orden de la matriz, verificando que sea un numero y sea mayor o igual a 2
def pedirN():
    while True:
        try:
            n = int(input("\nIngrese el orden de la matriz cuadrada: "))
            n = int(n)
            if n >= 2:
                break
            else:
                print("El número debe ser mayor o igual a 2. Intente nuevamente.")
        except ValueError:
            print("Eso no es un número entero válido. Intente nuevamente.")
    return n

# Crea la matriz ingresada por el usuario
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

    # Retorna la matriz
    return matriz

# Imprime el vector en "formato matriz" para que sea mas amigable al usuario.
def convertirVector(vector,n):
    texto = "\nSolución"
    fila_actual = 1
    for i in range(0, len(vector), n):
        fila = vector[i:i + n]
        texto += f"\nFila {fila_actual}: {fila}"
        fila_actual += 1
    texto += "\n"
    print(texto)
    return

# Funcion principal que llama a todas las funciones necesarias para resolver el problema.
def jugar():
    n = pedirN()
    matriz = crearMatriz(n)
    solucion = lightsOut(matriz, n)
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