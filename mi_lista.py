import streamlit as st
import pandas as pd
import json

FILE_PATH = "listas_personalizadas.json"

# Cargar el nombre del usuario actual en la sesión
usuario_actual = st.session_state.get('username')

# Función para cargar el JSON y convertirlo en un DataFrame
def load_json():
    try:
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        st.warning("El archivo JSON está vacío o no se encuentra.")
        return {}

# Función para guardar los datos modificados al JSON
def save_json(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

# Cargar los datos del JSON
listas = load_json()

# Mostrar listas por usuario con secciones separadas (expandido por defecto)
for user, regalos in listas.items():
    if user == usuario_actual:
        st.write(f"Lista de {user}", expanded=True)
        # Crear DataFrame con los regalos del usuario
        df_user = pd.DataFrame(regalos)
        if not df_user.empty:
            # Filtrar para que solo muestre las columnas deseadas
            df_user = df_user[["Nombre regalo", "Detalles"]]
            edited_df = st.data_editor(df_user, num_rows="dynamic")
                
            # Botón para guardar los cambios en el JSON
            if st.button(f"Guardar cambios en la lista de {user}", key=f"guardar_{user}"):
                # Actualizar el JSON con los datos editados
                listas[user] = edited_df.to_dict(orient="list")
                save_json(listas)
                st.success(f"Lista de {user} actualizada.")

        else:
            st.write("No hay regalos en la lista de este usuario.")