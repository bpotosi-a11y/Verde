import streamlit as st

# ================================
# 🌱 Interfaz con Streamlit
# ================================
st.title("🌱 Cálculo de Dosis para Control de Malezas")

# Parámetros del lote
hectareas = st.number_input("Número de hectáreas del lote", min_value=0.1, step=0.1)

altura_maleza = st.checkbox("¿La maleza supera los 50 cm?")

pres_gramineas = st.selectbox("Presencia de gramíneas", ["Ninguna", "Baja", "Media", "Alta"])
pres_hoja_ancha = st.selectbox("Presencia de hoja ancha", ["Ninguna", "Baja", "Media", "Alta"])

pres_helechos = st.checkbox("¿Presencia de helechos?")
pres_ciperaceas = st.checkbox("¿Presencia de ciperáceas?")
pres_mortino = st.checkbox("¿Presencia de mortiño?")
pres_gargantillo = st.checkbox("¿Presencia de gargantillo?")
pres_cuero_sapo = st.checkbox("¿Presencia de cuero de sapo?")
pres_meloso = st.checkbox("¿Presencia de pasto meloso?")

# ================================
# Conversión de niveles a porcentajes
# ================================
def porcentaje_por_nivel(nivel):
    if nivel == "Baja":
        return 17
    elif nivel == "Media":
        return 50
    elif nivel == "Alta":
        return 83
    else:
        return 0

# ================================
# Cálculo de dosis
# ================================
if st.button("📐 Calcular dosis"):

    promedio = max(
        porcentaje_por_nivel(pres_gramineas),
        porcentaje_por_nivel(pres_hoja_ancha)
    )

    dosis_touch = 0
    dosis_metsulfuron = 0

    # --- GRAMÍNEAS (Touchdown)
    if pres_gramineas != "Ninguna":
        if pres_gramineas == "Alta":
            porc_gram = (4/5) * promedio
        elif pres_gramineas == "Media":
            porc_gram = (1/2) * promedio
        elif pres_gramineas == "Baja":
            porc_gram = (1/3) * promedio

        factor = 2.9
        dosis_touch = (porc_gram / 100) * hectareas * factor

    # --- HOJA ANCHA (Metsulfurón)
    if pres_hoja_ancha != "Ninguna":
        if pres_hoja_ancha == "Alta":
            porc_hoja = promedio
        elif pres_hoja_ancha == "Media":
            porc_hoja = (1/2) * promedio
        elif pres_hoja_ancha == "Baja":
            porc_hoja = (1/3) * promedio

        dosis_metsulfuron = (porc_hoja / 100) * hectareas * 2.6

    # --- Ajustes adicionales (ORIGINALES)
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

    # --- Ajuste por altura de maleza
    if altura_maleza:
        dosis_touch += 0.3 * hectareas
        dosis_metsulfuron += 0.2 * hectareas

    # --- Condición especial original
    if (promedio < 30) and (not altura_maleza) and (not pres_meloso):
        if pres_gramineas in ["Baja", "Media"]:
            dosis_touch += 0.2 * hectareas

    # --- Condición final original
    if pres_hoja_ancha == "Ninguna" and not pres_helechos:
        dosis_metsulfuron = 0

    # ================================
    # Resultados
    # ================================
    st.subheader("📊 Resultados finales")

    st.write(f"🌾 **Touchdown total:** {dosis_touch:.3f} L")
    st.write(f"🌿 **Metsulfurón total:** {dosis_metsulfuron:.3f} unidades")

    st.subheader("🚜 Dosis por fumigadora (≈ 1 ha)")
    st.write(f"Touchdown: {dosis_touch / hectareas:.3f} L / fumigadora")
    st.write(f"Metsulfurón: {dosis_metsulfuron / hectareas:.3f} unidades / fumigadora")
