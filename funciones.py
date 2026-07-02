import pandas as pd
import os

def menu():
    print("\n" + "=" * 60)
    print("      FERRETERIA SIMULACION")
    print("=" * 60)
    print("1. Crear Factura")
    print("2. Gestión de Inventario")
    print("3. Gestión de Clientes")
    print("4. Ver Clientes")
    print("5. Reportes")
    print("0. Salir")
    print("=" * 60)

def menu_inventario():
    while True:
        print("\n" + "="*50)
        print("            INVENTARIO")
        print("="*50)
        print("1. Ver inventario")
        print("2. Agregar producto")
        print("3. Agregar stock")
        print("4. Modificar producto")
        print("5. Eliminar producto")
        print("0. Volver")
        print("="*50)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            ver_inventario()
        elif opcion == "2":
            agregar_inventario()
        elif opcion == "3":
            agregar_stock()
        elif opcion == "4":
            modificar_inventario()
        elif opcion == "5":
            eliminar_producto()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

def ver_inventario():
    archivo = "datos/inventario.csv"
    if not os.path.exists(archivo):
        print("\nNo existe el inventario.")
        return
    inventario = pd.read_csv(archivo)
    if inventario.empty:
        print("\nNo hay productos registrados.")
        return
    print("\n" + "="*50)
    print("        VER INVENTARIO")
    print("="*50)
    buscar = input("Buscar producto (ENTER para mostrar todos): ")
    if buscar == "":
        resultado = inventario
    else:
        resultado = inventario[
            inventario["nombre"].str.contains(buscar, case=False, na=False)
        ]
    if resultado.empty:
        print("\nNo se encontraron productos.")
        return
    print("\n")
    print(resultado.to_string(index=False))

def agregar_inventario():
    print("\n" + "="*50)
    print("        AGREGAR INVENTARIO")
    print("="*50)
    archivo = "datos/inventario.csv"
    if not os.path.exists(archivo) or os.path.getsize(archivo) == 0:
        pd.DataFrame(columns=[
            "codigo", "nombre", "categoria", "precio", "stock", "unidad"
        ]).to_csv(archivo, index=False)
    inventario = pd.read_csv(archivo)
    if inventario.empty:
        codigo = 1
    else:
        codigo = inventario["codigo"].max() + 1
    nombre = input("Nombre del producto: ")
    if nombre.lower() in inventario["nombre"].astype(str).str.lower().values:
        print("\nEse producto ya existe en el inventario.")
        return
    categoria = input("Categoría: ")
    precio = float(input("Precio: "))
    stock = int(input("Cantidad en stock: "))
    unidad = input("Unidad (Saco, m3, Unidad, Libra...): ")
    nuevo_producto = pd.DataFrame({
        "codigo":[codigo], "nombre":[nombre], "categoria":[categoria],
        "precio":[precio], "stock":[stock], "unidad":[unidad]
    })
    nuevo_producto.to_csv(archivo, mode="a", header=False, index=False)
    print("\nProducto agregado correctamente.")

def agregar_stock():
    archivo = "datos/inventario.csv"
    if not os.path.exists(archivo):
        print("\nNo existe el inventario.")
        return
    inventario = pd.read_csv(archivo)
    if inventario.empty:
        print("\nNo hay productos registrados.")
        return
    print("\n" + "="*50)
    print("        AGREGAR STOCK")
    print("="*50)
    buscar = input("Ingrese el nombre del producto: ")
    resultados = inventario[
        inventario["nombre"].str.contains(buscar, case=False, na=False)
    ]
    if resultados.empty:
        print("\nNo se encontraron productos.")
        return
    print("\nProductos encontrados:\n")
    for i, (_, producto) in enumerate(resultados.iterrows(), start=1):
        print(f"{i}. {producto['nombre']}")
        print(f"   Categoría : {producto['categoria']}")
        print(f"   Precio    : ${producto['precio']}")
        print(f"   Stock     : {producto['stock']} {producto['unidad']}")
        print("-" * 40)
    opcion = int(input("Seleccione un producto: "))
    if opcion < 1 or opcion > len(resultados):
        print("\nOpción inválida.")
        return
    indice = resultados.index[opcion - 1]
    stock_actual = inventario.loc[indice, "stock"]
    cantidad = int(input("Cantidad a agregar: "))
    inventario.loc[indice, "stock"] = stock_actual + cantidad
    inventario.to_csv(archivo, index=False)
    print("\nStock actualizado correctamente.")
    print(f"Stock anterior : {stock_actual}")
    print(f"Stock nuevo    : {inventario.loc[indice, 'stock']}")

def modificar_inventario():
    archivo = "datos/inventario.csv"
    if not os.path.exists(archivo):
        print("\nNo existe el inventario.")
        return
    inventario = pd.read_csv(archivo)
    if inventario.empty:
        print("\nNo hay productos registrados.")
        return
    print("\n" + "="*50)
    print("        MODIFICAR PRODUCTO")
    print("="*50)
    buscar = input("Ingrese el nombre del producto: ")
    resultados = inventario[
        inventario["nombre"].str.contains(buscar, case=False, na=False)
    ]
    if resultados.empty:
        print("\nProducto no encontrado.")
        return
    print()
    for i, (_, producto) in enumerate(resultados.iterrows(), start=1):
        print(f"{i}. {producto['nombre']} - ${producto['precio']}")
    opcion = int(input("\nSeleccione el producto: "))
    if opcion < 1 or opcion > len(resultados):
        print("\nOpción inválida.")
        return
    indice = resultados.index[opcion-1]
    print("\nDeje vacío si no desea modificar ese dato.\n")
    nombre = input(f"Nombre ({inventario.loc[indice,'nombre']}): ")
    categoria = input(f"Categoría ({inventario.loc[indice,'categoria']}): ")
    precio = input(f"Precio ({inventario.loc[indice,'precio']}): ")
    if nombre != "":
        inventario.loc[indice,"nombre"] = nombre
    if categoria != "":
        inventario.loc[indice,"categoria"] = categoria
    if precio != "":
        inventario.loc[indice,"precio"] = float(precio)
    inventario.to_csv(archivo,index=False)
    print("\nProducto actualizado correctamente.")

def eliminar_producto():
    archivo = "datos/inventario.csv"
    if not os.path.exists(archivo):
        print("\nNo existe el inventario.")
        return
    inventario = pd.read_csv(archivo)
    if inventario.empty:
        print("\nNo hay productos registrados.")
        return
    print("\n" + "="*50)
    print("         ELIMINAR PRODUCTO")
    print("="*50)
    buscar = input("Ingrese el nombre del producto: ")
    resultados = inventario[
        inventario["nombre"].str.contains(buscar, case=False, na=False)
    ]
    if resultados.empty:
        print("\nProducto no encontrado.")
        return
    print()
    for i, (_, producto) in enumerate(resultados.iterrows(), start=1):
        print(f"{i}. {producto['nombre']} ({producto['stock']} {producto['unidad']})")
    opcion = int(input("\nSeleccione el producto: "))
    if opcion < 1 or opcion > len(resultados):
        print("\nOpción inválida.")
        return
    indice = resultados.index[opcion-1]
    confirmar = input(f"\n¿Seguro que desea eliminar '{inventario.loc[indice,'nombre']}'? (S/N): ")
    if confirmar.upper() == "S":
        inventario = inventario.drop(indice)
        inventario.to_csv(archivo,index=False)
        print("\nProducto eliminado correctamente.")
    else:
        print("\nOperación cancelada.")

def registrar_cliente():
    print("\n" + "="*50)
    print("        REGISTRO DE CLIENTES")
    print("="*50)
    archivo = "datos/clientes.csv"
    if not os.path.exists(archivo) or os.path.getsize(archivo) == 0:
        pd.DataFrame(columns=[
            "cedula", "nombre", "telefono", "direccion"
        ]).to_csv(archivo, index=False)
    clientes = pd.read_csv(archivo)
    cedula = input("Ingrese la cédula: ")
    nombre = input("Ingrese el nombre: ")
    telefono = input("Ingrese el teléfono: ")
    direccion = input("Ingrese la dirección: ")
    if cedula in clientes["cedula"].astype(str).values:
        print("\nEse cliente ya está registrado.")
        return
    nuevo_cliente = pd.DataFrame({
        "cedula": [cedula], "nombre": [nombre],
        "telefono": [telefono], "direccion": [direccion]
    })
    nuevo_cliente.to_csv(archivo, mode="a", header=False, index=False)
    print("\nCliente registrado correctamente.")

def ver_clientes():
    archivo = "datos/clientes.csv"
    if not os.path.exists(archivo):
        print("\nNo existe la base de datos de clientes.")
        return
    if os.path.getsize(archivo) == 0:
        print("\nNo hay clientes registrados.")
        return
    try:
        clientes = pd.read_csv(archivo)
        if clientes.empty:
            print("\nNo hay clientes registrados.")
            return
        print("\n" + "="*80)
        print("LISTA DE CLIENTES")
        print("="*80)
        print(clientes.to_string(index=False))
    except Exception as e:
        print(f"\nOcurrió un error: {e}")

def buscar_cliente_factura():

    archivo = "datos/clientes.csv"

    clientes = pd.read_csv(archivo)

    buscar = input("Ingrese la cédula o nombre del cliente: ")

    resultado = clientes[
        clientes["cedula"].astype(str).str.contains(buscar, case=False, na=False) |
        clientes["nombre"].str.contains(buscar, case=False, na=False)
    ]

    if resultado.empty:
        print("\nCliente no encontrado.")
        return None

    print("\nClientes encontrados:\n")

    for i, (_, cliente) in enumerate(resultado.iterrows(), start=1):
        print(f"{i}. {cliente['nombre']} - {cliente['cedula']}")

    opcion = int(input("\nSeleccione un cliente: "))

    if opcion < 1 or opcion > len(resultado):
        return None

    return resultado.iloc[opcion-1]

def agregar_productos_factura():

    inventario = pd.read_csv("datos/inventario.csv")

    productos = []

    while True:

        buscar = input("\nProducto: ")

        encontrados = inventario[
            inventario["nombre"].str.contains(buscar, case=False, na=False)
        ]

        if encontrados.empty:
            print("Producto no encontrado.")
            continue

        print()

        for i, (_, p) in enumerate(encontrados.iterrows(), start=1):

            print(f"{i}. {p['nombre']}")

            print(f"   Precio : ${p['precio']}")

            print(f"   Stock  : {p['stock']} {p['unidad']}")

        opcion = int(input("\nSeleccione: "))

        indice = encontrados.index[opcion-1]

        cantidad = int(input("Cantidad: "))

        if cantidad > inventario.loc[indice,"stock"]:

            print("Stock insuficiente.")

            continue

        subtotal = cantidad * inventario.loc[indice,"precio"]

        productos.append({

            "indice": indice,

            "producto": inventario.loc[indice,"nombre"],

            "cantidad": cantidad,

            "precio": inventario.loc[indice,"precio"],

            "subtotal": subtotal

        })

        seguir = input("\nAgregar otro producto (S/N): ")

        if seguir.upper() != "S":
            break

    return productos

from datetime import datetime
import os

def guardar_factura(cliente, productos):

    archivo = "datos/facturas.csv"

    if not os.path.exists(archivo) or os.path.getsize(archivo)==0:

        pd.DataFrame(columns=[
            "numero",
            "fecha",
            "cedula",
            "cliente",
            "producto",
            "cantidad",
            "precio",
            "subtotal",
            "iva",
            "total"
        ]).to_csv(archivo,index=False)

    facturas = pd.read_csv(archivo)

    if facturas.empty:

        numero = 1

    else:

        numero = facturas["numero"].max()+1

    subtotal = sum(p["subtotal"] for p in productos)

    iva = subtotal * 0.15

    total = subtotal + iva

    fecha = datetime.now().strftime("%d/%m/%Y")

    inventario = pd.read_csv("datos/inventario.csv")

    for p in productos:

        nueva = pd.DataFrame({

            "numero":[numero],

            "fecha":[fecha],

            "cedula":[cliente["cedula"]],

            "cliente":[cliente["nombre"]],

            "producto":[p["producto"]],

            "cantidad":[p["cantidad"]],

            "precio":[p["precio"]],

            "subtotal":[subtotal],

            "iva":[iva],

            "total":[total]

        })

        nueva.to_csv(

            archivo,

            mode="a",

            header=False,

            index=False

        )

        inventario.loc[p["indice"],"stock"] -= p["cantidad"]

    inventario.to_csv("datos/inventario.csv",index=False)

    print("\n"+"="*55)

    print("              FACTURA")

    print("="*55)

    print(f"Número : {numero}")

    print(f"Cliente: {cliente['nombre']}")

    print(f"Fecha  : {fecha}")

    print("-"*55)

    for p in productos:

        print(f"{p['producto']}")

        print(f"{p['cantidad']} x ${p['precio']} = ${p['subtotal']:.2f}")

    print("-"*55)

    print(f"Subtotal : ${subtotal:.2f}")

    print(f"IVA 15%  : ${iva:.2f}")

    print(f"TOTAL    : ${total:.2f}")

    print("="*55)

def crear_factura():

    print("\n"+"="*50)

    print("          CREAR FACTURA")

    print("="*50)

    cliente = buscar_cliente_factura()

    if cliente is None:

        return

    productos = agregar_productos_factura()

    if len(productos)==0:

        print("\nNo se agregaron productos.")

        return

    guardar_factura(cliente,productos)

def reporte_facturas():

    while True:

        print("\n"+"="*50)
        print("              REPORTES")
        print("="*50)
        print("1. Ver todas las facturas")
        print("2. Buscar factura por cliente")
        print("3. Buscar factura por número")
        print("0. Volver")
        print("="*50)

        opcion = input("Seleccione una opción: ")

        if opcion=="1":
            ver_todas_facturas()

        elif opcion=="2":
            buscar_factura_cliente()

        elif opcion=="3":
            buscar_factura_numero()

        elif opcion=="0":
            break

        else:
            print("\nOpción inválida.")

def ver_todas_facturas():

    archivo="datos/facturas.csv"

    if not os.path.exists(archivo):
        print("\nNo existen facturas.")
        return

    facturas=pd.read_csv(archivo)

    if facturas.empty:
        print("\nNo existen facturas.")
        return

    resumen=facturas.groupby("numero").first().reset_index()

    print()

    for _,f in resumen.iterrows():

        print(f"Factura #{f['numero']}")

        print(f"Cliente : {f['cliente']}")

        print(f"Fecha    : {f['fecha']}")

        print(f"Total    : ${f['total']:.2f}")

        print("-"*40)

    numero=int(input("\nNúmero de factura para ver detalle: "))

    mostrar_factura(numero)

def buscar_factura_cliente():

    facturas=pd.read_csv("datos/facturas.csv")

    buscar=input("\nNombre del cliente: ")

    clientes=facturas[
        facturas["cliente"].str.contains(buscar,case=False,na=False)
    ]

    if clientes.empty:

        print("\nNo se encontraron facturas.")

        return

    resumen=clientes.groupby("numero").first().reset_index()

    print()

    for _,f in resumen.iterrows():

        print(f"{f['numero']} - {f['cliente']} - ${f['total']:.2f}")

    numero=int(input("\nSeleccione una factura: "))

    mostrar_factura(numero)

def buscar_factura_numero():

    numero=int(input("\nNúmero de factura: "))

    mostrar_factura(numero)

def mostrar_factura(numero):

    facturas=pd.read_csv("datos/facturas.csv")

    factura=facturas[facturas["numero"]==numero]

    if factura.empty:

        print("\nFactura no encontrada.")

        return

    print("\n"+"="*55)

    print("              FACTURA")

    print("="*55)

    print(f"Número : {numero}")

    print(f"Cliente: {factura.iloc[0]['cliente']}")

    print(f"Fecha  : {factura.iloc[0]['fecha']}")

    print("-"*55)

    for _,p in factura.iterrows():

        print(f"{p['producto']}")

        print(f"{p['cantidad']} x ${p['precio']} = ${p['cantidad']*p['precio']:.2f}")

    print("-"*55)

    print(f"Subtotal : ${factura.iloc[0]['subtotal']:.2f}")

    print(f"IVA 15%  : ${factura.iloc[0]['iva']:.2f}")

    print(f"TOTAL    : ${factura.iloc[0]['total']:.2f}")

    print("="*55)

    input("\nPresione ENTER para continuar...")

