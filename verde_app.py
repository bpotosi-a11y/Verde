import streamlit as st

# ================================
# 🌱 Interfaz con Streamlit
# ================================
st.title("🌱 Cálculo de dosis para control de malezas")

# -------------------------------
# Parámetros del lote
# -------------------------------
hectareas = st.number_input(
    "Número de hectáreas del lote",
    min_value=0.1,
    step=0.1
)

altura_maleza = st.checkbox("¿La maleza supera los 50 cm?")

# -------------------------------
# NUEVO: Porcentaje real de malezas
# -------------------------------
porc_gramineas = st.number_input(
    "Porcentaje de gramíneas (%)",
    min_value=0.0,
    max_value=100.0,
    step=1.0
)

porc_hoja_ancha = st.number_input(
    "Porcentaje de hoja ancha (%)",
    min_value=0.0,
    max_value=100.0,
    step=1.0
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
# Función: clasificar presencia
# ================================
def clasificar_presencia(p):
    if p == 0:
        return "Ninguna"
    elif p <= 33:
        return "Baja"
    elif p <= 66:
        return "Media"
    else:
        return "Alta"

# ================================
# Cálculo
# ================================
if st.button("📐 Calcular dosis"):

    pres_gramineas = clasificar_presencia(porc_gramineas)
    pres_hoja_ancha = clasificar_presencia(porc_hoja_ancha)

    dosis_touch = 0
    dosis_metsulfuron = 0

    # ==========================
    # GRAMÍNEAS – Touchdown
    # ==========================
    if pres_gramineas != "Ninguna":

        if pres_gramineas == "Alta":
            porc_gram_calc = (4/5) * porc_gramineas
        elif pres_gramineas == "Media":
            porc_gram_calc = (1/2) * porc_gramineas
        else:  # Baja
            porc_gram_calc = (1/3) * porc_gramineas

        dosis_touch = (porc_gram_calc / 100) * hectareas * 2.9

    # ==========================
    # HOJA ANCHA – Metsulfurón
    # ==========================
    if pres_hoja_ancha != "Ninguna":

        if pres_hoja_ancha == "Alta":
            porc_hoja_calc = (5/5) * porc_hoja_ancha
        elif pres_hoja_ancha == "Media":
            porc_hoja_calc = (1/2) * porc_hoja_ancha
        else:  # Baja
            porc_hoja_calc = (1/3) * porc_hoja_ancha

        dosis_metsulfuron = (porc_hoja_calc / 100) * hectareas * 2.6

    # ==========================
    # Ajustes adicionales (IGUALES)
    # ==========================
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

    # --------------------------
    # Ajuste por altura de maleza
    # --------------------------
    if altura_maleza:
        dosis_touch += 0.3 * hectareas
        dosis_metsulfuron += 0.2 * hectareas

    # --------------------------
    # Condición final Metsulfurón
    # --------------------------
    if pres_hoja_ancha == "Ninguna" and not pres_helechos:
        dosis_metsulfuron = 0

    # ==========================
    # Resultados
    # ==========================
    st.subheader("📊 Resultados finales")

    st.write(f"**Clasificación gramíneas:** {pres_gramineas}")
    st.write(f"**Clasificación hoja ancha:** {pres_hoja_ancha}")

    st.write(f"🌾 **Touchdown total:** {dosis_touch:.3f} L")
    st.write(f"🌾 **Touchdown por fumigadora:** {dosis_touch/hectareas:.3f} L")

    st.write(f"🌿 **Metsulfurón total:** {dosis_metsulfuron:.3f} unidades")
    st.write(f"🌿 **Metsulfurón por fumigadora:** {dosis_metsulfuron/hectareas:.3f} unidades")
