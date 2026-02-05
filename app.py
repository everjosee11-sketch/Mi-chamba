import streamlit as st
import json
import os
import pandas as pd

# --- LÓGICA DE DATOS ---
def cargar_datos():
    if os.path.exists('datos_empresa.json'):
        with open('datos_empresa.json', 'r') as f:
            return json.load(f)
    return {
        "inventario": {"Producto A": {"precio": 10.0, "stock": 50}},
        "ventas": []
    }

def guardar_datos(datos):
    with open('datos_empresa.json', 'w') as f:
        json.dump(datos, f, indent=4)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mi Empresa Digital", layout="wide")
datos = cargar_datos()

st.title("📊 Panel de Gestión Empresarial")

# --- BARRA LATERAL (Navegación) ---
menu = st.sidebar.selectbox("Ir a:", ["Inventario", "Nueva Venta", "Reportes"])

# --- SECCIÓN: INVENTARIO ---
if menu == "Inventario":
    st.header("📦 Control de Inventario")
    
    with st.form("nuevo_producto"):
        col1, col2, col3 = st.columns(3)
        nombre = col1.text_input("Nombre del Producto")
        precio = col2.number_input("Precio", min_value=0.0)
        stock = col3.number_input("Stock Inicial", min_value=0)
        
        if st.form_submit_button("Agregar/Actualizar"):
            datos["inventario"][nombre] = {"precio": precio, "stock": stock}
            guardar_datos(datos)
            st.success(f"Producto {nombre} actualizado")

    # Mostrar tabla de productos
    if datos["inventario"]:
        df_inv = pd.DataFrame.from_dict(datos["inventario"], orient='index')
        st.table(df_inv)

# --- SECCIÓN: NUEVA VENTA ---
elif menu == "Nueva Venta":
    st.header("💰 Registrar Venta")
    
    opciones_prod = list(datos["inventario"].keys())
    seleccion = st.selectbox("Selecciona producto:", opciones_prod)
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    
    if st.button("Confirmar Venta"):
        stock_actual = datos["inventario"][seleccion]["stock"]
        if stock_actual >= cantidad:
            # Procesar venta
            datos["inventario"][seleccion]["stock"] -= cantidad
            total = datos["inventario"][seleccion]["precio"] * cantidad
            datos["ventas"].append({"producto": seleccion, "cantidad": cantidad, "total": total})
            
            guardar_datos(datos)
            st.balloons()
            st.success(f"Venta realizada: ${total}")
        else:
            st.error("No hay suficiente stock.")

# --- SECCIÓN: REPORTES ---
elif menu == "Reportes":
    st.header("📈 Análisis de Negocio")
    
    if datos["ventas"]:
        df_ventas = pd.DataFrame(datos["ventas"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Ventas Totales", f"${df_ventas['total'].sum()}")
        with col2:
            st.metric("Productos Vendidos", df_ventas['cantidad'].sum())
            
        st.subheader("Histórico de Ventas")
        st.dataframe(df_ventas)
        
        # Gráfico simple
        st.bar_chart(df_ventas.set_index('producto')['total'])
    else:
        st.info("Aún no hay ventas registradas.")
