import streamlit as st

#Configuración de página
st.set_page_config(
    page_title="Ideas de regalos",
    page_icon=":featured_seasonal_and_gifts:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Título de la página
st.title("Ideas regalos :gift:")

# Mostrar el usuario en la parte superior si ha iniciado sesión
if 'username' in st.session_state:
    st.subheader(f"Sesión iniciada como: {st.session_state['username']}")

# Menú
pages = {
    "Mi cuenta":[
        st.Page("login.py", title="Iniciar sesión")
    ],
    "Listas de regalos":[
        st.Page("mi_lista.py", title="Mi lista de regalos"),
        st.Page("listas.py", title="Todas las listas de regalos")
    ]
}

pg = st.navigation(pages)
pg.run()