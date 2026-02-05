
    .brand-title {{
        color: #00fbff;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: 12px;
        margin: 0;
        text-shadow: 0 0 20px rgba(0, 251, 255, 0.4);
    }}

    /* Estilo de Expedientes (Cards) */
    .folder-box {{
        background: #0d0d0d;
        border: 1px solid #1f1f1f;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-top: 2px solid #00fbff22;
        transition: 0.3s;
    }}
    .folder-box:hover {{ border-color: #00fbff; box-shadow: 0 0 15px rgba(0, 251, 255, 0.1); }}

    /* Inputs de Consola */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {{
        background-color: #000 !important;
        border: 1px solid #333 !important;
        color: #00fbff !important;
    }}

    /* Botones de Comando */
    .stButton>button {{
        border: 1px solid #00fbff;
        background: transparent;
        color: #00fbff;
        text-transform: uppercase;
        font-weight: bold;
        width: 100%;
        border-radius: 5px;
    }}
    .stButton>button:hover {{
        background: #00fbff;
        color: #000;
        box-shadow: 0 0 25px #00fbff;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS LOCAL (SESSION) ---
if 'db_jj' not in st.session_state:
    st.session_state.db_jj = {}

# --- RENDER DE IDENTIDAD CORPORATIVA ---
st.markdown(f"""
    <div class="brand-container">
        <p style="color: #00fbff66; font-size: 11px; margin: 0; letter-spacing: 2px;">// ENTERPRISE_RESOURCE_MANAGEMENT //</p>
        <h1 class="brand-title">{EMPRESA}</h1>
    </div>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN POR MÓDULOS ---
tabs = st.tabs(["[ 👤 PERSONAL ]", "[ 📂 EXPEDIENTES ]", "[ 💰 NÓMINA ]"])

# 1. MÓDULO: CREACIÓN DE PERSONAL
with tabs[0]:
    st.markdown("### >>_INITIALIZE_NEW_CARRIER")
    with st.expander("FORMULARIO DE INGRESO"):
        with st.form("form_jj"):
            c1, c2 = st.columns(2)
            nombre = c1.text_input("NOMBRE_COMPLETO")
            cargo = c2.text_input("CARGO_ASIGNADO")
            dni = c1.text_input("DNI_ID_LEGAL")
            sueldo = c2.number_input("SUELDO_BASE ($)", min_value=0.0)
            
            if st.form_submit_button("SINCRONIZAR CON J&J C.A."):
                if nombre:
                    st.session_state.db_jj[nombre] = {
                        "cargo": cargo, "dni": dni, "sueldo": sueldo,
                        "docs": [], "logs": [f"Init: {datetime.now().strftime('%Y-%m-%d %H:%M')}"]
                    }
                    st.success(f"CARPETA GENERADA: {nombre}")
                    st.rerun()

    st.write("---")
    if not st.session_state.db_jj:
        st.info("SISTEMA_STANDBY: No hay carpetas activas.")
    else:
        for emp, data in list(st.session_state.db_jj.items()):
            st.markdown(f"""
            <div class="folder-box">
                <span style="color:#888; font-size:10px;">ID_REF: {hash(emp) % 10000}</span>
                <h4 style="margin:5px 0; color:#fff;">📂 {emp}</h4>
                <p style="font-size:12px; color:#00fbff;">{data['cargo']} | Sueldo: ${data['sueldo']:,}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"BORRAR_REGISTRO: {emp}", key=f"del_{emp}"):
                del st.session_state.db_jj[emp]
                st.rerun()

# 2. MÓDULO: ARCHIVOS Y DOCUMENTACIÓN
with tabs[1]:
    st.markdown("### >>_BLOB_STORAGE_VINCULATOR")
    if st.session_state.db_jj:
        target = st.selectbox("DIRECCIONAR_A_CARPETA:", list(st.session_state.db_jj.keys()))
        up_file = st.file_uploader("SUBIR_FOTO_CONTRATO_ART_DNI", type=['png', 'jpg', 'jpeg', 'pdf'])
        
        if st.button("VINCULAR_ARCHIVO"):
            if up_file:
                st.session_state.db_jj[target]['docs'].append({
                    "name": up_file.name,
                    "date": datetime.now().strftime('%d/%m/%Y')
                })
                st.success(f"'{up_file.name}' VINCULADO A {target}")
            else:
                st.error("ERROR: NO_SOURCE_FILE")
        
        st.write("---")
        st.markdown(f"#### CONTENIDO_VIRTUAL: {target}")
        if not st.session_state.db_jj[target]['docs']:
            st.text("Carpeta vacía.")
        else:
            for d in st.session_state.db_jj[target]['docs']:
                st.code(f"ARCHIVO: {d['name']} | FECHA: {d['date']}")
    else:
        st.warning("ERROR: Se requiere al menos un expediente creado.")

# 3. MÓDULO: NÓMINA FINANCIERA
with tabs[2]:
    st.markdown("### >>_FINANCIAL_CORE_REPORTS")
    if st.session_state.db_jj:
        data_table = [{"EMPLEADO": k, "CARGO": v['cargo'], "SUELDO": v['sueldo']} for k, v in st.session_state.db_jj.items()]
        df = pd.DataFrame(data_table)
        st.dataframe(df, use_container_width=True)
        
        total_pago = df["SUELDO"].sum()
        st.markdown(f"""
            <div style="background:rgba(0,251,255,0.05); border:1px solid #00fbff; padding:30px; border-radius:10px; text-align:right;">
                <p style="color:#00fbff; font-size:12px; margin:0; letter-spacing:3px;">TOTAL_PAYROLL_J&J_CA</p>
                <h1 style="color:#fff; margin:0; font-size:45px;">$ {total_pago:,.2f}</h1>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("NO_DATA_FOR_CALCULATION")
