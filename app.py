import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="J&J C.A. Ops Center", layout="wide")

# ESTILO "CYBERPUNK" (CSS Personalizado)
st.markdown("""
    <style>
    .main {
        background-color: #00050a;
        color: #e0e0e0;
    }
    .stMetric {
        background-color: rgba(0, 242, 255, 0.05);
        border: 1px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 10px #00f2ff;
    }
    div[data-testid="stVerticalBlock"] > div:has(div.stMetric) {
        background-color: transparent;
    }
    .neon-border-purple {
        border: 2px solid #bc00ff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 15px #bc00ff;
        margin-bottom: 20px;
    }
    .neon-border-green {
        border: 2px solid #39ff14;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 15px #39ff14;
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        color: #00f2ff !important;
        text-shadow: 0 0 10px #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# ENCABEZADO
st.title("⚡ J&J C.A. | Centro de Control Operativo")
st.markdown("---")

# FILA 1: MÉTRICAS CLAVE (INDICADORES RÁPIDOS)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Personal en Campo", value="42", delta="3 hoy")
with col2:
    st.metric(label="Equipos Activos", value="12", delta="-1 mant.")
with col3:
    st.metric(label="Proyectos en Curso", value="5")
with col4:
    st.metric(label="Facturación Pendiente", value="$12.5k")

st.write("")

# FILA 2: MÓDULOS DE GESTIÓN
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown('<div class="neon-border-purple">', unsafe_allow_html=True)
    st.subheader("👥 Gestión de Cuadrillas (RRHH)")
    # Datos simulados de personal
    datos_personal = pd.DataFrame({
        'Proyecto': ['Pozo-01', 'Planta-X', 'Logística', 'Taller'],
        'Personal': [15, 10, 8, 9]
    })
    fig_pers = px.bar(datos_personal, x='Proyecto', y='Personal', 
                     color_discrete_sequence=['#bc00ff'])
    fig_pers.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_pers, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="neon-border-green">', unsafe_allow_html=True)
    st.subheader("🚛 Estatus de Flota y Equipos")
    # Datos simulados de vehículos
    datos_flota = pd.DataFrame({
        'Vehículo': ['Camioneta 01', 'Camioneta 02', 'Grúa 01', 'Camión 05'],
        'Estatus': ['Operativo', 'Operativo', 'Mantenimiento', 'Operativo'],
        'Ubicación': ['Maturín', 'Anaco', 'Base J&J', 'El Tigre']
    })
    st.table(datos_flota)
    st.markdown('</div>', unsafe_allow_html=True)

# FILA 3: PROYECTOS FINANCIEROS
st.markdown('<div style="border: 1px solid #00f2ff; padding: 20px; border-radius: 15px;">', unsafe_allow_html=True)
st.subheader("📊 Avance de Contratos y Finanzas")
tab1, tab2 = st.tabs(["Avance de Obra", "Cuentas por Cobrar"])

with tab1:
    st.info("Visualización de cronogramas de proyectos activos.")
    progreso = st.slider("Avance Proyecto Principal (Contrato PDVSA-XYZ)", 0, 100, 65)
    st.progress(progreso/100)

with tab2:
    st.write("Listado de facturas emitidas por J&J C.A.")
    st.checkbox("Factura #9901 - Procesada")
    st.checkbox("Factura #9902 - Pendiente", value=True)
st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.image("https://via.placeholder.com/150x50.png?text=J%26J+C.A.", use_container_width=True)
st.sidebar.write("Usuario: Administrador")
if st.sidebar.button("Cerrar Sesión"):
    st.write("Saliendo...")
    import streamlit as st
import pandas as pd

st.set_page_config(page_title="J&J C.A. Ops", layout="wide")

# Estilo Neón Básico
st.markdown("<style>main {background-color: #000; color: #00f2ff;}</style>", unsafe_allow_html=True)

st.title("⚡ J&J C.A. | Control Interno")

col1, col2 = st.columns(2)
with col1:
    st.metric("Personal Activo", "42", "3")
with col2:
    st.metric("Equipos en Campo", "12", "-1")

st.subheader("📊 Gráfico de Actividad")
# Gráfico nativo (no necesita plotly)
data = pd.DataFrame({"Proyecto": ["A", "B", "C"], "Horas": [10, 20, 30]})
st.bar_chart(data.set_index("Proyecto"))

st.success("App operativa para J&J C.A.")

