import streamlit as st

# Obtener usuarios desde secrets
def get_users():
    return st.secrets["users"]

# Función para verificar credenciales
def login_user(username, password):
    users = get_users()
    return username in users and users[username] == password

# Formulario para el inicio de sesión
def login():
    st.subheader("Inicio de sesión")
    username = st.text_input("Usuario", key="login_username")
    password = st.text_input("Contraseña", type="password", key="login_password")
    
    if st.button("Iniciar sesión"):
        if login_user(username, password):
            st.session_state['username'] = username  # Guardar usuario en la sesión
            if username == "Rogelio":
                st.success(f"Bienvenido,  {username}")
            else:
                st.success(f"Bienvenida,  {username}")
        else:
            st.error("Usuario o contraseña incorrectos.")

# Lógica principal de la interfaz
def main():
    # Mostrar el formulario de login si no hay un usuario en la sesión
    if 'username' not in st.session_state:
        login()  # Formulario de inicio de sesión
    else:
        # Mostrar mensaje de sesión iniciada
        st.write(f"Sesión iniciada como: {st.session_state['username']}")
        st.button("Cerrar sesión", on_click=lambda: st.session_state.pop('username'))  # Cerrar sesión

# Ejecución principal de la app
main()