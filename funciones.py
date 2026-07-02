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