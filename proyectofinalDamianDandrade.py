from colorama import Fore, Back, Style, init
import sqlite3


# Inicializar Colorama
init(autoreset=True)

#Conexion a la base de datos SQLite(se creara si no existe)

conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    cantidad INT NOT NULL,
    precio FLOAT NOT NULL,
    categoria TEXT NOT NULL
);

""")

conn.commit()


productos = [] #Creacion de lista de productos (vacia)


#funciones

def agregar_producto():
    print(Fore.GREEN + "Alta de producto: ")#se hace ingreso de datos para el alta

    nombreproducto = input(Fore.CYAN + "Ingrese el nombre del producto: ")
    descripcionproducto = input(Fore.CYAN + "Ingrese la descripcion del producto: ")
    cantidadproducto = int(input(Fore.CYAN + "Ingrese la cantidad del producto: "))
    precioproducto = float(input(Fore.CYAN + "Ingrese el precio del producto: "))
    categoriaproducto = input(Fore.CYAN + "Ingrese la categoria del producto: ")

    querry = (f"""
    INSERT INTO productos (nombre,descripcion,cantidad,precio,categoria) VALUES ('{nombreproducto}','{descripcionproducto}',{cantidadproducto},{precioproducto},'{categoriaproducto}');                       
    """)
    cursor.execute(querry)
    #se ejecuta para insertar en la tabla productos los datos
    conn.commit()

    producto = [nombreproducto, descripcionproducto, cantidadproducto, precioproducto, categoriaproducto]  # Insertamos el producto ingresado
    productos.append(producto)  # Agregar el producto al listado

def mostrar_productos():
    print(Fore.CYAN + "Listado de Productos")     

    cursor.execute("""
    SELECT * FROM productos 
    """)#se ejecuta consulta para traer toda la tabla
    
    productos = cursor.fetchall()

    if not productos:
        print(Fore.RED + "No hay productos agregados.")
        return#en caso de que la lista se encuentre vacia, devuelva null
    print(Fore.YELLOW + "ID".ljust(5) + Fore.GREEN + "Nombre".ljust(15) + Fore.YELLOW + "Descripcion".ljust(20) + Fore.CYAN + "Cantidad".ljust(10) + Fore.MAGENTA + "Precio".ljust(10) + Fore.BLUE + "Categoria".ljust(15))
    for producto in productos:#un for para recorrer todos los productos
        print(f"{str(producto[0]).ljust(5)}{str(producto[1]).ljust(15)}{str(producto[2]).ljust(20)}{str(producto[3]).ljust(10)}{str(producto[4]).ljust(10)}{str(producto[5]).ljust(15)}")

def actualizar_producto():
    id_producto = int(input(Fore.YELLOW + "ID del producto a modificar: "))

    cursor.execute(f"""
        SELECT * FROM productos WHERE id = {id_producto};
    """)
    producto = cursor.fetchone()

    if producto:
        nueva_cantidad = float(input(Fore.CYAN + f"Inserte la nueva cantidad: "))
        cursor.execute(f"""
        UPDATE productos SET cantidad = {nueva_cantidad} WHERE id = {id_producto} ;
        """)
        conn.commit()
        print(Fore.GREEN + "Cantidad de producto actualizada!")
    else:
        print(Fore.RED + "El id NO existe!!! ")

def eliminar_producto():
    id_producto = int(input(Fore.YELLOW + "ID del producto a eliminar: "))#se ingresa el id del producto a eliminar
    cursor.execute(f"""
        SELECT * FROM productos WHERE id = {id_producto};
    """)
    producto = cursor.fetchone()#se guarda el producto en la tupla
    if producto:
        cursor.execute(f"""
        DELETE FROM productos WHERE id = {id_producto};
        """)#se ejecuta consulta para eliminar el producto filtrado
        conn.commit()
        print(Fore.GREEN + "Producto Eliminado")
    else:
        print(Fore.RED + "El id NO existe!!! ")#caso en que el id no haya sido encontrado

def busqueda_id():
        id_producto = int(input(Fore.YELLOW + "ID del producto a buscar: ")) #se ingresa el id a buscar

        cursor.execute(f"""
            SELECT * FROM productos WHERE id = {id_producto};
        """)#consulta para accerder al resultado, en este caso se utiliza fetchone, ya que el id es uno solo y unico
        producto = cursor.fetchone()

        if producto:
            print(Fore.YELLOW + "ID".ljust(5) + Fore.GREEN + "Nombre".ljust(15) + Fore.YELLOW + "Descripcion".ljust(20) + Fore.CYAN + "Cantidad".ljust(10) + Fore.MAGENTA + "Precio".ljust(10) + Fore.BLUE + "Categoria".ljust(15))
            print(f"{str(producto[0]).ljust(5)}{str(producto[1]).ljust(15)}{str(producto[2]).ljust(20)}{str(producto[3]).ljust(10)}{str(producto[4]).ljust(10)}{str(producto[5]).ljust(15)}")
        else:
            print(Fore.RED + "El id NO existe!!! ")    

def busqueda_nombre():
        nombre_producto = (input(Fore.YELLOW + "Nombre del producto a buscar: "))#se ingresa el nombre a buscar

        cursor.execute(f"""
            SELECT * FROM productos WHERE nombre = '{nombre_producto}';
        """)#consulta para acceder a el nombre correspondiete, se utiliza fetchall ya que suponemos que los nombres son unicos, pero pueden tener diferente descripcion
        productos = cursor.fetchall()

        print(Fore.YELLOW + "ID".ljust(5) + Fore.GREEN + "Nombre".ljust(15) + Fore.YELLOW + "Descripcion".ljust(20) + Fore.CYAN + "Cantidad".ljust(10) + Fore.MAGENTA + "Precio".ljust(10) + Fore.BLUE + "Categoria".ljust(15))
        for producto in productos: #se recorre los productos filtrados y se muestran
            print(f"{str(producto[0]).ljust(5)}{str(producto[1]).ljust(15)}{str(producto[2]).ljust(20)}{str(producto[3]).ljust(10)}{str(producto[4]).ljust(10)}{str(producto[5]).ljust(15)}")
        if not productos:
            print(Fore.RED + "El nombre de ese producto NO existe!!! ")     

def busqueda_categoria():
        categoria_producto = (input(Fore.YELLOW + "Categoria del producto a buscar: ")) #se ingresa la categoria a buscar

        cursor.execute(f"""
            SELECT * FROM productos WHERE categoria = '{categoria_producto}';
        """)#consulta para acceder a las categoria correspondiente, se utiliza fetchall para traer si hay varios con misma categoria
        productos = cursor.fetchall()

        print(Fore.YELLOW + "ID".ljust(5) + Fore.GREEN + "Nombre".ljust(15) + Fore.YELLOW + "Descripcion".ljust(20) + Fore.CYAN + "Cantidad".ljust(10) + Fore.MAGENTA + "Precio".ljust(10) + Fore.BLUE + "Categoria".ljust(15))
        for producto in productos: #se recorre los productos filtrados y se muestran
            print(f"{str(producto[0]).ljust(5)}{str(producto[1]).ljust(15)}{str(producto[2]).ljust(20)}{str(producto[3]).ljust(10)}{str(producto[4]).ljust(10)}{str(producto[5]).ljust(15)}")
        if not productos:
            print(Fore.RED + "la categoria NO existe!!! ")    

def buscar_producto():
    print(Fore.GREEN+ "Tipos de Busqueda") #menu de opciones para filtrar la busqueda
    print(Fore.CYAN+"1. Por ID")
    print(Fore.CYAN+"2. Por Nombre")
    print(Fore.CYAN+"3. Por Categoria")
    print(Back.BLUE+"*"*30)
    opcion = int(input(Fore.YELLOW+"Selecciona una opcion: "))
    if opcion == 1:
        busqueda_id()
    elif opcion == 2:
        busqueda_nombre()
    elif opcion == 3:
        busqueda_categoria()
    else:
        print(Fore.RED + "Opción incorrecta")

def reporte_bajostock():
    cant_bajostock = int(input(Fore.YELLOW + "Ingrese la cantidad menor o igual de productos a buscar: "))# se ingresa la cantidad a buscar

    cursor.execute(f"""
        SELECT * FROM productos WHERE cantidad <= {cant_bajostock};
    """)#consulta para acceder a los productos con cantidad menor o igual
    productos_bajo_stock = cursor.fetchall() #se guardan en la tupla

    if productos_bajo_stock: 
        print(Fore.YELLOW + "ID".ljust(5) + Fore.GREEN + "Nombre".ljust(15) + Fore.YELLOW + "Descripcion".ljust(20) + Fore.CYAN + "Cantidad".ljust(10) + Fore.MAGENTA + "Precio".ljust(10) + Fore.BLUE + "Categoria".ljust(15))
        for producto in productos_bajo_stock: #se recorre la tupla y se muestra
            print(f"{str(producto[0]).ljust(5)}{str(producto[1]).ljust(15)}{str(producto[2]).ljust(20)}{str(producto[3]).ljust(10)}{str(producto[4]).ljust(10)}{str(producto[5]).ljust(15)}")
    else:
        print(Fore.RED + "No hay productos con bajo stock!")

#Menu
while True:
    print(Back.BLUE + Style.BRIGHT + "*" * 30)
    print(Fore.GREEN + "Menú Principal")
    print(Fore.CYAN + "1. Agregar productos")
    print(Fore.CYAN + "2. Mostrar productos")
    print(Fore.CYAN + "3. Actualizar cantidad de producto")
    print(Fore.CYAN + "4. Eliminar producto")
    print(Fore.CYAN + "5. Buscar producto")
    print(Fore.CYAN + "6. Reporte de Bajo Stock")           
    print(Fore.RED + "7. Salir")
    print(Back.BLUE + "*" * 30)

    opcion = int(input(Fore.YELLOW + "Seleccione una opción: "))
    #se ingresa el valor de la opcion, que llamara a la funcion correspondiente
    if opcion == 7:
        print(Fore.MAGENTA + "¡Adios!")
        break
    elif opcion == 1:
        agregar_producto()
    elif opcion == 2:
        mostrar_productos()
    elif opcion == 3:
        actualizar_producto()
    elif opcion == 4:
        eliminar_producto()
    elif opcion == 5:
        buscar_producto()  
    elif opcion == 6:
        reporte_bajostock()              
    else:
        print(Fore.RED + "Opción incorrecta, intenta nuevamente.")

#Cerramos la conexion
conn.close()
