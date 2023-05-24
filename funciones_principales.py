import re
import os
import json
# 1.0>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# def cargar_datos_desde_archivo(archivo_csv: str) -> list:
#     lista = []
#     with open(archivo_csv, "r", encoding='utf-8') as file:    #lo abro en modo lectura
#         for elemento in file:   #Itero cada linea del archivo
#             elemento = elemento.replace("\n", "")  #remplazo los salto de linea por ""
#             lista.append(elemento.split(","))   #Como los csv terminan en coma, me lo divide y transforma a lista a partir de esa coma.
#     return lista

def cargar_datos_desde_archivo(archivo: str) -> str:
    lista = []
    with open(archivo, 'r', encoding="utf-8") as archivo_csv:
        contenido = archivo_csv.readlines()[1:]     #leo todas las lineas a partir de la 2da linea
        for linea in contenido:
            fila = linea.strip().split(',')   #dividido por las comas y elimnino el \n con el strip
            lista.append(fila)
    return lista

def transformar_entero_o_flotante(num: int or float):
    #Recibe un entero o un flotante
    try:  #que intente transforma a entero el numero recibido
        num = int(num)   #si no es un entero, da un error de valor
    except ValueError:  #captura el error
        try:  #intenta convertirlo a flotante
            num = float(num)   #Si no es flotante, da error de valor(ValuError)
        except ValueError:  #Una vez mas captura el error, quiero decir que no es entero ni flotante.
            return False  #Retorna false
    return num


def normalizar_datos(lista: list) -> list:
    #Me transforma a flotante y entero los valores de ID y Precio
    if not lista:
        return False
    for diccionario in lista:
        diccionario["ID"] = transformar_entero_o_flotante(diccionario["ID"])
        diccionario["PRECIO"] = transformar_entero_o_flotante(diccionario["PRECIO"].replace("$", ""))

def generar_lista_diccionario_archivo_csv(archivo: str) -> list:
    lista_insumos = list(map(lambda lista: {"ID": lista[0], "NOMBRE": lista[1], "MARCA": lista[2], "PRECIO": lista[3], "CARACTERISTICAS": lista[4]}, cargar_datos_desde_archivo(archivo)))
    normalizar_datos(lista_insumos)
    return lista_insumos
#Con la funcion cargar_datos_desde_archivo, obtengo una lista de lista de cada linea del archivo. Con map itero cada elemento(lista) de la lista, la funcion lambda me transforma la listas en diccionarios con sus claves y valores, y me lo guarda en otra lista. Asi obtengo una lista de diccionarios.

# 2.0>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def filtrar_lista(lista: list, key: str) -> list:
    """Recibe una lista y un clave y elimina los repetidos
    Args:
        lista (list): _una lista de diccionarios
        key (str): La clave del que quieres eliminar los valores repetidos
    Returns:
        list: Una lista sin repetidos
    """
    lista = list(set(map(lambda item: item[key], lista)))  #Itero la lista con map y obtengo los valores de las key, luego filtro y guardo los no repetidos en una lista.
    return lista
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def contar_insumos_por_marca(lista: list, key: str) -> None:
    """Recibe una Lista y una clave. Filtra la lista y obtiene una lista sin valores repetidos. Muestra la cantidad de veces que el valor aparece en la lista.
    Args:
        lista (list): Una lista de diccionarios
        key (str): Una clave
    """
    if not lista:   #si la lista esta vacia retorna falsa. Como no es true, entra al if y devuele el mensaje
        print("Error! La lista debe tener como minimo un elemento")
        return False
    for item in lista:   #Itero la lista
        if not(key in item):   #si la clave no esta en la lista. No es True, entro al if y retorno el mensaje
            print("La clave no se encuentra en la lista")
            return 
    lista_filtrada = filtrar_lista(lista, key)
    for item in lista_filtrada:  #itero la lista filtrada
        contador = len(list(filter(lambda valor: valor[key] == item, lista)))  #Con filter y lambda, me devuelve todas las coincidencia de las clave en la lista. lo guardo en otra, y obtengo el tamaño de esa lista que lo guardo en contador
        print(f"{item}: {contador}")  #Muestro la cantidad de veces que esta en la lista el valor
        

# 3.0>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def listar_insumos_por_marca(lista: list, marca: str):
    lista_filtrado = filtrar_lista(lista, marca)   #llamo a la funcion filtrar lista, y me devuelve todas las marcas sin repetir
    for item in lista_filtrado:   #recorro la lista filtrada
        print(f"MARCA: {item}")  #Imprimo la marca
        for clave in lista:   #recorro la lista recibida por parametro
            if(clave[marca] == item):   #Si La marca es igual a la marca de la lista filtrada, entro al if.
                print(f"NOMBRE: {clave['NOMBRE']}, PRECIO: {clave['PRECIO']}")   #Muestro todos los insumos y precio relacionados a esa marca.
        print("*"*100)

# 4.0>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# solo funciona con una lista de diccionarios o diccionario de diccionario
def listar_insumo_por_característica(lista: list, palabra_buscado: str) -> list:
    """Recibe una lista de diccionario y una carater o palabra y busca todas las concidencias de esas palabra en la lista.
    Returns:
        list: Una lista con las palabras relacionadas
    """
    if not(lista and type(palabra_buscado) == str):  #Si la lista esta vacia o la palabra recibida por parametro no es string, retorna false
        return False
    lista_nueva = []
    for insumo in lista:  #Itero la lista de diccionario
        if palabra_buscado.lower() in insumo["CARACTERISTICAS"].lower(): #Si la palabra o caracter se encuentra en la clave "CARACTERISTICAS" del diccionario que se encuentra
            lista_nueva.append(insumo["NOMBRE"])
    if not lista:   #Si no se encuentra resultados, la lista esta vacia(al estar vacia devuelve una false). Entra al if y retorna false
        return False
    return lista_nueva  #Devuelvo una lista con todos los insumos 


def mostrar_insumos_por_caracteristica(lista: list, caracter_buscado: str) -> None:
    insumos_por_caracteristica = listar_insumo_por_característica(lista, caracter_buscado)
    if not insumos_por_caracteristica:   #si retorna false, devuelve ese mensaje
        print(f"no se encontro resultados con '{caracter_buscado}'")
        return
    print(f'resultados con "{caracter_buscado}":')
    print("-"*40)
    for item in insumos_por_caracteristica:
        print(item)
    print("-"*40)

def buscar_insumo_por_característica(lista: list)-> list:
    while True:
        palabra = input("ingrese una palabra, caracter a buscar o s para salir: ")
        if palabra == "s":
            break
        mostrar_insumos_por_caracteristica(lista, palabra)

# 5>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#Es otra version, este devuelve otra lista, con los valores ordenados
def ordenar_lista_diccionario(lista: list, key: str, ascendente: bool=True):
    lista_nueva = lista.copy()
    tam = len(lista_nueva)
    for i in range(tam -1):
        for j in range(i +1, tam):
            if(ascendente and lista_nueva[i][key] > lista_nueva[j][key]) or (not ascendente and lista_nueva[i][key] < lista_nueva[j][key]):
                aux = lista_nueva[i]
                lista_nueva[i] = lista_nueva[j]
                lista_nueva[j] = aux
    return lista_nueva


def mostra_insumos_ordenados(lista: list, key: str) -> None:
    if not(lista and type(key) == str):  #Si la lista esta vacia o la palabra recibida por parametro no es string, retorna false
        print("¡ERROR! La lista no debe estar vacio o el tipo de dato no debe ser distinto a un string")
        return
    lista_ordenada = ordenar_lista_diccionario(lista, key)
    print("-"*111)
    print("| ID  |           DESCRIPCION            |         MARCA          |  PRECIO  |          CARACTERISTICA        |")
    print("-"*111)
    for item in lista_ordenada:
        primera_caracteristica = item["CARACTERISTICAS"].split("~")  #lo divido a partir de "~" y devuelve una lista de elemntos a partir de esa division
        id_centrado = f'{str(item["ID"]):^3s}'
        nombre_centrado = f'{item["NOMBRE"]:^32s}'
        marca_centrada = f'{item["MARCA"]:^22s}'
        precio_centrado = f'{str(item["PRECIO"]):^8s}'
        caracteristica_centrado = f"{primera_caracteristica[0]:^30s}"   #Guardo el primer elemento de esa lista que es la primera caracteristica
        print(f'| {id_centrado} | {nombre_centrado} | {marca_centrada} | {precio_centrado} | {caracteristica_centrado} |')
        print("-"*111)
        #lo asi, porque todos item en el mismo print no me lo centraba

# 6>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def mostrar_productos_encontrados(lista_coincidencia) -> None:
    #recibe una lista con todas las coincidencias con la palabra que ingreso el usuario, itero la lista y muestro el producto el precio y las caracteristicas del producto(esto porque hay algunos iguales)
    x = 0
    print("-"*50)
    print("Elija que producto quiere comprar o s para salir")
    print("-"*50)
    for item in lista_coincidencia:
        x += 1
        print(f"{x}- PRODUCTO: {item['NOMBRE']} | PRECIO: ${item['PRECIO']} | {item['CARACTERISTICAS']}")

def obtener_opcion(lista: list) -> int:
    #recibo la lista de coicidencias, ya que ese es el maximo rango.
    while True:
        seleccion = input("ingrese el numero del producto que desee comprar: ")
        try:
            seleccion = int(seleccion)   #si no es un numero entero, es invalido
            if seleccion >= 1 and seleccion <= len(lista):   #si esta fuera del rango de eleccion, es invalido.
                return seleccion
            else:
                print("Seleccion invalida: Intentente nuevamente")
        except ValueError:
            print("Seleccion invalida: Intentente nuevamente")

def obtener_cantidad() -> int:
    #no recibe nada, si retorna
    while True:
        try:
            cantidad = int(input("Ingrese la cantidad deseada: "))
            if cantidad > 0:   #si es mayor que ser retorna la cantidad
                return cantidad
            else:
                print("Cantidad inválida. Intente nuevamente.")
        except ValueError:
            print("Cantidad inválida. Intente nuevamente.")



def generar_factura(lista_compra: list, total: int) -> None:
    #Recibe la lista de diccionarios de la compras realizadas y el total de compra. Itero la lista y acumulo todos los resultados en la variable factura_txt para luego abrir un archivo en modo escritura. y generar un archivo tipo texto con todos los resultados
    factura_txt = "La factura de compra es: "
    factura_txt += "\n------------------------------------"
    for item in lista_compra:
        factura_txt += f"\nProducto: {item['producto']}\nCantidad: {item['cantidad']}\nSubtotal: {item['subtotal']:.2f}"
        factura_txt += "\n------------------------------------"
    factura_txt += f"\nEl total de la compra es: {total:.2f}"
    with open("factura.txt", "w") as file:
        file.write(factura_txt)
        
def realizar_compra(lista: list):
    total_compra = 0
    lista_compra = []  #en esta lista se guardara todos los productos y la factura
    while True:
        os.system("cls")
        marca_ingresada = input("Ingrese la marca o s para salir: ")
        if marca_ingresada == "s":  #si ingrese "s" se corta el bucle while
            break
        lista_coincidencia = list(filter(lambda insumo: marca_ingresada.lower() in insumo["MARCA"].lower(), lista)) #me regresa una lista con todas las coincidencias con la palabra que ingreso el usuario
        if not lista_coincidencia:  #Si devuelve una lista vacia y lo usas como condiccion en un if. la lista vacia es un bool y si esta vacia es False.
            print("No hubo resultados")
            os.system("pause")
            continue
        mostrar_productos_encontrados(lista_coincidencia)
        seleccion = obtener_opcion(lista_coincidencia)
        producto_seleccionado = lista_coincidencia[seleccion-1]   #obtengo el diccionario con la eleccion de usuario -1(esto se debe que la posicion arranca en 0)
        os.system("cls")
        cantidad = obtener_cantidad()
        subtotal = producto_seleccionado["PRECIO"] * cantidad  #multiplico el precio por la cantidad que ingreso al usuario
        total_compra += subtotal 
        lista_compra.append({
            "producto": producto_seleccionado["NOMBRE"],
            "cantidad": cantidad,
            "subtotal": subtotal
        }) #añado todo a un diccionario
        os.system("pause")
    if not lista_compra: #si no compro nada retorna el mensaje
        print("Ups. Una lastima que no hayas comprado nada, sera para la proxima. Chau!")
        return
    generar_factura(lista_compra, total_compra) #genero el archivo txt.
    
# 7>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def filtrar_lista_por_palabra_buscada(lista: list, key: str, palabra: str) -> list:
    #Recibe una lista, una clave y una palabra. Busca que sa palabra coincidas en los valores de la clave. devuelve una lista con todas las coincidencias
    if not lista:
        return False
    lista_coincidencia = list(filter(lambda x: palabra.lower() in x[key].lower(), lista))
    return lista_coincidencia

def generar_archivo_json(lista: list, nombre_archivo: str) -> None:
    #recibe una lista/diccionario y el nombre del archivo y genera un archivo json
    if not lista and type(archivo) != str:  #si la lista esta vacia o el nombre del archivo no es un string. Retorna el mensaje
        print("Argurmentos invalidos")
        return
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(lista, archivo, indent=2, ensure_ascii=False)
    print("Archivo json generado con exitos!")

# generar_archivo_json(filtrar_lista_por_palabra_buscada(lista_insumos, "NOMBRE", "alimento"), "insumos.json")


# 8>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def cargar_datos_json(nombre_archivo: str) -> list:
    #Abro el archivo en modo lectura, cargo una lista de dicionario con la funcion json.load
    with open(nombre_archivo, "r", encoding="utf-8") as file:
        lista = json.load(file)
    return lista

def mostrar_datos_json(nombre_archivo: str) -> None:
    if not (type(nombre_archivo) == str):
        print("Tipo de dato incorreto")
        return
    lista_datos = cargar_datos_json(nombre_archivo)
    print("-"*142)
    print("| ID  |      DESCRIPCION       |        MARCA       |  PRECIO  |                             CARACTERISTICA"+" "*34+"|")
    print("-"*142)
    for item in lista_datos:
        id_centrado = f'{str(item["ID"]):^3s}'
        nombre_centrado = f'{item["NOMBRE"]:^22s}'
        marca_centrada = f'{item["MARCA"]:^18s}'
        precio_centrado = f'{str(item["PRECIO"]):^8s}'
        caracteristica_centrado = f'{item["CARACTERISTICAS"]:75s}'
        print(f'| {id_centrado} | {nombre_centrado} | {marca_centrada} | {precio_centrado} | {caracteristica_centrado} |')
        print("-"*142)


# 9>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#otra version
def cargar_csv(archivo: str) -> str:
    lista = []
    with open(archivo, 'r', encoding="utf-8") as archivo_csv:
        contenido = archivo_csv.readlines()    #leo todas las lineas a partir de la 2da linea
        for linea in contenido:
            fila = linea.split(",")   #dividido por las comas y elimnino el \n con el strip
            lista.append(fila)
    return lista

def actualizar_precio_csv(archivo_csv: str):
    lista = cargar_csv(archivo_csv)   #consigo una lista de lista
    linea_unida = ""  #creo un acumulador
    linea_unida += ",".join(lista[0])  #uno la linea 1 de la lista, con su descripciones
    aumento = 1 + 0.084   #aplico el aumento del 8.4
    for x in range(1, len(lista)):   #recorro la lista del 1 al ultimo
        numero_float = float(lista[x][3].replace("$", ""))   #remplazo los el caracterer $ y lo flotabilizo
        lista[x][3] = f"${round(numero_float * aumento, 2)}"   #le aumento el valor en un 8.4 y lo uno a una cadena
        linea_modificada = ",".join(lista[x])  #uno cada elemento de la lista
        linea_unida += linea_modificada  #lo acumulo en linea

    with open("insumo-copy.csv", "w", encoding="utf-8") as file:   #lo abro modo escritura
        file.writelines(linea_unida) #lo escribo



# /////////////////////////////////////////////////////////////////////////////////////////////
# PARCIAL>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 1>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><
def cargar_dato_a_lista_txt(txt: str) -> list:
    with open(txt, "r") as file:
        contenido = file.read()
    
    lista = contenido.split("\n")
    return lista

def mostrar_marca(lista):
    print("Las Marcas son: ")
    for marca in lista:
        print(marca)


def esta_id_en_lista(lista, id):
    for item in lista:  #Itero la lista de diccionario
        if str(id) in str(item["ID"]):
            return True
    return False

def esta_en_lista_la_marca(lista, marca):
    for item in lista:
        if(marca.lower() == item.lower()):
            return True
    return False

def validar_caracteristicas(entrada:str):
    caracteristicas = entrada.split("~")
    tam = len(caracteristicas)
    if tam >= 1 and tam <=3:
        return True
    else:
        return False
            
def agregar_producto(lista: list) -> None:
    os.system("cls")
    lista_marca = cargar_dato_a_lista_txt("marcas.txt")
    while True:
        try:
            id = int(input("Ingrese Id del producto: "))
            if not esta_id_en_lista(lista, id):
                break
            else:
                print("esa clave ya esta")
        except ValueError:
            print("Solo ingrese numeros")
    nombre = input("Ingrese el nombre del producto: ")
    while True:
        mostrar_marca(lista_marca)
        marca = input("ingrese marca: ")
        if esta_en_lista_la_marca(lista_marca, marca):
            break
        else:
            print("La marca no esta en la opciones")
    while True:
        try:
            precio = float(input("Ingrese precio del producto: "))
            if precio > 0:
                break
            else:
                print("No se puede agregar valores negativos")
        except ValueError:
            print("Valor invalido.")

    while True:
        caracteristica = input("ingrese caracteristica de 1 a 3: ")
        if validar_caracteristicas(caracteristica):
            break
        else:
            print("Caracteristica invalida")
            os.system("pause")

    dic = {"ID": id, "NOMBRE": nombre, "MARCA": marca, "PRECIO": precio, "CARACTERISTICAS": caracteristica}
    lista.append(dic)

# 2. Agregar una opción para guardar todos los datos actualizados (incluyendo las altas).
# El usuario elegirá el tipo de formato de exportación: csv o json.


def crear_archivo_json(lista: list) -> None:
    #recibe una lista/diccionario y el nombre del archivo y genera un archivo json
    if not lista and type(archivo) != str:
        print("Argurmentos invalidos")
        return
    nombre_archivo = input("ingrese el nombre del archivo json: ")
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(lista, archivo, indent=2, ensure_ascii=False)
    print("Archivo json generado con exitos!")

def agregar_tipo_archivo(lista):
    respuesta = input("En que formato lo quiere guarda en csv o en json: ").lower()
    if respuesta == "csv":
        pass
    elif respuesta == "json":
        crear_archivo_json(lista)
    else:
        print("opcion invalida")



# 2>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ///////////////////////////////////////////////////////////////////////////
def imprimir_menu():
    print("""
    ******************MENU***********************
    1. Cargar datos desde archivo
    2. Listar cantidad por marca
    3. Mostrar insumos por marca
    4. Buscar insumo por característica
    5. Mostrar insumos ordenados
    6. Realizar compras
    7. Guardar en formato JSON
    8. Leer desde formato JSON
    9. Actualizar precios
    10. Agregar nuevo producto
    11. Guardar cambios
    12. Salir del programa
    """)

def mostrar_opciones():
    try:
        opcion = input("ingrese una opcion: ")
        return int(opcion)
    except ValueError:
        return -1
    
def app_principal():
    flag_carga = False
    flag_json = False
    flag_generar_archivo = False
    lista_insumos = []
    while True:
        os.system("cls")
        imprimir_menu()
        opcion = mostrar_opciones()
        os.system("cls")
        match(opcion):
            case 1:
                lista_insumos = generar_lista_diccionario_archivo_csv("insumos.csv")
                flag_carga = True
            case 2:
                if flag_carga:
                    contar_insumos_por_marca(lista_insumos, "MARCA")
                else:
                    print("primero debes cargar datos")
            case 3:
                if flag_carga:
                    listar_insumos_por_marca(lista_insumos, "MARCA")
                else:
                    print("primero debes cargar datos")
            case 4:
                if flag_carga:
                    buscar_insumo_por_característica(lista_insumos)
                else:
                    print("primero debes cargar datos")
            case 5:
                if flag_carga:
                    mostra_insumos_ordenados(lista_insumos, "MARCA")
                else:
                    print("primero debes cargar datos")
            case 6:
                if flag_carga:
                    realizar_compra(lista_insumos)
                else:
                    print("primero debes cargar datos")
            case 7:
                if flag_carga:
                    flag_json = True
                    generar_archivo_json(filtrar_lista_por_palabra_buscada(lista_insumos, "NOMBRE", "alimento"), "insumos.json")
                else:
                    print("primero debes cargar datos")
            case 8:
                if flag_json:
                    mostrar_datos_json("insumos.json")
                else:
                    print("Primero debes generar el archivo json")
            case 9:
                actualizar_precio_csv("insumos.csv")
            case 10:
                if flag_carga:
                    flag_generar_archivo = True
                    agregar_producto(lista_insumos)
                else:
                    print("primero debes cargar datos")
            case 11:
                if flag_generar_archivo:
                    agregar_tipo_archivo(lista_insumos)
                else:
                    print("primero debes agregar un nuevo producto")
            case 12:
                break
            case -1:
                print("opcion incorrecta")
        os.system("pause")


app_principal()