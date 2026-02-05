import json
import os

class Empresa:
    def __init__(self, nombre_archivo='datos_empresa.json'):
        self.nombre_archivo = nombre_archivo
        self.datos = self.cargar_datos()

    def cargar_datos(self):
        """Carga la base de datos desde un archivo JSON."""
        if os.path.exists(self.nombre_archivo):
            with open(self.nombre_archivo, 'r') as f:
                return json.load(f)
        return {
            "inventario": {},
            "clientes": [],
            "finanzas": {"balance": 0.0, "ventas_totales": 0}
        }

    def guardar_datos(self):
        """Guarda el estado actual en el archivo JSON."""
        with open(self.nombre_archivo, 'w') as f:
            json.dump(self.datos, f, indent=4)

    def agregar_producto(self, nombre, precio, stock):
        self.datos["inventario"][nombre] = {"precio": precio, "stock": stock}
        self.guardar_datos()
        print(f"\n✅ Producto '{nombre}' registrado.")

    def registrar_venta(self, nombre, cantidad):
        if nombre in self.datos["inventario"] and self.datos["inventario"][nombre]["stock"] >= cantidad:
            precio_unitario = self.datos["inventario"][nombre]["precio"]
            total = precio_unitario * cantidad
            
            # Actualizar Stock
            self.datos["inventario"][nombre]["stock"] -= cantidad
            # Actualizar Finanzas
            self.datos["finanzas"]["balance"] += total
            self.datos["finanzas"]["ventas_totales"] += 1
            
            self.guardar_datos()
            print(f"\n💰 Venta exitosa: {cantidad}x {nombre}. Total: ${total}")
        else:
            print("\n❌ Error: Stock insuficiente o producto no existe.")

    def reporte_general(self):
        print("\n" + "="*30)
        print(f"📊 REPORTE DE GESTIÓN")
        print("="*30)
        print(f"💰 Balance en Caja: ${self.datos['finanzas']['balance']}")
        print(f"📦 Productos en Inventario: {len(self.datos['inventario'])}")
        print("-" * 30)
        for prod, info in self.datos["inventario"].items():
            print(f"- {prod}: ${info['precio']} (Stock: {info['stock']})")
        print("="*30)

def menu():
    mi_negocio = Empresa()
    
    while True:
        print("\n--- SISTEMA EMPRESARIAL DIGITAL ---")
        print("1. Inventario (Agregar/Actualizar)")
        print("2. Registrar Venta")
        print("3. Ver Reporte de Empresa")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nom = input("Nombre del producto: ")
            try:
                pre = float(input("Precio: "))
                can = int(input("Cantidad: "))
                mi_negocio.agregar_producto(nom, pre, can)
            except ValueError:
                print("Error: Ingrese números válidos para precio y cantidad.")

        elif opcion == '2':
            nom = input("Producto vendido: ")
            try:
                can = int(input("Cantidad: "))
                mi_negocio.registrar_venta(nom, can)
            except ValueError:
                print("Error: Ingrese una cantidad válida.")

        elif opcion == '3':
            mi_negocio.reporte_general()

        elif opcion == '4':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
