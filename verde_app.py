import pandas as pd
import streamlit as st

# ================================
# 🌱 Interfaz con Streamlit
# ================================
st.title("🌱 Cálculo de Dosis para Control de Malezas")

# -------------------------------
# Parámetros del lote
# -------------------------------
hectareas = st.number_input(
    "Número de hectáreas del lote",
    min_value=0.1,
    step=0.1
)

# -------------------------------
# NUEVO: Cobertura manual
# -------------------------------
cobertura_pastos = st.number_input(
    "Porcentaje de cobertura de pastos (%)",
    min_value=0.0,
    max_value=100.0,
    step=1.0
)

cobertura_hojas = st.number_input(
    "Porcentaje de cobertura de hojas anchas (%)",
    min_value=0.0,
    max_value=100.0,
    step=1.0
)

# -------------------------------
# NUEVO: Altura de la plantación
# -------------------------------
altura_plantacion = st.number_input(
    "Altura promedio de la plantación (m)",
    min_value=0.1,
    step=0.1
)

# -------------------------------
# Presencias específicas
# -------------------------------
pres_helechos = st.checkbox("¿Presencia de helechos?")
pres_ciperaceas = st.checkbox("¿Presencia de ciperáceas?")
pres_mortino = st.checkbox("¿Presencia de mortiño?")
pres_gargantillo = st.checkbox("¿Presencia de gargantillo?")
pres_cuero_sapo = st.checkbox("¿Presencia de cuero de sapo?")
pres_meloso = st.checkbox("¿Presencia de pasto meloso?")

# ================================
# Función: nivel de resistencia
# ================================
def nivel_resistencia(porc):
    if porc < 30:
        return "Bajo"
    elif porc < 60:
        return "Medio"
    else:
        return "Alto"

# ================================
# Botón de cálculo
# ================================
if st.button("📐 Calcular dosis"):

    # -------------------------------
    # Nivel de resistencia
    # -------------------------------
    nivel_pastos = nivel_resistencia(cobertura_pastos)
    nivel_hojas = nivel_resistencia(cobertura_hojas)

    # -------------------------------
    # Dosis base por fumigadora
    # -------------------------------
    dosis_touch_fumi = 0      # cm³
    dosis_mets_fumi = 0       # g

    # --- TOUCHDOWN (Pastos)
    if cobertura_pastos > 0:
        if nivel_pastos == "Bajo":
            dosis_touch_fumi = 350
        elif nivel_pastos == "Medio":
            dosis_touch_fumi = 400
        elif nivel_pastos == "Alto":
            dosis_touch_fumi = 550

    # --- METSULFURÓN (Hojas anchas)
    if cobertura_hojas > 0:
        if nivel_hojas == "Bajo":
            dosis_mets_fumi = 4
        elif nivel_hojas == "Medio":
            dosis_mets_fumi = 6
        elif nivel_hojas == "Alto":
            dosis_mets_fumi = 8

    # -------------------------------
    # Ajustes adicionales
    # -------------------------------
    if pres_ciperaceas:
        dosis_touch_fumi += 50

    if pres_helechos:
        dosis_mets_fumi += 1

    if pres_meloso:
        dosis_touch_fumi += 50

    pres_extra = sum([pres_mortino, pres_gargantillo, pres_cuero_sapo])
    if pres_extra == 2:
        dosis_mets_fumi += 1
    elif pres_extra == 3:
        dosis_mets_fumi += 2

    # -------------------------------
    # Selección de boquilla
    # -------------------------------
    if altura_plantacion <= 1.5:
        boquilla = "Boquilla marcadora"
        descarga = 320
    elif altura_plantacion <= 3:
        boquilla = "110015 ASJ o AI 110015"
        descarga = 300
    else:
        boquilla = "8001 TEEJET"
        descarga = 270

    # -------------------------------
    # Resultados finales
    # -------------------------------
    st.subheader("📊 Resultados finales")

    st.write(f"**Nivel de resistencia en pastos:** {nivel_pastos}")
    st.write(f"**Nivel de resistencia en hojas anchas:** {nivel_hojas}")

    st.write(f"🌾 **Touchdown:** {dosis_touch_fumi:.0f} cm³ por fumigadora")
    st.write(f"🌿 **Metsulfurón:** {dosis_mets_fumi:.1f} g por fumigadora")

    st.subheader("🔧 Configuración de aplicación")
    st.write(f"**Boquilla recomendada:** {boquilla}")
    st.write(f"**Descarga:** {descarga} cm³/min")


