from os import remove
import streamlit as st
from PIL import Image
import hmac
import pandas as pd

# --- CONFIGURACIÓN DE USUARIO Y CONTRASEÑA ---
def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Usuario", key="username")
            st.text_input("Contraseña", type="password", key="password")
            st.form_submit_button("Ingresar", on_click=password_entered)

    def password_entered():
        """Guarda el usuario en session_state tras la autenticación."""
        if st.session_state["username"] in st.secrets["passwords"] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            st.session_state["is_logged_in"] = True
            st.session_state["user_id"] = st.session_state["username"]
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    login_form()

    if "password_correct" in st.session_state:
        st.error("Contraseña o usuario incorrecto")
    return False

# --- PÁGINA DE LOGIN Y ESTILO ---
logo_2 = Image.open("logo_2.png")


###### ESTILO ######
st.markdown("""
    <style>
        /* Selector específico para los botones primarios con 'data-testid' */
        button[data-testid="stBaseButton-primary"] {
            background-color: #27F5E0 !important;  /* Color azul */
            color: white !important;  /* Texto blanco */
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            font-size: 16px !important;
            cursor: pointer;
        }
        /* Selector específico para los botones secundarios con 'data-testid' */
        button[data-testid="stBaseButton-secondary"] {
            background-color: #27B4F5 !important;
            color: white!important;  /* Texto oscuro */
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            font-size: 16px !important;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

if 'is_logged_in' not in st.session_state or not st.session_state['is_logged_in']:
    st.set_page_config(layout="centered")
    st.markdown("""
    <style>
    [data-testid="stApp"] {
        background: #F4F7FD;
    }
    [data-testid="stForm"] {
        background-color: #ffffff;
        border-radius: 10px;
        border: 2px solid #ccc;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([5, 8, 2], vertical_alignment="center")
    with col2:
        st.image(logo_2, width=200)
    st.markdown("""
    <div style="text-align: center; font-size: 30px;">
        <strong><em>Sistema de Evaluación UREP</em></strong>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

else:
    st.set_page_config(page_title="Sistema de Evaluación UREP", layout="wide")
    logo = Image.open("logo_2.png")
    col1, space1, col = st.columns([2, 4.5,10], vertical_alignment="center")
    with col1:
        if st.button("Cerrar sesión", key="cerrar", type="secondary", help="Cerrar sesión", use_container_width=True):
            st.session_state.clear()
            st.switch_page("principal.py")
    with col:
        st.image(logo_2, width=150)

    # Centrar el título
    st.markdown("""
        <style>
            section[data-testid="stMain"] {
                background-color: #f4f7fd !important;
            }
            div[data-testid="stMarkdownContainer"] p {
                font-size: 20px !important;
                color: #000000 !important;
                text-align: center !important;
            }
            .center-title {
                text-align: center !important;
                font-size: 32px !important;
                font-weight: bold !important;
                margin-bottom: 30px !important;
            }
            /* Resalta los campos de texto */
            .stTextInput > div > div > input {
                background-color: #fff !important;
                border: 1.5px solid #b0b0b0 !important;
                color: #222 !important;
            }
            /* Resalta el selectbox */
            div[data-baseweb="select"] > div {
                background-color: #fff !important;
                border: 1.5px solid #b0b0b0 !important;
                color: #222 !important;
            }
            /* Opcional: resalta el menú desplegable */
            div[data-baseweb="popover"] {
                background-color: #fff !important;
                border: 1.5px solid #b0b0b0 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    try:
        df = pd.read_excel("requisitos_urep.xlsx", sheet_name="Documentos")

        tipo = ["Autorización de funcionamiento de establecimientos regulados por la SRS",
                 "Autorización de funcionamiento de unidades de transporte de alimentos regulados por la SRS",
                 "Renovación de Autorización de funcionamiento de establecimientos regulados por la SRS", 
                 "Renovación de funcionamiento de unidades de transporte de alimentos regulados por la SRS"]


        opciones = df["Tipos de establecimientos"].dropna().unique()
        opciones = sorted(opciones)
        opciones.remove("Unidades de transporte de alimentos")


        opciones_unidades=["Autorización de vehículos que transportan alimentos perecederos",
                           "Autorización de vehículos que transportan alimentos no perecederos",
                           "Autorización de vehículos que transportan servicios de banquetes"]
        
        col_left, col_center, col_right = st.columns([0.7, 2, 1])

        with col_center:

            st.markdown('<div class="center-title">Sistema de Evaluación UREP</div>', unsafe_allow_html=True)

            # Campos de entrada resaltados y guardado en session_state
            nombre_titular = st.text_input(
                "Nombre de titular"
            )
            nombre_establecimiento = st.text_input(
                "Nombre de establecimiento"
            )

            tipo_tramite= st.selectbox(
                "Seleccione el tipo de trámite:",
                tipo,
                index=None,
                placeholder="Seleccione una opción"
            )

            if tipo_tramite == "Autorización de funcionamiento de establecimientos regulados por la SRS" or tipo_tramite == "Renovación de Autorización de funcionamiento de establecimientos regulados por la SRS":
                seleccion = st.selectbox(
                    "Seleccione el tipo de establecimiento:",
                    opciones,
                    index=None,
                    placeholder="Seleccione una opción"
                )
                st.session_state["seleccion"] = seleccion
            else:
                seleccion="Unidades de transporte de alimentos"
                st.session_state["seleccion"] = seleccion


        if tipo_tramite == "Autorización de funcionamiento de unidades de transporte de alimentos regulados por la SRS" or tipo_tramite == "Renovación de funcionamiento de unidades de transporte de alimentos regulados por la SRS":
            # Inicialización de estado
            if 'num_fields' not in st.session_state:
                st.session_state['num_fields'] = 1
            if 'fields_active' not in st.session_state:
                st.session_state['fields_active'] = [True] * st.session_state['num_fields']
            if 'placas_vehiculos_dict' not in st.session_state:
                st.session_state['placas_vehiculos_dict'] = {}

            st.write("Detalle el número de placa de cada vehículo:")

            visible_count = 1  # contador para la numeración visual

            for i in range(st.session_state['num_fields']):
                field_key = f"campo_{i}"
                if st.session_state['fields_active'][i]:
                    soli, col1, col2, col3 = st.columns([3, 3, 4, 1])
                    with soli:
                        prev_solicitud = st.session_state['placas_vehiculos_dict'].get(field_key, {}).get("solicitud", st.session_state["numero_solicitud"])
                        new_solicitud = st.text_input(f"Número solicitud {visible_count}", value=prev_solicitud, key=f"solicitud_{i}")
                    with col1:
                        prev_placa = st.session_state['placas_vehiculos_dict'].get(field_key, {}).get("placa", "")
                        new_placa = st.text_input(f"Placas Vehículo No. {visible_count}", value=prev_placa, key=field_key)
                    with col2:
                        prev_tipo = st.session_state['placas_vehiculos_dict'].get(field_key, {}).get("tipo_establecimiento", None)
                        new_tipo = st.selectbox(
                            f"Tipo ficha de inspección {visible_count}",
                            opciones_unidades,
                            index=opciones_unidades.index(prev_tipo) if prev_tipo in opciones_unidades else None,
                            placeholder="Seleccione una opción",
                            key=f"tipo_est_{i}" )
                    with col3:
                        st.write("")  # Espacio para alinear el botón 
                        # No mostrar botón eliminar para el primer campo (i == 0)
                        if i != 0:
                            if st.button("❌", key=f"del_{i}"):
                                st.session_state['fields_active'][i] = False
                                st.rerun()


                    # Guardar los tres valores juntos en el diccionario
                    st.session_state['placas_vehiculos_dict'][field_key] = {
                        "solicitud": new_solicitud,
                        "placa": new_placa,
                        "tipo_establecimiento": new_tipo  # Ahora guarda el valor directo, no como lista
                    }
                    
                    visible_count += 1

            # Botón para agregar nuevos campos
            if st.button("Agregar vehículo"):
                st.session_state['num_fields'] += 1
                st.session_state['fields_active'].append(True)
                new_key = f"campo_{st.session_state['num_fields'] - 1}"
                st.session_state['placas_vehiculos_dict'][new_key] = {"solicitud": st.session_state["numero_solicitud"], "placa": "", "tipo_establecimiento": None}
                st.rerun()

            # Generar la lista final solo con los campos activos
            placas_activas = []
            for i in range(st.session_state['num_fields']):
                if st.session_state['fields_active'][i]:
                    key = f"campo_{i}"
                    par = st.session_state['placas_vehiculos_dict'].get(key, {})
                    if par.get("solicitud") or par.get("placa"):
                        placas_activas.append(par)

            st.session_state["placas_vehiculos"] = placas_activas

            # Mostrar lista final
            #st.write("Placas activas registradas:", st.session_state["placas_vehiculos"])
            
        else:
            col_left, col_center, col_right = st.columns([0.7, 2, 1])
            with col_center:
                #Para los que no sean Vehiculos          
                numero_solicitud = st.text_input(
                        "Número de solicitud"
                    )
                st.session_state["numero_solicitud"] = numero_solicitud

        # Guardar los valores en session_state
        st.session_state["nombre_titular"] = nombre_titular
        st.session_state["nombre_establecimiento"] = nombre_establecimiento 
        st.session_state["tipo_tramite"] = tipo_tramite


        # Guardar los valores en session_state
        col_btn = st.columns([3, 2, 3])
        with col_btn[1]:
            if st.button("Dictamen",type="primary", key="dictamen_btn"):
                st.switch_page("pages/dictamen.py")

            
    except Exception as e:
        st.error(f"Error:  {e}")

if not check_password():
    st.stop()

    
