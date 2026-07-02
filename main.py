from funciones import *

while True:

    menu()

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        """crear_factura()"""

    elif opcion == "2":
        menu_inventario()

    elif opcion == "3":
        registrar_cliente()

    elif opcion == "4":
        ver_clientes()

    elif opcion == "5":
        """reportes()"""

    elif opcion == "0":
        print("Gracias por usar el sistema.")
        break

    else:
        print("Opción inválida.")