import streamlit as st
import pandas as pd
import json

# Archivos JSON para listas de regalos y reservas
LISTAS_FILE = "listas_personalizadas.json"
RESERVAS_FILE = "reservas.json"

# Cargar el nombre del usuario actual en la sesión
usuario_actual = st.session_state.get('username')

# Función para cargar los datos de listas de regalos desde el archivo JSON
def load_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        st.warning("El archivo JSON está vacío o no se encuentra.")
        return {}

# Función para guardar datos en el archivo JSON
def save_json(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Cargar las listas de regalos y las reservas
listas = load_json(LISTAS_FILE)
reservas = load_json(RESERVAS_FILE)

# Función para crear un DataFrame vacío con columnas de texto si el usuario no tiene regalos
def obtener_lista_usuario(regalos):
    if not regalos:
        return pd.DataFrame({
            "Nombre regalo": pd.Series([], dtype="str"),
            "Detalles": pd.Series([], dtype="str")
        })
    else:
        # Convertimos todas las columnas a string explícitamente
        df = pd.DataFrame(regalos)
        df["Nombre regalo"] = df["Nombre regalo"].astype("str")
        df["Detalles"] = df["Detalles"].astype("str")
        return df

# Función para limpiar las reservas de los regalos eliminados
def limpiar_reservas(user, regalos_actualizados):
    # Crear un set de nombres de regalos actualizados
    nombres_regalos_actualizados = set(regalos_actualizados["Nombre regalo"])
    
    # Revisar las reservas y eliminar los regalos que ya no están en la lista del usuario
    if user in reservas:
        for reserva_user, regalos in list(reservas[user].items()):
            # Filtrar las reservas para conservar solo los regalos que existen en la lista actualizada
            reservas[user][reserva_user] = [
                r for r in regalos if r["Nombre regalo"] in nombres_regalos_actualizados
            ]
            # Eliminar la clave de reservas del usuario si ya no tiene regalos reservados
            if not reservas[user][reserva_user]:
                del reservas[user][reserva_user]

        # Eliminar el usuario de reservas si no quedan reservas
        if not reservas[user]:
            del reservas[user]

    # Guardar los cambios en el archivo de reservas
    save_json(reservas, RESERVAS_FILE)

# Mostrar listas por usuario con secciones separadas (expandido por defecto)
for user, regalos in listas.items():
    if user == usuario_actual:
        st.write(f"Lista de {user}", expanded=True)
        
        # Obtener el DataFrame del usuario actual (vacío si no tiene regalos)
        df_user = obtener_lista_usuario(regalos)
        
        # Mostrar el DataFrame en el editor de datos
        edited_df = st.data_editor(df_user, num_rows="dynamic")

        # Botón para guardar los cambios en el JSON
        if st.button(f"Guardar cambios en la lista de {user}", key=f"guardar_{user}"):
            # Actualizar el JSON con los datos editados
            listas[user] = edited_df.to_dict(orient="list")
            save_json(listas, LISTAS_FILE)
            
            # Limpiar reservas de regalos eliminados
            limpiar_reservas(user, listas[user])
            
            st.success(f"Lista de {user} actualizada.")
