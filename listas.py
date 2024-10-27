import streamlit as st
import json
import time

# Archivos JSON para listas de regalos y reservas
LISTAS_FILE = "listas_personalizadas.json"
RESERVAS_FILE = "reservas.json"

# Obtener el usuario logueado en la sesión
usuario_actual = st.session_state.get('username')

# Función para cargar las listas de regalos desde el archivo JSON
def cargar_listas():
    try:
        with open(LISTAS_FILE, "r") as f:
            listas = json.load(f)
        return listas
    except (FileNotFoundError, json.JSONDecodeError):
        st.write("Las listas están vacías o el archivo no existe.")
        return {}

# Función para guardar listas de regalos en el archivo JSON
def guardar_listas(listas):
    with open(LISTAS_FILE, "w") as f:
        json.dump(listas, f, indent=4)

# Función para cargar las reservas desde el archivo JSON
def cargar_reservas():
    try:
        with open(RESERVAS_FILE, "r") as f:
            reservas = json.load(f)
        return reservas
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Función para guardar reservas en el archivo JSON
def guardar_reservas(reservas):
    with open(RESERVAS_FILE, "w") as f:
        json.dump(reservas, f, indent=4)

# Cargar las listas de regalos y reservas
listas_personalizadas = cargar_listas()
reservas = cargar_reservas()

# Mostrar las listas de los otros usuarios con opción de reservar
if usuario_actual:
    for user, lista in listas_personalizadas.items():
        if user != usuario_actual:
            with st.expander(f"Lista de {user}", expanded=True):
                for idx, (nombre_regalo, detalles) in enumerate(zip(lista["Nombre regalo"], lista["Detalles"])):
                    st.write(f"**{nombre_regalo}** - {detalles}")
                    
                    # Verificar si el regalo ya está reservado
                    reservado_por_otros = any(
                        any(r['Nombre regalo'] == nombre_regalo for r in regalos) 
                        for _, regalos in reservas.get(user, {}).items()
                    )

                    if reservado_por_otros:
                        st.warning("Este regalo ya ha sido reservado.")
                    else:
                        # Botón para reservar el regalo si no está reservado
                        if st.button(f"Reservar '{nombre_regalo}'", key=f"reservar_{user}_{idx}"):
                            with st.spinner("Guardando reserva..."):
                                time.sleep(2)
                                if user not in reservas:
                                    reservas[user] = {}
                                if usuario_actual not in reservas[user]:
                                    reservas[user][usuario_actual] = []
                                reservas[user][usuario_actual].append({
                                    "Nombre regalo": nombre_regalo,
                                    "Detalles": detalles
                                })
                                guardar_reservas(reservas)
                                st.success(f"Has reservado '{nombre_regalo}' de la lista de {user}.")
                                st.rerun()

# Lista de reservas, muestra la lista con botón para dejar de reservar
if usuario_actual:
    with st.expander("Mis regalos reservados", expanded=False):
        st.subheader("Regalos que has reservado")
        
        user_reservas = [
            (owner, r) for owner, regalos in reservas.items()
            if usuario_actual in regalos for r in regalos[usuario_actual]
        ]
        
        if user_reservas:
            for owner, regalo in user_reservas:
                # Verificar si el regalo sigue en la lista del propietario
                if regalo["Nombre regalo"] in listas_personalizadas.get(owner, {}).get("Nombre regalo", []):
                    st.write(f"{regalo['Nombre regalo']} - {regalo['Detalles']} (de la lista de {owner})")
                    if st.button(f"Dejar de reservar '{regalo['Nombre regalo']}'", key=f"dejar_{owner}_{regalo['Nombre regalo']}"):
                        with st.spinner("Borrando reserva..."):
                            time.sleep(3)
                            reservas[owner][usuario_actual].remove(regalo)
                            if not reservas[owner][usuario_actual]:
                                del reservas[owner][usuario_actual]
                            guardar_reservas(reservas)
                            st.success(f"Has dejado de reservar '{regalo['Nombre regalo']}'.")
                            st.rerun()
        else:
            st.write("No has reservado ningún regalo.")
else:
    st.warning("Inicia sesión para ver las listas.")
