import streamlit as st
import pandas as pd
from datetime import datetime

# 1. ESTILO "COMMAND CENTER" (Futurista y Funcional)
st.set_page_config(page_title="CORE COMMAND", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #c9d1d9; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: #58a6ff;
    }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; }
    .employee-card {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 5px solid #238636;
    }
    .neon-text { color: #58a6ff; text-shadow: 0 0 5px #58a6ff; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE PERSISTENCIA (Base de Datos Temporal)
if 'nomina' not in st.session_state:
    st.session_state.nomina = {} # Formato: { 'Nombre': {datos, documentos} }

# 3. ENCABEZADO
st.markdown('<h1 class="neon-text">CORE_SYSTEM_OS v4.0</h1>', unsafe_allow_html=True)
st.caption(f"Terminal Activa: iPhone User | Fecha: {datetime.now().strftime('%d/%m/%Y')}")

# 4. PANELES DE CONTROL
tabs = st.tabs(["👥 PERSONAL & CARPETAS", "💰 NÓMINAS & COSTOS", "📁 CARGAR DOCUMENTOS"])

# --- PESTAÑA 1: GESTIÓN DE PERSONAS Y EXPEDIENTES ---
with tabs[0]:
    col_f1, col_f2 = st.columns([1, 2])
    
    with col_f1:
        st.subheader("Crear Expediente")
        with st.form("crear_persona"):
            nombre = st.text_input("Nombre Completo")
            cargo = st.text_input("Cargo / Función")
            salario = st.number_input("Salario Base", min_value=0)
            if st.form_submit_button("CREAR CARPETA"):
                if nombre and nombre not in st.session_state.nomina:
                    st.session_state.nomina[nombre] = {
                        "cargo": cargo,
                        "salario": salario,
                        "docs": [],
                        "fecha_ingreso": datetime.now().strftime("%Y-%m-%d")
                    }
                    st.success(f"Carpeta de {nombre} creada.")
                    st.rerun()

    with col_f2:
        st.subheader("Expedientes Activos")
        for persona, datos in list(st.session_state.nomina.items()):
            with st.container():
                st.markdown(f"""
                <div class="employee-card">
                    <h3 style="margin:0;">📂 {persona}</h3>
                    <p style="color:#8b949e; font-size:14px;">Cargo: {datos['cargo']} | Ingreso: {datos['fecha_ingreso']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                if c1.button(f"Ver Documentos ({len(datos['docs'])})", key=f"ver_{persona}"):
                    st.write(f"Documentos en carpeta: {datos['docs']}")
                
                if c2.button(f"🗑️ ELIMINAR EXPEDIENTE", key=f"del_{persona}"):
                    del st.session_state.nomina[persona]
                    st.rerun()

# --- PESTAÑA 2: NÓMINAS & PRESUPUESTOS ---
with tabs[1]:
    st.subheader("Control Financiero de Nómina")
    if st.session_state.nomina:
        df_data = []
        for p, d in st.session_state.nomina.items():
            df_data.append({"Empleado": p, "Cargo": d['cargo'], "Sueldo": d['salario']})
        
        df = pd.DataFrame(df_data)
        st.table(df)
        
        total = df['Sueldo'].sum()
        st.metric("COSTO MENSUAL TOTAL", f"${total:,.2f}", delta="Costo Operativo")
    else:
        st.info("No hay personal registrado para calcular nómina.")

# --- PESTAÑA 3: CARGA DE ARCHIVOS (IMÁGENES/PDF) ---
with tabs[2]:
    st.subheader("Subir Contratos / ART / Fotos")
    if st.session_state.nomina:
        empleado_sel = st.selectbox("Seleccionar Carpeta de Destino", list(st.session_state.nomina.keys()))
        archivo = st.file_uploader("Subir Imagen o Documento", type=['png', 'jpg', 'pdf'])
        
        if st.button("SUBIR A EXPEDIENTE"):
            if archivo:
                # En un app real esto iría a la nube, aquí simulamos la ruta
                st.session_state.nomina[empleado_sel]['docs'].append(archivo.name)
                st.success(f"Archivo '{archivo.name}' guardado en la carpeta de {empleado_sel}")
            else:
                st.error("Selecciona un archivo primero.")
    else:
        st.warning("Debe crear al menos un empleado para subir documentos.")
