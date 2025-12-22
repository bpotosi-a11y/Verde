import streamlit as st

# ================================
# 🌱 Interfaz con Streamlit
# ================================
st.title("🌱 Cálculo técnico de dosis para control de malezas")

# -------------------------------
# Parámetros del lote
# -------------------------------
hectareas = st.number_input(
    "Número de hectáreas del lote",
    min_value=0.1,
    step=0.1
)

altura_plantacion = st.number_input(
    "Altura promedio de la plantación (m)",
    min_value=0.1,
    step=0.1
)

altura_maleza = st.checkbox("¿La maleza supera los 50 cm?")

# -------------------------------
# Presencia de grupos de malezas
# -------------------------------
pres_gramineas = st.selectbox("Presencia de gramíneas", ["Ninguna", "Baja", "Media", "Alta"])
pres_hoja_ancha = st.selectbox("Presencia de hoja ancha", ["Ninguna", "Baja", "Media", "Alta"])

pres_helechos = st.checkbox("¿Presencia de helechos?")
pres_ciperaceas = st.checkbox("¿Presencia de ciperáceas?")
pres_mortino = st.checkbox("¿Presencia de mortiño?")
pres_gargantillo = st.checkbox("¿Presencia de gargantillo?")
pres_cuero_sapo = st.checkbox("¿Presencia de cuero de sapo?")
pres_meloso = st.checkbox("¿Presencia de pasto meloso?")

# ================================
# 📐 Cálculo de dosis
# ================================
if st.button("📐 Calcular dosis"):

    # -------------------------------
    # Boquilla y descarga (TUS PARÁMETROS)
    # -------------------------------
    if altura_plantacion <= 1.5:
        boquilla = "Boquilla marcadora"
        descarga = 320
        dosis_touch_ha = 2.0
        dosis_mets_ha = 4

    elif altura_plantacion <= 3.0:
        boquilla = "110015 ASJ o AI 110015"
        descarga = 300
        dosis_touch_ha = 2.8
        dosis_mets_ha = 6

    else:
        boquilla = "8001 TEEJET"
        descarga = 270
        dosis_touch_ha = 3.5
        dosis_mets_ha = 8

    # -------------------------------
    # Ajustes por composición florística
    # -------------------------------
    if pres_gramineas == "Ninguna":
        dosis_touch_ha = 0

    if pres_hoja_ancha == "Ninguna" and not pres_helechos:
        dosis_mets_ha = 0

    if pres_ciperaceas:
        dosis_touch_ha += 0.3

    if pres_meloso:
        dosis_touch_ha += 0.4

    if pres_helechos:
        dosis_mets_ha += 1

    especies_dificiles = sum([pres_mortino, pres_gargantillo, pres_cuero_sapo])
    if especies_dificiles == 2:
        dosis_mets_ha += 1
    elif especies_dificiles == 3:
        dosis_mets_ha += 2

    # -------------------------------
    # Ajuste por altura de maleza
    # -------------------------------
    if altura_maleza:
        dosis_touch_ha += 0.4
        dosis_mets_ha += 1

    # -------------------------------
    # Totales
    # -------------------------------
    total_touch = dosis_touch_ha * hectareas
    total_mets = dosis_mets_ha * hectareas

    # ================================
    # Resultados finales
    # ================================
    st.subheader("📊 Resultados finales")

    st.write(f"🔧 **Boquilla recomendada:** {boquilla}")
    st.write(f"💧 **Descarga:** {descarga} cm³/min")

    st.write(f"🌾 **Touchdown:** {dosis_touch_ha:.2f} L/ha → **Total:** {total_touch:.2f} L")
    st.write(f"🌿 **Metsulfurón:** {dosis_mets_ha:.1f} g/ha → **Total:** {total_mets:.1f} g")

    # -------------------------------
    # Recomendación técnica final
    # -------------------------------
    if dosis_touch_ha >= 3.5 and dosis_mets_ha >= 8:
        st.warning(
            "⚠️ Bajo estas condiciones se recomienda evaluar "
            "control mecanizado complementario para mejorar la eficacia."
        )
