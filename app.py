import streamlit as st
import pandas as pd

# Configuración de la página con estilo oscuro
st.set_page_config(page_title="CORE Enterprise", layout="wide")

# Inyectar CSS para la estética futurista y "Glassmorphism"
st.markdown("""
    <style>
    .main { background-color: #02040a; color: #e2e8f0; }
    .stButton>button {
        border: 1px solid #22d3ee;
        background-color: rgba(34, 211, 238, 0.1);
        color: #22d3ee;
        border-radius: 20px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #22d3ee;
        color: black;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        border-left: 4px solid #22d3ee;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE DATOS (Estado de la sesión) ---
if 'proyectos' not in st.session_state:
    st.session_state.proyectos = [
        {"Nombre": "Torre Norte", "Presupuesto": 150000, "Personal": 12, "ART": "Al día", "Avance": 65},
        {"Nombre": "Refinería Delta", "Presupuesto": 450000, "Personal": 45, "ART": "Pendiente", "Avance": 20}
    ]

# --- LÓGICA DE NEGOCIO ---
df = pd.DataFrame(st.session_state.proyectos)
total_presupuesto = df['Presupuesto'].sum()

# --- INTERFAZ ---
st.title("CORE.")
st.caption("ENTERPRISE RESOURCE CONTROL v4.0")

# Fila de métricas
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card"><h5>Capital Total</h5><h2>${total_presupuesto:,}</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><h5>Staff Activo</h5><h2>{df["Personal"].sum()}</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><h5>Proyectos</h5><h2>{len(df)}</h2></div>', unsafe_allow_html=True)

st.divider()

# Sección de Control
tab1, tab2 = st.tabs(["📊 Monitor de Avance", "➕ Agregar Proyecto"])

with tab1:
    st.subheader("Estado de Proyectos")
    for idx, p in df.iterrows():
        with st.expander(f"{p['Nombre']} - {p['Avance']}%"):
            c1, c2, c3 = st.columns(3)
            c1.write(f"**Presupuesto:** ${p['Presupuesto']:,}")
            c2.write(f"**Personal:** {p['Personal']} operarios")
            c3.write(f"**ART:** {p['ART']}")
            st.progress(p['Avance'] / 100)

with tab2:
    with st.form("nuevo_proyecto"):
        nombre = st.text_input("Nombre del Proyecto")
        pres = st.number_input("Presupuesto ($)", min_value=0)
        pers = st.number_input("Cantidad de Personal", min_value=0)
        art = st.selectbox("Estado ART", ["Al día", "Pendiente", "Vencido"])
        avance = st.slider("Avance inicial (%)", 0, 100, 0)
        
        if st.form_submit_button("Sincronizar con CORE"):
            nuevo = {"Nombre": nombre, "Presupuesto": pres, "Personal": pers, "ART": art, "Avance": avance}
            st.session_state.proyectos.append(nuevo)
            st.rerun()

