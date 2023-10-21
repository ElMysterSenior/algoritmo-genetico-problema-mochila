import random
import tabulate  #  instalar este módulo con "pip install tabulate"

#Clase para hacer mas visible la salida por codigo de las etapas del algoritmo genetico
class bcolors:
    OK = '\033[92m'  # Verde
    YELLOW = '\033[93m'  # Amrillo
    FAIL = '\033[91m'  # Rojo
    RESET = '\033[0m'  # Reestablecer color
    BLUE = '\033[94m'  # Azul
    CYAN = '\033[96m'  # Cian
    MAGENTA = '\033[95m'  # Morado
    WHITE = '\033[97m'  # Blanco
    BLACK = '\033[90m'  # Nergro



# Leer los datos del archivo
with open("lista_productos.txt", "r") as archivo:
    lineas = archivo.readlines()

valores = []
for linea in lineas:
    partes = linea.strip().split(',')
    nombre_producto = partes[0]
    valor1 = float(partes[1])
    valor2 = int(partes[2])
    array_valores = [nombre_producto, valor1, valor2]
    valores.append(array_valores) # Almacenando los datos de los productos en una lista


# Solicitando al usuario el número de mochilas y generaciones
num_mochilas = int(input("Ingrese cuántas mochilas desea llenar: "))
# Asegurar que el número de mochilas sea par
if num_mochilas % 2 != 0:
    num_mochilas += 1
    print(f"El número de mochilas se ha ajustado a {num_mochilas} para mantenerlo par.")
num_generaciones = int(input("Ingrese el número de generaciones: "))

##################################Datos dados por el usuario######################################


limite_mochila = 2.1  # Límite de peso de la mochila
prob_mutacion = .1  # Probabilidad de mutación
calorias_minimas = 2700 #Minimo de calorias impuestas por el usuario


##################################################################################################

 # Genera una mochila con una representación binaria aleatoria con valores de 1's o 0's
def crear_mochila(num_lineas):
    return [random.randint(0, 1) for _ in range(num_lineas)]

 # Evalúa el peso y las calorías de una mochila
def evaluar_mochila(mochila):
    peso_total = 0
    calorias_totales = 0
    for i in range(len(mochila)):
        if mochila[i] == 1:
            peso_total += valores[i][1] #Segundo valor de la lista (Nombre del producto, PESO, calorias)
            calorias_totales += valores[i][2] #Tercer valor de la lista (Nombre del producto, Peso, CALORIAS)
    return peso_total, calorias_totales


 # Selecciona las mochilas válidas y las mejores mochilas para la siguiente generación
 # PRIMERO SE ASEGURA QUE ESTE DENTRO DEL LIMITE PARA POSTERIORMENTE ORDENAR POR EL MAYOR NUMERO DE CALORIAS
def seleccion(mochilas):
    mochilas_validas = [mochila for mochila in mochilas if mochila[1] <= limite_mochila and mochila[2] >=calorias_minimas]
    mochilas_validas.sort(key=lambda x: x[2], reverse=True)
    seleccionados = mochilas_validas[:num_mochilas // 2]
    return seleccionados


 # Realiza un cruce de un punto entre dos mochila
 # ESTO DE MANERA RANDOM SIEMPRE Y CUANDO NO SEA EL CALOR 0 O EL ULTIMO +1
def cruce(padre1, padre2):
    punto_cruce = random.randint(1, len(padre1) - 2)

 # Creacion de los hijos a partir del punto de cruce seleccionado
 # La primera parte del padre uno y la segunda del padre dos, luego a la inversa para el segundo hijo
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]

    #print(bcolors.CYAN+f"Punto de cruce: {punto_cruce}"+bcolors.RESET)
    #print(f"Padre 1: {padre1}")
    #print(f"Padre 2: {padre2}")
    #print(bcolors.BLUE+f"Parte del Padre 1: {padre1[:punto_cruce]}"+bcolors.RESET)
    #print(bcolors.BLUE+f"Parte del Padre 2: {padre2[punto_cruce:]}"+bcolors.RESET)
    #print(f"Hijo 1: {hijo1}")
    #print(f"Hijo 2: {hijo2}")

    return hijo1, hijo2


def mutacion(mochila):
    # Esta función ahora mutará un gen aleatorio en la mochila
    indice_gen_a_mutar = random.randint(0, len(mochila) - 1)
    mochila_mutada = mochila.copy()
    mochila_mutada[indice_gen_a_mutar] = 1 - mochila[indice_gen_a_mutar]
    return mochila_mutada

 # Imprime una tabla con las mochilas, su peso y sus calorías
def imprimir_mochilas(mochilas, titulo):
    print(titulo)
    headers = ["Mochila", "Peso", "Calorías"]
    table = []
    for mochila, peso, calorias in mochilas:
        color = bcolors.OK if peso <= limite_mochila and calorias >= calorias_minimas else bcolors.FAIL
        table.append((color + str(mochila) + bcolors.RESET, color + str(peso) + bcolors.RESET, color + str(calorias) + bcolors.RESET))
   # print(tabulate.tabulate(table, headers, tablefmt="grid"))
    #print()  # Imprimir una línea en blanco para separar las secciones


# Inicializar población
poblacion = [crear_mochila(len(valores)) for _ in range(num_mochilas)]
mejores_por_generacion = []

# Ejecutar algoritmo genético
for generacion in range(num_generaciones):
    #print(bcolors.YELLOW + f"\nGeneración {generacion + 1}:")

    # Evaluar población
    mochilas_evaluadas = [(mochila, *evaluar_mochila(mochila)) for mochila in poblacion]
    #imprimir_mochilas(mochilas_evaluadas, bcolors.YELLOW+"Población inicial:"+bcolors.RESET)

    # Cruzar individuos
    nueva_poblacion = []
    for i in range(0, len(poblacion), 2):
        hijos = cruce(poblacion[i], poblacion[i + 1])
        nueva_poblacion.extend(hijos)


    # Mutar nueva población
    if random.random() < prob_mutacion:  # random.random() genera un número entre 0 y 1
        indice_mochila_a_mutar = random.randint(0, len(nueva_poblacion) - 1)
        #print(bcolors.YELLOW+f"Mochila a mutar (antes): {nueva_poblacion[indice_mochila_a_mutar]}"+bcolors.RESET)  # Agregar esta línea
        nueva_poblacion[indice_mochila_a_mutar] = mutacion(nueva_poblacion[indice_mochila_a_mutar])
        #print(bcolors.YELLOW+f"Mochila mutada (después): {nueva_poblacion[indice_mochila_a_mutar]}"+bcolors.RESET)  # Agregar esta línea

    poblacion = nueva_poblacion
    mochilas_mutadas_evaluadas = [(mochila, *evaluar_mochila(mochila)) for mochila in poblacion]
    #imprimir_mochilas(mochilas_mutadas_evaluadas, "Población después de mutación:" + bcolors.RESET)
    
    # Encontrar y guardar el más apto de esta generación
    mejor_de_generacion = None
    mochilas_validas_generacion = [mochila for mochila in mochilas_evaluadas if mochila[1] <= limite_mochila and mochila[2] >=calorias_minimas]
    if mochilas_validas_generacion:
        mochilas_validas_generacion.sort(key=lambda x: x[2], reverse=True)
        mejor_de_generacion = mochilas_validas_generacion[0]
    if mejor_de_generacion:
        mejores_por_generacion.append((generacion + 1, mejor_de_generacion))



# Evaluar población final

mochilas_evaluadas = [(mochila, *evaluar_mochila(mochila)) for mochila in poblacion]
# Filtrar mochilas dentro del límite de peso y que cumplan con el límite de calorías
mochilas_validas = [mochila for mochila in mochilas_evaluadas if mochila[1] <= limite_mochila and mochila[2] >= calorias_minimas]
mochilas_validas.sort(key=lambda x: x[2], reverse=True)  # Ordenar por calorías



# Imprimir los mejores de cada generación
print(bcolors.YELLOW + "\nMejores de cada generación:")
headers = ["Generación", "Mochila", "Peso", "Calorías"]
table = [(gen, str(mochila), peso, calorias) for gen, (mochila, peso, calorias) in mejores_por_generacion]
print(tabulate.tabulate(table, headers, tablefmt="grid"))

# Encontrar y imprimir el mejor total

# Ordena la lista 'mejores_por_generacion' en orden descendente basado en el número de calorías.
# Cada elemento en 'mejores_por_generacion' es una tupla, donde el segundo elemento (x[1]) es otra tupla
# que contiene información sobre una mochila, y el tercer elemento de esta sub-tupla (x[1][2]) representa
# el número de calorías de la mochila.
# El argumento 'key' especifica una función lambda que extrae el número de calorías de cada mochila,
# que se utiliza como la clave de comparación para el ordenamiento.
# El argumento 'reverse=True' indica que el ordenamiento debe ser en orden descendente, es decir,
# las mochilas con más calorías aparecerán primero en la lista.
mejores_por_generacion.sort(key=lambda x: x[1][2], reverse=True)  # Ordenar por calorias
# Ordenar por calorias
if mejores_por_generacion:
    mejor_total = mejores_por_generacion[0]
    print(bcolors.OK + "\nMejor total:")
    print(f"Generación: {mejor_total[0]}")
    print("Contenido de la mochila:", mejor_total[1][0])
    print(f"Calorías totales: {mejor_total[1][2]}")
    print(f"Peso total: {mejor_total[1][1]}"+bcolors.RESET)
else:
    print(bcolors.FAIL + "No se encontró ninguna mochila válida dentro del límite de peso."+bcolors.RESET)