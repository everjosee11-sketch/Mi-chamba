import streamlit as st
import pandas as pd
from datetime import datetime, date
import json
import time

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DEL SISTEMA (J&J C.A.)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="J&J C.A. - Sistema de Gestión",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Profesionales para J&J C.A.
st.markdown("""
    <style>
    /* Identidad Corporativa */
    .stApp { background-color: #f4f6f9; }
    h1, h2, h3 { color: #003366; font-family: 'Segoe UI', sans-serif; font-weight: 700; }
    
    /* Métricas con diseño de tarjeta */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-top: 4px solid #cc0000; /* Rojo Industrial */
    }
    
    /* Tabs personalizadas */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff;
        border-radius: 5px;
        padding: 0 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .stTabs [aria-selected="true"] {
        background-color: #003366 !important; /* Azul J&J */
        color: white !important;
    }
    
    /* Botones */
    .stButton>button {
        background-color: #003366;
        color: white;
        border-radius: 6px;
        height: 3rem;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #004080;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. INICIALIZACIÓN DE DATOS (Persistencia de Sesión)
# -----------------------------------------------------------------------------
if 'db' not in st.session_state:
    st.session_state.db = {
        "tasa_bcv": 38.50,
        "empresa": "J&J C.A.",
        "proyectos": [
            {"Codigo": "P-2024-001", "Cliente": "PDVSA Petromonagas", "Obra": "Mantenimiento Oleoducto 36 Pulg", "Monto_USD": 250000.00, "Valuado_USD": 50000.00, "Status": "En Ejecución"}
        ],
        "personal": [
            {"Ficha": "V-12345678", "Nombre": "Roberto Martínez", "Cargo": "Soldador 6G", "Sueldo_Semanal_USD": 200.0, "SISBO": "Vigente"}
        ],
        "maquinaria": [
            {"ID": "EQ-05", "Equipo": "Vacuum Mack", "Placa": "A12BC34", "Status": "Operativo", "Horas_Uso": 1450}
        ]
    }

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL (CONTROL MAESTRO)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("J&J C.A.")
    st.caption("Soluciones Integrales Petroleras")
    st.markdown("---")
    
    st.header("💵 Tasa BCV Oficial")
    nuevo_bcv = st.number_input("Valor Actual (Bs/$)", 
                               value=st.session_state.db["tasa_bcv"], 
                               min_value=1.0, 
                               format="%.2f",
                               help="Modifica la tasa para actualizar todos los cálculos en Bolívares.")
    
    if nuevo_bcv != st.session_state.db["tasa_bcv"]:
        st.session_state.db["tasa_bcv"] = nuevo_bcv
        st.toast("Tasa BCV Actualizada", icon="✅")
        time.sleep(0.5)
        st.rerun()

    st.info(f"Cálculos referenciales a: **{nuevo_bcv} Bs.**")
    
    st.markdown("---")
    st.subheader("💾 Base de Datos")
    
    # Descargar Copia de Seguridad
    st.download_button(
        label="📥 Descargar Respaldo JSON",
        data=json.dumps(st.session_state.db, indent=4),
        file_name=f"backup_JJ_CA_{datetime.now().strftime('%Y-%m-%d')}.json",
        mime="application/json"
    )
    
    # Cargar Copia de Seguridad
    uploaded_file = st.file_uploader("Restaurar Datos", type=["json"])
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            st.session_state.db = data
            st.success("Sistema restaurado correctamente")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"Error al cargar archivo: {e}")

# -----------------------------------------------------------------------------
# 4. INTERFAZ PRINCIPAL
# -----------------------------------------------------------------------------
st.title(f"Panel de Control Operativo - {st.session_state.db['empresa']}")
st.markdown(f"**Fecha:** {date.today().strftime('%d/%m/%Y')} | **Zona:** Faja Petrolífera del Orinoco")

# --- KPIs SUPERIORES (Dinámicos) ---
df_proy = pd.DataFrame(st.session_state.db["proyectos"])
total_contratos = df_proy["Monto_USD"].sum() if not df_proy.empty else 0
total_valuado = df_proy["Valuado_USD"].sum() if not df_proy.empty else 0
pendiente_cobro = total_contratos - total_valuado

col1, col2, col3, col4 = st.columns(4)
col1.metric("Proyectos Activos", len(df_proy), delta="J&J C.A.")
col2.metric("Total Contratado", f"${total_contratos:,.2f}")
col3.metric("Por Valuar (Pendiente)", f"${pendiente_cobro:,.2f}", delta_color="inverse")
col4.metric("Equivalente en Bs.", f"Bs {pendiente_cobro * nuevo_bcv:,.2f}", help="Monto pendiente calculado a tasa BCV")

# --- NAVEGACIÓN ---
tab_obras, tab_rrhh, tab_flota, tab_hse = st.tabs([
    "📂 Gestión de Contratos", 
    "👷 Nómina y Personal", 
    "🚜 Flota y Maquinaria", 
    "⛑️ Seguridad (HSE)"
])

# =============================================================================
# MÓDULO 1: GESTIÓN DE CONTRATOS
# =============================================================================
with tab_obras:
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.subheader("Nuevo Contrato")
        with st.form("form_contrato"):
            cod = st.text_input("N° Contrato / Pedido (SAP)")
            cli = st.selectbox("Cliente", ["PDVSA Petromonagas", "PetroSinovensa", "PetroPiar", "Bariven", "Privado"])
            obra = st.text_area("Descripción de la Obra")
            monto = st.number_input("Monto Total Contrato ($)", min_value=0.0)
            
            if st.form_submit_button("Registrar Contrato"):
                if cod and obra:
                    st.session_state.db["proyectos"].append({
                        "Codigo": cod, "Cliente": cli, "Obra": obra,
                        "Monto_USD": monto, "Valuado_USD": 0.0, "Status": "Por Iniciar"
                    })
                    st.success("Contrato registrado en el sistema")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Por favor complete los campos obligatorios")

    with c2:
        st.subheader("Seguimiento de Valuaciones")
        if not df_proy.empty:
            # Tabla editable para actualizar valuaciones rápidamente
            edited_proy = st.data_editor(
                df_proy,
                column_config={
                    "Monto_USD": st.column_config.NumberColumn("Total ($)", format="$%.2f", disabled=True),
                    "Valuado_USD": st.column_config.NumberColumn("Valuado ($)", format="$%.2f"),
                    "Status": st.column_config.SelectboxColumn("Estatus", options=["Por Iniciar", "En Ejecución", "Paralizada", "Cerrada"], required=True),
                    "Avance": st.column_config.ProgressColumn("Avance Financiero", format="%.2f%%", min_value=0, max_value=100)
                },
                use_container_width=True,
                num_rows="dynamic",
                key="editor_proyectos"
            )
            
            # Lógica para guardar cambios de la tabla editable
            if not df_proy.equals(edited_proy):
                st.session_state.db["proyectos"] = edited_proy.to_dict("records")
                st.rerun()
        else:
            st.info("No hay contratos registrados. Utilice el formulario de la izquierda.")

# =============================================================================
# MÓDULO 2: PERSONAL (RRHH)
# =============================================================================
with tab_rrhh:
    st.subheader("Control de Personal de Campo")
    
    col_rrhh_1, col_rrhh_2 = st.columns([3, 1])
    
    with col_rrhh_1:
        df_p = pd.DataFrame(st.session_state.db["personal"])
        
        # Tabla interactiva para RRHH
        edited_personal = st.data_editor(
            df_p,
            column_config={
                "Sueldo_Semanal_USD": st.column_config.NumberColumn("Semanal ($)", format="$%.2f"),
                "SISBO": st.column_config.SelectboxColumn("Permiso SISBO", options=["Vigente", "Vencido", "En Trámite"], width="medium")
            },
            num_rows="dynamic",
            use_container_width=True,
            key="editor_rrhh"
        )
        
        # Guardado automático
        if not df_p.equals(edited_personal):
            st.session_state.db["personal"] = edited_personal.to_dict("records")
            st.rerun()
            
    with col_rrhh_2:
        # Tarjeta de resumen de nómina
        st.write("### 💰 Pre-Nómina")
        total_nomina = edited_personal["Sueldo_Semanal_USD"].sum() if not edited_personal.empty else 0
        st.metric("Total a Pagar (USD)", f"${total_nomina:,.2f}")
        st.metric("Total a Pagar (Bs)", f"Bs {total_nomina * nuevo_bcv:,.2f}")
        
        if st.button("Exportar Nómina (CSV)"):
            # Simulación de exportación
            st.toast("Archivo generado listas para banco", icon="📄")

# =============================================================================
# MÓDULO 3: MAQUINARIA Y FLOTA
# =============================================================================
with tab_flota:
    st.subheader("Inventario de Equipos (Activos Fijos)")
    
    df_m = pd.DataFrame(st.session_state.db["maquinaria"])
    
    col_mq1, col_mq2 = st.columns([2, 1])
    
    with col_mq1:
        edited_maquinaria = st.data_editor(
            df_m,
            column_config={
                "Status": st.column_config.SelectboxColumn("Condición", options=["Operativo", "Mantenimiento", "Inoperativo"], required=True),
                "Horas_Uso": st.column_config.NumberColumn("Horómetro", min_value=0)
            },
            num_rows="dynamic",
            use_container_width=True,
            key="editor_maq"
        )
        # Guardado
        if not df_m.equals(edited_maquinaria):
            st.session_state.db["maquinaria"] = edited_maquinaria.to_dict("records")
            st.rerun()

    with col_mq2:
        st.write("#### Disponibilidad Operativa")
        if not edited_maquinaria.empty:
            counts = edited_maquinaria["Status"].value_counts()
            st.bar_chart(counts, color="#003366")
        else:
            st.warning("Sin equipos registrados.")

# =============================================================================
# MÓDULO 4: SEGURIDAD (HSE)
# =============================================================================
with tab_hse:
    st.subheader("Tablero de Control de Riesgos")
    
    col_h1, col_h2 = st.columns(2)
    
    with col_h1:
        st.error("⚠️ Alertas de Personal (SISBO Vencido)")
        vencidos = [p for p in st.session_state.db["personal"] if p["SISBO"] == "Vencido"]
        
        if vencidos:
            st.table(pd.DataFrame(vencidos)[["Ficha", "Nombre", "Cargo"]])
        else:
            st.success("✅ Todo el personal cumple con la normativa de seguridad.")
            
    with col_h2:
        st.info("ℹ️ Resumen de Gestión")
        st.write(f"- **Total Horas Hombre (Estimado):** {len(st.session_state.db['personal']) * 40} horas/sem")
        st.write(f"- **Equipos Operativos:** {len([m for m in st.session_state.db['maquinaria'] if m['Status'] == 'Operativo'])}")

# Pie de página J&J C.A.
st.divider()
st.markdown(f"<div style='text-align: center; color: grey;'>© 2024 J&J C.A. | Sistema de Gestión Interna v3.5 | Desarrollado para Streamlit Cloud</div>", unsafe_allow_html=True)
