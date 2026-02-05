
import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

# ==========================================
# CONFIGURACIÓN INICIAL J&J C.A.
# ==========================================
EMPRESA = "J&J C.A."
RUTA_BD = "jyj_erp.db"
RUTA_DATOS = Path("data_jyj")

st.set_page_config(page_title=f"ERP {EMPRESA}", layout="wide", page_icon="🛢️")

# ==========================================
# MOTOR DE BASE DE DATOS Y ARCHIVOS
# ==========================================

def init_db():
    """Inicializa el sistema, crea BD y Carpetas."""
    # Crear Carpetas Físicas
    (RUTA_DATOS / "PROYECTOS").mkdir(parents=True, exist_ok=True)
    (RUTA_DATOS / "SOLVENCIAS").mkdir(parents=True, exist_ok=True)
    (RUTA_DATOS / "FINANZAS").mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(RUTA_BD)
    c = conn.cursor()
    
    # Tabla Proyectos
    c.execute('''CREATE TABLE IF NOT EXISTS proyectos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        filial TEXT,
        nombre TEXT,
        fecha_inicio TEXT,
        estado TEXT
    )''')
    
    # Tabla Finanzas
    c.execute('''CREATE TABLE IF NOT EXISTS finanzas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT, 
        monto REAL,
        descripcion TEXT,
        fecha TEXT
    )''')
    
    # Tabla Archivos
    c.execute('''CREATE TABLE IF NOT EXISTS archivos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        ruta TEXT,
        categoria TEXT,
        subcategoria TEXT,
        fecha_subida TEXT,
        notas TEXT
    )''')
    
    conn.commit()
    conn.close()

# Ejecutar inicio
init_db()

def get_conn():
    conn = sqlite3.connect(RUTA_BD)
    conn.row_factory = sqlite3.Row
    return conn

def guardar_archivo(archivo, carpeta_categoria, subcat=""):
    """Guarda el archivo en disco y lo registra en la BD."""
    if archivo is None: return None
    
    # Crear nombre único con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"{timestamp}_{archivo.name}"
    ruta_final = RUTA_DATOS / carpeta_categoria / nombre_archivo
    
    with open(ruta_final, "wb") as f:
        f.write(archivo.getbuffer())
        
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO archivos (nombre, ruta, categoria, subcategoria, fecha_subida, notas) VALUES (?, ?, ?, ?, ?, ?)",
              (archivo.name, str(ruta_final), carpeta_categoria, subcat, str(datetime.now()), ""))
    conn.commit()
    conn.close()
    return str(ruta_final)

# ==========================================
# INTERFAZ DE USUARIO
# ==========================================

st.sidebar.title(f"🛢️ {EMPRESA}")
st.sidebar.markdown("Contratista PDVSA")

# Menú
menu = ["🏠 Dashboard", "🏗️ Proyectos", "📜 Solvencias", "💰 Finanzas", "📂 Archivos Global"]
opcion = st.sidebar.radio("Menú", menu)

# --- DASHBOARD ---
if opcion == "🏠 Dashboard":
    st.title(f"Panel de Control - {EMPRESA}")
    
    conn = get_conn()
    
    # Métricas
    proyectos = len(conn.execute("SELECT * FROM proyectos").fetchall())
    archivos = len(conn.execute("SELECT * FROM archivos").fetchall())
    balance_row = conn.execute("SELECT SUM(monto) FROM finanzas").fetchone()
    balance = balance_row[0] if balance_row[0] else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Proyectos Activos", proyectos)
    col2.metric("Archivos Digitales", archivos)
    col3.metric("Balance Total", f"${balance:,.2f}")
    
    st.info(f"Base de datos: `{RUTA_BD}` | Carpeta de Datos: `{RUTA_DATOS.resolve()}`")

# --- PROYECTOS ---
elif opcion == "🏗️ Proyectos":
    st.header("Gestión de Contratos PDVSA")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.form("nuevo_proyecto"):
            st.subheader("Nuevo Contrato")
            codigo = st.text_input("Código Contrato (Ej: 2400555)")
            filial = st.selectbox("Filial", ["Bariven", "Petrocedeño", "CVP", "PDVSA Occidente"])
            nombre = st.text_input("Descripción")
            fecha = st.date_input("Fecha Inicio")
            
            if st.form_submit_button("Crear Proyecto"):
                conn = get_conn()
                conn.execute("INSERT INTO proyectos (codigo, filial, nombre, fecha_inicio, estado) VALUES (?, ?, ?, ?, 'Activo')",
                             (codigo, filial, nombre, str(fecha)))
                conn.commit()
                conn.close()
                st.success("Proyecto Creado")
                st.rerun()
                
    with col2:
        conn = get_conn()
        proyectos = conn.execute("SELECT * FROM proyectos ORDER BY id DESC").fetchall()
        
        if proyectos:
            for p in proyectos:
                with st.expander(f"🏗️ {p['codigo']} - {p['filial']}"):
                    st.write(f"**Nombre:** {p['nombre']}")
                    st.write(f"**Estado:** {p['estado']}")
                    
                    # Subir archivo al proyecto
                    archivo_p = st.file_uploader("Subir documento a este contrato", key=f"up_{p['id']}")
                    
                    if archivo_p:
                        subcat_proyecto = f"{p['codigo']}_{p['filial']}"
                        guardar_archivo(archivo_p, "PROYECTOS", subcat_proyecto)
                        st.success("Archivo guardado")
                        st.rerun()
                    
                    # Ver archivos del proyecto
                    archivos_p = conn.execute("SELECT * FROM archivos WHERE categoria='PROYECTOS' AND subcategoria=?", 
                                             (f"{p['codigo']}_{p['filial']}",)).fetchall()
                    if archivos_p:
                        st.write("Documentos:")
                        for a in archivos_p:
                            st.caption(f"📄 {a['nombre']}")
        else:
            st.warning("No hay proyectos creados.")

# --- SOLVENCIAS ---
elif opcion == "📜 Solvencias":
    st.header("Solvencias Especiales PDVSA")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.form("solvencia"):
            st.subheader("Subir Solvencia")
            tipo = st.selectbox("Tipo", ["COFACE", "LUT", "Solvencia Laboral", "IVA", "ISLR"])
            archivo = st.file_uploader("Archivo PDF/Img")
            
            if st.form_submit_button("Guardar"):
                if archivo:
                    guardar_archivo(archivo, "SOLVENCIAS", tipo)
                    conn = get_conn()
                    conn.execute("UPDATE archivos SET notas='Solvencia subida recientemente' WHERE id=(SELECT MAX(id) FROM archivos)")
                    conn.commit()
                    conn.close()
                    st.success("Guardado")
                    st.rerun()
                else:
                    st.error("Por favor selecciona un archivo.")
    
    with col2:
        conn = get_conn()
        docs = conn.execute("SELECT * FROM archivos WHERE categoria='SOLVENCIAS' ORDER BY id DESC").fetchall()
        if docs:
            for d in docs:
                with st.expander(f"📜 {d['subcategoria']} - {d['nombre']}"):
                    st.write(f"Subido: {d['fecha_subida']}")
                    if Path(d['ruta']).exists():
                        with open(d['ruta'], "rb") as f:
                            st.download_button("Descargar", f, d['nombre'])
                    else:
                        st.error("Archivo no encontrado en disco.")

# --- FINANZAS ---
elif opcion == "💰 Finanzas":
    st.header("Balances y Movimientos")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.form("movimiento"):
            st.subheader("Registrar Movimiento")
            tipo = st.selectbox("Tipo", ["Ingreso", "Egreso"])
            monto = st.number_input("Monto", min_value=0.0, format="%.2f")
            desc = st.text_input("Descripción")
            
            if st.form_submit_button("Registrar"):
                conn = get_conn()
                conn.execute("INSERT INTO finanzas (tipo, monto, descripcion, fecha) VALUES (?, ?, ?, ?)",
                             (tipo, monto, desc, str(datetime.now())))
                conn.commit()
                conn.close()
                st.success("Registrado")
                st.rerun()
    
    with col2:
        conn = get_conn()
        movs = conn.execute("SELECT * FROM finanzas ORDER BY id DESC").fetchall()
        if movs:
            df = pd.DataFrame(movs)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Sin movimientos")

# --- ARCHIVOS GLOBAL ---
elif opcion == "📂 Archivos Global":
    st.header("Buscador y Gestión de Archivos")
    
    buscador = st.text_input("🔍 Buscar archivo por nombre o tipo...")
    
    conn = get_conn()
    if buscador:
        resultados = conn.execute("SELECT * FROM archivos WHERE nombre LIKE ? OR subcategoria LIKE ?", 
                                 (f'%{buscador}%', f'%{buscador}%')).fetchall()
    else:
        resultados = conn.execute("SELECT * FROM archivos ORDER BY id DESC LIMIT 50").fetchall()
        
    if resultados:
        for r in resultados:
            with st.expander(f"📂 {r['categoria']}/{r['subcategoria']} -> 📄 {r['nombre']}"):
                st.write(f"**Ruta:** `{r['ruta']}`")
                st.write(f"**Fecha:** {r['fecha_subida']}")
                if Path(r['ruta']).exists():
                    with open(r['ruta'], "rb") as f:
                        st.download_button("Descargar", f, r['nombre'])
    else:
        st.warning("No se encontraron archivos.")

# Cerrar conexión al final del script
conn = get_conn()
conn.close()
pandas
