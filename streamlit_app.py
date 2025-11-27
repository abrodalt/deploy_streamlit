import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

st.set_page_config(page_title="Registro de Nombres", page_icon="📝")

# ===========================
#   FIRESTORE (CONECCIÓN)
# ===========================

@st.cache_resource
def get_db():
    """Carga credenciales desde st.secrets, crea cliente Firestore y lo cachéa."""
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="names-project-demo")
    return db


# Obtener cliente Firestore
db = get_db()
collection = db.collection("names")


# ===========================
#   FUNCIÓN PARA CARGAR POR NOMBRE
# ===========================

def loadByName(name):
    """Buscar un documento exacto por nombre."""
    doc_ref = collection.document(name)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None


# ===========================
#   INTERFAZ PRINCIPAL
# ===========================

st.title("Base de Datos con Firestore")
st.subheader("Nuevo registro")

index = st.text_input("Index")
name = st.text_input("Name")
sex = st.selectbox("Select Sex", ("F", "M", "Other"))
submit = st.button("Crear nuevo registro")

# ===========================
#   INSERTAR NUEVO REGISTRO
# ===========================

if submit:
    if index.strip() == "" or name.strip() == "":
        st.error("Index y Name son obligatorios.")
    else:
        doc_ref = collection.document(name)
        doc_ref.set({
            "index": index,
            "name": name,
            "sex": sex
        })
        st.success("Registro insertado correctamente.")
        st.balloons()


# ===========================
#   BÚSQUEDA DE REGISTROS
# ===========================

st.sidebar.header("Buscar registro")
search_name = st.sidebar.text_input("Nombre a buscar")
search_btn = st.sidebar.button("Buscar")

if search_btn and search_name.strip() != "":
    data = loadByName(search_name)
    if data:
        st.sidebar.success("Registro encontrado:")
        st.sidebar.json(data)
    else:
        st.sidebar.error("No existe un registro con ese nombre.")
