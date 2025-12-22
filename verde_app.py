import pandas as pd
import streamlit as st

# ================================
# 🌱 Interfaz con Streamlit
# ================================
st.title("🌱 Análisis de Cobertura y Cálculo de Dosis")

# -------------------------------
# Parámetros del lote
# -------------------------------
hectareas = st.number_input(
    "Número de hectáreas del lote",
    min_value=0.1,
    step=0.1
)

# -------------------------------
# NUEVO: Cobertura manual (%)
# -------------------------------
cobertura_pastos = st.number_input(
    "Cobertura de pastos (%)",
    min_value=0.0,
    max_value=100.0,
    step=1.0
)

cobertura_hoja_ancha = st.number_input(
    "Cobertura de hoja ancha (%)",
    min_value=0.0,
    max_value=100.0,
    step=1.0
)

# -------------------------------
# Alturas
# -------------------------------
altura_maleza = st.checkbox("¿La maleza supera los 50 cm?")

altura_plantacion = st.number_input(
    "Altura de la plantación (m)",
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
# Función: clasificar cobertura
# ================================
def clasificar_cobertura(porc):
    if porc == 0:
        return "Ninguna"
    elif porc <= 30:
        return "Baja"
    elif porc <= 60:
        return "Media"
    else:
        return "Alta"

# ================================
# Cálculo
# ================================
if st.button("📐 Calcular dosis"):

    pres_gramineas = clasificar_cobertura(cobertura_pastos)
    pres_hoja_ancha = clasificar_cobertura(cobertura_hoja_ancha)

    # ==========================
    # Cálculo de dosis
    # ==========================
    dosis_touch = 0
    dosis_metsulfuron = 0

    # --- GRAMÍNEAS (Touchdown)
    if pres_gramineas != "Ninguna":
        if pres_gramineas == "Alta":
            porc_gram = (4/5) * cobertura_pastos
        elif pres_gramineas == "Media":
            porc_gram = (1/2) * cobertura_pastos
        elif pres_gramineas == "Baja":
            porc_gram = (1/3) * cobertura_pastos

        factor = 2.9
        dosis_touch = (porc_gram / 100) * hectareas * factor
    else:
        dosis_touch = 0

    # --- HOJA ANCHA (Metsulfurón)
    if pres_hoja_ancha != "Ninguna":
        if pres_hoja_ancha == "Alta":
            porc_hoja = (5/5) * cobertura_hoja_ancha
        elif pres_hoja_ancha == "Media":
            porc_hoja = (1/2) * cobertura_hoja_ancha
        elif pres_hoja_ancha == "Baja":
            porc_hoja = (1/3) * cobertura_hoja_ancha

        dosis_metsulfuron = (porc_hoja / 100) * hectareas * 2.6
    else:
        dosis_metsulfuron = 0

    # --- Ajustes adicionales (SIN CAMBIOS)
    if pres_ciperaceas:
        dosis_touch += 0.2 * hectareas
    if pres_helechos:
        dosis_metsulfuron += 0.1 * hectareas
    if pres_meloso:
        dosis_touch += 0.2 * hectareas

    pres_extra = sum([pres_mortino, pres_gargantillo, pres_cuero_sapo])
    if pres_extra == 2:
        dosis_metsulfuron += 0.1 * hectareas
    elif pres_extra == 3:
        dosis_metsulfuron += 0.2 * hectareas

    if altura_maleza:
        dosis_touch += 0.3 * hectareas
        dosis_metsulfuron += 0.2 * hectareas

    if (cobertura_pastos < 30) and (not altura_maleza) and (not pres_meloso):
        if pres_gramineas in ["Baja", "Media"]:
            dosis_touch += 0.2 * hectareas

    if pres_hoja_ancha == "Ninguna" and not pres_helechos:
        dosis_metsulfuron = 0

    # ==========================
    # Boquilla y descarga (ALTURA PLANTACIÓN)
    # ==========================
    if altura_plantacion <= 1.5:
        boquilla = "Boquilla marcadora"
        descarga = 320
    elif altura_plantacion <= 3.0:
        boquilla = "110015 ASJ o AI 110015"
        descarga = 300
    else:
        boquilla = "8001 TEEJET"
        descarga = 270

    # ==========================
    # Dosis por fumigadora
    # ==========================
    # Asumido: fumigadora de 200 L
    volumen_fumi = 200

    dosis_touch_fumi = (dosis_touch / hectareas) * volumen_fumi * 1000  # cm³
    dosis_mets_fumi = (dosis_metsulfuron / hectareas) * volumen_fumi     # g

    # ==========================
    # Resultados finales
    # ==========================
    st.subheader("📊 Resultados finales")

    st.write(f"🌾 **Touchdown total:** {dosis_touch:.3f} L")
    st.write(f"🌿 **Metsulfurón total:** {dosis_metsulfuron:.3f} unidades")

    st.subheader("🚿 Dosis por fumigadora (200 L)")
    st.write(f"Touchdown: **{dosis_touch_fumi:.0f} cm³ / fumigadora**")
    st.write(f"Metsulfurón: **{dosis_mets_fumi:.1f} g / fumigadora**")

    st.subheader("🔧 Configuración de aplicación")
    st.write(f"**Boquilla recomendada:** {boquilla}")
    st.write(f"**Descarga:** {descarga} cm³/min")

    st.subheader("🔧 Configuración de aplicación")
    st.write(f"**Boquilla recomendada:** {boquilla}")
    st.write(f"**Descarga:** {descarga} cm³/min")

